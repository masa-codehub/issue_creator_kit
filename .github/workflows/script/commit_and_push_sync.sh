#!/bin/bash
set -e

cd public-repo

git config user.name "${GITHUB_USER:-github-actions[bot]}"
git config user.email "${GITHUB_EMAIL:-github-actions[bot]@users.noreply.github.com}"

git add .

if ! git diff --staged --quiet; then
  BRANCH_NAME="sync-release-${RELEASE_TAG_NAME}"
  git checkout -b "$BRANCH_NAME"
  git commit -m "chore: release ${RELEASE_TAG_NAME}"
  git push origin "$BRANCH_NAME"
  
  # GitHub CLIを使用してPRを作成
  gh pr create \
    --title "chore: sync release ${RELEASE_TAG_NAME}" \
    --body "Automated synchronization of release ${RELEASE_TAG_NAME} from the development repository." \
    --head "$BRANCH_NAME" \
    --base main
fi

# タグの作成とプッシュ（タグはPRマージ後に別途手動か別の仕組みで打つ必要が出る場合がありますが、ここでは一旦PRブランチに対してタグを打つか、エラーを回避するため一旦タグプッシュは残しておきます。ただし、mainにマージされる前にタグが存在することになります）
# Branch protection に tag protection がなければこれは成功します。
git tag "${RELEASE_TAG_NAME}" -f
git push origin "${RELEASE_TAG_NAME}" -f