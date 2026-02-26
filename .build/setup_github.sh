#!/bin/bash

# --- GitHub 関連の認証・識別設定を一括で行うスクリプト ---

# 1. GitHub トークンの特定
# 優先順位: GITHUB_MCP_PAT > GITHUB_TOKEN > GH_TOKEN
TOKEN=""
if [ -n "$GITHUB_MCP_PAT" ]; then
    TOKEN="$GITHUB_MCP_PAT"
elif [ -n "$GITHUB_TOKEN" ]; then
    TOKEN="$GITHUB_TOKEN"
elif [ -n "$GH_TOKEN" ]; then
    TOKEN="$GH_TOKEN"
fi

if [ -z "$TOKEN" ]; then
    echo "Warning: No GitHub token found. Skipping GitHub authentication."
    return 0 2>/dev/null || exit 0
fi

# 2. MCP サーバー用変数の確定
export GITHUB_MCP_PAT="$TOKEN"

# 3. GitHub CLI (gh) の認証
if command -v gh &> /dev/null; then
    echo "Authenticating GitHub CLI..."
    echo "$TOKEN" | gh auth login --with-token
fi

# 4. Git ユーザー識別（Identification）の設定
if [ -n "$GITHUB_USER" ]; then
    echo "Configuring Git user identity as '$GITHUB_USER' (environment only)..."
    export GIT_AUTHOR_NAME="$GITHUB_USER"
    export GIT_COMMITTER_NAME="$GITHUB_USER"
fi

if [ -n "$GITHUB_EMAIL" ]; then
    echo "Configuring Git user email as '$GITHUB_EMAIL' (environment only)..."
    export GIT_AUTHOR_EMAIL="$GITHUB_EMAIL"
    export GIT_COMMITTER_EMAIL="$GITHUB_EMAIL"
fi

# 5. Git 認証（Authentication）の設定
# ユーザー名の設定（指定がなければ x-access-token を使用）
GIT_USER="${GITHUB_USER:-x-access-token}"

# Dogfooding（repo: .）を可能にするため、現在のディレクトリを安全なディレクトリとして登録
echo "Configuring safe.directory..."
git config --global --add safe.directory /app/.git
git config --global --add safe.directory /app

# CI環境（GITHUB_ACTIONS=true）では、プロセス越しの認証を確実にするためグローバル設定に直接追加
if [ "$GITHUB_ACTIONS" = "true" ]; then
    echo "Configuring git insteadOf for CI environment..."
    git config --global "url.https://${GIT_USER}:${TOKEN}@github.com/.insteadOf" "https://github.com/"
fi

# トークンがプロセス一覧（ps等）に露出しないよう、一時的な git 設定ファイルを使用する
export TMP_GITCONFIG="$(mktemp "${TMPDIR:-/tmp}/gitconfig.XXXXXX")"
chmod 600 "$TMP_GITCONFIG"
cat > "$TMP_GITCONFIG" <<EOF
[url "https://${GIT_USER}:${TOKEN}@github.com/"]
    insteadOf = https://github.com/
EOF

# グローバル設定に一時ファイルを追加（セッション内でのみ有効にするため、呼び出し元で trap が必要）
git config --global --add include.path "$TMP_GITCONFIG"

# このスクリプトが直接実行された（source されていない）場合は、終了時に一時ファイルをクリーンアップする
if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
    trap 'git config --global --unset-all include.path "$TMP_GITCONFIG" || true; rm -f "$TMP_GITCONFIG"' EXIT
fi
