---
id: 007-T4-01
parent: adr-007
parent_issue: 
type: task
title: "[TDD] Document & Metadata Implementation (Domain)"
status: Draft
phase: domain
labels:
  - "gemini:tdd"
  - "P1"
  - "BACKENDCODER"
roadmap: "docs/specs/plans/adr-007-metadata-driven-lifecycle/tdd-plan.md"
depends_on: []
issue_id: 
---
# [TDD] Document & Metadata Implementation (Domain)

## 1. 目的と背景 (Goal & Context)
- **As-is (現状)**: 既存の `Document` クラスは ADR-003 の古いメタデータ構造に依存しており、ADR-007 で定義された必須フィールド（id, parent, type, phase 等）のバリデーションや日本語キーの正規化ロジックが欠如している。
- **To-be (あるべき姿)**: `docs/specs/data/document_model.md` に準拠し、新しいメタデータスキーマを完全サポートする `Document` および `Metadata` クラスが実装されている。日本語キーから英語キーへの自動変換（正規化）がテストにより保証されている。
- **Design Evidence (設計の根拠)**: 
    - `docs/specs/data/document_model.md`
    - `docs/specs/plans/adr-007-metadata-driven-lifecycle/spec-to-tdd.md`

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `docs/specs/data/document_model.md`
- [ ] `src/issue_creator_kit/domain/document.py`
- [ ] `tests/unit/domain/test_document.py`

## 3. 実装手順と制約 (Implementation Steps & Constraints)

### 3.1. 負の制約 (Negative Constraints)
- [ ] **変更禁止**: `src/issue_creator_kit/infrastructure/` や `usecase/` への波及的修正（このタスク内ではドメインに集中）。
- [ ] **スコープ外**: ファイルシステムへの永続化ロジック（`domain` レイヤーの純粋なロジックに限定）。

### 3.2. 実装手順 (Changes)
- [ ] **ファイル**: `src/issue_creator_kit/domain/document.py`
    - **処理内容**: 
        - `Metadata` クラスを `dataclass` または通常のクラスとして詳細化。
        - `Document.parse()` の正規化ルール（日本語キー対応）を実装。
        - `Metadata.validate()` による必須フィールドチェックの実装。
        - シリアライズ（YAML Frontmatter への統一）の実装。
- [ ] **ファイル**: `tests/unit/domain/test_document.py`
    - **処理内容**: 
        - 正常系: 全必須フィールドを含む YAML/Markdown 形式のパース。
        - 異常系: `id` フォーマット不正、必須フィールド欠落時の `ValidationError`。
        - 境界値: 日本語キー（タイトル、フェーズ等）の正規化検証。

## 4. ブランチ戦略 (Branching Strategy)
- **ベースブランチ (Base Branch)**: feature/impl-adr007-lifecycle
- **作業ブランチ (Feature Branch)**: tdd/task-007-T4-01-impl-domain

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **自動テスト**: `pytest tests/unit/domain/test_document.py` がパスすること。
- [ ] **静的解析**: `ruff check .` および `mypy .` がパスすること。
- [ ] **観測される挙動**: 内部的に `metadata["id"]` で日本語の `ID` キーから取得した値を参照できること。

## 6. 成果物 (Deliverables)
- `src/issue_creator_kit/domain/document.py`
- `tests/unit/domain/test_document.py`
