---
title: "次フェーズ PR 自動作成（Auto-PR）とブランチ自動作成ロジックの TDD 実装"
labels:
  - "task"
  - "P1"
  - "BACKENDCODER"
roadmap: "reqs/roadmap/active/roadmap-adr003-task-lifecycle.md"
task_id: "T2-4"
depends_on: ["issue-T2-3.md"]
next_phase_path: ""
status: "Draft"
---
# 次フェーズ PR 自動作成（Auto-PR）とブランチ自動作成ロジックの TDD 実装

## 親Issue / ロードマップ (Context)
- **Roadmap**: reqs/roadmap/active/roadmap-adr003-task-lifecycle.md
- **Task ID**: T2-4

## 1. 目的と背景 (Goal & Context)
- **As-is (現状)**: フェーズ完了後、次のフェーズの準備は手動で行う必要がある。
- **To-be (あるべき姿)**: `next_phase_path` を検知し、自動的に次フェーズ用のブランチ作成、ファイル移動、PR 作成が行われる。
- **Design Evidence (設計の根拠)**: `design-003-logic.md`

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `reqs/design/_inbox/design-003-logic.md`
- [ ] `docs/specs/infra-interface.md`

## 3. 実装手順と制約 (Implementation Steps & Constraints)

### 3.1. 負の制約 (Negative Constraints)
- [ ] **変更禁止**: 無限ループを引き起こすような再帰呼び出し。

### 3.2. 実装手順 (Changes)
- [ ] **ファイル**: `src/issue_creator_kit/usecase/workflow.py`
    - **処理内容**: `PhasePromoter` クラスの実装。
- [ ] **ファイル**: `tests/unit/usecase/test_workflow.py`

### 3.3. 構成変更・削除 (Configuration / Cleanup)
- なし

## 4. ブランチ戦略 (Branching Strategy)
- **ベースブランチ (Base Branch)**: `feature/phase-2-foundation`
- **作業ブランチ (Feature Branch)**: `feature/T2-4-auto-pr-impl`

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **自動テスト**: パスすること。

## 6. 成果物 (Deliverables)
- `workflow.py`
