#!/bin/bash

# --- 仮想環境 (venv) の自動アクティベート設定のセットアップ ---

echo "Adding venv auto-activation settings to .bashrc..."

# 1. .bashrc への自動アクティベート設定の追記
TARGET_FILE="$HOME/.bashrc"
MARKER="# === AUTO-ACTIVATE-VENV ==="

if grep -qF "$MARKER" "$TARGET_FILE" 2>/dev/null; then
    echo "✅ venv setup is already present in $TARGET_FILE. Skipping update."
else
    echo "✍️  Adding venv setup to $TARGET_FILE..."
    cat <<EOT >> "$TARGET_FILE"

$MARKER
# シェル起動時にカレントディレクトリに .venv があれば自動で activate する
# (起動後のディレクトリ移動には追従しません)
if [ -z "$VIRTUAL_ENV" ]; then
    if [ -d ".venv" ] && [ -f ".venv/bin/activate" ]; then
        source .venv/bin/activate
    fi
fi
EOT
    echo "🎉 Done! Please restart your shell or run 'source $TARGET_FILE' to reflect changes."
fi
