#!/bin/bash
set -e

# public-repo の中のファイルを一旦空にする（.git履歴は残す）
find public-repo -mindepth 1 -maxdepth 1 ! -name '.git' -exec rm -rf {} +

# YAMLからリストを抽出し、rsyncのexclude-fromファイルを作成
grep -E '^\s*-\s+' dev-repo/.github/sync-config.yml | sed -E 's/^\s*-\s+['\''"]?([^'\''"]+)['\''"]?/\1/' > exclude.txt

# dev-repo から public-repo へ必要なファイルだけコピー
# --filter='dir-merge,- .gitignore' で、各ディレクトリの .gitignore を読み込んで除外します
rsync -av --filter='dir-merge,- .gitignore' --exclude-from=exclude.txt dev-repo/ public-repo/