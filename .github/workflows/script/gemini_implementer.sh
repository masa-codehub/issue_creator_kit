#!/bin/bash
set -e

# ラベル情報の取得 (環境変数 ISSUE_LABELS を使用)
LABELS="${ISSUE_LABELS}"

echo "Processing Issue #${ISSUE_NUMBER}: ${ISSUE_TITLE}"
echo "Debug: LABELS='${LABELS}'"

# 仮想環境のアクティベート
if [ -f ".venv/bin/activate" ]; then
  source ".venv/bin/activate"
fi

# ワークフローで確定した AGENT_ROLE を使用
if [ -z "$AGENT_ROLE" ]; then
  echo "Error: AGENT_ROLE is not set. It should be determined in the workflow step."
  exit 1
fi

# CONTEXT_FILE の取得 (ick dispatch を再度実行するが、ツールとして実行)
# ※将来的にワークフローからパスを渡せるようにするとなお良い
CONTEXT_FILE=$(uv tool run --from git+https://github.com/masa-codehub/issue_creator_kit.git ick dispatch --labels "$LABELS" --get-context || echo "UNKNOWN")

if [ "$CONTEXT_FILE" = "UNKNOWN" ]; then
  echo "Error: Failed to determine context file for role: $AGENT_ROLE"
  exit 1
fi

echo "Selected Agent Role: $AGENT_ROLE"
echo "Selected Context File: $CONTEXT_FILE"


# ファイル存在確認
if [[ ! -f "$CONTEXT_FILE" ]]; then
  echo "Error: Context file not found: $CONTEXT_FILE"
  exit 1
fi

# 環境変数のエクスポート（envsubst用）
export ISSUE_NUMBER
export ISSUE_TITLE
export ISSUE_BODY

# 一時ファイルのクリーンアップ設定
trap 'rm -f prompt.md' EXIT

# コンテキストの置換と実行
envsubst '$ISSUE_NUMBER $ISSUE_TITLE $ISSUE_BODY' < "${CONTEXT_FILE}" > prompt.md

echo "--- Gemini Execution Start ---"

# gemini コマンドの存在確認
if ! command -v gemini >/dev/null 2>&1; then
  echo "Error: 'gemini' command not found."
  echo "Please install or activate the environment that provides the 'gemini' CLI."
  exit 1
fi

# geminiコマンドにプロンプトを渡し、モデルを指定して実行させる
cat prompt.md | gemini --yolo -m "gemini-3-flash-preview"

echo "--- Gemini Execution End ---"
