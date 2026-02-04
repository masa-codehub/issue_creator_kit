# Specification Planning Self-Audit Report

## 1. Plan Overview
- **Source Design Doc:** [Link]
- **Common Definition Doc:** [Link]

## 2. Audit Checklist
各項目について、[ ] にチェックを入れ、**「根拠/エビデンス」**を具体的に記述してください。

### 2.1. Clarity & Standards (明確性と標準化)
- [ ] **Ubiquitous Language:** 曖昧な用語を排除し、実装でそのまま使える用語が定義されているか？
  - **根拠:** 
- [ ] **Type Constraints:** 文字列や数値の型定義に、具体的な制約（最大長、範囲、Regex）が含まれているか？
  - **根拠:** 
- [ ] **Error Policy:** 実装者が統一的に扱えるエラーコード体系が定義されているか？
  - **根拠:** 

### 2.2. Coverage & SSOT Alignment
- [ ] **Design Doc Fulfillment:** ソースとなるDesign Docの要件を全てカバーしているか？
  - **根拠:** 
- [ ] **Arch Plan Alignment:** アーキテクチャ計画（`docs/architecture/plans/`）で定義された物理構造と矛盾していないか？
  - **根拠:** 

### 2.3. Task Strategy
- [ ] **TDD Criteria:** 各Issue案に、実装者がTDDを行うための「検証条件（Happy/Error/Boundary）」を記述するよう指示があるか？
  - **根拠:** 
- [ ] **Integration Issue:** 全タスクを束ねる統合Issueが定義され、最終監査の手順が含まれているか？
  - **根拠:** 

## 3. Improvement Proposals (改善提案)
<!-- 必須ではないが、より良くするためのアイデア -->
- **提案 1:** ...

## 4. Final Verdict
- [ ] **PASS**
- [ ] **FAIL**
