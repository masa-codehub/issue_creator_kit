#!/bin/bash
set -e

# ラベル情報の取得 (環境変数 ISSUE_LABELS を使用)
LABELS="${ISSUE_LABELS}"

echo "Processing Issue #${ISSUE_NUMBER}: ${ISSUE_TITLE}"
echo "Debug: LABELS='${LABELS}'"

# 仮想環境のアクティベート (ick コマンドを使うために先に実行)
if [ -f ".venv/bin/activate" ]; then
  source ".venv/bin/activate"
fi

# ick dispatch でロール（エージェント名）とコンテキストファイル（プロンプト）を決定
# 設定ファイルは .github/issue-kit-config.json をデフォルトで使用
ROLE=$(ick dispatch --labels "$LABELS" || echo "UNKNOWN")
CONTEXT_FILE=$(ick dispatch --labels "$LABELS" --get-context || echo "UNKNOWN")

if [ "$ROLE" = "UNKNOWN" ] || [ "$CONTEXT_FILE" = "UNKNOWN" ]; then
  echo "Error: No matching gemini role or context file found for labels: $LABELS"
  exit 1
fi

echo "Selected Agent Role: $ROLE"
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
  echo "Please install or activate the environment that provides the 'gemini' CLI (e.g., create and activate .venv with gemini installed)."
  exit 1
fi

# geminiコマンドにプロンプトを渡し、モデルを指定して実行させる
cat prompt.md | gemini --yolo -m "gemini-3-flash-preview"

echo "--- Gemini Execution End ---"

