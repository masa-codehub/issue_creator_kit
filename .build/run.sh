#!/bin/bash

echo "=== Environment Setup ==="

# ★ 追加設定: uv の暴走（リソース食いつぶし）を防ぐ
# 並列数を 4 程度に制限（デフォルトはCPU全開なので、Dockerだと落ちやすい）
export UV_CONCURRENT_DOWNLOADS=4
export UV_CONCURRENT_BUILDS=2
export UV_CONCURRENT_INSTALLS=4

# ★ 追加設定: 警告が出ていたハードリンク問題を明示的に解決
export UV_LINK_MODE=copy

# 1. 依存関係の同期
if [ -f "pyproject.toml" ]; then
    echo "Syncing dependencies..."
    # --all-extras: dev依存なども含めて全部入れる
    uv sync --all-extras
fi

# .gemini サブモジュールの更新
# 優先順位: GITHUB_MCP_PAT > GH_TOKEN > GITHUB_TOKEN
TOKEN=""
if [ -n "$GITHUB_MCP_PAT" ]; then
    TOKEN="$GITHUB_MCP_PAT"
elif [ -n "$GH_TOKEN" ]; then
    TOKEN="$GH_TOKEN"
elif [ -n "$GITHUB_TOKEN" ]; then
    TOKEN="$GITHUB_TOKEN"
fi

if [ -n "$TOKEN" ]; then
    echo "Configuring git to use token for submodule updates..."
    # サブモジュールのURLを動的にトークン付きに変更する代わりに、git config の insteadOf を使用
    # これにより .gitmodules のURLを汚さずに認証を通せる
    git config --global url."https://x-access-token:${TOKEN}@github.com/".insteadOf "https://github.com/"
fi

echo "Updating submodules..."
git submodule update --init --recursive || echo "Warning: Failed to update submodules. Continuing anyway..."

# 2. pre-commit のインストール
if [ -d ".git" ]; then
    echo "Installing pre-commit hooks..."
    uv run pre-commit install
fi

# コンテキスト更新など
if [ -f ".build/update_gemini_context.sh" ]; then
    bash .build/update_gemini_context.sh
fi

# 仮想環境のアクティベート
echo "Activating virtual environment..."
# 設定対象のファイル
TARGET_FILE="$HOME/.bashrc"
# 重複チェック用のマーカー（この文字列があれば追記しない）
MARKER="# === AUTO-ACTIVATE-VENV ==="
echo "Checking $TARGET_FILE ..."
# ファイル内にマーカーが存在するか検索
if grep -qF "$MARKER" "$TARGET_FILE"; then
    echo "✅ 設定は既に $TARGET_FILE に存在します。追記をスキップしました。"
else
    echo "✍️  $TARGET_FILE に設定を追記します..."
    # ファイルの末尾に追記
    cat <<EOT >> "$TARGET_FILE"

$MARKER
# カレントディレクトリに .venv があれば自動で activate する
if [ -z "\$VIRTUAL_ENV" ]; then
    if [ -d ".venv" ] && [ -f ".venv/bin/activate" ]; then
        source .venv/bin/activate
    fi
fi
EOT
    echo "🎉 完了しました！"
    echo "設定を反映させるために、以下のコマンドを実行してください："
    echo "source $TARGET_FILE"
fi

# 仮想環境をアクティベート（このスクリプト内での実行用）
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
fi

# Gemini拡張機能のインストール
gemini extensions install https://github.com/github/github-mcp-server --consent --auto-update

echo "=== Setup Complete ==="
