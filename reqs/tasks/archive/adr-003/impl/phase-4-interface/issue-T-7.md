---
title: "[TDD] Implement CLI Commands & Entrypoint"
labels: ["gemini:tdd"]
roadmap: "../../../../../docs/implementation/plans/adr-003/tdd-plan.md"
task_id: "T-7"
depends_on: ["../phase-3-usecase/issue-T-4.md", "../phase-3-usecase/issue-T-5.md", "../phase-3-usecase/issue-T-6.md"]
status: "Draft"
---

## 1. Goal & Context (Why & What)

### Goal
- 実装された各 UseCase を呼び出すための CLI コマンド（`process-diff`, `process-merge`）を実装し、GitHub Actions から実行可能にする。

### As-is (現状)
- `cli.py` に古いロジック（`run-workflow`）が残っている可能性がある。

### To-be (あるべき姿)
- `cli.py` が新しいサブコマンドをサポートし、環境変数 `GITHUB_MCP_PAT` のチェックや例外ハンドリング（終了コード制御）を適切に行う。

### Design Evidence
- [CLI Spec](../../../../../docs/specs/api/cli_commands.md)

## 2. Input Context (資料 & 情報)
- **Interface**: `src/issue_creator_kit/cli.py`
- **Spec**: `docs/specs/api/cli_commands.md`

## 3. Implementation Steps & Constraints (How)

### 3.1. Negative Constraints (してはいけないこと)
- CLI 層にビジネスロジックを書くこと（UseCase を呼ぶだけにする）。
- `print` でデバッグ情報を出力しないこと（`logging` を使う）。

### 3.2. Implementation Steps (実行手順)
1.  **Red Phase**:
    - `tests/test_cli.py` を作成。
    - `python -m issue_creator_kit.cli process-diff` を実行し、引数不足でエラーになること、正常時に UseCase が呼ばれることを検証。
2.  **Green Phase**:
    - `argparse` または `typer` を用いてサブコマンドを実装。
    - 依存性注入（DI）を行い、UseCase を初期化して実行。

### 3.3. Configuration Changes
- `pyproject.toml` の `[project.scripts]` は既に設定済み。

## 4. Branching Strategy
- **Base Branch**: `feature/impl-adr003`
- **Feature Branch**: `feature/task-T-7-cli`

## 5. Verification & DoD (完了条件)
- [ ] コマンドラインから `process-diff`, `process-merge` が実行可能であること。
- [ ] 正常終了時に exit code 0、エラー時に非 0 を返すこと。

## 6. TDD Scenarios
- **Scenario 1 (Args)**: `process-diff` without args -> Exit code 2 (usage error).
- **Scenario 2 (Success)**: `process-diff --base-sha HEAD~1` -> Calls UseCase, Exit code 0.
