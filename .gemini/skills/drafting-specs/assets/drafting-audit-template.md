# Specification Drafting Self-Audit Report

## 1. Overview
- **Target File:** [File Name]
- **Related Issue:** [Issue Link]

## 2. Audit Checklist
各項目について、[ ] にチェックを入れ、**「根拠/エビデンス」**を記述してください。

### 2.1. TDD Readiness (TDD適合性)
- [ ] **Concrete Inputs/Outputs:** 入力パラメータと期待される戻り値（型、フォーマット）が具体的に定義されているか？
  - **根拠:** 
- [ ] **Validation Rules:** すべての入力項目に対して、具体的なバリデーションルール（必須、Max長、文字種）が書かれているか？
  - **根拠:** 
- [ ] **Test Cases (Edge Cases):** Null、空文字、境界値、異常系などのエッジケースが「Edge Cases」セクションに網羅されているか？
  - **根拠:** 

### 2.2. SSOT Integrity
- [ ] **Common Defs Compliance:** 用語、エラーコード、データ型は `Common Definitions` に準拠しているか？
  - **根拠:** 
- [ ] **Design Alignment:** 上位のDesign Docの意図を正しく反映しているか？
  - **根拠:** 

### 2.3. No Ambiguity
- [ ] **Forbidden Terms:** "TBD", "Pending", "Any" などの曖昧な表現が含まれていないか？
  - **根拠:** 

## 3. Improvement Proposals (改善提案)
- **Proposal 1:** ...

## 4. Final Verdict
- [ ] **PASS**
- [ ] **FAIL**
