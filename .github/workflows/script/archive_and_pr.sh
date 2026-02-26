#!/bin/bash
set -euo pipefail

# ==============================================================================
# Archive and PR Script
# ==============================================================================
# ADR-014準拠: インラインスクリプトの排除とパラメータ経由の制御
#
# プロセスが完了したタスクファイル（reqs配下）を _archive に移動した変更を、
# 新しいブランチにコミットしてPull Requestを作成します。
#
# 引数 (Arguments):
#   $1 - ACTOR         : GitHub アクター（実行者）の名前
#   $2 - COMMIT_EMAIL  : コミット時に使用するメールアドレス
#   $3 - COMMIT_MSG    : トリガーとなったコミットのメッセージ（[skip ci]の判定用）
#   $4 - BASE_BRANCH   : Pull Request の宛先ブランチ
# ==============================================================================

ACTOR="${1:-github-actions[bot]}"
COMMIT_EMAIL="${2:-}"
COMMIT_MSG="${3:-}"
BASE_BRANCH="${4:-main}"

echo "=== Archiving and Pull Request Creation ==="

# 1. 変更の有無を確認
# reqs/ ディレクトリ内の変更をすべてステージングし、差分がない場合は終了
git add -A reqs/
if git diff --cached --quiet reqs/; then
    echo "Info: No changes in reqs/ detected. Skipping PR creation."
    exit 0
fi

# 2. 無限ループ防止 (Bot アクターからの実行を除外)
if [ "$ACTOR" = "github-actions[bot]" ]; then
    echo "Info: Skipping PR creation for github-actions[bot] to prevent execution loops."
    exit 0
fi

# 3. [skip ci] の判定
if [[ "$COMMIT_MSG" == *"[skip ci]"* ]]; then
    echo "Info: Skipping PR creation due to [skip ci] directive in commit message."
    exit 0
fi

# 4. Git ユーザー情報の設定
# メールアドレスが未指定の場合は、GitHub提供のnoreplyアドレスを使用
if [ -z "$COMMIT_EMAIL" ]; then
  if [ -n "${GITHUB_EMAIL:-}" ]; then
    COMMIT_EMAIL="$GITHUB_EMAIL"
  else
    COMMIT_EMAIL="${ACTOR}@users.noreply.github.com"
  fi
fi

GIT_USER="${GITHUB_USER:-masa-codehub}"
echo "Configuring git user identity (Name: $GIT_USER, Email: $COMMIT_EMAIL)..."
git config user.name "$GIT_USER"
git config user.email "$COMMIT_EMAIL"

# 5. ブランチの判定とコミット
git fetch origin

# Release Please のデフォルトブランチ名
RP_BRANCH="release-please--branches--main"

# Release PR 用ブランチに紐づくオープン PR の有無を確認
OPEN_RP_PR_COUNT=$(gh pr list --head "$RP_BRANCH" --state open --json number --jq 'length')

if git ls-remote --exit-code --heads origin "$RP_BRANCH" > /dev/null && [ "$OPEN_RP_PR_COUNT" -gt 0 ]; then
    echo "Release PR branch ($RP_BRANCH) with open PR exists. Merging archive changes into it..."
    # リモートのPRブランチからローカル追跡ブランチを作成/更新してチェックアウト
    git fetch origin "$RP_BRANCH:refs/heads/$RP_BRANCH"
    git checkout "$RP_BRANCH"
    
    echo "Committing archived tasks to Release PR..."
    git commit -m "chore: archive processed tasks"
    
    echo "Pushing branch to origin..."
    git push origin "$RP_BRANCH"
    echo "Archive changes successfully pushed to existing Release PR."
else
    BRANCH_NAME="chore/archive-tasks-$(date +%Y%m%d-%H%M%S)"
    echo "Creating new standalone branch: $BRANCH_NAME"
    git checkout -b "$BRANCH_NAME"

    echo "Committing archived tasks..."
    git commit -m "chore: archive processed tasks"

    echo "Pushing branch to origin..."
    git push origin "$BRANCH_NAME"

    # 6. Pull Request の作成
    echo "Creating Pull Request to base branch '$BASE_BRANCH'..."
    gh pr create \
      --title "chore: archive processed tasks" \
      --body "Automated task archiving after issue creation. Please review and merge." \
      --base "$BASE_BRANCH" \
      --head "$BRANCH_NAME" \
      --label chore

    echo "Standalone Pull Request successfully created."
fi
