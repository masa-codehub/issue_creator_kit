---
title: "[TDD] Implement GitHub Adapter with Mocking Strategy"
labels: ["gemini:tdd"]
roadmap: "docs/implementation/plans/adr-003/tdd-plan.md"
task_id: "T-3"
depends_on: ["../phase-1-domain/issue-T-1.md"]
status: "Draft"
---

## 1. Goal & Context (Why & What)

### Goal
- GitHub API（Issue検索、作成、PR作成）を操作するアダプターを実装し、テスト時には API コールを発生させない安全なモック戦略を確立する。

### As-is (現状)
- `PyGithub` を使用したコードが散在している、またはテスト不能な状態。

### To-be (あるべき姿)
- `GitHubAdapter` が `PyGithub` をラップし、例外処理（404, 429等）を統一的に行う。
- テストコードからは `MockGitHubAdapter` または `unittest.mock` を通じて振る舞いを検証できる。

### Design Evidence
- [Adapter Spec](../../../../docs/specs/components/infra_adapters.md)

## 2. Input Context (資料 & 情報)
- **Adapter Logic**: `src/issue_creator_kit/infrastructure/github_adapter.py`
- **Spec**: `docs/specs/components/infra_adapters.md`

## 3. Implementation Steps & Constraints (How)

### 3.1. Negative Constraints (してはいけないこと)
- テスト実行時に実際の GitHub API を叩くこと（トークン漏洩やレート制限のリスク）。
- API レスポンスの生データをそのまま UseCase 層へ渡すこと（Domain Model に変換して渡す）。

### 3.2. Implementation Steps (実行手順)
1.  **Red Phase**:
    - `tests/infrastructure/test_github_adapter.py` を作成。
    - `find_or_create_issue` が、既存 Issue がある場合はそれを返し、ない場合は新規作成するロジックを検証するテスト（Mock使用）。
2.  **Green Phase**:
    - `src/issue_creator_kit/infrastructure/github_adapter.py` を実装。
    - `PyGithub` の `GithubException` を捕捉し、独自の `InfrastructureError` に変換するロジックを追加。

### 3.3. Configuration Changes
- なし

## 4. Branching Strategy
- **Base Branch**: `feature/impl-adr003`
- **Feature Branch**: `feature/task-T-3-github-adapter`

## 5. Verification & DoD (完了条件)
- [ ] `find_or_create_issue` が冪等性（既存があれば作成しない）を持つことがテストで証明されていること。
- [ ] API エラー発生時に適切な独自例外が送出されること。

## 6. TDD Scenarios
- **Scenario 1 (Idempotency)**:
    - Given: Issue with title "Task A" exists.
    - When: `find_or_create_issue("Task A")`.
    - Then: Returns existing issue number, `create_issue` is NOT called.
