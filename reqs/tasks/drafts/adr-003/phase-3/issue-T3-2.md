---
title: "物理 _queue フォルダ関連コードの完全削除"
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
# 物理 _queue フォルダ関連コードの完全削除

## 親Issue / ロードマップ (Context)
- **Roadmap**: reqs/roadmap/active/roadmap-adr003-task-lifecycle.md
- **Task ID**: T3-2

## 1. 目的と背景 (Goal & Context)
- **As-is (現状)**: 古い物理キュー方式のコード（`_queue` ディレクトリを走査するロジック）が残っている可能性がある。
- **To-be (あるべき姿)**: 不要なコードが削除され、システムがクリーンになっている。
- **Design Evidence (設計の根拠)**: ADR-003

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `src/issue_creator_kit/` (grep `_queue`)

## 3. 実装手順と制約 (Implementation Steps & Constraints)

### 3.1. 負の制約 (Negative Constraints)
- [ ] **注意**: 誤って必要なコードを消さないこと。

### 3.2. 実装手順 (Changes)
- [ ] **ファイル**: `src/...`
    - **処理内容**: `reqs/tasks/_queue` を参照している古いロジックを特定し削除する。
- [ ] **ファイル**: `reqs/tasks/_queue/` (ディレクトリ自体)
    - **処理内容**: 空であれば削除（`.gitkeep` も含む）。

### 3.3. 構成変更・削除 (Configuration / Cleanup)
- [ ] **削除**: `reqs/tasks/_queue/`

## 4. ブランチ戦略 (Branching Strategy)
- **ベースブランチ (Base Branch)**: `feature/phase-3-foundation`
- **作業ブランチ (Feature Branch)**: `feature/T3-2-cleanup`

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **自動テスト**: 既存テストが全てパスすること（リグレッションがないこと）。

## 6. 成果物 (Deliverables)
- 削除コミット
