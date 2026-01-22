---
depends_on:
- issue-T1-1.md
issue: '#229'
labels:
- task
- TECHNICAL_DESIGNER
next_phase_path: ''
roadmap: docs/architecture/plans/20260122-adr003-plan.md
status: Draft
task_id: T1-3
title: '[Arch] Create Behavior Diagram for Auto-PR (Phase Chain)'
---

## 1. Goal & Context (Why & What)

### Goal
- ADR-003 の「フェーズ連鎖 (Phase Chain)」メカニズム、すなわち「最終タスク完了 -> 次フェーズ Draft の Archive 移動 -> PR 作成」の流れを可視化する。
- どのタイミングでブランチが作られ、ファイルが移動されるかを時系列で定義する。

### As-is (現状)
- 「Auto-PR」という言葉はあるが、具体的にどのディレクトリからどこへファイルを移動させるのか、ブランチの派生元はどこか等の詳細フロー図がない。

### To-be (あるべき姿)
- `docs/architecture/arch-behavior-003-autopr.md` が作成され、以下のシーケンスが描かれている。
    - **Trigger**: PR Merge Event (Subject: Last Task of Phase).
    - **Process**:
        1. `WorkflowUseCase` checks `next_phase_path`.
        2. If exists:
            - `GitAdapter.checkout` (New Branch from `main`).
            - `GitAdapter.move_file` (Drafts -> Archive).
            - `GitAdapter.commit`.
            - `GitAdapter.push`.
            - `GitHubAdapter.create_pull_request`.

### Design Evidence
- [ADR-003](../../../design/_approved/adr-003-task-and-roadmap-lifecycle.md) (Section: 自己推進型ワークフロー)
- [Architecture Plan](../../../docs/architecture/plans/20260122-adr003-plan.md)

## 2. Input Context (資料 & 情報)

- **Common Definitions Doc**: `docs/architecture/plans/20260122-adr003-plan.md`
- **Template**: `docs/template/arch-behavior.md`

## 3. Implementation Steps & Constraints (How)

### 3.1. Negative Constraints (してはいけないこと)
- 複雑な条件分岐（無限ループ検知など）は図が煩雑になるため、注釈での補足に留め、メインフローは「正常系（連鎖成功）」にフォーカスする。

### 3.2. Implementation Steps (実行手順)
1.  **Read Plan**: `docs/architecture/plans/20260122-adr003-plan.md`.
2.  **Create File**: `docs/architecture/arch-behavior-003-autopr.md`.
3.  **Draft Diagram (Mermaid Sequence)**:
    - Participants: `WorkflowUseCase`, `GitAdapter`, `GitHubAdapter`.
    - **Flow**:
        - `promote_next_phase()` called.
        - `GitAdapter.checkout(new_branch, base="main")`.
        - `GitAdapter.move_file(draft_dir, archive_dir)`.
        - `GitAdapter.commit("feat: promote next phase")`.
        - `GitAdapter.push()`.
        - `GitHubAdapter.create_pull_request()`.
4.  **Description**:
    - `next_phase_path` が指定されていない場合は何もしない（End）ことを明記する。

### 3.3. Configuration Changes
- なし

## 4. Branching Strategy
- **Base Branch**: `feature/arch-adr003-implementation`
- **Feature Branch**: `feature/task-T1-3-behavior-autopr`

## 5. Verification & DoD (完了条件)
- [ ] `docs/architecture/arch-behavior-003-autopr.md` が存在し、空でないこと。
- [ ] ファイル移動 (`move_file`) が `Draft` から `Archive` へ行われることが図示されていること。
- [ ] ブランチ作成の基点が `main` であることが明示されていること。
