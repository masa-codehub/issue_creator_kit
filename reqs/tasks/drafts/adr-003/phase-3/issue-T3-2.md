---
title: "旧キュー方式関連資産の清掃とアーカイブ"
labels:
  - "task"
  - "P1"
  - "BACKENDCODER"
roadmap: "reqs/roadmap/active/roadmap-adr003-task-lifecycle.md"
task_id: "T3-2"
depends_on: ["issue-T3-1.md"]
next_phase_path: ""
status: "Draft"
---
# 旧キュー方式関連資産の清掃とアーカイブ

## 親Issue / ロードマップ (Context)
- **Roadmap**: reqs/roadmap/active/roadmap-adr003-task-lifecycle.md
- **Task ID**: T3-2

## 1. 目的と背景 (Goal & Context)
- **As-is (現状)**: 物理キュー方式を定義していた `adr-001` が承認済みとして残っており、物理フォルダ `reqs/tasks/_queue` も残存している可能性がある。
- **To-be (あるべき姿)**: 物理キュー方式が過去のものであることが明確化され、不要なフォルダが削除されている。
- **Design Evidence (設計の根拠)**: ADR-003

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `reqs/design/_approved/adr-001-issue-creation-logic.md`
- [ ] `reqs/tasks/_queue/`

## 3. 実装手順と制約 (Implementation Steps & Constraints)

### 3.1. 負の制約 (Negative Constraints)
- [ ] **注意**: 誤って必要なコードを消さないこと（CLI等の実装は既にクリーンであることを確認済み）。

### 3.2. 実装手順 (Changes)
- [ ] **アーカイブ**: `reqs/design/_approved/adr-001-issue-creation-logic.md`
    - **処理内容**: `reqs/design/_archive/` へ移動、またはファイルの先頭に「ADR-003 により廃止」等の注釈を追記して `_approved` に残す（どちらが適切か判断して実行）。
- [ ] **ディレクトリ削除**: `reqs/tasks/_queue/`
    - **処理内容**: 存在する場合は削除する。

### 3.3. 構成変更・削除 (Configuration / Cleanup)
- [ ] **削除**: `reqs/tasks/_queue/`

## 4. ブランチ戦略 (Branching Strategy)
- **ベースブランチ (Base Branch)**: `feature/phase-3-foundation`
- **作業ブランチ (Feature Branch)**: `feature/T3-2-cleanup`

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **観測される挙動**: `_queue` フォルダが存在しないこと。
- [ ] **観測される挙動**: テストが全てパスすること。

## 6. 成果物 (Deliverables)
- 削除コミット
