---
title: "Phase 3 Foundation ブランチ作成・確認"
labels:
  - "task"
  - "P1"
  - "SYSTEM_ARCHITECT"
roadmap: "reqs/roadmap/active/roadmap-adr003-task-lifecycle.md"
task_id: "T3-1"
depends_on: ["issue-T2-7.md"]
next_phase_path: ""
status: "Draft"
issue: "#154"
---
# Phase 3 Foundation ブランチ作成・確認

## 親Issue / ロードマップ (Context)
- **Roadmap**: reqs/roadmap/active/roadmap-adr003-task-lifecycle.md
- **Task ID**: T3-1
- **Depends on**: #126 (T2-7)

## 1. 目的と背景 (Goal & Context)
- **As-is (現状)**: Phase 3 は「自動化ロジックの修正」フェーズとして再定義された。以前の Auto-PR 試行により `feature/phase-3-foundation` が存在している可能性がある。
- **To-be (あるべき姿)**: `feature/phase-3-foundation` が存在し、最新の `main` (ADR-003 の 8 ステップ修正反映済み) と同期されている。
- **Design Evidence (設計の根拠)**: ADR-003 第 3.3 項 (フェーズ連鎖の基点)

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `reqs/roadmap/active/roadmap-adr003-task-lifecycle.md`
- [ ] `reqs/design/_approved/adr-003-task-and-roadmap-lifecycle.md`

## 3. 実装手順と制約 (Implementation Steps & Constraints)

### 3.1. 負の制約 (Negative Constraints)
- [ ] **リセット禁止**: 既存の `feature/phase-3-foundation` を削除して作り直すのではなく、可能な限り `merge` または `rebase` で最新化すること（履歴の連続性を重視）。
- [ ] **作業禁止**: このタスクで `src/` 配下のコード変更を行わないこと。

### 3.2. 実装手順 (Changes)
- [ ] **ブランチ確認**: `git branch -a | grep feature/phase-3-foundation` で存在を確認。
- [ ] **最新化**: 
    - 存在する場合: checkout し、`git merge origin/main` を実行。
    - 存在しない場合: `git checkout -b feature/phase-3-foundation main` で作成。
- [ ] **プッシュ**: `git push origin feature/phase-3-foundation` でリモートと同期。

### 3.3. 構成変更・削除 (Configuration / Cleanup)
- なし

## 4. ブランチ戦略 (Branching Strategy)
- **Pattern**: Foundation (Setup)
- **Base Branch**: `main`
- **Head Branch**: `feature/phase-3-foundation`

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **観測される挙動**: `git branch --show-current` が `feature/phase-3-foundation` であること。
- [ ] **観測される挙動**: `git log origin/main..HEAD` で、`main` の最新修正（ADR-003 等）が取り込まれていることを確認。

## 6. 成果物 (Deliverables)
- 同期済みの `feature/phase-3-foundation` ブランチ
