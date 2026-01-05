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
- **As-is (現状)**: フェーズが完了しても、次フェーズの準備（移動 PR 作成）は手動で行う必要がある。
- **To-be (あるべき姿)**: `next_phase_path` メタデータを検知し、自動的に「次フェーズ起票用 PR」が作成される。
- **Design Evidence (設計の根拠)**: `design-003-logic.md` 第 4 項

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `reqs/design/_inbox/design-003-logic.md`
- [ ] `docs/specs/infra-interface.md`
- [ ] `docs/specs/test-criteria.md`

## 3. 実装手順と制約 (Implementation Steps & Constraints)

### 3.1. 負の制約 (Negative Constraints)
- [ ] **無限ループ防止**: 同一の `head` ブランチ名が既に存在する場合や、循環参照（P1->P2->P1）を検知した場合は PR 作成を停止すること。
- [ ] **変更禁止**: `main` ブランチへの直接プッシュ。必ず新ブランチを作成すること。

### 3.2. 実装手順 (Changes)
- [ ] **UseCase実装**: `src/issue_creator_kit/usecase/workflow.py`
    - **PhasePromoter**: `design-003-logic.md` 第 4.2 項のフロー（ブランチ作成、ファイル移動、コミット、PR作成）を実装。
    - **SafetyMechanisms**: 無限ループ防止用のセット（`visited_phase_paths`）および最大深度チェックを実装。
- [ ] **テスト実装**: `tests/unit/usecase/test_workflow.py`
    - **Scenario**: `docs/specs/test-criteria.md` の `AP-001`〜`AP-004` をカバーするテストを記述。

### 3.3. 構成変更・削除 (Configuration / Cleanup)
- なし

## 4. ブランチ戦略 (Branching Strategy)
- **ベースブランチ (Base Branch)**: `feature/phase-2-foundation`
- **作業ブランチ (Feature Branch)**: `feature/task-T2-4-auto-pr`

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **自動テスト**: `pytest tests/unit/usecase/test_workflow.py` がパスすること（TC: AP-001〜AP-004）。
- [ ] **観測される挙動**: 循環参照を模した入力に対し、警告ログを出力して PR 作成をスキップすること。

## 6. 成果物 (Deliverables)
- `src/issue_creator_kit/usecase/workflow.py`
- `tests/unit/usecase/test_workflow.py`
