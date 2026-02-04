# 🛡 SSOT Audit Report

## 1. 監査概要 (Audit Overview)
- **Target (対象):** <!-- 監査対象のファイルや提案 -->
- **SSOT References (参照した正解):** <!-- 比較対象としたADRやContext -->
- **Date:** <!-- YYYY-MM-DD -->
- **Auditor:** SSOT Integrity Guardian

## 2. 判定結果 (Verdict)
<!-- いずれかを選択 -->
- [ ] **✅ PASS** (承認 - 整合性に問題なし)
- [ ] **⚠️ CONDITIONAL PASS** (条件付き承認 - 軽微な修正で対応可能)
- [ ] **❌ FAIL** (却下 - 重大な不整合あり)

---

## 3. 監査チェックリスト (Audit Checklist)

### A. Strategic Alignment (戦略的整合性)
*過去のADRや設計原則との適合性*
- [ ] **ADR Compliance:** 既定の技術選定やパターンに違反していないか？
- [ ] **Trade-off:** 過去に受容したトレードオフ（パフォーマンス vs 保守性など）を覆していないか？

### B. Conceptual Integrity (概念的整合性)
*用語と境界の一貫性*
- [ ] **Ubiquitous Language:** コード/ドキュメントの用語はSSOTと一致しているか？
- [ ] **Boundary:** コンポーネントの責任範囲（境界）を侵犯していないか？

### C. Operational Integrity (行動規範)
*アーキテクトとしての振る舞い*
- [ ] **No Direct Impl:** 直接実装せず、タスク（Issue）に落とし込んでいるか？
- [ ] **No Silent Change:** 合意なしにドキュメントや仕様を変更していないか？

### D. Logical Consistency (論理的一貫性)
*構造的な正しさ*
- [ ] **Dependency:** 循環参照やレイヤー違反はないか？
- [ ] **Completeness:** 要件に対する過不足はないか？

---

## 4. 論理的根拠 (Reasoning)
<!-- 判定に至った理由を、上記のチェックリスト項目を参照しながら記述 -->

## 5. 検出された乖離と是正措置 (Discrepancies & Actions)
<!-- NGまたはConditional Passの場合のみ記述 -->

| 区分 | 乖離内容 (Discrepancy) | 影響 (Impact) | 是正措置 (Action) |
| :--- | :--- | :--- | :--- |
| <!-- Strategic / Conceptual etc --> | <!-- 具体的な内容 --> | <!-- リスク --> | <!-- Issue作成、修正依頼など --> |
