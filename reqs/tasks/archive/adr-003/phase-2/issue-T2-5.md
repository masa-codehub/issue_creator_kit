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
- **As-is (現状)**: 現在のワークフロー定義は古いロジックに基づいているか、今回の新機能（仮想キュー）に対応していない。
- **To-be (あるべき姿)**: `main` への `push` イベントをトリガーに、今回実装した新ロジック（`process-diff` 等）が起動するよう設定されている。
- **Design Evidence (設計の根拠)**: `design-003-logic.md` 第 1.1 項

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `.github/workflows/ci.yml` (既存)
- [ ] `docs/spikes/git-diff-logic.md` (確定したコマンドの確認)

## 3. 実装手順と制約 (Implementation Steps & Constraints)

### 3.1. 負の制約 (Negative Constraints)
- [ ] **権限最小化**: `GITHUB_TOKEN` に必要以上の権限を付与しない（`contents: write`, `issues: write`, `pull-requests: write` に限定）。

### 3.2. 実装手順 (Changes)
- [ ] **ワークフロー更新**: `.github/workflows/issue-automator.yml` (新規)
    - **Trigger**: `on: push: branches: [main]`
    - **Step**: ICK CLI を実行し、`github.event.before` と `after` を引数に渡す設定を記述。
    - **Context**: 取得した差分ファイルを `archive/` 配下に限定するフィルタ設定。

### 3.3. 構成変更・削除 (Configuration / Cleanup)
- [ ] **削除**: 旧式の Issue 起票ワークフロー（もし独立していれば）。

## 4. ブランチ戦略 (Branching Strategy)
- **ベースブランチ (Base Branch)**: `feature/phase-2-foundation`
- **作業ブランチ (Feature Branch)**: `feature/task-T2-5-workflow-config`

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **観測される挙動**: YAML のシンタックスチェックがパスし、`main` へのマージ後に Actions ジョブがスケジュールされること。

## 6. 成果物 (Deliverables)
- `.github/workflows/issue-automator.yml`