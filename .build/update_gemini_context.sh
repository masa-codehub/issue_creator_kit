#!/bin/bash

AGENT_ROLE_UPPER=$(echo $AGENT_ROLE | tr '[:lower:]' '[:upper:]')

if [ -z "$AGENT_ROLE_UPPER" ]; then
    echo "エラー: AGENT_ROLE 環境変数が設定されていません。" >&2
    exit 1
fi

# リポジトリのルートディレクトリを取得
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

GEMINI_MD_PATH="${REPO_ROOT}/.gemini/GEMINI.md"
AGENT_MD_PATH="${REPO_ROOT}/.gemini/AGENTS/${AGENT_ROLE_UPPER}.md"

if [ ! -f "$AGENT_MD_PATH" ]; then
    echo "エラー: エージェントロールファイルが $AGENT_MD_PATH に見つかりません。" >&2
    exit 1
fi

if [ ! -f "$GEMINI_MD_PATH" ]; then
    touch "$GEMINI_MD_PATH"
fi

cp "$AGENT_MD_PATH" "$GEMINI_MD_PATH"

if [ $? -eq 0 ]; then
    echo "$GEMINI_MD_PATH を $AGENT_MD_PATH の内容で正常に更新しました。"
else
    echo "エラー: $AGENT_MD_PATH から $GEMINI_MD_PATH へのファイルコピーに失敗しました。" >&2
    exit 1
fi
