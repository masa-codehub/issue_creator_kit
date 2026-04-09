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
# プライバシー保護のため、noreply アドレスを優先的に組み立てる
# フォーマット: ID+username@users.noreply.github.com
DEFAULT_USER="masa-codehub"
DEFAULT_NOREPLY_EMAIL="155802505+masa-codehub@users.noreply.github.com"

# ユーザー名の確定
GIT_USER="${GITHUB_USER:-$DEFAULT_USER}"

# noreply メールアドレスの動的組み立て
if [ -n "${GITHUB_NOREPLY_EMAIL:-}" ]; then
    NOREPLY_EMAIL="$GITHUB_NOREPLY_EMAIL"
elif [ -n "${GITHUB_USER_ID:-}" ] && [ -n "$GIT_USER" ]; then
    NOREPLY_EMAIL="${GITHUB_USER_ID}+${GIT_USER}@users.noreply.github.com"
elif [ -n "$GIT_USER" ] && [ "$GIT_USER" != "$DEFAULT_USER" ]; then
    NOREPLY_EMAIL="${GIT_USER}@users.noreply.github.com"
else
    NOREPLY_EMAIL="$DEFAULT_NOREPLY_EMAIL"
fi

# メールアドレスの確定と安全性チェック
# 外部からの注入（GITHUB_EMAIL）は、基本的なメール形式を満たし、
# かつ明示的に拒否したいドメイン（過去の汚染原因や仮アドレス）でない場合のみ採用する。
# ブロック対象ドメインは GITHUB_BLOCKED_DOMAINS から取得可能（デフォルトは google.com, outlook.jp）
FINAL_EMAIL="$NOREPLY_EMAIL"
if [ -n "${GITHUB_EMAIL:-}" ] && [[ "$GITHUB_EMAIL" =~ ^[^@[:space:]]+@[^@[:space:]]+$ ]]; then
    IS_BLOCKED=false
    for domain in ${GITHUB_BLOCKED_DOMAINS:-google.com outlook.jp}; do
        if [[ "$GITHUB_EMAIL" == *"$domain"* ]]; then
            IS_BLOCKED=true
            break
        fi
    done
    if [ "$IS_BLOCKED" = false ]; then
        FINAL_EMAIL="$GITHUB_EMAIL"
    else
        echo "Warning: GITHUB_EMAIL domain is in blocklist. Falling back to noreply."
    fi
fi

echo "Configuring Git identity: $GIT_USER <$FINAL_EMAIL>"

# 環境変数の設定 (Git の最優先)
export GIT_AUTHOR_NAME="$GIT_USER"
export GIT_AUTHOR_EMAIL="$FINAL_EMAIL"
export GIT_COMMITTER_NAME="$GIT_USER"
export GIT_COMMITTER_EMAIL="$FINAL_EMAIL"

# Git Config (--local) の強制上書き
# これにより、環境変数を引き継がないサブシェルやツールでも正しい識別情報が維持される
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    git config --local user.name "$GIT_USER"
    git config --local user.email "$FINAL_EMAIL"
fi

# 5. Git 認証（Authentication）の設定
# ユーザー名の設定（指定がなければ x-access-token を使用）
AUTH_USER="${GITHUB_USER:-x-access-token}"

# Dogfooding（repo: .）を可能にするため、現在のディレクトリを安全なディレクトリとして登録
echo "Configuring safe.directory..."
git config --global --add safe.directory /app/.git
git config --global --add safe.directory /app

# CI環境（GITHUB_ACTIONS=true）では、プロセス越しの認証を確実にするためグローバル設定に直接追加
if [ "$GITHUB_ACTIONS" = "true" ]; then
    echo "Configuring git insteadOf for CI environment..."
    git config --global "url.https://${AUTH_USER}:${TOKEN}@github.com/.insteadOf" "https://github.com/"
fi

# トークンがプロセス一覧（ps等）に露出しないよう、一時的な git 設定ファイルを使用する
export TMP_GITCONFIG="$(mktemp "${TMPDIR:-/tmp}/gitconfig.XXXXXX")"
chmod 600 "$TMP_GITCONFIG"
cat > "$TMP_GITCONFIG" <<EOF
[url "https://${AUTH_USER}:${TOKEN}@github.com/"]
    insteadOf = https://github.com/
EOF

# グローバル設定に一時ファイルを追加（セッション内でのみ有効にするため、呼び出し元で trap が必要）
git config --global --add include.path "$TMP_GITCONFIG"

# このスクリプトが直接実行された（source されていない）場合は、終了時に一時ファイルをクリーンアップする
if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
    trap 'git config --global --unset-all include.path "$TMP_GITCONFIG" || true; rm -f "$TMP_GITCONFIG"' EXIT
fi
