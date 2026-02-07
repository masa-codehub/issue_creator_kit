# Review Analysis Report - PR #318

## 1. 概要 (Overview)
- **PR:** [#318 Spec Plan: ADR-008 Scanner Foundation](https://github.com/masa-codehub/issue_creator_kit/pull/318)
- **Status:** Action Required
- **Analyst:** Review Analyst (Gemini)

## 2. 指摘の分類と分析 (Categorization & Analysis)

### 2.1. Accept (修正すべき指摘)
| No. | 指摘内容 (Summary) | 真因分析 (Root Cause) | 対応方針 (Action Policy) |
| :--- | :--- | :--- | :--- |
| 1 | `definitions.md` の Mermaid 図で `Graph` と `Visualizer` が分離されているが、タスク定義 `task-008-04` では統合されているため、図を統合して整合性を取るべき。 | **粒度の不一致**: タスク分割時に実装効率を考慮して統合したが、図の更新が漏れていた。 | **修正**: `definitions.md` の Mermaid 図を更新し、GraphBuilder と Visualizer を一つのノード（またはタスク単位のノード）として表現する。 |
| 2 | `self-audit.md` の根拠記述にある "Directory Mapping" セクションが存在しない。 | **セクション名の誤記**: おそらく "2. Directory Mapping" (Arch Handover) または "3. Directory Structure & Naming" を指していたが、正確な名称でなかった。 | **修正**: 監査レポートの記述を正しいセクション名（"3. Directory Structure & Naming"）に修正する。 |
| 3 | `Directory Structure & Naming` のファイル命名規則が、現状の `reqs/tasks/...` の実態と合っていない。 | **スコープの混同**: "Spec File Naming" (仕様書) と "Task File Naming" (Issue定義) が混在または説明不足だった。 | **修正**: SpecファイルとTaskファイルの命名規則を明確に分離し、Taskファイルについては既存の命名規則（`task-{NN}-{slug}.md`）に合わせる記述を追加する。 |
| 4 | Markdown テーブルのフォーマット崩れ（`||` の重複）。 | **Typo**: パイプ記号の過剰入力。 | **修正**: 余分なパイプを削除し、正しい Markdown テーブル形式にする。 |
| 5 | `Goal Definition` の完了定義で「日本語で作成」とあるが、実物は英語メインである。 | **定義の形骸化**: テンプレートや慣習で「日本語」と書いてしまったが、実際は英語で記述していた。 | **修正**: 完了定義を「`self-audit.md` が作成され...」に緩和するか、実態に合わせて記述を修正する。今回は完了定義側を修正する。 |
| 6 | `TaskID` の正規表現が既存の `007-T3-*` 等と不整合（互換性問題）。 | **考慮漏れ**: 新規ルールのみを定義し、レガシーデータの扱いを定義していなかった。 | **修正**: ADR-008 以降の新規タスクに適用するルールであることを明記し、既存IDはレガシーとして許容する旨を注記する。 |

## 3. アセット化・再発防止 (Retrospective for Assetization)
- **命名規則の明文化**: SpecファイルとTaskファイルの命名規則の違いは混乱しやすいため、`definitions.md` テンプレート自体に両方の記入欄を設けることを検討する。
- **Mermaid図とタスクの同期**: タスク分割を変更した際は、必ず依存関係図も更新するチェックリストを設ける。

## 4. 対応方針 (Action Plan)
このPR内で以下の修正を行う。

1.  **`docs/specs/plans/adr-008-automation-cleanup/definitions.md` の修正**:
    - Mermaid 図のノード統合。
    - ファイル命名規則の明確化と修正。
    - Markdown テーブルのフォーマット修正。
    - TaskID の正規表現に関する注記追加。
2.  **`docs/specs/plans/adr-008-automation-cleanup/reviews/self-audit.md` の修正**:
    - 根拠記述のセクション名修正。
3.  **`docs/specs/plans/adr-008-automation-cleanup/reviews/goal-definition.md` の修正**:
    - 完了定義の「日本語で」という記述を削除/修正。
