---
id: 007-T4-02
parent: adr-007
type: task
title: "[TDD] Infrastructure Implementation (Infra)"
status: Draft
phase: infrastructure
date: 2026-02-05
labels:
  - "gemini:tdd"
  - "P1"
  - "BACKENDCODER"
roadmap: "docs/specs/plans/adr-007-metadata-driven-lifecycle/tdd-plan.md"
depends_on: ["007-T4-01"]
---
# [TDD] Infrastructure Implementation (Infra)

## 1. 目的と背景 (Goal & Context)
- **Goal**: `007-T4-01` で定義されたインターフェース（Protocol）に基づき、具象クラス（FileSystem, GitHub API）の実装を完了させ、実環境での動作を保証する。
- **As-is (現状)**: `FileSystemAdapter` には ID ベースのファイル検索ロジックがなく、`GitHubAdapter` は既存 Issue の更新（`sync_issue`）に未対応。
- **To-be (あるべき姿)**: `interfaces.py` の契約を満たし、`_archive/` 配下を含めた ID 検索や、`Document` オブジェクトを介した GitHub Issue 同期が可能なアダプターが実装されている。
- **Design Evidence (設計の根拠)**: 
    - `docs/specs/components/infra_adapters.md`

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `docs/specs/components/infra_adapters.md`
- [ ] `src/issue_creator_kit/domain/interfaces.py` (T4-01成果物)
- [ ] `src/issue_creator_kit/infrastructure/filesystem.py`
- [ ] `src/issue_creator_kit/infrastructure/github_adapter.py`

## 3. 実装手順と制約 (Implementation Steps & Constraints)

### 3.1. 負の制約 (Negative Constraints)
- [ ] **変更禁止**: `interfaces.py` で定義されたメソッド名や引数（変更が必要な場合は T4-01 に戻る）。
- [ ] **安全策**: 外部 API を直接叩かず、必ずモックテストを実施すること。

### 3.2. 実装手順 (Changes)
- [ ] **ファイル**: `src/issue_creator_kit/infrastructure/filesystem.py`
    - **処理内容**: 
        - `find_file_by_id(task_id, search_dirs)` の実装。
        - `Path` オブジェクトを戻り値とするように統一。
- [ ] **ファイル**: `src/issue_creator_kit/infrastructure/github_adapter.py`
    - **処理内容**: 
        - `sync_issue(doc: Document)` の実装。
        - タイトル検索ロジックおよび `issue_id` に基づく更新ロジックの統合。
- [ ] **ファイル**: `tests/unit/infrastructure/`
    - **処理内容**: 
        - `pyfakefs` を使用した `find_file_by_id` のテスト。
        - `unittest.mock` を使用した `sync_issue` の正常/異常系テスト。

## 4. ブランチ戦略 (Branching Strategy)
- **ベースブランチ (Base Branch)**: feature/impl-adr007-lifecycle
- **作業ブランチ (Feature Branch)**: tdd/task-007-T4-02-impl-infra

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **自動テスト**: `pytest tests/unit/infrastructure/` がパスすること。
- [ ] **静的解析**: `ruff check .` および `mypy .` がパスすること。
- [ ] **インターフェース適合**: 実装クラスが `interfaces.py` の Protocol を満たしていること。

## 6. 成果物 (Deliverables)
- `src/issue_creator_kit/infrastructure/filesystem.py`
- `src/issue_creator_kit/infrastructure/github_adapter.py`
- `tests/unit/infrastructure/test_filesystem.py`
- `tests/unit/infrastructure/test_github_adapter.py`
