---
title: "[Spec] Define Phase Promotion Logic (Auto-PR & 1PR=1Task)"
labels:
  - task
  - TECHNICAL_DESIGNER
roadmap: "docs/specs/plans/20260122-spec-adr003-plan.md"
task_id: "S1-3"
depends_on: ["issue-S1-1.md"]
next_phase_path: ""
status: "Draft"
---

## 1. Goal & Context (Why & What)

### Goal
- `WorkflowUseCase` による「フェーズ連鎖」の仕様を定義し、PR マージ後の自動 PR 作成ロジックを確定させる。
- 「1 PR = 1 Task Transition」の原則を適用し、シンプルな実装を保証する。

### As-is (現状)
- フェーズ遷移の概念はあるが、PR Body から Issue 番号を抽出する正規表現や、複数の Issue が Close された場合の優先順位が未定義。

### To-be (あるべき姿)
- `docs/specs/logic/promotion_logic.md` が作成され、以下の仕様が記述されている。
    - **Trigger**: PR Body の解析ロジック（`Closes #123` 等の抽出）。
    - **Task Mapping**: 抽出された Issue 番号に対応する Archive 下のファイルを特定する手順。
    - **1PR=1Task Rule**: 複数の Issue が見つかった場合、最初の 1 件のみをトリガーとする。
    - **Promotion Action**: ブランチ作成 (`main` 基点)、ファイル移動 (`git mv`)、PR 作成の連鎖。
    - **Infinite Loop Guard**: 深度制限 (Max 10) の定義。

### Design Evidence
- [Auto-PR Behavior Diagram](../../../docs/architecture/arch-behavior-003-autopr.md)
- [Decision on Simple Implementation](../../../reqs/design/_approved/adr-003-task-and-roadmap-lifecycle.md)

## 2. Input Context (資料 & 情報)
- **Common Definitions**: `docs/specs/plans/20260122-spec-adr003-plan.md`
- **Existing Workflows**: `.github/workflows/auto-phase-promotion.yml` (参考)

## 3. Implementation Steps & Constraints (How)

### 3.1. Negative Constraints (してはいけないこと)
- 複雑な「複数 Issue 統合 PR」のロジックを含めないこと。
- `main` 以外のブランチから Foundation Branch を派生させないこと。

### 3.2. Implementation Steps (実行手順)
1.  **Define Extraction Regex**: GitHub がサポートするキーワード (`close`, `fix`, `resolve` 等) とマッチする正規表現を提示。
2.  **Define Branch Naming**: 作成されるブランチ名の命名規則を定義。
3.  **Safety Mechanism**: 深度制限を超えた際のエラーハンドリングを記述。

### 3.3. Configuration Changes
- なし

## 4. Branching Strategy
- **Base Branch**: `feature/spec-adr003-implementation`
- **Feature Branch**: `feature/task-S1-3-promotion-logic-spec`

## 5. Verification & DoD (完了条件)
- [ ] 「1つのPRで #1 と #2 を Close した場合、#1 の `next_phase_path` のみが処理されること」が明記されている。
- [ ] 循環参照を検知して停止するフローが図解またはステップで定義されている。
