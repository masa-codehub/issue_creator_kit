# Review Analysis Report - PR #316

## 1. 概要 (Overview)
- **PR:** [#316 Arch Integration: ADR-008 Scanner Foundation](https://github.com/masa-codehub/issue_creator_kit/pull/316)
- **Status:** Conditional Pass -> Action Required
- **Analyst:** Review Analyst (Gemini)

## 2. 指摘の分類と分析 (Categorization & Analysis)

### 2.1. Accept (修正すべき指摘)
SSOT（ADR-008, 既存の定義）と整合させるために修正が必要な項目。

| No. | 指摘内容 (Summary) | 真因分析 (Root Cause) | 対応方針 (Action Policy) |
| :--- | :--- | :--- | :--- |
| 1 | `arch-state-007-lifecycle.md` での Draft Task の配置が `reqs/tasks/<ADR-ID>/` となっており、`_inbox` ルールと不整合。 | **記述の不統一**: `definitions.md` では `_inbox` を定義しているが、タスク配置の記述で明記漏れがあった。 | **修正**: タスク配置を `reqs/tasks/<ADR-ID>/_inbox/` に統一する（ただし、ADR-008の設計意図としてタスクはフォルダ分けしない方針であれば、例外記述を追加する）。今回はレビュアー提案の `reqs/tasks/_inbox/<ADR-ID>/` または `reqs/tasks/<ADR-ID>/_inbox/` への統一を検討するが、ADR-007のオリジナル設計を確認し、最も自然な形に修正する。 |
| 2 | `arch-structure-007-metadata.md` のテーブル後の空行によるレンダリング崩れリスク。 | **Markdown Lint**: 余計な空行が含まれていた。 | **修正**: 空行を削除する。 |
| 3 | `arch-structure-008-scanner.md` で `GraphBuilder` が `Visualizer` に依存している（Downstreamにある）という誤記。 | **依存方向の誤認**: データフロー（Graph -> Visualizer）とコード依存（Visualizer imports Graph? or CLI orchestrates?）の混同。図では `Visualizer` が `Builder` を使う形だが、実際は `CLI` が両者を使い、`Visualizer` が `Graph` オブジェクト（Model）を使う設計が自然。記述を修正する。 | **修正**: `GraphBuilder` の Downstream から `Visualizer` を削除。 |
| 4 | `Visualizer` の Upstream/Downstream の記述逆転。 | **依存方向の誤認**: 上記と同様。 | **修正**: Upstream/Downstream を入れ替える。 |
| 5 | `arch-structure-008-scanner.md` の Code Mapping パス（`domain/services/`）が実在しない。 | **先行記述**: 実装前の計画段階であるため実在しないのは正常だが、誤解を招く。 | **修正**: `(New)` または `(Planned)` と明記するか、`Task-008-07` でディレクトリ作成を含める。今回はドキュメント修正で対応。 |

### 2.2. Discuss / Explain (議論が必要な指摘)

| No. | 指摘内容 (Summary) | 論点 (Discussion Point) | 推奨する回答 (Response) |
| :--- | :--- | :--- | :--- |
| 6 | 監査レポート (`integration-audit.md`) の内容が現状（修正済み）と食い違っている。 | **タイミングのズレ**: PR作成時点では `arch-structure-issue-kit.md` は未修正だったが、その後のコミット（Task-07相当の修正があった場合）で修正された可能性がある、あるいはレビュアーが「PRに含まれるべき修正がまだ反映されていない」ことを「監査レポートが古い」と表現しているか。確認が必要。 | 現状のブランチ (`feature/arch-update-adr008`) ではまだ `arch-structure-issue-kit.md` は **修正されていない**（Task-07はこれから実施）。したがって監査レポートは正しいが、レビュアーが「このPRで修正するはずでは？」と意図している可能性がある。「Task-07で修正予定」であることを明示するか、このPR内で修正を完結させる。 |
| 7 | `arch-to-spec.md` の Known Issues が古い（解決済み扱いすべき）。 | **同上**: PR内で修正を行うならば、Known Issues からは削除し、解決済みとするのが適切。 | PR内で修正を完遂し、Known Issues を削除する。 |

## 3. アセット化・再発防止 (Retrospective for Assetization)

- **依存方向の記述ルール**:
  - `Upstream` = **依存元** (User, Caller)
  - `Downstream` = **依存先** (Used, Callee)
  - この定義を `styleguide.md` または `coding-guidelines.md` に明記し、今後のドキュメント作成時の混乱を防ぐ。
- **監査レポートの同期**:
  - 監査レポート作成後にコード修正を行った場合、必ずレポートも更新（Re-audit）してからPRを出す、あるいはPR内で整合性を保つフローを徹底する。

## 4. 対応方針 (Action Plan)

このPR (`feature/arch-update-adr008`) 内で以下の修正を一括して行い、マージ可能な状態にする。

1.  **ドキュメントの軽微な修正**:
    - `arch-state-007-lifecycle.md`: タスク配置パスの明確化。
    - `arch-structure-007-metadata.md`: 空行削除。
    - `arch-structure-008-scanner.md`: 依存関係記述の修正、Code Mapping への注記追加。
2.  **構造図の更新 (Task-07 の前倒し実施)**:
    - `arch-structure-issue-kit.md` の更新（Legacy UseCase削除、Scanner追加）。
    - これにより、監査レポートの「指摘事項」を解消し、`arch-to-spec.md` の「残存課題」をクリアにする。
3.  **監査レポート・Handover の更新**:
    - 修正を反映し、Verdict を `PASS` に変更。
    - Known Issues を削除。
