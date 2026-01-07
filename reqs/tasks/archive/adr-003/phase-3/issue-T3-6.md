---
title: "Phase 3 完了監査と次フェーズへのプロモーション"
labels:
  - "task"
  - "P1"
  - "SYSTEM_ARCHITECT"
roadmap: "reqs/roadmap/active/roadmap-adr003-task-lifecycle.md"
task_id: "T3-6"
depends_on: ["issue-T3-5.md"]
next_phase_path: "reqs/tasks/drafts/adr-003/phase-4/"
status: "Draft"
issue: "#159"
---
# Phase 3 完了監査と次フェーズへのプロモーション

## 親Issue / ロードマップ (Context)
- **Roadmap**: reqs/roadmap/active/roadmap-adr003-task-lifecycle.md
- **Task ID**: T3-6
- **Depends on**: issue-T3-5.md

## 1. 目的と背景 (Goal & Context)
- **As-is (現状)**: Phase 3 (Logic Repair) の実装と検証が完了した。
- **To-be (あるべき姿)**: ロジックの修正が ADR-003 (8-step) の意図を完全に満たし、高品質な状態で `main` に統合される。
- **Design Evidence (設計の根拠)**: SYSTEM_ARCHITECT Phase Completion Audit Protocol

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `docs/specs/auto-pr-logic.md`
- [ ] `docs/system-context.md`
- [ ] `reqs/roadmap/active/roadmap-adr003-task-lifecycle.md`

## 3. 実装手順と制約 (Implementation Steps & Constraints)

### 3.1. 負の制約 (Negative Constraints)
- [ ] **マージ禁止**: エージェント自身が `main` へのマージを行ってはならない。
- [ ] **Gate Check**: 以下の監査項目に一つでも不備がある場合は、DoD 達成とみなさない。

### 3.2. 実装手順 (Changes)
- [ ] **フェーズ完了監査 (Audit)**:
    - **SSOT整合性**: 実装コード (`WorkflowUseCase`, CLI) が `docs/specs/auto-pr-logic.md` および ADR-003 (8-step) と乖離していないか。
    - **無駄の排除**: 以前の暴発バグに関連する古いコード（`creation.py` 内の不要ロジック等）が完全に削除されているか。
    - **コンテキスト整合性**: システムコンテキストで再定義された `Archive` の意味と実装が矛盾していないか。
    - **テスト網羅性**: 正常系（PRマージ）、異常系（Issue特定失敗）、境界系（循環参照）のテストが全てパスしているか。
- [ ] **監査レポート作成**: PR プロトコルに従い、詳細な監査結果を Body に記載して `main` への PR を提出する。

### 3.3. 構成変更・削除 (Configuration / Cleanup)
- なし

## 4. ブランチ戦略 (Branching Strategy)
- **Pattern**: Audit (Review & Promote)
- **Base Branch**: `feature/phase-3-foundation`
- **Target Branch**: `main`

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **観測される挙動**: 監査レポート付きの PR が作成されていること。
- [ ] **観測される挙動**: CI が `feature/phase-3-foundation` 上で完遂していること。

## 6. 成果物 (Deliverables)
- 監査レポート付きの Pull Request
