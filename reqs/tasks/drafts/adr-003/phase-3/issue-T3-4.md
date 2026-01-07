---
title: "GitHub Actions ワークフローの構築"
labels:
  - "task"
  - "P1"
  - "SYSTEM_ARCHITECT"
roadmap: "reqs/roadmap/active/roadmap-adr003-task-lifecycle.md"
task_id: "T3-4"
depends_on: ["issue-T3-3.md"]
next_phase_path: ""
status: "Draft"
---
# GitHub Actions ワークフローの構築

## 親Issue / ロードマップ (Context)
- **Roadmap**: reqs/roadmap/active/roadmap-adr003-task-lifecycle.md
- **Task ID**: T3-4

## 1. 目的と背景 (Goal & Context)
- **As-is (現状)**: `auto-create-issues.yml` (pushトリガー) しかない。
- **To-be (あるべき姿)**: `auto-phase-promotion.yml` (pull_request closedトリガー) が存在し、完了時に Auto-PR ロジックを呼び出す。
- **Design Evidence (設計の根拠)**: docs/specs/auto-pr-logic.md

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `docs/specs/auto-pr-logic.md`

## 3. 実装手順と制約 (Implementation Steps & Constraints)

### 3.1. 負の制約 (Negative Constraints)
- [ ] **無限ループ防止**: Auto-PR 自身がマージされた時に再度 Auto-PR が走らないよう、トリガー条件やロジックで制御する（マージされたPRが「タスク完了」なのか「ドラフト移動」なのかの区別）。

### 3.2. 実装手順 (Changes)
- [ ] **ファイル作成**: `.github/workflows/auto-phase-promotion.yml`
- [ ] **定義**: `on: pull_request: types: [closed]`かつ`if: github.event.pull_request.merged == true`

### 3.3. 構成変更・削除 (Configuration / Cleanup)
- なし

## 4. ブランチ戦略 (Branching Strategy)
- **ベースブランチ (Base Branch)**: `feature/phase-3-foundation`
- **作業ブランチ (Feature Branch)**: `feature/task-T3-4-workflow`

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **観測される挙動**: ワークフローが正しく定義されていること（動作確認は次タスク）。

## 6. 成果物 (Deliverables)
- ワークフロー定義ファイル
