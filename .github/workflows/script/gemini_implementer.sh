#!/bin/bash
set -e

# ラベル情報の取得 (環境変数 ISSUE_LABELS を使用)
LABELS="${ISSUE_LABELS}"

echo "Processing Issue #${ISSUE_NUMBER}: ${ISSUE_TITLE}"
echo "Labels: ${LABELS}"

# コンテキストファイルの選択
CONTEXT_FILE=""
MATCH_COUNT=0

if [[ "$LABELS" == *"gemini:arch"* ]]; then
  CONTEXT_FILE=".github/workflows/context/arch-prompt.md"
  echo "Selected Skill: Architecture Drafting"
  ((++MATCH_COUNT))
fi

if [[ "$LABELS" == *"gemini:spec"* ]]; then
  CONTEXT_FILE=".github/workflows/context/spec-prompt.md"
  echo "Selected Skill: Specification Drafting"
  ((++MATCH_COUNT))
fi

if [[ "$LABELS" == *"gemini:tdd"* ]]; then
  CONTEXT_FILE=".github/workflows/context/tdd-prompt.md"
  echo "Selected Skill: TDD Implementation"
  ((++MATCH_COUNT))
fi

# 複数ラベルまたは該当なしのチェック
if [[ "$MATCH_COUNT" -gt 1 ]]; then
  echo "Error: Multiple gemini labels detected. Please use only one label per issue."
  exit 1
elif [[ "$MATCH_COUNT" -eq 0 ]]; then
  echo "No matching gemini label found. Skipping execution."
  exit 0
fi

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
# envsubst で許可された変数のみを展開して一時ファイルに保存（セキュリティ対策）
envsubst '$ISSUE_NUMBER $ISSUE_TITLE $ISSUE_BODY' < "${CONTEXT_FILE}" > prompt.md

echo "--- Gemini Execution Start ---"

# 仮想環境のアクティベート
if [ -f ".venv/bin/activate" ]; then
  source ".venv/bin/activate"
else
  echo "Warning: .venv/bin/activate not found. Assuming gemini is in PATH."
fi

# gemini コマンドの存在確認
if ! command -v gemini >/dev/null 2>&1; then
  echo "Error: 'gemini' command not found."
  echo "Please install or activate the environment that provides the 'gemini' CLI (e.g., create and activate .venv with gemini installed)."
  exit 1
fi

# geminiコマンドにプロンプトを渡し、モデルを指定して実行させる

cat prompt.md | gemini --yolo -m "gemini-3-flash-preview"

echo "--- Gemini Execution End ---"
