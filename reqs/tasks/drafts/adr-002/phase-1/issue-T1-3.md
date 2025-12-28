# Issue案: 共通ユーティリティ関数のインターフェース設計

- **Roadmap**: [roadmap-adr002-document-approval-flow.md](../../../../roadmap/_inbox/roadmap-adr002-document-approval-flow.md)
- **Task ID**: T1-3
- **Depends-On**: issue-T1-2.md
- **Status**: Draft

## 1. 目的と背景
ADR-002 実現に必要なユーティリティ関数の「インターフェース（シグネチャ）」を定義します。
入出力の型と役割を明確にすることで、Phase 2 での実装をスムーズにします。

## 2. 実装指示 (Implementation Instructions)
- [ ] `src/issue_creator_kit/utils.py` に実装予定の関数シグネチャを設計・定義せよ。
    - **`parse_metadata`**: 既存ロジックの移植版。
        - 引数: Markdownコンテンツ(str)
        - 戻り値: メタデータ辞書(dict)
    - **`update_metadata`**: 新規実装。
        - 引数: Markdownコンテンツ(str), 更新データ(dict)
        - 戻り値: 更新後のMarkdownコンテンツ(str)
- [ ] ファイル操作（移動、リネーム）に関するヘルパー関数が必要か検討し、必要であれば定義せよ。
- [ ] これらを「インターフェース定義書」としてまとめるか、空の関数定義（ドックストリング付き）としてファイルを作成せよ（※ロジックの中身は書かない）。

## 3. 検証基準 (Definition of DoD)
- [ ] 各関数の役割、引数、戻り値、発生しうる例外が明確に定義されていること。
- [ ] 定義されたインターフェースが、ADR-002 の要件（Status更新、日付更新）を満たしていること。

## 4. 影響範囲と注意事項
- 型ヒント（Type Hints）を積極的に活用すること。
