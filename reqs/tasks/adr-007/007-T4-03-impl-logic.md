---
id: 007-T4-03
parent: adr-007
parent_issue: 
type: task
title: "[TDD] Issue Creation Logic (UseCase)"
status: Draft
phase: usecase
labels:
  - "gemini:tdd"
  - "P1"
  - "BACKENDCODER"
roadmap: "docs/specs/plans/adr-007-metadata-driven-lifecycle/tdd-plan.md"
depends_on: ["007-T4-02"]
issue_id: 
---
# [TDD] Issue Creation Logic (UseCase)

## 1. 目的と背景 (Goal & Context)
- **As-is (現状)**: 既存の起票ロジックは物理ディレクトリ階層（phase-X-xxx/）のスキャンに依存しており、ADR-007 のメタデータ（`depends_on`）ベースの DAG 解析が未実装。
- **To-be (あるべき姿)**: Git Diff から対象ファイルを検知し、依存関係をトポロジカルソートし、原子的な「起票 -> メタデータ更新 -> 移動」を行う UseCase が実装されている。
- **Design Evidence (設計の根拠)**: 
    - `docs/specs/logic/creation_logic.md`

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `docs/specs/logic/creation_logic.md`
- [ ] `src/issue_creator_kit/usecase/creation.py`
- [ ] `src/issue_creator_kit/infrastructure/git_adapter.py`

## 3. 実装手順と制約 (Implementation Steps & Constraints)

### 3.1. 負の制約 (Negative Constraints)
- [ ] **Fail-fast**: 1件でも起票 API が失敗した場合は、そのバッチにおけるファイル移動（Commit Phase）を実行してはならない。
- [ ] **変更禁止**: `Document` クラスの内部構造（T4-01で確定したもの）を勝手に変更しない。

### 3.2. 実装手順 (Changes)
- [ ] **ファイル**: `src/issue_creator_kit/usecase/creation.py`
    - **処理内容**: 
        - `IssueCreationUseCase.create_issues(before, after, adr_id=None)` の実装。
        - `graphlib.TopologicalSorter` を用いた依存関係の解決。
        - `depends_on` が archive 内や GitHub 上にある場合の解決ロジック。
        - アトミックな起票・移動シーケンスの実装。
- [ ] **ファイル**: `tests/unit/usecase/test_creation.py`
    - **処理内容**: 
        - 正常系: 複雑な依存関係を持つ複数タスクの順序通り起票。
        - 異常系: 循環依存検出時のエラー。
        - 異常系: APIエラー時のアトミック性（ファイルが未移動であること）の検証。

## 4. ブランチ戦略 (Branching Strategy)
- **ベースブランチ (Base Branch)**: feature/impl-adr007-lifecycle
- **作業ブランチ (Feature Branch)**: tdd/task-007-T4-03-impl-logic

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **自動テスト**: `pytest tests/unit/usecase/test_creation.py` がパスすること。
- [ ] **静的解析**: `ruff check .` および `mypy .` がパスすること。
- [ ] **観測される挙動**: ログにて `Topological sort successful` 的なメッセージが確認できること。

## 6. 成果物 (Deliverables)
- `src/issue_creator_kit/usecase/creation.py`
- `tests/unit/usecase/test_creation.py`
