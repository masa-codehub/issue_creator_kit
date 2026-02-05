#!/bin/bash
set -e

# 環境変数のチェック
if [ -z "$PR_NUMBER" ] || [ -z "$REVIEW_ID" ]; then
  echo "Error: Required environment variables (PR_NUMBER, REVIEW_ID) are missing."
  exit 1
fi

# 必須ツールの存在確認
for cmd in gemini gh envsubst jq; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "Error: Required command '$cmd' not found. Please ensure it is installed in the runner environment."
    exit 1
  fi
done

# GitHub CLI 認証状態の確認
if ! gh auth status >/dev/null 2>&1; then
  echo "Error: GitHub CLI is not authenticated or GITHUB_TOKEN is invalid."
  exit 1
fi

# PR全体の全レビューコメントを全取得して整形
echo "Fetching all review comments for PR #$PR_NUMBER..."
ALL_REVIEW_COMMENTS=$(gh api "repos/$GITHUB_REPOSITORY/pulls/$PR_NUMBER/comments" \
  --jq 'sort_by(.created_at) | .[] | "### File: \(.path) (Line: \(.line // .original_line))\n#### Author: \(.user.login)\n#### Comment:\n\(.body)\n\n#### Code Context:\n```diff\n\(.diff_hunk)\n```\n"')

if [ -z "$ALL_REVIEW_COMMENTS" ]; then
  echo "No review comments found on this PR. Skipping analysis."
  exit 0
fi

export REVIEW_COMMENTS_FORMATTED="$ALL_REVIEW_COMMENTS"

# タスクタイプの判定とプロンプトの選択
CONTEXT_FILE=""
MATCH_COUNT=0
if [[ "$PR_LABELS" == *"gemini:arch"* ]]; then
  TASK_TYPE="ARCH"
  CONTEXT_FILE=".github/workflows/context/review-arch-prompt.md"
  ((++MATCH_COUNT))
fi

if [[ "$PR_LABELS" == *"gemini:spec"* ]]; then
  TASK_TYPE="SPEC"
  CONTEXT_FILE=".github/workflows/context/review-spec-prompt.md"
  ((++MATCH_COUNT))
fi

if [[ "$PR_LABELS" == *"gemini:tdd"* ]]; then
  TASK_TYPE="TDD"
  CONTEXT_FILE=".github/workflows/context/review-tdd-prompt.md"
  ((++MATCH_COUNT))
fi

# 複数ラベルまたは該当なしのチェック
if [[ "$MATCH_COUNT" -gt 1 ]]; then
  echo "Error: Multiple gemini labels detected. Please use only one label per pull request."
  exit 1
elif [[ "$MATCH_COUNT" -eq 0 ]]; then
  echo "No matching gemini label found. Skipping execution."
  exit 0
fi

export TASK_TYPE

echo "Task Type: $TASK_TYPE"
echo "Selected Context: $CONTEXT_FILE"

# プロンプトファイルの存在確認
if [ ! -f "$CONTEXT_FILE" ]; then
  echo "Error: Context file not found: $CONTEXT_FILE"
  exit 1
fi

# 一時ファイルの作成 (一意なパス)
PROMPT_FILE="$(mktemp "${RUNNER_TEMP:-/tmp}/prompt.XXXXXX.md")"
RESPONSE_FILE="$(mktemp "${RUNNER_TEMP:-/tmp}/response.XXXXXX.md")"
trap 'rm -f "$PROMPT_FILE" "$RESPONSE_FILE"' EXIT

# プロンプトの生成 (envsubst でホワイトリスト展開)
export PR_NUMBER REVIEW_AUTHOR REVIEW_BODY GITHUB_REPOSITORY TASK_TYPE
envsubst '$PR_NUMBER $REVIEW_AUTHOR $REVIEW_BODY $REVIEW_COMMENTS_FORMATTED $GITHUB_REPOSITORY $TASK_TYPE' < "${CONTEXT_FILE}" > "$PROMPT_FILE"

echo "--- Gemini Analysis Start ---"

# Gemini CLI を実行
# --yolo: ユーザー確認なしで実行 (CI/CD用)
cat "$PROMPT_FILE" | gemini --yolo -m "gemini-3-flash-preview" > "$RESPONSE_FILE"

echo "--- Gemini Analysis End ---"

# GitHub CLI でコメントを投稿
if [ -f "$RESPONSE_FILE" ] && [ -s "$RESPONSE_FILE" ]; then
  echo "Posting summary comment to PR #${PR_NUMBER}..."
  gh pr comment "$PR_NUMBER" --body-file "$RESPONSE_FILE"
else
  echo "Error: Gemini produced empty response."
  exit 1
fi
