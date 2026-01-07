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
- **Depends on**: issue-T3-1.md

## 1. 目的と背景 (Goal & Context)
- **As-is (現状)**: 以前の実装は「Issue起票時」に Auto-PR を作成していたため、タスク開始時に次フェーズへ進んでしまうバグがあった。
- **To-be (あるべき姿)**: ユーザー提示の「8ステップ・ライフサイクル」を論理ロジックとして詳細化した仕様書が作成されている。
- **Design Evidence (設計の根拠)**: ADR-003 第 3.3 項 (ステップ 5-6 の詳細化)

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `reqs/design/_approved/adr-003-task-and-roadmap-lifecycle.md`
- [ ] `docs/system-context.md`

## 3. 実装手順と制約 (Implementation Steps & Constraints)

### 3.1. 負の制約 (Negative Constraints)
- [ ] **責務混同禁止**: `process-diff` (Added検知) コマンドの中に「完了検知」ロジックを混ぜないこと。
- [ ] **妄想禁止**: ADR-003 の 8 ステップ（特にステップ 5 と 6 の境界）を勝手に解釈せず、忠実に設計すること。

### 3.2. 実装手順 (Changes)
- [ ] **詳細設計**: `docs/specs/auto-pr-logic.md` を新規作成。
    - **トリガー定義**: GitHub `pull_request` イベント (closed) かつ `merged == true` であることの厳密な定義。
    - **Issue特定アルゴリズム**: マージされた PR の Body から `Closes #XXX` を抽出し、`archive/` 内の該当ファイルを特定する手順。
    - **完了判定**: 特定したファイルの `next_phase_path` の有無による連鎖判定。
    - **ブランチ・PR作成**: 移動先パスの算出ロジック。
- [ ] **ドキュメントレビュー**: 内容の正確性をセルフレビューし、不整合を修正。

### 3.3. 構成変更・削除 (Configuration / Cleanup)
- なし

## 4. ブランチ戦略 (Branching Strategy)
- **Pattern**: Feature (Implementation - Document)
- **Base Branch**: `feature/phase-3-foundation`
- **Head Branch**: `feature/task-T3-2-redesign`

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **観測される挙動**: `docs/specs/auto-pr-logic.md` が作成され、マージされていること。
- [ ] **整合性**: 設計内容が ADR-003 のストーリーと 100% 合致していること。

## 6. 成果物 (Deliverables)
- `docs/specs/auto-pr-logic.md`
