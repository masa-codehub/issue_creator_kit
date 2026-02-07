#!/bin/bash
set -e

echo "=== Environment Setup ==="

# 0. Global Git Safety (Prevent credential leakage on self-hosted runners)
if [ -d ".git" ]; then
    echo "Disabling local credential helper to prevent token leakage..."
    # リポジトリローカルの設定でヘルパーを空文字に上書きする
    # これにより、システム/グローバルの認証情報保存機能がこのリポジトリに対して無効化される
    git config --local credential.helper ""
fi

# uv settings
export UV_CONCURRENT_DOWNLOADS=4
export UV_LINK_MODE=copy

# 1. Sync dependencies
if [ -f "pyproject.toml" ]; then
    echo "Syncing dependencies..."
    uv sync --all-extras
fi

# 2. Update submodules (Securely)
TOKEN="${GITHUB_MCP_PAT:-${GH_TOKEN:-$GITHUB_TOKEN}}"

if [ -n "$TOKEN" ]; then
    echo "Updating submodules with token (Storage disabled)..."
    # Inject token on the fly and disable credential helper for this command
    git -c "url.https://x-access-token:${TOKEN}@github.com/.insteadOf=https://github.com/" \
        -c credential.helper= \
        submodule update --init --recursive || (echo "Fallback to standard update..." && git submodule update --init --recursive)
else
    echo "Updating submodules..."
    git submodule update --init --recursive
fi

# 3. Install pre-commit
if [ -d ".git" ]; then
    # pre-commit自体の実行時も認証キャッシュを使わないよう徹底
    GIT_CONFIG_PARAMETERS="'credential.helper='" uv run pre-commit install
fi

# 4. Update context
if [ -f ".build/update_gemini_context.sh" ]; then
    bash .build/update_gemini_context.sh
fi

# 5. Bashrc auto-activate
MARKER="# === AUTO-ACTIVATE-VENV ==="
TARGET="$HOME/.bashrc"
if [ -f "$TARGET" ] && ! grep -qF "$MARKER" "$TARGET"; then
    echo "Adding auto-activate to $TARGET"
    printf "\n%s\nif [ -z \"\$VIRTUAL_ENV\" ] && [ -f \".venv/bin/activate\" ]; then source .venv/bin/activate; fi\n" "$MARKER" >> "$TARGET"
fi

# 6. Gemini extension
gemini extensions install https://github.com/github/github-mcp-server --consent --auto-update 2>/dev/null || true

echo "=== Setup Complete ==="
