# Goal Definition: Specification Fixes for PR #285

## 1. 概要 (Context)
PR #285 における `document_model.md` のレビュー指摘に基づき、仕様の不整合とタイポを修正する。これにより、ADR-007 および `definitions.md` との完全な同期を実現する。

## 2. SMART目標 (Outcome)
- [ ] `docs/specs/data/document_model.md` において、`parent_issue` フィールドが追加され、`labels` のタイポが修正され、`phase` の値が `infrastructure` に統一され、`issue_id` の型が `int` に統一されていること。
- [ ] `docs/specs/plans/adr-007-metadata-driven-lifecycle/definitions.md` において、`phase` の値が `infrastructure` に統一されていること。
- [ ] 自己監査レポート（`drafting-audit-template.md` 準拠）が作成され、すべてのチェックをパスしていること。

## 3. 検証方法 (DoD - Definition of Done)

### 3.1. 内容の検証
- `grep "parent_issue" docs/specs/data/document_model.md` で追加を確認。
- `grep "infrastructure" docs/specs/data/document_model.md` で統一を確認。
- `grep "infrastructure" docs/specs/plans/adr-007-metadata-driven-lifecycle/definitions.md` で統一を確認。
- `grep "Issue ラベルのリスト。" docs/specs/data/document_model.md` でタイポ修正を確認。

### 3.2. 整合性検証
- `auditing-ssot` を用いて、ADR-007 との整合性を最終確認する。

## 4. 制約・前提条件 (Constraints/Assumptions)
- ADR-007 を最上位の正（SSOT）とする。
- すでに `spec/task-007-T3-01-model` ブランチで作業中である。

---
Created by TECHNICAL_DESIGNER.
