#!/bin/bash
set -e

DEST_DIR="${SYNC_DEST_DIR:-template-repo}"

# ターゲット先の中のファイルを一旦空にする（.git履歴は残す）
find "$DEST_DIR" -mindepth 1 -maxdepth 1 ! -name '.git' -exec rm -rf {} +

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
rsync -av --filter="merge filter-rules.txt" dev-repo/ "$DEST_DIR"/