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
    echo "Error: Required command '$cmd' not found."
    exit 1
  fi
done

# GitHub CLI 認証状態の確認
if ! gh auth status >/dev/null 2>&1; then
  echo "Error: GitHub CLI is not authenticated or GITHUB_TOKEN is invalid."
  exit 1
fi

# PR全体の全レビューコメントを全取得して整形
ALL_REVIEW_COMMENTS=$(gh api "repos/$GITHUB_REPOSITORY/pulls/$PR_NUMBER/comments" \
  --jq 'sort_by(.created_at) | .[] | "### File: \(.path) (Line: \(.line // .original_line))\n#### Author: \(.user.login)\n#### Comment:\n\(.body)\n\n#### Code Context:\n```diff\n\(.diff_hunk)\n```\n"')

if [ -z "$ALL_REVIEW_COMMENTS" ]; then
  echo "No review comments found on this PR. Skipping analysis."
  exit 0
fi

export REVIEW_COMMENTS_FORMATTED="$ALL_REVIEW_COMMENTS"

# 仮想環境のアクティベート
if [ -f ".venv/bin/activate" ]; then
  source ".venv/bin/activate"
fi

# ワークフローで確定した AGENT_ROLE を使用
if [ -z "$AGENT_ROLE" ]; then
  echo "Error: AGENT_ROLE is not set."
  exit 1
fi

# 一時ファイルの一意な生成とクリーンアップ設定
# ick のセキュリティ制約（絶対パス禁止）を回避するため、カレントディレクトリ内に相対パスで作成
TEMP_CONFIG=$(mktemp "./review_config_${PR_NUMBER}.XXXXXX.json")
PROMPT_FILE=$(mktemp "./prompt_${PR_NUMBER}.XXXXXX.md")

cleanup() {
  echo "Cleaning up temporary files..."
  rm -f "$TEMP_CONFIG" "$PROMPT_FILE"
}
trap cleanup EXIT

# ick dispatch でレビュー用コンテキストファイル（プロンプト）を決定
# issue-kit-config.json から "reviews" 要素を抽出し、一時的に "roles" キーとして持つ設定ファイルを作成
jq '.roles = .reviews | del(.reviews)' .github/issue-kit-config.json > "$TEMP_CONFIG"

# 相対パス（./）を明示して呼び出す
CONTEXT_FILE=$(uv tool run --from git+https://github.com/masa-codehub/issue_creator_kit.git ick dispatch --labels "$PR_LABELS" --config-path "$TEMP_CONFIG" --get-context || echo "UNKNOWN")

if [ "$CONTEXT_FILE" = "UNKNOWN" ]; then
  echo "Error: No matching gemini review context found for labels: $PR_LABELS"
  exit 1
fi

echo "Selected Agent Role: $AGENT_ROLE"
echo "Review Context File: $CONTEXT_FILE"

export TASK_TYPE="$AGENT_ROLE"

# プロンプトファイルの存在確認
if [ ! -f "$CONTEXT_FILE" ]; then
  echo "Error: Context file not found: $CONTEXT_FILE"
  exit 1
fi

# プロンプトの生成 (envsubst でホワイトリスト展開)
export PR_NUMBER REVIEW_AUTHOR REVIEW_BODY GITHUB_REPOSITORY TASK_TYPE
envsubst '$PR_NUMBER $REVIEW_AUTHOR $REVIEW_BODY $REVIEW_COMMENTS_FORMATTED $GITHUB_REPOSITORY $TASK_TYPE' < "${CONTEXT_FILE}" > "$PROMPT_FILE"

echo "--- Gemini Analysis Start ---"
cat "$PROMPT_FILE" | gemini --yolo -m "gemini-3-flash-preview"
echo "--- Gemini Analysis End ---"
