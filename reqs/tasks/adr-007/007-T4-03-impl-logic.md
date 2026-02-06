---
id: 007-T4-03
parent: adr-007
type: task
title: "[TDD] Issue Creation Logic (UseCase)"
status: Draft
phase: usecase
date: 2026-02-05
labels:
  - "gemini:tdd"
  - "P1"
  - "BACKENDCODER"
roadmap: "docs/specs/plans/adr-007-metadata-driven-lifecycle/tdd-plan.md"
depends_on: ["007-T4-01"]
---
# [TDD] Issue Creation Logic (UseCase)

## 1. 目的と背景 (Goal & Context)
- **Goal**: ADR-007 の中核である「メタデータ駆動型ライフサイクル」のビジネスロジックを実装する。T4-01 で定義されたインターフェースを Mock することで、インフラの実装を待たずにロジックの正しさを検証する。
- **As-is (現状)**: 既存の起票ロジックは物理ディレクトリ階層のスキャンに依存しており、メタデータ（`depends_on`）ベースの DAG 解析が未実装。
- **To-be (あるべき姿)**: Git Diff から対象ファイルを検知し、依存関係をトポロジカルソートし、原子的な「起票 -> メタデータ更新 -> 移動」を行う UseCase が実装されている。
- **Design Evidence (設計の根拠)**: 
    - `docs/specs/logic/creation_logic.md`

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `docs/specs/logic/creation_logic.md`
- [ ] `src/issue_creator_kit/domain/interfaces.py` (T4-01成果物)
- [ ] `src/issue_creator_kit/usecase/creation.py`

## 3. 実装手順と制約 (Implementation Steps & Constraints)

### 3.1. 負の制約 (Negative Constraints)
- [ ] **DI の徹底**: `FileSystemAdapter` 等を直接インスタンス化せず、`IFileSystemAdapter` 等の型ヒントで受け取り、テスト時は Mock を注入すること。
- [ ] **Fail-fast**: 1件でも起票 API が失敗した場合は、そのバッチにおけるファイル移動（Commit Phase）を実行してはならない。

### 3.2. 実装手順 (Changes)
- [ ] **ファイル**: `src/issue_creator_kit/usecase/creation.py`
    - **処理内容**: 
        - `IssueCreationUseCase.create_issues(before, after, adr_id=None)` の実装。
        - `graphlib.TopologicalSorter` を用いた依存関係の解決。
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
- [ ] **Mock 検証**: テストにおいて、各 Adapter のメソッドが期待される順序と引数で呼び出されていること。
- [ ] **静的解析**: `ruff check .` および `mypy .` がパスすること。

## 6. 成果物 (Deliverables)
- `src/issue_creator_kit/usecase/creation.py`
- `tests/unit/usecase/test_creation.py`
