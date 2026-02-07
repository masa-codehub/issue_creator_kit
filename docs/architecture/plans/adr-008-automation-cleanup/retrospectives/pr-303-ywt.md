# 振り返りレポート (YWT) - ADR-008 Planning Inconsistency

## 1. Y (やったこと)

- **作業の実施内容:**
  - ADR-008 に基づくアーキテクチャ更新計画を作成し、PR #303 として提出した。
  - `definitions.md`, `design-brief.md`, `goal_definition.md` および 6つのタスクドラフトを作成した。
- **事象の観測:**
  - `definitions.md` で定義した ID 形式（`adr-\d{3}-.*` / `task-\d{3}-.*`）と、実際のタスクファイルで付与した ID（`008-01`）が乖離していた。
  - `goal_definition.md` や `design-brief.md` において、「(or similar)」や「Move or Delete」といった曖昧な表現が含まれていた。
  - `task-008-03` に必要な依存関係 (`task-008-04`) が欠落していた。
- **分析情報の集約:**
  - `docs/architecture/plans/adr-008-automation-cleanup/definitions.md`: Line 22
  - `reqs/tasks/adr-008/task-01-archive.md`: Line 2
  - Review Comments: r2774098826, r2774098841, etc.

## 2. W (わかったこと)

- **結果の確認:**
  - アーキテクチャ定義（ルール策定）とタスク分割（ルール適用）の間に、セルフチェックのステップが不足していた。
  - 計画段階での曖昧な記述は、後続の Spec/TDD フェーズにおいて「判断の丸投げ」となり、品質低下の要因となる。

### ギャップ分析

- **理想 (To-Be):** 共通定義（Definitions）で定められた命名規則や ID 体系が、全てのタスクドラフトに厳密に適用されている。
- **現状 (As-Is):** 定義した正規表現に適合しない ID が複数のタスクファイルで使用されている。
- **ギャップ:** 正規表現 `task-\d{3}-.*` vs 文字列 `008-01`。
- **要因 (Root Cause):** スキル `planning-architecture` の実行過程で、定義書を作成した直後の「不変条件のセルフバリデーション」が形式化されていなかった。

## 3. T (次やること / 仮説立案)

- **実証的仮説:**
  - `definitions.md` の正規表現と、タスクファイルの ID を修正すれば整合性は回復する。
- **飛躍的仮説:**
  - `issue-kit` 自体に Pydantic バリデーションを実装し、タスクドラフト作成時に CLI で即座にチェックできる仕組みを整える（ADR-008 の実装自体がこれにあたる）。
- **逆説的仮説:**
  - そもそも ID のプレフィックス (`task-`) が冗長である可能性があるが、現在の SSOT 規約（ADR-007）に従うべき。

### 検証アクション

- [x] PR #303 の指摘に基づき、`definitions.md`, `design-brief.md`, `goal_definition.md` を修正する。
- [x] 全てのタスク ID を `task-008-xx` 形式に統一し、依存関係を更新する。
- [x] 修正後の PR を push し、レビュアーの承認を得る。
