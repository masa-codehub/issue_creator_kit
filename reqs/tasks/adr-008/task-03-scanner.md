---
id: task-008-03
parent: adr-008
type: task
title: "ADR-008: Implement FileSystem Scanner Logic"
status: Draft
phase: domain
labels:
  - "gemini:spec"
  - "P1"
  - "BACKENDCODER"
roadmap: "docs/specs/plans/adr-008-automation-cleanup/definitions.md"
depends_on: ["task-008-01"]
issue_id: 
---
# ADR-008: Implement FileSystem Scanner Logic

## 1. 目的と背景 (Goal & Context)
- **As-is (現状)**: 物理ファイルシステムを走査し、`_inbox`, `_approved`, `_archive` の状態を判定するロジックが存在しない。
- **To-be (あるべき姿)**: `FileSystemScanner` が実装され、指定ディレクトリ配下のファイルを再帰的に走査し、Domain Model (`Task`) のリストを返却できる。
- **Design Evidence**: `docs/architecture/arch-structure-008-scanner.md` (FileSystemScanner)

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `src/issue_creator_kit/domain/models/` (Task-01 成果物)
- [ ] `docs/specs/plans/adr-008-automation-cleanup/definitions.md`

## 3. 実装手順と制約 (Implementation Steps & Constraints)

### 3.1. 負の制約 (Negative Constraints)
- [ ] **変更禁止**: Git コマンドの呼び出し（Gitには依存しない）。

### 3.2. 実装手順 (Changes)
#### 3.2.1. Implement Scanner Service
- [ ] **ファイル**: `src/issue_creator_kit/domain/services/scanner.py` (新規作成)
    - **処理内容**: `pathlib` を使用して `reqs/` 配下を走査。
    - **処理内容**: ファイルパスから `status` を判定するロジックの実装。
    - **処理内容**: `TaskParser` (Task-01で定義されたモデルのパース機能) を呼び出し、モデル化する。

## 4. ブランチ戦略 (Branching Strategy)
- **ベースブランチ (Base Branch)**: feature/spec-update-adr008
- **作業ブランチ (Feature Branch)**: feature/task-008-03-scanner

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **自動テスト**: `pytest tests/unit/domain/services/test_scanner.py` がパスすること。
- [ ] **TDD Criteria (Happy Path)**: テスト用ディレクトリ構造を用意し、正しい `Task` リストが返却されること。
- [ ] **TDD Criteria (Boundary)**: 空のディレクトリや、対象外のファイルが存在する場合の挙動が正しいこと。

## 6. 成果物 (Deliverables)
- `src/issue_creator_kit/domain/services/scanner.py`
- `tests/unit/domain/services/test_scanner.py`
