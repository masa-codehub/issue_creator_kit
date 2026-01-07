---
title: "Issue起票オートメーション・ワークフローの新規作成"
labels:
  - "task"
  - "P1"
  - "TECHNICAL_DESIGNER"
roadmap: "reqs/roadmap/active/roadmap-adr003-task-lifecycle.md"
task_id: "T2-5"
depends_on: ["issue-T2-4.md"]
next_phase_path: ""
status: "Archived"
issue: 128
---
# Issue起票オートメーション・ワークフローの新規作成

## 親Issue / ロードマップ (Context)
- **Roadmap**: reqs/roadmap/active/roadmap-adr003-task-lifecycle.md
- **Task ID**: T2-5

## 1. 目的と背景 (Goal & Context)
- **As-is (現状)**: 仮想キュー（マージ差分）を検知して ICK を起動する自動化環境が存在しない。
- **To-be (あるべき姿)**: `main` への `push` イベントをトリガーに、今回実装した新ロジック（`process-diff` 等）を安全に起動する「専用のワークフローファイル」が構築されている。
- **Design Evidence (設計の根拠)**: `design-003-logic.md` 第 1.1 項

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `.github/workflows/ci.yml` (既存のCI設定を壊さないための参照)
- [ ] `docs/spikes/git-diff-logic.md` (確定したコマンドの確認)

## 3. 実装手順と制約 (Implementation Steps & Constraints)

### 3.1. 負の制約 (Negative Constraints)
- [ ] **変更禁止**: 既存の CI (Test/Lint) ワークフロー（`ci.yml`）。本タスクはこれらを置換するものではなく、独立したオートメーションを追加するものである。
- [ ] **権限最小化**: `GITHUB_TOKEN` に必要以上の権限を付与しない（`contents: write`, `issues: write`, `pull-requests: write` に限定）。

### 3.2. 実装手順 (Changes)
- [ ] **ワークフロー新規作成**: `.github/workflows/issue-automator.yml`
    - **Trigger**: `on: push: branches: [main]`
    - **Job**: 
        - `fetch-depth: 2` (before/after の差分取得に必要)
        - `github.event.before` と `after` を引数に渡して ICK CLI コマンドを実行する設定を記述。
    - **Context**: 取得した差分ファイルを `reqs/tasks/archive/` 配下に限定するフィルタ設定。

### 3.3. 構成変更・削除 (Configuration / Cleanup)
- なし

## 4. ブランチ戦略 (Branching Strategy)
- **ベースブランチ (Base Branch)**: `feature/phase-2-foundation`
- **作業ブランチ (Feature Branch)**: `feature/task-T2-5-workflow-config`

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **観測される挙動**: YAML のシンタックスチェックがパスし、`main` へのマージ後にこの新しい Actions ジョブがスケジュールされること。
- [ ] **構成確認**: `ci.yml` とは別に `issue-automator.yml` が存在すること。

## 6. 成果物 (Deliverables)
- `.github/workflows/issue-automator.yml`
