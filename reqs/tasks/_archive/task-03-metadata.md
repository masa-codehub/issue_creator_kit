---
id: task-008-03
parent: adr-008
type: task
title: "Update Architecture Metadata for Domain Guardrails"
status: Draft
phase: architecture
labels:
  - "gemini:arch"
  - "P1"
  - "SYSTEM_ARCHITECT"
roadmap: "docs/architecture/plans/adr-008-automation-cleanup/design-brief.md"
depends_on: ["task-008-04"]
issue_id:
---

# Update Architecture Metadata for Domain Guardrails

## 1. 目的と背景 (Goal & Context)

- **As-is (現状)**: メタデータ定義はあるが、その検証ロジック（Guardrails）としてのPydanticモデルへのマッピングが記述されていない。
- **To-be (あるべき姿)**: `id` や `depends_on` の制約（循環参照禁止など）がアーキテクチャ上のルールとして明記されている。
- **Design Evidence (設計の根拠)**: ADR-008 "Domain Guardrails".

## 2. 参照資料・入力ファイル (Input Context)

- [ ] `docs/architecture/plans/adr-008-automation-cleanup/definitions.md` (Domain Guardrails)
- [ ] `docs/architecture/arch-structure-007-metadata.md` (編集対象)

## 3. 実装手順と制約 (Implementation Steps & Constraints)

### 3.1. 実装手順 (Changes)

- [ ] **ファイル**: `docs/architecture/arch-structure-007-metadata.md`
  - **Validation Rules**: 各フィールドに対する検証ルール（Regex, Graph Integrity）を追記。
  - **Implementation Mapping**: これらが `src/issue_creator_kit/domain/models` で実装される旨を注記。

## 4. ブランチ戦略 (Branching Strategy)

- **ベースブランチ (Base Branch)**: feature/arch-update-adr008
- **作業ブランチ (Feature Branch)**: feature/task-008-03-metadata

## 5. 検証手順・完了条件 (Verification & DoD)

- [ ] **内容確認**: Pydantic Validator に相当する制約が自然言語で記述されていること。
