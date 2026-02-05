# Integration Issue Draft: Spec Update for ADR-007

## Overview
ADR-007「Metadata-driven Lifecycle」の実装に向けた詳細仕様書の更新を行う。
本Issueは Spec フェーズの統合管理を行い、全ての仕様変更が整合性を持って完了することを保証する。

## Scope
- `docs/specs/data/document_model.md`
- `docs/specs/logic/*.md`
- `docs/specs/api/cli_commands.md`

## Tasks (L3 Issues)
- [ ] `007-T3-01`: Update Document Model Specification (Schema & Status)
- [ ] `007-T3-02`: Update Lifecycle Logic Specifications (DAG & Atomic Move)
- [ ] `007-T3-03`: Update CLI Interface Specification (Paths & Arguments)

## Definition of Done (Spec Phase)
- 全ての仕様書変更が `feature/spec-update-adr007` ブランチにマージされていること。
- `auditing-specs` による監査レポートが作成され、承認されていること。
- 実装者（Implementer）への申し送り事項 (`spec-to-tdd.md`) が作成されていること。
