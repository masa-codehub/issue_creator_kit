---
title: "ロードマップ WBS リンク自動置換ロジックの TDD 実装"
labels:
  - "task"
  - "P1"
  - "BACKENDCODER"
roadmap: "reqs/roadmap/active/roadmap-adr003-task-lifecycle.md"
task_id: "T2-3"
depends_on: ["issue-T2-2.md"]
next_phase_path: ""
status: "Draft"
---
# ロードマップ WBS リンク自動置換ロジックの TDD 実装

## 親Issue / ロードマップ (Context)
- **Roadmap**: reqs/roadmap/active/roadmap-adr003-task-lifecycle.md
- **Task ID**: T2-3

## 1. 目的と背景 (Goal & Context)
- **As-is (現状)**: Issue 起票後、ロードマップ内の WBS テーブルのリンクは手動で `drafts` から `archive` へ修正し、Issue 番号を追記する必要がある。
- **To-be (あるべき姿)**: `RoadmapSyncEngine` により、起票されたタスクに関連するロードマップ行が自動的に更新される。
- **Design Evidence (設計の根拠)**: `design-003-logic.md` 第 3 項

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `reqs/design/_inbox/design-003-logic.md`
- [ ] `docs/specs/test-criteria.md`

## 3. 実装手順と制約 (Implementation Steps & Constraints)

### 3.1. 負の制約 (Negative Constraints)
- [ ] **破壊の禁止**: 置換対象以外の Markdown 行（ヘッダー、説明文、他タスクの行）を破壊しないこと。
- [ ] **エラー処理**: リンクが見つからない場合は、警告ではなくエラーとして扱い処理を中断すること（設計書 3.3 参照）。

### 3.2. 実装手順 (Changes)
- [ ] **UseCase実装**: `src/issue_creator_kit/usecase/roadmap_sync.py` (新規または既存)
    - **RoadmapUpdater**: `design-003-logic.md` 第 3 項の置換ロジック（Draft->Archiveパス置換、Issue番号追記）を実装。
- [ ] **テスト実装**: `tests/unit/usecase/test_roadmap_sync.py`
    - **Scenario**: `docs/specs/test-criteria.md` の `RS-001`〜`RS-003` をカバーするテストを記述。

### 3.3. 構成変更・削除 (Configuration / Cleanup)
- なし

## 4. ブランチ戦略 (Branching Strategy)
- **ベースブランチ (Base Branch)**: `feature/phase-2-foundation`
- **作業ブランチ (Feature Branch)**: `feature/task-T2-3-roadmap-sync`

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **自動テスト**: `pytest tests/unit/usecase/test_roadmap_sync.py` がパスすること（TC: RS-001〜RS-003）。
- [ ] **観測される挙動**: 存在しないタスク ID を指定した際、エラーで安全に停止すること。

## 6. 成果物 (Deliverables)
- `src/issue_creator_kit/usecase/roadmap_sync.py`
- `tests/unit/usecase/test_roadmap_sync.py`
