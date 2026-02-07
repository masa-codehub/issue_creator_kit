# Review Analysis Report: PR #274

## 1. 概要 (Overview)

PR #274 「docs(arch): 新アーキテクチャ図（Structure/State）の起草 [007-T2]」に対するレビュー指摘（全15件）の分析と対応方針をまとめます。

- **分析日:** 2026-02-05
- **対象PR:** #274
- **分析者:** Review Analyst (SYSTEM_ARCHITECT)

## 2. 指摘の分類と対応方針 (Categorization & Actions)

### 2.1 docs/architecture/arch-state-007-lifecycle.md

| ID  | 指摘内容                                                 | 分類       | 対応方針 (Action)                                                                                      |
| :-- | :------------------------------------------------------- | :--------- | :----------------------------------------------------------------------------------------------------- |
| 1   | `Archived_ADR` からの終了遷移 `[*]` を追加。             | **Accept** | 図の完全性を高めるため、最終状態への遷移を明示します。                                                 |
| 2   | `Physical Movement` ブロックを `note` または説明に分離。 | **Accept** | ステート図の抽象度を統一するため、副作用（物理移動）は `note` として表現します。                       |
| 3   | `Task` ステート定義テーブルに `Cancelled` を追加。       | **Accept** | 図とテーブルの不整合を解消するため、指摘の suggestion を採用して追加します。                           |
| 4   | `Issued` の副作用と `Movement` ステートの関係の曖昧さ。  | **Accept** | ID 2 の修正と合わせ、図からは物理移動ステートを削除し、テーブルの副作用として整理します。              |
| 5   | 日本語の状態名（`L1_L2_起票`）を英語に変更。             | **Accept** | レンダリングの安定性と一貫性のため、`L1_L2_Issue_Creation` 等に修正します。                            |
| 6   | `Issued`, `Archived_ADR` が ADR-007 のスキーマに未定義。 | **Accept** | 図のステータス名を ADR-007 (SSOT) に厳密に合わせるか、ADR 側を更新します。今回は図の修正を優先します。 |
| 7   | `Archived_ADR` を `Postponed` と `Superseded` に分割。   | **Accept** | 情報の損失を防ぐため、ADR のステータス定義（SSOT）通りに分割します。                                   |

### 2.2 docs/architecture/arch-structure-007-metadata.md

| ID  | 指摘内容                                                 | 分類       | 対応方針 (Action)                                                             |
| :-- | :------------------------------------------------------- | :--------- | :---------------------------------------------------------------------------- |
| 8   | `F2 -- I1` の矢印ラベルを `depends on` に変更。          | **Accept** | 依存関係とアクションの混同を避けるため、より正確なラベルに変更します。        |
| 9   | CLI のレイヤー表記を `Interface Adapters` に修正。       | **Accept** | Clean Architecture の原則および既存ドキュメントとの整合性のため、修正します。 |
| 10  | 「Invisible SSOT」図の自己参照矢印（F1->F1等）の削除。   | **Accept** | 論理的な不正確さを排除し、ノードの整理を行います。                            |
| 11  | 矢印ラベルのケース（大文字小文字）の統一。               | **Accept** | ドキュメントの一貫性のため、`Issuance` に統一します。                         |
| 12  | `ick CLI` から `archive` コンテナへの関係 `Rel` の追加。 | **Accept** | 物理移動の責任を明示するため、関係線を追加します。                            |

## 3. 真実（SSOT）との乖離と是正 (SSOT Alignment)

- **ADR-007 との不整合:** ステート図で使用していた名前（`Archived_ADR`, `Issued`）が、ADR-007 で定義された `status` フィールドの値（`Postponed`, `Superseded` 等）と乖離していました。
- **是正措置:** アーキテクチャ図は ADR-007 (SSOT) の用語を厳密に使用するように修正します。

## 4. 実行アクション (Execution Plan)

1. `arch-state-007-lifecycle.md` のステート図とテーブルを、指摘に基づき修正（用語の SSOT 準拠、副作用の note 化）。
2. `arch-structure-007-metadata.md` の C4 図と SSOT マッピング図を修正（レイヤー名、依存ラベル、関係線の追加）。
3. 修正内容を PR #274 にプッシュ。
