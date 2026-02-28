#!/bin/bash
set -e

# 環境変数のチェック
if [ -z "$PR_NUMBER" ] || [ -z "$GITHUB_REPOSITORY" ]; then
  echo "Error: Required environment variables (PR_NUMBER, GITHUB_REPOSITORY) are missing."
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
echo "Debug: PR_LABELS='${PR_LABELS}'"

ALL_REVIEW_COMMENTS=$(gh api "repos/$GITHUB_REPOSITORY/pulls/$PR_NUMBER/comments" \
  --jq 'sort_by(.created_at) | .[] | "### File: \(.path) (Line: \(.line // .original_line))\n#### Author: \(.user.login)\n#### Comment:\n\(.body)\n\n#### Code Context:\n```diff\n\(.diff_hunk)\n```\n"')

if [ -z "$ALL_REVIEW_COMMENTS" ]; then
  echo "No review comments found on this PR. Skipping analysis."
  exit 0
fi

export REVIEW_COMMENTS_FORMATTED="$ALL_REVIEW_COMMENTS"

# 仮想環境のアクティベート (ick コマンドを使うために先に実行)
if [ -f ".venv/bin/activate" ]; then
  source ".venv/bin/activate"
fi

# ick dispatch でロール（エージェント名）とコンテキストファイル（プロンプト）を決定
ROLE=$(ick dispatch --labels "$PR_LABELS" || echo "UNKNOWN")
CONTEXT_FILE=$(ick dispatch --labels "$PR_LABELS" --get-context || echo "UNKNOWN")

if [ "$ROLE" = "UNKNOWN" ] || [ "$CONTEXT_FILE" = "UNKNOWN" ]; then
  echo "Error: No matching gemini role or context file found for labels: $PR_LABELS"
  exit 1
fi

echo "Selected Agent Role: $ROLE"
echo "Selected Context File: $CONTEXT_FILE"

export TASK_TYPE="$ROLE"


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
# cat "$PROMPT_FILE" | gemini --yolo -m "gemini-3-flash-preview" > "$RESPONSE_FILE"
cat "$PROMPT_FILE" | gemini --yolo -m "gemini-3-flash-preview"

echo "--- Gemini Analysis End ---"

# # GitHub CLI でコメントを投稿
# if [ -f "$RESPONSE_FILE" ] && [ -s "$RESPONSE_FILE" ]; then
#   echo "Posting summary comment to PR #${PR_NUMBER}..."
#   gh pr comment "$PR_NUMBER" --body-file "$RESPONSE_FILE"
# else
#   echo "Error: Gemini produced empty response."
#   exit 1
# fi
