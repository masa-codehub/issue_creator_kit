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
- **As-is (現状)**: Issue 起票後、ロードマップ内のリンクは手動更新が必要。
- **To-be (あるべき姿)**: 起票されたタスクファイルのパス変更（Draft->Archive）と Issue 番号の付与がロードマップに自動反映される。
- **Design Evidence (設計の根拠)**: `design-003-logic.md`

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `reqs/design/_inbox/design-003-logic.md`

## 3. 実装手順と制約 (Implementation Steps & Constraints)

### 3.1. 負の制約 (Negative Constraints)
- [ ] **変更禁止**: ロードマップの他の行を破壊しない。

### 3.2. 実装手順 (Changes)
- [ ] **ファイル**: `src/issue_creator_kit/usecase/roadmap_sync.py` (新規)
    - **処理内容**: `RoadmapUpdater` クラスの実装。
        - 入力: 起票された Issue 情報（ファイルパス、Issue番号）。
        - 処理: 指定されたロードマップファイルを読み込み、行単位で正規表現マッチングを行う。
        - 置換: `drafts/` を `archive/` に置換し、Issue リンクを追記。
        - 保存: ファイルを上書き保存。
- [ ] **ファイル**: `tests/unit/usecase/test_roadmap_sync.py`

### 3.3. 構成変更・削除 (Configuration / Cleanup)
- なし

## 4. ブランチ戦略 (Branching Strategy)
- **ベースブランチ (Base Branch)**: `feature/phase-2-foundation`
- **作業ブランチ (Feature Branch)**: `feature/T2-3-roadmap-sync`

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **自動テスト**: パスすること。
- [ ] **コード**: `roadmap_sync.py` に `RoadmapUpdater` クラスが存在すること。

## 6. 成果物 (Deliverables)
- `roadmap_sync.py`