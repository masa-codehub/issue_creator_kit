---
title: "[TDD] Implement Git & FileSystem Adapters"
labels: ["gemini:tdd"]
roadmap: "docs/implementation/plans/adr-003/tdd-plan.md"
task_id: "T-2"
depends_on: ["issue-T-1.md"]
status: "Draft"
---

## 1. Goal & Context (Why & What)

### Goal
- Git 操作（差分取得、コミット、ブランチ作成）とファイルシステム操作を抽象化するアダプターを実装し、外部システムへの依存をテスト可能な形で隔離する。

### As-is (現状)
- `src/issue_creator_kit/infrastructure/` 配下の実装が不足しており、特に `--no-renames` オプション付きの差分取得ロジックが未実装。

### To-be (あるべき姿)
- `GitAdapter.get_added_files` が移動されたファイルを「削除と追加」ではなく「追加」として正しく検知できる（仮想キューの要件）。
- `FileSystemAdapter` がファイルの読み書きを安全に行える。

### Design Evidence
- [Adapter Spec](../../../../docs/specs/components/infra_adapters.md)
- [Handover: Virtual Queue](../../../../docs/handovers/spec-to-tdd.md)

## 2. Input Context (資料 & 情報)
- **Adapter Logic**: `src/issue_creator_kit/infrastructure/git_adapter.py`, `fs_adapter.py`
- **Spec**: `docs/specs/components/infra_adapters.md`

## 3. Implementation Steps & Constraints (How)

### 3.1. Negative Constraints (してはいけないこと)
- `git` コマンドを `subprocess` で直接叩くコードを UseCase 層に書かない（Adapter に閉じ込める）。
- テスト内で実際の `.git` ディレクトリを操作しない（一時ディレクトリを作成して検証する）。

### 3.2. Implementation Steps (実行手順)
1.  **Red Phase (GitAdapter)**:
    - `tests/infrastructure/test_git_adapter.py` を作成。
    - ファイルをリネーム（移動）しただけのコミットに対し、`get_added_files` がそのファイルを返すことを期待するテスト（`--no-renames` の検証）を作成。
2.  **Green Phase (GitAdapter)**:
    - `src/issue_creator_kit/infrastructure/git_adapter.py` を実装。
    - `subprocess.run(["git", "diff", "--name-only", "--diff-filter=A", "--no-renames", ...])` を使用。
3.  **Red/Green (FSAdapter)**:
    - 基本的な読み書きのテストと実装を行う。

### 3.3. Configuration Changes
- なし

## 4. Branching Strategy
- **Base Branch**: `feature/impl-adr003`
- **Feature Branch**: `feature/task-T-2-git-adapter`

## 5. Verification & DoD (完了条件)
- [ ] `GitAdapter` が仮想キュー（移動ファイル）を「追加」として検知できること。
- [ ] `pytest tests/infrastructure/` が全件パスすること。

## 6. TDD Scenarios
- **Scenario 1 (Virtual Queue)**:
    - Setup: `git mv drafts/file.md archive/file.md`
    - Action: `get_added_files(base_sha)`
    - Expect: `archive/file.md` is in the list.
