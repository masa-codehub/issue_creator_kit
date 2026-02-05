---
id: 007-T3-L2
parent: adr-007
type: integration
phase: spec
status: Issued
issue_id: 279
depends_on:
  - "007-T3-01"
  - "007-T3-02"
  - "007-T3-03"
  - "007-T3-04"
issue_id: 279 # NOTE: Exceptionally manual entry for retroactive linking
date: 2026-02-05
title: "[L2] ADR-007 Specification Phase Integration"
labels:
  - "gemini:spec"
  - "P1" # Priority: P0 (Critical), P1 (High), P2 (Medium), P3 (Low)
  - "SYSTEM_ARCHITECT" # Role: BACKENDCODER, SYSTEM_ARCHITECT, etc.
---

# [L2] ADR-007 Specification Phase Integration

## 親Issue / ロードマップ (Context)
- **Roadmap**: #260 (ADR-007 L1 Issue)
- **Task ID**: 007-T3-L2

## 1. 目的と背景 (Goal & Context)
- **As-is (現状)**: ADR-007「Metadata-driven Lifecycle」のアーキテクチャ設計は完了しているが、実装に向けた詳細仕様（Spec）が旧来の物理構造前提のままになっている。
- **To-be (あるべき姿)**: メタデータスキーマ、DAG解析ロジック、および新しいCLIコマンド体系の仕様が策定され、実装（TDD）フェーズへ移行可能な状態になっている。

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `reqs/design/_approved/adr-007-metadata-driven-lifecycle.md` (ADR-SSOT)
- [ ] `docs/architecture/plans/adr-007-metadata-driven-lifecycle/arch-to-spec.md` (申し送り)
- [ ] `docs/specs/plans/adr-007-metadata-driven-lifecycle/definitions.md` (共通定義)

## 3. 実装手順 (Implementation Steps)

### 3.1. 仕様書の更新 (Changes)
- [ ] **ファイル**: `docs/specs/data/document_model.md`
    - **内容**: メタデータスキーマとステータス定義の反映 (007-T3-01)
- [ ] **ファイル**: `docs/specs/logic/creation_logic.md`
    - **内容**: DAG解析と状態遷移ロジックの定義 (007-T3-02)
- [ ] **ファイル**: `docs/specs/components/infra_adapters.md`
    - **内容**: 物理移動とGitHub連携の定義 (007-T3-03)
- [ ] **ファイル**: `docs/specs/api/cli_commands.md`
    - **内容**: コマンド引数とデフォルトパスの更新 (007-T3-04)

## 4. ブランチ戦略 (Branching Strategy)
- **ベースブランチ (Base Branch)**: `main`
- **作業ブランチ (Feature Branch)**: `feature/spec-update-adr007`

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **自動監査**: `auditing-specs` スキルによる監査を通過すること。
- [ ] **静的解析**: ドキュメント内の用語が `definitions.md` と整合していること。
- [ ] **成果物**: `spec-to-tdd.md` (TDDフェーズへの申し送り) が作成されていること。

## 6. 成果物 (Deliverables)
- `docs/specs/data/document_model.md`
- `docs/specs/logic/creation_logic.md`
- `docs/specs/components/infra_adapters.md`
- `docs/specs/api/cli_commands.md`
- `docs/specs/plans/adr-007-metadata-driven-lifecycle/spec-to-tdd.md`
