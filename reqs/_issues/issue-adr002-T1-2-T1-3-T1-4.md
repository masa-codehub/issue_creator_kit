# Issue案: メタデータ操作ユーティリティの実装と共通化

- **Roadmap**: [roadmap-adr002-document-approval-flow.md](../_inbox/roadmap-adr002-document-approval-flow.md)
- **Task ID**: T1-2, T1-3, T1-4
- **Depends-On**: issue-adr002-T1-1.md
- **Status**: Draft

## 1. 目的と背景
ADR-002 で定義された承認フロー自動化には、ドキュメントのメタデータ（Status, Date 等）を確実に解析・更新する共通ユーティリティが必要です。
現在 `create_issues.py` に存在する解析ロジックを抽出し、置換（更新）にも対応した堅牢なモジュールを構築し、テストで品質を担保します。

## 2. 実装指示 (Implementation Instructions)
- [ ] `src/issue_creator_kit/utils.py` を新規作成し、以下の機能を実装せよ。
    - `parse_metadata(content: str) -> dict`: 既存の `create_issues.py` から移植し、Markdown のメタデータを辞書形式で抽出する。
    - `update_metadata(content: str, updates: dict) -> str`: 指定されたキー（Status, Date 等）の値を置換し、更新後の全文を返す。正規表現を用いて、行頭の `- **Key**: Value` 形式に厳密にマッチさせること。
- [ ] `src/issue_creator_kit/scripts/create_issues.py` を修正し、上記ユーティリティを使用するようにリファクタリングせよ。
- [ ] `tests/unit/test_utils.py` を作成し、メタデータ置換の各パターン（上書き、存在しない場合の挙動等）をテストせよ。

## 3. 検証基準 (Definition of DoD)
- [ ] `pytest tests/unit/test_utils.py` がパスすること。
- [ ] リファクタリング後の `create_issues.py` が既存の挙動を維持していること。

## 4. 影響範囲と注意事項
- 正規表現による置換の際、Markdown の他のテキストを誤って書き換えないよう、行頭チェック等を厳密に行うこと。
