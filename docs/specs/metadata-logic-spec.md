# 詳細設計: メタデータ操作ロジック (ADR-002)

## 1. 目的
ADR-002（ドキュメント承認フローの自動化）において、Markdownファイルのメタデータを安全かつ正確に読み取り・更新するための技術仕様を定義する。
本仕様では、構造化データの扱いやすさと拡張性を考慮し、**YAML Frontmatter** を採用する。

## 2. メタデータの構造
ドキュメントの最上部に、YAML形式でメタデータを記述する（Frontmatter）。

- **形式**:
  ```markdown
  ---
  key1: value1
  key2: value2
  list_key:
    - item1
    - item2
  ---
  # タイトル
  ...
  ```
- **必須キー (Issue Draftの場合)**:
    - `title`: 文字列
    - `status`: 文字列 (Draft, Open, Closed, etc.)
    - `roadmap`: 文字列 (パス)
    - `task_id`: 文字列
    - `depends_on`: リスト (依存ファイル名)

## 3. 操作ロジック

### 3.1. ライブラリ選定
Python の `python-frontmatter` ライブラリを使用する。
正規表現による独自解析は行わない（保守性と堅牢性のため）。

### 3.2. 読み込み (Load)
`frontmatter.load(file_path)` または `frontmatter.loads(content)` を使用して、メタデータ（辞書）と本文を取得する。

### 3.3. 更新・保存 (Update & Save)
1. ファイルを読み込み、Postオブジェクト（メタデータ + 本文）を取得する。
2. Postオブジェクトのメタデータ辞書を更新する。
3. `frontmatter.dumps(post)` を使用して文字列に再変換し、ファイルに書き込む。

## 4. 検証パターン
YAML Frontmatter の仕様に準拠するため、以下のケースを検証対象とする。

| ケース | 入力例 | 期待される動作 |
| :--- | :--- | :--- |
| 標準形式 | `---`<br>`status: Draft`<br>`---` | `{"status": "Draft"}` として解析可能 |
| リスト形式 | `labels:`<br>`  - bug` | `{"labels": ["bug"]}` として解析可能 |
| Frontmatterなし | (本文のみ) | メタデータは空 `{}`、本文はそのまま取得 |
| 不正なYAML | `key: value: error` | `yaml.scanner.ScannerError` 等の例外が発生 |

## 5. 考慮事項
- **文字コード**: UTF-8 を前提とする。
- **コメント**: YAML内のコメント `# comment` は維持されるが、ライブラリの挙動に依存するため、重要な情報はコメントではなくキーとして保持することを推奨する。
- **順序**: `python-frontmatter` (および PyYAML) は通常、キーの順序を保持しない場合があるが、メタデータとしての意味には影響しない。