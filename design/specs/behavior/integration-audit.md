# Integration Audit Specification (ADR-017)

## 1. Overview

- **Responsibility**: ADR-017 「TDA-based Project Restructuring」のリファクタリングが正しく完了していることを検証する。
- **Collaborators**: すべての Permanent Specs (`design/specs/**/*.md`), `specs-migration-backlog.md`.

## 2. Input

| Name                         | Type           | Description                                                            |
| :--------------------------- | :------------- | :--------------------------------------------------------------------- |
| `specs-migration-backlog.md` | Markdown File  | 移行マッピング定義 (`reqs/context/adr-017/specs-migration-backlog.md`) |
| `specs_dir`                  | Directory Path | 仕様書が配置されている新ディレクトリ (`design/specs/`)                 |

## 3. Output

| Type          | Description                                    |
| :------------ | :--------------------------------------------- |
| `AuditReport` | 各項目の PASS/FAIL 判定と、FAIL 時の修正指示。 |

## 4. Algorithm / Flow

### 4.1. Legacy File Elimination Check

1. `specs-migration-backlog.md` の "元ファイル (Source)" 列に記載されているすべてのファイルをリストアップする。
2. それらのファイルが物理的に削除されている（存在しない）ことを確認する。
3. もし存在する場合、`LEGACY_FILE_REMAINING` エラーを報告する。

**検証コマンド例:**

```bash
# specs-migration-backlog.md からレガシーファイルリストを抽出 (design/specs/ および design/architecture/)
LEGACY_FILES=$(grep -hE "^\| \`docs/(specs|architecture)/" reqs/context/adr-017/specs-migration-backlog.md | awk -F'|' '{gsub(/ /,""); gsub(/`/,""); print $2}')

for file in $LEGACY_FILES; do
  if [ -f "$file" ]; then
    echo "LEGACY_FILE_REMAINING: $file"
  fi
done
```

### 4.2. Permanent File Existence Check

1. `specs-migration-backlog.md` の "移行先 (Target)" 列に記載されているすべてのファイルをリストアップする。
2. それらのファイルが指定されたパスに存在することを確認する。
3. もし存在しない場合、`PERMANENT_FILE_MISSING` エラーを報告する。

**検証コマンド例:**

```bash
# specs-migration-backlog.md から移行先ファイルリストを抽出
TARGET_FILES=$(grep -hE "^\| \`docs/(specs|architecture)/" reqs/context/adr-017/specs-migration-backlog.md | awk -F'|' '{gsub(/ /,""); gsub(/`/,""); print $3}')

for file in $TARGET_FILES; do
  # 実際の実装では  プレフィックスが付与されているかを確認
  dir=$(dirname "$file")
  base=$(basename "$file")
  expected_file="$dir/$base"

  if [ ! -f "$expected_file" ]; then
    # プレフィックスなしでも存在しない場合はエラー
    if [ ! -f "$file" ]; then
      echo "PERMANENT_FILE_MISSING: $expected_file (or $file)"
    fi
  fi
done
```

### 4.3. Traceability Consistency Check

1. 各 Target File を開き、末尾の `Traceability` セクションを確認する。
2. `Merged Files` リストに、対応する Source Files がすべて含まれていることを確認する。
3. 欠落がある場合、`TRACEABILITY_INCOMPLETE` エラーを報告する。

**検証コマンド例:**

```bash
# 特定の恒久ファイル内に対象の旧ファイルが記載されているか確認
grep -q "design/specs/api/github-adapter.md" design/specs/api/github-adapter.md || echo "TRACEABILITY_INCOMPLETE: design/specs/api/github-adapter.md"
```

### 4.4. Frontmatter Schema Check

1. `reqs/tasks/` 配下のすべての `.md` ファイルをスキャンする。
2. フロントマターに `type` フィールドが存在し、以下のいずれかであることを確認する：
   - `adr`
   - `task`
   - `integration`
   - `spec`
3. 欠落または不正な値がある場合、`METADATA_INVALID_TYPE` エラーを報告する。

**検証コマンド例:**

```bash
# reqs/tasks/ 配下の type フィールドを検証
find reqs/tasks/ -name "*.md" | xargs grep -L "^type: "
find reqs/tasks/ -name "*.md" | xargs grep "^type: " | grep -vE "^type: (adr|task|integration|spec)$"
```

### 4.5. Path Consistency Check (Interim)

1. **スキャン対象**: `design/specs/` 配下のすべての `.md` ファイル。
2. **判定**: ファイル内で、Markdown リンクなどの「参照」として `design/specs/` などの古いパスが残っていないかを確認する。
3. **報告**: 古いパスが見つかった場合、`OBSOLETE_PATH_FOUND` エラーを報告する。

**検証コマンド例:**

```bash
# Markdown リンクにおける design/specs/ または design/architecture/ の残存を検出
# (コードブロックや Traceability セクション内のプレーンテキストは除外するため、リンク形式を狙う)
grep -rE "\[[^]]*\]\(docs/(specs|architecture)/" design/specs/
```

## 5. Edge Cases

- `specs-migration-backlog.md` 自体が見つからない場合: 監査不能として即時エラー終了。
- `` プレフィックスの有無: 一貫性を保つため、すべての新規/移行ファイルに必須とする。

## 6. Traceability

- **Merged Files**: `design/specs/integration-audit.md`
- **Handover Constraints**:
  - ADR-017: TDA-based Project Restructuring
  - ADR-017: Filename Normalization ( prefix)
