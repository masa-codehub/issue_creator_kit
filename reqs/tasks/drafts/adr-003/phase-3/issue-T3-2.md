---
title: "Auto-PR ロジックの詳細設計 (Re-Design)"
labels:
  - "task"
  - "P1"
  - "SYSTEM_ARCHITECT"
roadmap: "reqs/roadmap/active/roadmap-adr003-task-lifecycle.md"
task_id: "T3-2"
depends_on: ["issue-T3-1.md"]
next_phase_path: ""
status: "Draft"
---
# Auto-PR ロジックの詳細設計 (Re-Design)

## 親Issue / ロードマップ (Context)
- **Roadmap**: reqs/roadmap/active/roadmap-adr003-task-lifecycle.md
- **Task ID**: T3-2

## 1. 目的と背景 (Goal & Context)
- **As-is (現状)**: 以前の実装は「Issue起票時」に Auto-PR を作成していたため、タスク開始時に次フェーズへ進んでしまうバグがあった。
- **To-be (あるべき姿)**: 「最終 Issue 完了時（PRマージ時）」にのみ Auto-PR を作成する正しいロジックが設計されている。
- **Design Evidence (設計の根拠)**: ADR-003 (8-step lifecycle)

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `reqs/design/_approved/adr-003-task-and-roadmap-lifecycle.md`

## 3. 実装手順と制約 (Implementation Steps & Constraints)

### 3.1. 負の制約 (Negative Constraints)
- [ ] **制約**: `process-diff` コマンドにロジックを混在させないこと（責務分離）。

### 3.2. 実装手順 (Changes)
- [ ] **設計**: `docs/specs/auto-pr-logic.md` を作成。
    - トリガー: `pull_request` (closed & merged == true)
    - ロジック: マージされたPRから関連Issueを特定 -> Issueのメタデータ(next_phase_path)を取得 -> Auto-PR作成。
- [ ] **承認**: レビューとマージ。

### 3.3. 構成変更・削除 (Configuration / Cleanup)
- なし

## 4. ブランチ戦略 (Branching Strategy)
- **ベースブランチ (Base Branch)**: `feature/phase-3-foundation`
- **作業ブランチ (Feature Branch)**: `feature/task-T3-2-redesign`

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **観測される挙動**: 設計ドキュメントが承認（マージ）されること。

## 6. 成果物 (Deliverables)
- `docs/specs/auto-pr-logic.md`
