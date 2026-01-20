---
title: "[Spec] Define Approval UseCase"
labels:
  - "task"
  - "P1"
  - "TECHNICAL_DESIGNER"
roadmap: "reqs/roadmap/archive/roadmap-adr002-document-approval-flow.md"
task_id: "SPEC-03"
depends_on: ["spec-01-domain.md", "spec-02-infra.md"]
status: "Draft"
---
# [Spec] Define Approval UseCase

## 親Issue / ロードマップ (Context)
- **Roadmap**: reqs/roadmap/archive/roadmap-adr002-document-approval-flow.md
- **Task ID**: SPEC-03
- **Common Definitions**: docs/specs/plans/20260120-approval-flow.md

## 1. 目的と背景 (Goal & Context)
- **As-is (現状)**: 承認フローの手順（移動→起票→更新）がアーキテクチャ図にしか存在しない。
- **To-be (あるべき姿)**: `ApprovalUseCase` の実行フロー、エラーハンドリング、ロールバック方針が詳細仕様書として定義される。
- **Design Evidence**: `docs/architecture/arch-behavior-approval-flow.md` (Sequence)

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `docs/specs/plans/20260120-approval-flow.md`
- [ ] `docs/architecture/arch-behavior-approval-flow.md`

## 3. 実装手順と制約 (Implementation Steps & Constraints)

### 3.1. 負の制約 (Negative Constraints)
- [ ] **複雑性排除**: ロールバックロジックは複雑にしすぎず、ADR-002の範囲内（ファイル移動の取り消し程度）に留める。

### 3.2. 実装手順 (Changes)
- [ ] **ファイル**: `docs/specs/logic/approval_usecase.md`
    - **処理内容**:
      - `ApprovalUseCase.process_single_file()` および `ApprovalUseCase.process_all_files()` のフロー定義（オーケストレーションは `WorkflowUseCase.run()`）。
      - 異常系フロー（Issue起票失敗時の補償トランザクション）の定義。
    - **Verify (TDD Criteria)**:
      - 「Issue起票に失敗した場合、移動したファイルを元のInboxに戻し、先行して更新したメタデータも元に戻すこと」
      - 「全ての処理が成功した場合のみ、GitAdapter.commit() を呼ぶこと」

## 4. ブランチ戦略 (Branching Strategy)
- **ベースブランチ (Base Branch)**: `feature/spec-update-approval-flow`
- **作業ブランチ (Feature Branch)**: `feature/spec-03-usecase`

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **レビュー**: `docs/specs/logic/approval_usecase.md` が作成されていること。
- [ ] **整合性**: アーキテクチャ図のシーケンスと完全に一致していること。

## 6. 成果物 (Deliverables)
- `docs/specs/logic/approval_usecase.md`