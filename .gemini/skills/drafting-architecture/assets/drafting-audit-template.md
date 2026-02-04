# Architecture Drafting Self-Audit Report

## 1. Overview
- **Target File:** [File Name]
- **Related Issue:** [Issue Link]

## 2. Audit Checklist
各項目について、[ ] にチェックを入れ、**「根拠/エビデンス」**（図の該当箇所や記述内容）を具体的に記述してください。

### 2.1. Structural Accuracy (構造の正確性)
- [ ] **Dependency Direction:** 依存の矢印は正しい方向（依存する側 -> される側）に向いているか？（Clean Architecture原則）
  - **根拠:** 
- [ ] **Boundary Definition:** システム境界やコンポーネントの責務範囲は明確に可視化されているか？
  - **根拠:** 
- [ ] **Consistency:** 定義されたコンポーネント名は、共通定義書（Plan）と一致しているか？
  - **根拠:** 

### 2.2. Quality & Policy (品質方針)
- [ ] **Quality Attributes:** データ整合性、エラー処理、非同期境界などの品質特性が図上に表現されているか？
  - **根拠:** 
- [ ] **Notes & Alerts:** 重要な制約事項や注意点は `Note` として記載されているか？
  - **根拠:** 

### 2.3. Visual Readability (視覚的可読性)
- [ ] **Cognitive Load:** 矢印の交差は最小限か？ ひとつの図に要素を詰め込みすぎていないか？
  - **根拠:** 
- [ ] **Flow Direction:** 配置（TB/LR）は情報の流れに沿っており、自然に読めるか？
  - **根拠:** 

## 3. Improvement Proposals (改善提案)
<!-- 
必須ではないが、可読性や保守性をさらに高めるための提案があれば記述する。
-->
- **Proposal 1:** ...
- **Benefit:** ...

## 4. Final Verdict
- [ ] **PASS:** Ready to push.
- [ ] **FAIL:** Needs correction.
