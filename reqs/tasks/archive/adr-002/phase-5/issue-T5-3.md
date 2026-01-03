---
title: "docs(arch): 検証基準（テストケース）をモック活用型テストに刷新"
status: "Open"
roadmap: "reqs/roadmap/active/roadmap-adr002-document-approval-flow.md"
task_id: "T5-3"
labels: ["documentation", "ADR-002"]
---

## 状況 / Context
`docs/specs/test-criteria-spec.md` が関数単位の単純な入出力テストのみを記述している。Phase 4 で到達した「Infrastructure を Mock 化した Usecase のロジック検証」という高度なテスタビリティを仕様として残す必要がある。

## 期待される成果物 / Deliverables
- `docs/specs/test-criteria-spec.md` の更新
    - **Usecase テスト**: Mock を用いた `ApprovalUseCase`, `WorkflowUseCase` の検証シナリオの定義。
    - **Infrastructure テスト**: 実際のファイル I/O を伴う `FileSystemAdapter` の検証基準。
    - **カバレッジ基準**: 100% 維持という品質基準の明文化。

## 検証基準 / Verification Criteria
- 定義されたシナリオが、`tests/unit/` の `test_approval.py` や `test_workflow.py` で実際に検証されていること。