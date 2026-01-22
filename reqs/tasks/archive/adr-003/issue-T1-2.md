---
depends_on:
- issue-T1-1.md
issue: '#228'
labels:
- task
- TECHNICAL_DESIGNER
next_phase_path: ''
roadmap: docs/architecture/plans/20260122-adr003-plan.md
status: Draft
task_id: T1-2
title: '[Arch] Create Behavior Diagram for Atomic Creation'
---

## 1. Goal & Context (Why & What)

### Goal
- ADR-003 の「原子的な起票 (Atomic Execution)」と「Fail-fast」のロジックを可視化する Sequence Diagram を作成する。
- どこでエラーが発生した場合に、システムがどのように停止し、Gitリポジトリの整合性（SSOT）を守るかを示す。

### As-is (現状)
- 「一括起票」や「Fail-fast」の挙動は文章（ADR）でしか定義されておらず、実装時の例外ハンドリング方針が直感的に理解しづらい。

### To-be (あるべき姿)
- `docs/architecture/arch-behavior-003-creation.md` が作成され、以下のシーケンスが描かれている。
    - **Trigger**: PR Merge Event.
    - **Process**:
        1. `GitAdapter.get_added_files` (Archive内の新規ファイル検知).
        2. `CreationUseCase` loop (各ファイルのバリデーション).
        3. `GitHubAdapter.create_issue` (起票).
        4. **Fail-fast Check**: 1件でも失敗したら即停止（コミットしない）。
        5. **Success**: 全件成功時のみ `FileSystemAdapter.update_metadata` -> `GitAdapter.commit`.

### Design Evidence
- [ADR-003](../../../design/_approved/adr-003-task-and-roadmap-lifecycle.md) (Section: 原子的な起票)
- [Architecture Plan](../../../docs/architecture/plans/20260122-adr003-plan.md)

## 2. Input Context (資料 & 情報)

- **Common Definitions Doc**: `docs/architecture/plans/20260122-adr003-plan.md`
- **Reference**: `docs/specs/logic/approval_usecase.md` (ADR-002のロジックだが、エラー処理の参考になる)
- **Template**: `docs/template/arch-behavior.md`

## 3. Implementation Steps & Constraints (How)

### 3.1. Negative Constraints (してはいけないこと)
- 成功パターン（Happy Path）だけを描かないこと。**必ず「APIエラー時の停止フロー（Alt/Opt fragment）」を含めること。**
- `RoadmapSync` の詳細は別タスクとするため、ここでは「Sync呼び出し」程度の記述に留める。

### 3.2. Implementation Steps (実行手順)
1.  **Read Plan**: `docs/architecture/plans/20260122-adr003-plan.md` (Section 4 の Behavior 定義) を確認。
2.  **Create File**: `docs/architecture/arch-behavior-003-creation.md` を作成。
3.  **Draft Diagram (Mermaid Sequence)**:
    - Participants: `CLI`, `WorkflowUseCase`, `CreationUseCase`, `GitAdapter`, `GitHubAdapter`, `FileSystemAdapter`.
    - **Main Flow**:
        - `get_added_files` -> `files`
        - Loop `files`: `create_issue` -> `issue_number` (Store in memory)
    - **Error Handling (Alt Fragment)**:
        - `create_issue` fails -> `Raise Exception` -> `CLI` catches -> **Exit(1) without Commit**.
    - **Commit Flow**:
        - `update_metadata` (Write back issue numbers)
        - `GitAdapter.add` & `commit`.
4.  **Description**: 「なぜここで止まるのか（Fail-fast）」の理由を注釈として記述する。

### 3.3. Configuration Changes
- なし

## 4. Branching Strategy
- **Base Branch**: `feature/arch-adr003-implementation`
- **Feature Branch**: `feature/task-T1-2-behavior-creation`

## 5. Verification & DoD (完了条件)
- [ ] `docs/architecture/arch-behavior-003-creation.md` が存在し、空でないこと。
- [ ] Mermaid シーケンス図において、APIエラー発生時にコミット処理へ進まずに終了するパスが明確に描かれていること。
