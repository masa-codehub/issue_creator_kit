---
title: "[Audit] Integration & TDD Audit for ADR-003 Implementation"
labels: ["gemini:tdd", "gemini:audit"]
roadmap: "docs/implementation/plans/adr-003/tdd-plan.md"
task_id: "T-Integration"
depends_on: ["issue-T-7.md"]
status: "Draft"
---

## 1. Goal & Context (Why & What)

### Goal
- 実装された全てのコード（Domain, Infra, UseCase, CLI）を統合し、ADR-003 の要件（仮想キュー、Fail-fast、Roadmap Sync）が完全に動作することを保証する。

### As-is (現状)
- 個別のタスクは完了しているが、全体としての結合テストが未実施。

### To-be (あるべき姿)
- 全テストがパスし、カバレッジ目標を達成している。
- `feature/impl-adr003` ブランチが `main` にマージ可能な品質になっている。

### Design Evidence
- [TDD Plan](../../../../docs/implementation/plans/adr-003/tdd-plan.md)

## 2. Input Context (資料 & 情報)
- **Source Code**: `src/`
- **Tests**: `tests/`

## 3. Implementation Steps & Constraints (How)

### 3.1. Negative Constraints (してはいけないこと)
- このタスクで新たな機能追加を行うこと（バグ修正のみ許可）。
- テストが失敗している状態で PR をマージすること。

### 3.2. Implementation Steps (実行手順)
1.  **Full Test**:
    - `pytest` を実行し、全件パスすることを確認。
    - `pytest --cov=src` でカバレッジを確認。
2.  **Lint & Type Check**:
    - `ruff check .`, `ruff format .`, `mypy .` を実行し、静的解析をパスさせる。
3.  **SSOT Check**:
    - `ssot-verification` を実行し、実装が詳細仕様書 (`docs/specs/`) と乖離していないか最終確認。
4.  **Handover Creation**:
    - 次のステップ（本番運用）に向けた `docs/handovers/tdd-to-ops.md` を作成。
5.  **Final PR**:
    - `main` への PR を作成。

### 3.3. Configuration Changes
- なし

## 4. Branching Strategy
- **Base Branch**: `main`
- **Feature Branch**: `feature/impl-adr003`

## 5. Verification & DoD (完了条件)
- [ ] 全テスト Green。
- [ ] Lint/Type Check Green。
- [ ] SSOT 整合性確認済み。
- [ ] `main` への PR が作成されている。
