#!/bin/bash
set -e

DEST_DIR="${SYNC_DEST_DIR:-template-repo}"

cd dev-repo

# YAMLからrsync用のフィルタールールを生成
uv run python -c '
import yaml

with open(".github/sync-template-config.yml") as f:
    config = yaml.safe_load(f)

with open("../filter-rules.txt", "w") as f:
    # 1. 除外リスト (優先)
    for exc in config.get("exclude", []):
        f.write(f"- {exc}\n")
    # 2. 許可リスト
    for inc in config.get("include", []):
        f.write(f"+ {inc}\n")
    # 3. その他すべてを除外
    f.write("- *\n")
'
cd ..

# dev-repo から template-repo へ必要なファイルだけコピー
# --delete オプションをつけることで、dev-repo 側で削除されたファイルは
# template-repo 側（の同期対象ディレクトリ内）でも削除されます。
rsync -av --delete --filter="merge filter-rules.txt" dev-repo/ "$DEST_DIR"/