---
title: "統合検証（完了トリガーによるAuto-PR）"
labels:
  - "task"
  - "P1"
  - "SYSTEM_ARCHITECT"
roadmap: "reqs/roadmap/active/roadmap-adr003-task-lifecycle.md"
task_id: "T3-5"
depends_on: ["issue-T3-4.md"]
next_phase_path: ""
status: "Draft"
issue: "#158"
---
# 統合検証（完了トリガーによるAuto-PR）

## 親Issue / ロードマップ (Context)
- **Roadmap**: reqs/roadmap/active/roadmap-adr003-task-lifecycle.md
- **Task ID**: T3-5
- **Depends on**: issue-T3-4.md

## 1. 目的と背景 (Goal & Context)
- **As-is (現状)**: ロジックとワークフローが実装されたが、実機（GitHub）での連鎖挙動が未確認。
- **To-be (あるべき姿)**: ダミーPRのマージを通じて、Auto-PR が正しく作成されることが実証されている。
- **Design Evidence (設計の根拠)**: ADR-003 第 3.3 項 (ステップ 5-6)

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `docs/specs/auto-pr-logic.md`
- [ ] `.github/workflows/auto-phase-promotion.yml`

## 3. 実装手順と制約 (Implementation Steps & Constraints)

### 3.1. 負の制約 (Negative Constraints)
- [ ] **自己マージ禁止**: 本タスク (T3-5) の PR をマージすることで検証完了としてはならない。必ず**別のダミー PR** を用いて検証すること。
- [ ] **汚染禁止**: 検証に使用するダミーの Issue や PR は、検証終了後に必ずクリーンアップすること。

### 3.2. 実装手順 (Changes)
- [ ] **模擬タスク投入**:
    - `reqs/tasks/drafts/test-phase/issue-test.md` (next_phase_path 設定済み) を作成。
    - これを `reqs/tasks/archive/test-phase/` へ移動する PR を作成・マージし、Issue を起票させる。
- [ ] **完了シミュレーション**:
    - 起票された Issue に対する「実装完了ダミー PR」を作成（`Closes #TestIssue` を記載）。
    - ダミー PR を `main` へマージ。
- [ ] **連鎖確認**:
    - 数分待機し、Actions が正常終了することを確認。
    - 次フェーズ（`test-phase-next` 等）の Draft が Archive に移動する新しい PR が自動作成されていることを確認。

### 3.3. 構成変更・削除 (Configuration / Cleanup)
- [ ] **クリーンアップ**: 検証で作成されたブランチ、Issue、PR、ファイルを全て削除。

## 4. ブランチ戦略 (Branching Strategy)
- **Pattern**: Feature (Integration Test)
- **Base Branch**: `feature/phase-3-foundation`
- **Head Branch**: `feature/task-T3-5-verify`

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **観測される挙動**: 自動作成された PR のタイトルが `feat: promote ...` 形式であること。
- [ ] **観測される挙動**: 自動作成された PR の Files changed が、期待通りの「移動 (git mv)」であること。

## 6. 成果物 (Deliverables)
- 検証ログ（PR コメントに記載）
