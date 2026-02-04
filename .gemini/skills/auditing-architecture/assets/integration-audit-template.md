# Architecture Integration Verification Report

## 1. Overview
- **Feature Name:** [Feature Name]
- **Target Branch:** [Integration Branch Name]
- **Common Definition Doc:** [Link to Plan Doc]

## 2. Verification Checklist
各項目について、[ ] にチェックを入れ、**「根拠/エビデンス」**（参照したファイル、行番号、図の箇所など）を具体的に記述してください。

### 2.1. Goal Achievement (目標達成度)
- [ ] **Design Brief Fulfillment:** Design Briefで設定された設計目標やスコープは、成果物によって満たされているか？
  - **根拠:** 
- [ ] **Completeness:** 共通定義（Common Definitions）に含まれる全てのコンポーネント・図面が実装されているか？
  - **根拠:** 

### 2.2. SSOT Alignment (SSOT整合性)
- [ ] **ADR Compliance:** 実装されたアーキテクチャは、ソースADRの決定事項（制約、パターン）に準拠しているか？
  - **根拠:** 
- [ ] **Context Consistency:** System Context (L1) との詳細図 (L2/L3) の間に矛盾はないか？
  - **根拠:** 
- [ ] **Ubiquitous Language:** コンポーネント名や用語は、共通定義書およびADRと完全に一致しているか？
  - **根拠:** 

### 2.3. Quality & Readability (品質と可読性)
- [ ] **Quality Policy:** 定義された品質方針（整合性、エラー処理、可観測性）は図面に反映されているか？
  - **根拠:** 
- [ ] **Clean Architecture:** 依存の方向（矢印）はClean Architectureの原則（内側への依存）を守っているか？
  - **根拠:** 
- [ ] **Readability:** 図面は Spec Strategist が仕様を策定するために十分な情報量と可読性を持っているか？
  - **根拠:** 

## 3. Improvement Proposals (改善提案)
<!-- 
必須の修正事項ではないが、将来的な品質向上や保守性のために推奨される改善案があれば記述する。
-->
- **Proposal 1:** ...
- **Benefit:** ...

## 4. Outstanding Issues (残存課題)
<!-- 
監査で見つかった、修正が必要な課題があれば記述する。
-->
- **Issue 1:** ...
- **Remediation:** (Create a new issue or fix in place if trivial)

## 5. Final Verdict
- [ ] **READY TO MERGE:** All checks passed. Ready for Spec Creation.
- [ ] **NEEDS REVISION:** Additional tasks required.
