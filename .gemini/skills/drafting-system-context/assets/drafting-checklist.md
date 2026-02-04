# Context Drafting & Audit Checklist

## 1. Content Verification (テキスト記述の監査)
- [ ] **Customer Value:** 「誰が」「何のために」「どんな価値を得るか」が具体的に記述されているか。
  - **根拠:** <!-- system-context.md の Section 1 の引用 -->
- [ ] **Boundaries:** システムの責任範囲（やること/やらないこと）が明確に定義されているか。
  - **根拠:** <!-- Section 3 の記述引用 -->
- [ ] **Ubiquitous Language:** 主要な用語の定義がなされ、一貫して使用されているか。
  - **根拠:** <!-- Section 2 の用語定義引用 -->

## 2. Visual Verification (作図の監査)
- [ ] **C4 Level 1 Compatibility:** Mermaid図が C4 Context Diagram (Level 1) の形式に従っているか。
  - **根拠:** <!-- Mermaid コードの確認結果 -->
- [ ] **Element Consistency:** 図内の `System`, `Person`, `System_Ext` が本文の記述と一致しているか。
  - **根拠:** <!-- テキストと図の突合結果 -->
- [ ] **Relationship Accuracy:** 矢印の向き（依存方向）とラベル（アクション）がビジネスロジックと一致しているか。
  - **根拠:** <!-- ビジネスロジックとの整合性確認 -->

## 3. Reality & SSOT Alignment (整合性監査)
- [ ] **Fact Alignment:** `scouting-facts` で得られた実装の事実（API, DB, 外部連携）と矛盾していないか。
  - **根拠:** <!-- 実装コードや設定ファイルとの突合結果 -->
- [ ] **Design Brief Alignment:** `scoping-design-tasks` で合意された設計指針（Design Brief）を完全に満たしているか。
  - **根拠:** <!-- Design Brief の要件との比較結果 -->
- [ ] **No Ambiguity:** "TBD", "よしなに", "適宜" といった曖昧な表現が排除されているか。
  - **根拠:** <!-- ドキュメント内の検索結果 -->