# Integration Audit Specification

## 1. Overview

- **Responsibility**: ADR-013 「Strict Data Standardization & Document Refactoring」のリファクタリングが正しく完了していることを検証する。
- **Collaborators**: すべての Permanent Specs (`docs/specs/**/*.md`), `definitions.md`.

## 2. Input

| Name             | Type           | Description                                                      |
| :--------------- | :------------- | :--------------------------------------------------------------- |
| `definitions.md` | Markdown File  | 統合マッピング定義 (`reqs/context/specs/adr-013/definitions.md`) |
| `specs_dir`      | Directory Path | 仕様書が配置されているディレクトリ (`docs/specs/`)               |

## 3. Output

| Type          | Description                                    |
| :------------ | :--------------------------------------------- |
| `AuditReport` | 各項目の PASS/FAIL 判定と、FAIL 時の修正指示。 |

## 4. Algorithm / Flow

### 4.1. Legacy File Elimination Check

1. `definitions.md` の "Source Files (Legacy)" 列に記載されているすべてのファイルをリストアップする。
2. それらのファイルが物理的に削除されている（存在しない）ことを確認する。
3. もし存在する場合、`LEGACY_FILE_REMAINING` エラーを報告する。

**検証コマンド例:**

```bash
# definitions.md からレガシーファイルリストを抽出
LEGACY_FILES=$(awk -F'|' 'NR > 2 {gsub(/ /,""); print $2}' reqs/context/specs/adr-013/definitions.md | grep -v ':-' | grep -v 'SourceFiles(Legacy)' | grep -v '^$')

for file in $LEGACY_FILES; do
  if [ -f "docs/specs/$file" ]; then
    echo "LEGACY_FILE_REMAINING: $file"
  fi
done
```

### 4.2. Permanent File Existence Check

1. `definitions.md` の "Destination File (Permanent)" 列に記載されているすべてのファイルをリストアップする。
2. それらのファイルが指定されたパスに存在することを確認する。
3. もし存在しない場合、`PERMANENT_FILE_MISSING` エラーを報告する。

**検証コマンド例:**

```bash
# definitions.md から恒久ファイルリストを抽出
PERM_FILES=$(awk -F'|' 'NR > 2 {gsub(/ /,""); print $3}' reqs/context/specs/adr-013/definitions.md | grep -v ':-' | grep -v 'DestinationFile(Permanent)' | grep -v '^$')

for file in $PERM_FILES; do
  if [ ! -f "docs/specs/$file" ]; then
    echo "PERMANENT_FILE_MISSING: docs/specs/$file"
  fi
done
```

### 4.3. Traceability Consistency Check

1. 各 Destination File を開き、末尾の `Traceability` セクションを確認する。
2. `Merged Files` リストに、対応する Source Files がすべて含まれていることを確認する。
3. 欠落がある場合、`TRACEABILITY_INCOMPLETE` エラーを報告する。

**検証コマンド例:**

```bash
# 特定の恒久ファイル内に対象の旧ファイルが記載されているか確認
grep -q "adr-010-github-adapter-ext.md" docs/specs/api/github-adapter.md || echo "TRACEABILITY_INCOMPLETE: docs/specs/api/github-adapter.md"
```

### 4.4. Frontmatter Schema Check

1. `reqs/` 配下のすべての `.md` ファイルをスキャンする。
2. フロントマターに `type` フィールドが存在し、以下のいずれかであることを確認する：
   - `adr`
   - `task`
   - `integration`
3. 欠落または不正な値がある場合、`METADATA_INVALID_TYPE` エラーを報告する。

**検証コマンド例:**

```bash
# type フィールドが許可された値以外（または不在）のファイルを検出
find reqs/ -name "*.md" | xargs grep -L "^type: "
find reqs/ -name "*.md" | xargs grep "^type: " | grep -vE "adr|task|integration"
```

### 4.5. Error Code Standardization Check

1. **スキャン対象**: `docs/specs/` 配下のすべての `.md` ファイル（`docs/specs/**/*.md`）。
2. **カスタムエラーコードの検出対象**: テキスト中の「大文字スネークケース」のトークンを候補とする。
   - 候補パターン: `\b[A-Z][A-Z0-9_]*_[A-Z0-9_]*\b`
3. **正しい形式（合格条件）**: カスタムエラーコードが `[ERROR_CODE]` 形式（大文字スネークケース、角括弧 `[]` 囲み）であること。
4. **判定アルゴリズム**:
   - (a) テキスト全体から角括弧で囲まれているトークンを `\[[^]]+\]` で抽出し、その中身が `[A-Z][A-Z0-9_]*_[A-Z0-9_]*` にマッチしないものをエラーとする。
   - (b) 角括弧の外側に出現するカスタムエラーコード候補（`\b[A-Z][A-Z0-9_]*_[A-Z0-9_]*\b` にマッチし、かつ直前直後が `[` `]` ではないもの）をエラーとする。
5. **報告**: フォーマットエラーが1件以上見つかった場合、`ERROR_CODE_FORMAT_INVALID` エラーを報告する。レポートには該当ファイルパス、行番号、検出された不正形式のトークンを含める。

**検証コマンド例:**

```bash
# 角括弧で囲まれていない大文字スネークケース（アンダースコア1つ以上含む）を検出
grep -rE "(^|[^[])\b[A-Z][A-Z0-9_]*_[A-Z0-9_]*\b([^]]|$)" docs/specs/ --exclude-dir=plans --exclude-dir=_archive
```

## 5. Edge Cases

- `definitions.md` 自体が見つからない場合: 監査不能として即時エラー終了。
- 統合先ファイルが複数の ADR に跨る場合: すべての関連 ADR 情報が `Traceability` に集約されているかを確認。

## 6. Traceability

- **Merged Files**: None (New Specification for Integration Audit)
- **Handover Constraints**:
  - ADR-013: Pure Active Git (Archive removal)
  - ADR-013: Strict Data Standardization (Required type field)
