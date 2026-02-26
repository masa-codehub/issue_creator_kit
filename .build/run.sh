#!/bin/bash

echo "=== Environment Setup ==="

# uvの設定
export UV_CONCURRENT_DOWNLOADS=4
export UV_CONCURRENT_BUILDS=2
export UV_CONCURRENT_INSTALLS=4
export UV_LINK_MODE=copy

# --- GitHub 認証・ユーザー設定 ---
if [ -f ".build/setup_github.sh" ]; then
    source ".build/setup_github.sh"
    # setup_github.sh で設定された git config と一時ファイルをクリーンアップする
    # CI環境（GITHUB_ACTIONS=true）では、後続のステップ（pre-commit等）で認証が必要なため解除しない
    if [ -n "$TMP_GITCONFIG" ] && [ "$GITHUB_ACTIONS" != "true" ]; then
        trap 'git config --global --unset-all include.path "$TMP_GITCONFIG" || true; rm -f "$TMP_GITCONFIG"' EXIT
    fi
fi

# 1. 依存関係の同期（毎回実行: 変更がなければ高速）
if [ -f "pyproject.toml" ]; then
    echo "Syncing dependencies..."
    # setup_github.sh で設定された git config が自動的に適用される
    uv sync --all-extras
fi

# 2. .gemini サブモジュールの更新（毎回実行: 変更がなければ高速）
if [ -d ".git" ] && [ -f ".gitmodules" ]; then
    echo "Updating submodules..."
    # setup_github.sh で設定された git config が自動的に適用される
    git submodule update --init --recursive || echo "Warning: Failed to update submodules."
fi

# 3. Git フックのセットアップ
if [ -d ".git" ]; then
    echo "Installing/Updating pre-commit hooks..."
    # 非対話環境でのハングを防ぐため credential.helper を無効化
    GIT_CONFIG_PARAMETERS="'credential.helper='" uv run pre-commit install
fi

# 4. 仮想環境の設定（.bashrc への追記など）
# SETUP_VENV_BASHRC=1 が指定されている場合のみ実行（副作用の抑制）
if [ "$SETUP_VENV_BASHRC" = "1" ] && [ -f ".build/setup_venv.sh" ]; then
    source .build/setup_venv.sh
fi

# --- 仮想環境のアクティベート（常に実行） ---
if [ -f ".venv/bin/activate" ]; then
    source ".venv/bin/activate"
fi

# --- 毎回実行が必要な更新処理 ---
# コンテキスト更新
if [ -f ".build/update_gemini_context.sh" ]; then
    bash .build/update_gemini_context.sh
fi

# Gemini拡張機能のインストール
gemini extensions install https://github.com/github/github-mcp-server --consent --auto-update || true

echo "=== Setup Complete ==="
