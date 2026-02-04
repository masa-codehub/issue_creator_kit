---
title: "[TDD] Implement Issue Creation UseCase (Fail-fast)"
labels: ["gemini:tdd"]
roadmap: "docs/implementation/plans/adr-003/tdd-plan.md"
task_id: "T-4"
depends_on: ["../phase-1-domain/issue-T-1.md", "../phase-2-infra/issue-T-2.md", "../phase-2-infra/issue-T-3.md"]
status: "Draft"
---

## 1. Goal & Context (Why & What)

### Goal
- 仮想キューから抽出されたタスク群を、依存関係順にソートし、原子的に（Fail-fastで）起票するビジネスロジックを実装する。

### As-is (現状)
- 個別の Adapter はあるが、それらを組み合わせて「一括起票」を行うロジックが存在しない。

### To-be (あるべき姿)
- `IssueCreationUseCase` が実装され、`drafts/` から `archive/` へのファイル移動を検知して Issue を作成する。
- 途中でエラーが発生した場合、Git への書き込み（Issue番号付与）を行わずに処理を中断する。

### Design Evidence
- [Logic Spec](../../../../docs/specs/logic/creation_logic.md)
- [ADR-003 (Fail-fast)](../../../../reqs/design/_approved/adr-003-task-and-roadmap-lifecycle.md)

## 2. Input Context (資料 & 情報)
- **UseCase Logic**: `src/issue_creator_kit/usecase/issue_creation_usecase.py`
- **Spec**: `docs/specs/logic/creation_logic.md`

## 3. Implementation Steps & Constraints (How)

### 3.1. Negative Constraints (してはいけないこと)
- 1件起票するたびに `git commit` すること（履歴汚染）。
- エラー発生時にロールバック（Issue削除）を試みること（複雑化回避のため、書き込みを行わずに終了するのが正解）。

### 3.2. Implementation Steps (実行手順)
1.  **Red Phase (Topo Sort)**:
    - `tests/usecase/test_issue_creation.py` を作成。
    - `depends_on` を持つ複数の Document オブジェクトを入力とし、依存順にソートされたリストが得られるかを検証。
    - 循環参照時にエラーとなることを検証。
2.  **Green Phase (Topo Sort)**:
    - `graphlib.TopologicalSorter` を用いたソートロジックを実装。
3.  **Red Phase (Fail-fast)**:
    - `GitHubAdapter.create_issue` が2件目で例外を投げるシナリオを作成。
    - 1件目のファイルも書き換えられずに終了することを検証。
4.  **Green Phase (UseCase)**:
    - 全件起票ループ -> 全件ファイル更新 -> コミット という処理順序を実装。

### 3.3. Configuration Changes
- なし

## 4. Branching Strategy
- **Base Branch**: `feature/impl-adr003`
- **Feature Branch**: `feature/task-T-4-creation-logic`

## 5. Verification & DoD (完了条件)
- [ ] 依存関係を考慮した順序で Issue が作成されること。
- [ ] エラー時に Git への変更が行われない（Atomicity）ことがテストで証明されていること。

## 6. TDD Scenarios
- **Scenario 1 (Dependency)**: Task B depends on Task A -> Created order: A then B.
- **Scenario 2 (Atomicity)**: Task A success, Task B fails -> Task A file remains untouched (no issue number).
