---
title: "[Arch] Visualize Document Lifecycle (State Diagram) for ADR-002"
labels:
  - "architecture"
  - "P1"
  - "TECHNICAL_DESIGNER"
roadmap: "reqs/roadmap/active/roadmap-phase-4-refactoring.md"
task_id: "ARCH-002-3"
depends_on: ["arch-002-behavior.md"]
next_phase_path: ""
status: "Draft"
---
# [Arch] Visualize Document Lifecycle (State Diagram) for ADR-002

## 親Issue / ロードマップ (Context)
- **Roadmap**: reqs/roadmap/active/roadmap-phase-4-refactoring.md
- **Task ID**: ARCH-002-3

## 1. 目的と背景 (Goal & Context)
- **As-is (現状)**: ドキュメントのステータス（Draft/Approved）と物理配置（Inbox/Approved）の関係がテキストでしか定義されておらず、遷移ルールが不明瞭。
- **To-be (あるべき姿)**: ドキュメントのライフサイクルが状態遷移図として定義され、実装者がステータス管理ロジックを実装できる状態。
- **Design Evidence (設計の根拠)**: 
    - `reqs/design/_archive/adr-002-document-approval-flow.md`
    - `docs/architecture/plans/20260118-doc-approval-plan.md`

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `reqs/design/_archive/adr-002-document-approval-flow.md`
- [ ] `docs/architecture/plans/20260118-doc-approval-plan.md`
- [ ] `docs/template/arch-state.md`

## 3. 実装手順と制約 (Implementation Steps & Constraints)

### 3.1. 負の制約 (Negative Constraints)
- [ ] **変更禁止**: 実装コードの変更。

### 3.2. 実装手順 (Changes)
- [ ] **ファイル**: `docs/architecture/arch-state-doc-lifecycle.md`
    - **処理内容**: 
        1. テンプレート `docs/template/arch-state.md` を適用する。
        2. ドキュメントの状態（Draft in Inbox, Approved in Approved Folder）を定義する。
        3. 遷移トリガー（Merge to Main）と副作用（Issue Update）を記述する。
        4. `arch-refactoring` を呼び出して品質を向上させる。

### 3.3. 構成変更・削除 (Configuration / Cleanup)
- なし

## 4. ブランチ戦略 (Branching Strategy)
- **ベースブランチ (Base Branch)**: `feature/arch-adr-002`
- **作業ブランチ (Feature Branch)**: `feature/task-ARCH-002-3-lifecycle`

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **SSOT整合性**: `ssot-verification` を実行し、遷移ルールがADRの定義と矛盾していないこと。
- [ ] **ターゲット読者**: Spec Strategist がこの図を見て、ステータスバリデーション仕様を計画できること。

## 6. 成果物 (Deliverables)
- `docs/architecture/arch-state-doc-lifecycle.md`