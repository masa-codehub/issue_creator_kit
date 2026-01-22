---
depends_on: []
issue: '#227'
labels:
- task
- TECHNICAL_DESIGNER
next_phase_path: ''
roadmap: docs/architecture/plans/20260122-adr003-plan.md
status: Draft
task_id: T1-4
title: '[Arch] Create State Diagram for Task Lifecycle'
---

## 1. Goal & Context (Why & What)

### Goal
- タスク（Document）がライフサイクルの中でどのような状態遷移（Draft -> Virtual Queue -> Active -> Archived）を辿るかを定義する State Diagram を作成する。
- 各遷移を引き起こすイベント（PR作成、マージ、同期）を明確にする。

### As-is (現状)
- 「仮想キュー」という概念が新しい状態として導入されたが、既存のステートマシン図には反映されていない。

### To-be (あるべき姿)
- `docs/architecture/arch-state-003-task-lifecycle.md` が作成され、以下の状態遷移が描かれている。
    - **Draft**: `drafts/` ディレクトリに存在。
    - **Queued (Virtual)**: `archive/` への移動 PR が Open された状態。
    - **Processing**: PR がマージされ、Issue 起票バッチが実行中の状態。
    - **Active**: Issue が起票され、開発中。
    - **Archived**: 全て完了。

### Design Evidence
- [ADR-003](../../../design/_approved/adr-003-task-and-roadmap-lifecycle.md)
- [Architecture Plan](../../../docs/architecture/plans/20260122-adr003-plan.md)

## 2. Input Context (資料 & 情報)

- **Common Definitions Doc**: `docs/architecture/plans/20260122-adr003-plan.md`
- **Template**: `docs/template/arch-state.md`

## 3. Implementation Steps & Constraints (How)

### 3.1. Negative Constraints (してはいけないこと)
- 物理的なディレクトリ移動（Implementation Detail）だけでなく、論理的なステータス（Logical State）の変化に着目すること。

### 3.2. Implementation Steps (実行手順)
1.  **Read Plan**: `docs/architecture/plans/20260122-adr003-plan.md`.
2.  **Create File**: `docs/architecture/arch-state-003-task-lifecycle.md`.
3.  **Draft Diagram (Mermaid State)**:
    - **States**: `Draft`, `Queued`, `Processing`, `Active`, `Archived`.
    - **Transitions**:
        - `Draft` --> `Queued`: Create PR (Move file).
        - `Queued` --> `Processing`: Merge PR.
        - `Processing` --> `Active`: Create Issue (Success).
        - `Processing` --> `Queued`: Fail (Rollback/Retry) - ※概念上。
    - **Notes**: 「Virtual Queue」は物理的には `Queued` 状態であることを注記する。
4.  **Description**: 各ステータスの定義（物理パスとの対応）を表形式で記述する。

### 3.3. Configuration Changes
- なし

## 4. Branching Strategy
- **Base Branch**: `feature/arch-adr003-implementation`
- **Feature Branch**: `feature/task-T1-4-state-lifecycle`

## 5. Verification & DoD (完了条件)
- [ ] `docs/architecture/arch-state-003-task-lifecycle.md` が存在し、空でないこと。
- [ ] 仮想キュー (`Queued`) 状態が定義されていること。
