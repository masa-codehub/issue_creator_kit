---
id: 007-T3-01
parent: adr-007
type: task
phase: spec
status: Draft
depends_on: []
---

# Task: Update Document Model Specification

## 1. Goal & Context
### Goal
`docs/specs/data/document_model.md` を更新し、ADR-007 で定義されたメタデータスキーマ（`id`, `parent`, `type`, `phase`, `depends_on` 等）と新しいステータス定義（Enum）を反映する。

### As-is
既存の `document_model.md` は ADR-003 時代の古いメタデータ構造（`Depends-On` ヘッダ等）と物理ステータス定義に基づいている。

### To-be
ADR-007 および `docs/specs/plans/adr-007-metadata-driven-lifecycle/definitions.md` で定義されたスキーマと完全に整合したドキュメントモデル定義となっている。

### Design Evidence
- `reqs/design/_approved/adr-007-metadata-driven-lifecycle.md`
- `docs/specs/plans/adr-007-metadata-driven-lifecycle/definitions.md`

## 2. Input Context
- `docs/specs/data/document_model.md` (編集対象)
- `docs/specs/plans/adr-007-metadata-driven-lifecycle/definitions.md` (参照: メタデータ定義)

## 3. Implementation Steps & Constraints
### Negative Constraints
- 既存のクラス図 (`mermaid`) を削除しないこと（更新は可）。
- Clean Architecture の原則（Entity層の独立性）を崩さないこと。

### Changes
1. **Metadata Class Definition Update:**
   - `docs/specs/data/document_model.md` の `Metadata` クラス定義を更新。
   - 必須フィールド `id`, `parent`, `type`, `phase`, `date` を追加。
   - `depends_on` の型定義を `List[String]` (ID List) に明記。
2. **Status Enum Update:**
   - ステータス定義表を更新。
   - ADR/Design Doc 用: `Draft`, `Approved`, `Postponed`, `Superseded`
   - Task 用: `Draft`, `Ready`, `Issued`, `Completed`, `Cancelled`
3. **Normalization Rules Update:**
   - 古いエイリアス（日本語キー等）の扱いは維持しつつ、新しい必須フィールドへのマッピングルールを追記（必要な場合）。

## 4. Branching Strategy
- **Base Branch:** `feature/spec-update-adr007`
- **Feature Branch:** `spec/task-007-T3-01-model`

## 5. Verification & DoD
### 5.1. Verification Criteria
- [ ] **Schema Check:** `document_model.md` に `id`, `type`, `phase` フィールドが含まれていること。
- [ ] **Enum Check:** ステータス `Ready`, `Issued` が定義されていること。
- [ ] **TDD Criteria:** `test_document.py` で検証すべき「必須フィールド欠損時のバリデーションエラー」のケースが記述されていること。

### 5.2. Automated Tests
- `grep "id" docs/specs/data/document_model.md`
- `grep "Issued" docs/specs/data/document_model.md`
