---
title: "資産の同期と不要スクリプトの削除"
labels:
  - "task"
  - "P2"
  - "SYSTEM_ARCHITECT"
roadmap: "reqs/roadmap/active/roadmap-adr002-document-approval-flow.md"
task_id: "T4-2"
depends_on:
  - "issue-T4-1.md"
status: "Draft"
---
# {{title}}

## 親Issue / ロードマップ (Context)
- **Roadmap**: {{roadmap}}
- **Task ID**: {{task_id}}

## 1. 目的と背景 (Goal & Context)
- **As-is (現状)**: `src/issue_creator_kit/assets/` 内のテンプレートやワークフロー定義が、実際の `.github/workflows/` 等と同期されていない可能性がある。また、旧式の承認スクリプトが残っているかもしれない。
- **To-be (あるべき姿)**: 配布用資産が最新化され、不要なコードが削除され、クリーンな状態になる。

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `src/issue_creator_kit/assets/` (配布用資産)
- [ ] `.github/workflows/` (正となる最新定義)

## 3. 実装手順 (Implementation Steps)

### 3.1. テンプレート同期 (Sync)
- [ ] **ファイル**: `src/issue_creator_kit/assets/workflows/auto-approve-docs.yml`
    - **処理内容**: `.github/workflows/auto-approve-docs.yml` の内容をコピーして最新化する。

### 3.2. 削除 (Cleanup)
- [ ] **削除**: 不要と判断されたシェルスクリプト等があれば削除する。

## 4. ブランチ戦略 (Branching Strategy)
- **ベースブランチ (Base Branch)**: `feature/phase-4-cleanup`
- **作業ブランチ (Feature Branch)**: `feature/T4-2-cleanup-assets`

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **差分確認**: `diff` コマンド等で、配布用アセットと実ファイルが一致していることを確認する。

## 6. 成果物 (Deliverables)
- 更新された `assets` ディレクトリ