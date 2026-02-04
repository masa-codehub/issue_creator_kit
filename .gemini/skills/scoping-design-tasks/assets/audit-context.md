# Audit Checklist for System Context (Design Brief)

## 1. Value Proposition (価値提案)
- [ ] **Business Value:** システムが提供する「誰にとっての」「どんな価値」かが具体的に定義されているか。
- [ ] **Metrics:** 成功を測る指標（KPI/KGI）や削減コスト等の数値目標が含まれているか（可能な場合）。

## 2. Boundaries & Scope (境界とスコープ)
- [ ] **System Boundary:** 自システム（System）と外部システム（External System）の境界線が明確か。
- [ ] **Responsibility:** 「やること（In-Scope）」と「やらないこと（Out-of-Scope）」が明記されているか。
- [ ] **External Dependencies:** 連携する外部システムやAPIが具体的に特定されているか。

## 3. Ubiquitous Language (ユビキタス言語)
- [ ] **Key Terms:** ビジネス上の主要な概念（名詞）が定義されているか。
- [ ] **Consistency:** コード内の用語や既存ドキュメントとの整合性が考慮されているか。

## 4. Strategic Decisions (戦略的決定)
- [ ] **Trade-offs:** 「正確性 vs 速度」などの重要なトレードオフに関する方針が含まれているか。
- [ ] **Risks:** 既知のリスクや制約事項（技術的・組織的）が挙げられているか。

## 5. Feasibility (実現可能性)
- [ ] **Diagram Readiness:** 後続のDraftingフェーズで、迷わず Context Diagram (Mermaid) を描けるだけの情報が揃っているか。
