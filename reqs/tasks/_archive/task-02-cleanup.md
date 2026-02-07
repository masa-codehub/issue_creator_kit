---
id: task-008-02
parent: adr-008
type: task
title: "ADR-008: Cleanup Legacy Automation Code"
status: Draft
phase: cleanup
labels:
  - "gemini:spec"
  - "P1"
  - "BACKENDCODER"
roadmap: "docs/specs/plans/adr-008-automation-cleanup/definitions.md"
depends_on: []
issue_id:
---

# ADR-008: Cleanup Legacy Automation Code

## 1. 目的と背景 (Goal & Context)

- **As-is (現状)**: ADR-008 で廃止が決定した `WorkflowUseCase`, `ApprovalUseCase`, `auto-approve-docs.yml` 等の旧コードが残存している。
- **To-be (あるべき姿)**: `definitions.md` の "Cleanup Targets" リストに基づき、不要なコードが物理削除され、関連するテストや呼び出し箇所も整理されている。
- **Design Evidence**: `docs/specs/plans/adr-008-automation-cleanup/definitions.md` (Cleanup Targets)

## 2. 参照資料・入力ファイル (Input Context)

- [ ] `docs/specs/plans/adr-008-automation-cleanup/definitions.md`

## 3. 実装手順と制約 (Implementation Steps & Constraints)

### 3.1. 負の制約 (Negative Constraints)

- [ ] **変更禁止**: 新しい Scanner ロジックの実装（削除のみに集中する）。

### 3.2. 実装手順 (Changes)

#### 3.2.1. Remove Legacy Files

- [ ] **削除**: `.github/workflows/auto-approve-docs.yml`
- [ ] **削除**: `src/issue_creator_kit/usecase/workflow.py`
- [ ] **削除**: `src/issue_creator_kit/usecase/approval.py`

#### 3.2.2. Clean References

- [ ] **ファイル**: `src/issue_creator_kit/cli.py`
  - **処理内容**: 削除された UseCase を呼び出しているコマンド（`approve`, `process-merge` 等）を削除またはコメントアウト（Scanner実装までの一時的な措置）。

## 4. ブランチ戦略 (Branching Strategy)

- **ベースブランチ (Base Branch)**: feature/spec-update-adr008
- **作業ブランチ (Feature Branch)**: feature/task-008-02-cleanup

## 5. 検証手順・完了条件 (Verification & DoD)

- [ ] **自動テスト**: `pytest` が（削除分を除いて）パスすること。
- [ ] **観測される挙動**: `ick approve` などの旧コマンドが削除されていること。
- [ ] **静的解析**: `ruff check .` および `mypy .` がパスすること（削除に伴うimportエラーがないこと）。

## 6. 成果物 (Deliverables)

- (削除コミット)
- `src/issue_creator_kit/cli.py` (更新)
