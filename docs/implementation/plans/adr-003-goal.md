# SMART Goal Definition: ADR-003 Implementation Plan

## 1. Goal Statement
**Outcome (達成すべき状態):**
ADR-003（仮想キューと自己推進型ワークフロー）の要件を完全に満たす実装計画（`tdd-plan.md`）と、実行可能なIssue案（`drafts/`）が作成され、チーム（ユーザー）の承認を得ている状態。

**Specific (具体的成果物):**
1.  **TDD Plan (`docs/implementation/plans/adr-003/tdd-plan.md`)**:
    - 実装の順序、テスト戦略（モック、フィクスチャ）、共通の実装方針を定義。
2.  **Draft Issues (`reqs/tasks/drafts/adr-003/impl/*.md`)**:
    - 各モジュール（Domain, Infra, UseCase, CLI）ごとに分割された実装タスク。
    - 各タスクには具体的な検証条件（TDD Criteria）が含まれる。
3.  **Pull Request**:
    - 上記計画を `main` へマージするための承認依頼。

**Relevant (関連性):**
- 詳細仕様書（`docs/specs/`）の定義を、具体的なコードとテストに変換するための設計図となる。
- 実装者が迷わずに作業を開始できる状態（Ready for Dev）を作る。

## 2. Verification Criteria (DoD)

### Measurable Metrics
- [ ] **File Existence**:
    - `docs/implementation/plans/adr-003/tdd-plan.md` が存在すること。
    - `reqs/tasks/drafts/adr-003/impl/` 配下に複数の Issue 案が存在すること。
- [ ] **Content Integrity**:
    - `tdd-plan.md` にテスト戦略（Mock, Fixture）が明記されていること。
    - 全ての Issue 案の `roadmap` フィールドが `tdd-plan.md` を指していること。
- [ ] **Approval**:
    - 作成された PR が Open 状態であること。

### Verification Command
```bash
ls -l docs/implementation/plans/adr-003/tdd-plan.md
ls -l reqs/tasks/drafts/adr-003/impl/*.md
gh pr list --head feature/impl-adr003-plan
```
