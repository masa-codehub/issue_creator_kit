#!/bin/bash
set -e

# 環境変数のチェック
if [ -z "$PR_NUMBER" ] || [ -z "$COMMENT_BODY" ]; then
  echo "Error: Required environment variables (PR_NUMBER, COMMENT_BODY) are missing."
  exit 1
fi

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

# 必須ツールの存在確認
for cmd in gemini gh envsubst; do
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
export PR_NUMBER COMMENT_AUTHOR COMMENT_BODY FILE_PATH LINE_NUMBER DIFF_HUNK GITHUB_REPOSITORY TASK_TYPE
envsubst '$PR_NUMBER $COMMENT_AUTHOR $COMMENT_BODY $FILE_PATH $LINE_NUMBER $DIFF_HUNK $GITHUB_REPOSITORY $TASK_TYPE' < "${CONTEXT_FILE}" > "$PROMPT_FILE"

echo "--- Gemini Analysis Start ---"

# Gemini CLI を実行
# --yolo: ユーザー確認なしで実行 (CI/CD用)
cat "$PROMPT_FILE" | gemini --yolo -m "gemini-3-flash-preview" > "$RESPONSE_FILE"

echo "--- Gemini Analysis End ---"

# GitHub CLI でコメントを投稿
if [ -f "$RESPONSE_FILE" ] && [ -s "$RESPONSE_FILE" ]; then
  echo "Posting comment to PR #${PR_NUMBER}..."
  gh pr comment "$PR_NUMBER" --body-file "$RESPONSE_FILE"
else
  echo "Error: Gemini produced empty response."
  exit 1
fi
