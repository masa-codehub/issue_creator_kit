---
title: "docs(arch): システムコンテキストの用語と境界定義を最新化"
status: "Open"
roadmap: "reqs/roadmap/active/roadmap-adr002-document-approval-flow.md"
task_id: "T5-0"
labels: ["documentation", "SSOT"]
---

## 状況 / Context
`docs/system-context.md` はシステムの最上位ドキュメント（SSOT）であるが、最終更新が 2025-12-27 となっており、Phase 4 で導入されたアーキテクチャ刷新が反映されていない。

## 期待される成果物 / Deliverables
- `docs/system-context.md` の更新
    - **用語の統一**: 「自動化スクリプト」という表現を排除し、「Usecase」「Infrastructure Adapter」に置換。
    - **境界定義の精緻化**: Clean Architecture Lite に基づく層別の責務を明記。
    - **Status 更新**: 「承認済み」とし、Last Updated を最新化。

## 検証基準 / Verification Criteria
- ドキュメント内の用語が、他の詳細設計書およびソースコードの構造と矛盾なく一致していること。
