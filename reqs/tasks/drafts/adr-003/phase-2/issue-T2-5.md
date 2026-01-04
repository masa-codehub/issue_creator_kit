---
title: "GitHub Actions ワークフロー定義の差し替え"
labels:
  - "task"
  - "P1"
  - "TECHNICAL_DESIGNER"
roadmap: "reqs/roadmap/active/roadmap-adr003-task-lifecycle.md"
task_id: "T2-5"
depends_on: ["issue-T2-4.md"]
next_phase_path: ""
status: "Draft"
---
# GitHub Actions ワークフロー定義の差し替え

## 親Issue / ロードマップ (Context)
- **Roadmap**: reqs/roadmap/active/roadmap-adr003-task-lifecycle.md
- **Task ID**: T2-5

## 1. 目的と背景 (Goal & Context)
- **As-is (現状)**: 古いワークフロー定義（`_queue` 監視）が動作している、あるいは停止している。
- **To-be (あるべき姿)**: 新しいロジック（`push` トリガーでの差分検知）を起動するワークフロー定義ファイルに置き換える。
- **Design Evidence (設計の根拠)**: ADR-003

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `.github/workflows/ci.yml` (または専用の `issue-creation.yml`)

## 3. 実装手順と制約 (Implementation Steps & Constraints)

### 3.1. 負の制約 (Negative Constraints)
- [ ] **変更禁止**: 既存の CI (Test/Lint) ワークフロー。

### 3.2. 実装手順 (Changes)
- [ ] **ファイル**: `.github/workflows/issue-automator.yml` (新規または更新)
    - **処理内容**: `main` への `push` をトリガーとし、ICK の新コマンド（例: `ick process-diff`）を実行する定義記述。

### 3.3. 構成変更・削除 (Configuration / Cleanup)
- なし

## 4. ブランチ戦略 (Branching Strategy)
- **ベースブランチ (Base Branch)**: `feature/phase-2-foundation`
- **作業ブランチ (Feature Branch)**: `feature/T2-5-workflow-update`

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **観測される挙動**: マージ後、Actions が正しく起動すること。

## 6. 成果物 (Deliverables)
- ワークフロー定義ファイル
