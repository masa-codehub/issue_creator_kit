---
title: "Auto-PR ロジックの実装"
labels:
  - "task"
  - "P1"
  - "BACKENDCODER"
roadmap: "reqs/roadmap/active/roadmap-adr003-task-lifecycle.md"
task_id: "T3-3"
depends_on: ["issue-T3-2.md"]
next_phase_path: ""
status: "Draft"
---
# Auto-PR ロジックの実装

## 親Issue / ロードマップ (Context)
- **Roadmap**: reqs/roadmap/active/roadmap-adr003-task-lifecycle.md
- **Task ID**: T3-3

## 1. 目的と背景 (Goal & Context)
- **As-is (現状)**: Auto-PR のロジックが存在しない（バグ修正で削除済み）。
- **To-be (あるべき姿)**: `design-003-v2-auto-pr.md` に基づき、タスク完了時に Auto-PR を作成する機能が実装されている。
- **Design Evidence (設計の根拠)**: design-003-v2-auto-pr.md

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `reqs/design/_approved/design-003-v2-auto-pr.md`

## 3. 実装手順と制約 (Implementation Steps & Constraints)

### 3.1. 負の制約 (Negative Constraints)
- [ ] なし

### 3.2. 実装手順 (Changes)
- [ ] **CLI拡張**: `process-pr-merge` (仮) のような新コマンド、または既存コマンドへのフラグ追加。
- [ ] **UseCase実装**: `WorkflowUseCase` に「完了Issueからの次フェーズ特定・PR作成」ロジックを追加。
- [ ] **テスト**: 単体テストの追加。

### 3.3. 構成変更・削除 (Configuration / Cleanup)
- なし

## 4. ブランチ戦略 (Branching Strategy)
- **ベースブランチ (Base Branch)**: `feature/phase-3-foundation`
- **作業ブランチ (Feature Branch)**: `feature/task-T3-3-impl`

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **自動テスト**: 新規ロジックのユニットテストがパスすること。

## 6. 成果物 (Deliverables)
- 実装コード
