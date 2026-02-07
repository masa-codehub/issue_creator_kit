# 能動的偵察レポート (Reconnaissance Report)

## 1. 調査対象と意図 (Scope & Context)
- **ユーザー依頼のキーワード:** `ADR-008`, `Cleanup Legacy Automation Code`, `WorkflowUseCase`, `ApprovalUseCase`, `auto-approve-docs.yml`
- **調査の目的:** ADR-008で廃止が決定したレガシーな自動化コードの現状と、その影響範囲（依存関係）を特定し、物理削除および参照の整理（CLI等）に向けた事実情報を収集する。
- **調査時のブランチ (Branch Context):** `main`

## 2. 収集された事実 (Evidence)

### A. ドキュメント上の規定 (SSOT)
- **[Source]:** `docs/specs/plans/adr-008-automation-cleanup/definitions.md`
  - **事実・規定:** "2.4. Cleanup Targets (Legacy Code)" として以下の3ファイルが明記されている。
  - **引用:**
    > - `src/issue_creator_kit/usecase/workflow.py`
    > - `src/issue_creator_kit/usecase/approval.py`
    > - `.github/workflows/auto-approve-docs.yml`

### B. 実装の現状 (Codebase Reality)
- **[File]:** `.github/workflows/auto-approve-docs.yml` (存在確認)
- **[File]:** `src/issue_creator_kit/usecase/approval.py` (存在確認, `ApprovalUseCase`)
- **[File]:** `src/issue_creator_kit/usecase/workflow.py` (存在確認, `WorkflowUseCase`)

### C. 物理構造と依存関係 (Structure & Dependencies)
- **[File]:** `src/issue_creator_kit/cli.py`
  - **インポート:** `ApprovalUseCase` (L13), `WorkflowUseCase` (L16)
  - **初期化:** L70-72, L99, L134-136, L164, L180
  - **コマンド定義:** `process-merge`, `approve`, `approve-all`
- **[File]:** `src/issue_creator_kit/usecase/creation.py`
  - **インポート:** `WorkflowUseCase` (L13)
  - **使用:** `workflow_usecase: WorkflowUseCase | None = None` (L27)
- **[Test Files] (関連テスト):**
  - `tests/unit/usecase/test_workflow.py` (WorkflowUseCaseのテスト)
  - `tests/unit/usecase/test_approval.py` (ApprovalUseCaseのテスト)
  - `tests/unit/test_cli.py` (CLIの各コマンドでのモック使用)

## 3. 発見された制約と矛盾 (Constraints & Contradictions)
- **制約事項:** 
    - `cli.py` だけでなく `usecase/creation.py` にも `WorkflowUseCase` への参照が存在する。
    - 単体テスト（`tests/unit/` 配下）に削除対象のユースケースを直接テストするもの、およびCLIテストでモックとして使用しているものが複数存在する。
- **SSOTとの乖離:** `definitions.md` には主要な3ファイルのみがリストアップされているが、実際には付随するテストファイルや他ユースケースからの参照も整理が必要。

## 4. 補足・未調査事項 (Notes & Unknowns)
- `tests/integration/test_issue_creation_flow.py` 等の統合テストにおいて、これらのレガシーコードに依存した挙動がないか。
