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
- **Depends on**: issue-T3-3.md

## 1. 目的と背景 (Goal & Context)
- **As-is (現状)**: 現在の Actions は `push` (Issue起票) のみ対応。
- **To-be (あるべき姿)**: `pull_request` のクローズを検知し、安全に次フェーズへの PR を作成するワークフローが定義されている。
- **Design Evidence (設計の根拠)**: docs/specs/auto-pr-logic.md

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `docs/specs/auto-pr-logic.md`
- [ ] `.github/workflows/auto-create-issues.yml` (参考用)

## 3. 実装手順と制約 (Implementation Steps & Constraints)

### 3.1. 負の制約 (Negative Constraints)
- [ ] **暴走防止**: `main` 以外のブランチへのマージで発火しないよう `branches: [main]` を厳守すること。
- [ ] **権限最小化**: `pull-requests: write` 以外の余計な権限を付与しないこと。

### 3.2. 実装手順 (Changes)
- [ ] **ファイル作成**: `.github/workflows/auto-phase-promotion.yml` を新規作成。
- [ ] **トリガー定義**:
    ```yaml
    on:
      pull_request:
        types: [closed]
        branches: [main]
    ```
- [ ] **実行条件**: `if: github.event.pull_request.merged == true`
- [ ] **ステップ定義**: 実装した CLI コマンド (T3-3) を呼び出すステップを記述。

### 3.3. 構成変更・削除 (Configuration / Cleanup)
- なし

## 4. ブランチ戦略 (Branching Strategy)
- **Pattern**: Feature (Configuration)
- **Base Branch**: `feature/phase-3-foundation`
- **Head Branch**: `feature/task-T3-4-workflow`

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **観測される挙動**: 構文エラーがなく、GitHub の Actions タブで認識されること。

## 6. 成果物 (Deliverables)
- `.github/workflows/auto-phase-promotion.yml`
