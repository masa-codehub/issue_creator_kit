---
title: "[TDD] Implement Phase Promotion Logic"
labels: ["gemini:tdd"]
roadmap: "docs/implementation/plans/adr-003/tdd-plan.md"
task_id: "T-6"
depends_on: ["issue-T-3.md"]
status: "Draft"
---

## 1. Goal & Context (Why & What)

### Goal
- フェーズ完了（マージ）をトリガーとして、次フェーズの Draft ファイル群を Archive へ移動させるための「新しい PR (Auto-PR)」を作成するロジックを実装する。

### As-is (現状)
- 次フェーズへの移行（PR作成）を手動で行う必要がある。

### To-be (あるべき姿)
- マージされた PR の Body または完了したタスクのメタデータ (`next_phase_path`) を解析し、自動的に次フェーズの準備を行う。

### Design Evidence
- [Logic Spec](../../../../docs/specs/logic/promotion_logic.md)

## 2. Input Context (資料 & 情報)
- **Logic**: `src/issue_creator_kit/usecase/promotion_usecase.py`
- **Spec**: `docs/specs/logic/promotion_logic.md`

## 3. Implementation Steps & Constraints (How)

### 3.1. Negative Constraints (してはいけないこと)
- 1つの PR に複数のフェーズ遷移を混在させること（`1 PR = 1 Task Transition` の原則）。

### 3.2. Implementation Steps (実行手順)
1.  **Red Phase**:
    - `tests/usecase/test_promotion.py` を作成。
    - 指定された `next_phase_path` （例: `tasks/drafts/phase-2`）のファイルを `archive/` へ移動するブランチが作成されることを検証。
2.  **Green Phase**:
    - `git checkout -b`, `git mv`, `git commit`, `git push`, `gh pr create` の一連の流れを `WorkflowAutomationUseCase` として実装。

### 3.3. Configuration Changes
- なし

## 4. Branching Strategy
- **Base Branch**: `feature/impl-adr003`
- **Feature Branch**: `feature/task-T-6-promotion-logic`

## 5. Verification & DoD (完了条件)
- [ ] 次フェーズのファイル移動を含む PR が自動作成されること。

## 6. TDD Scenarios
- **Scenario 1 (Promotion)**:
    - Input: `next_phase_path="reqs/tasks/drafts/phase-2"`
    - Action: Creates PR "chore: promote to phase-2" with file moves.
