---
title: "[Spec] Define Document Domain Model"
labels:
  - "task"
  - "P1"
  - "TECHNICAL_DESIGNER"
roadmap: "reqs/roadmap/archive/roadmap-adr002-document-approval-flow.md"
task_id: "SPEC-01"
depends_on: []
status: "Draft"
---
# [Spec] Define Document Domain Model

## 親Issue / ロードマップ (Context)
- **Roadmap**: reqs/roadmap/archive/roadmap-adr002-document-approval-flow.md
- **Task ID**: SPEC-01
- **Common Definitions**: docs/specs/plans/20260120-approval-flow.md

## 1. 目的と背景 (Goal & Context)
- **As-is (現状)**: ドキュメントの解析ロジックがスクリプト（`create_issues.py`）に埋め込まれており、SSOTとしてのデータ構造が定義されていない。
- **To-be (あるべき姿)**: `Domain.Document` および `Domain.Metadata` クラスの仕様が明確化され、実装者がパースロジックを TDD で実装できる状態。
- **Design Evidence**: `docs/architecture/arch-structure-issue-kit.md` (Domain Layer)

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `docs/specs/plans/20260120-approval-flow.md`
- [ ] `reqs/design/_archive/adr-002-document-approval-flow.md`

## 3. 実装手順と制約 (Implementation Steps & Constraints)

### 3.1. 負の制約 (Negative Constraints)
- [ ] **外部依存禁止**: Domain層の仕様において、GitHub API や ファイルシステムへの直接アクセスを含めてはならない。純粋なデータクラスとして定義する。

### 3.2. 実装手順 (Changes)
- [ ] **ファイル**: `docs/specs/data/document_model.md`
    - **処理内容**: 以下の要素を含むクラス図（Mermaid）とフィールド定義を作成する。
      - `Document`: ファイルパス、生コンテンツ、メタデータオブジェクトを持つ。
      - `Metadata`: `status`, `date`, `issue_id` を持つ。
    - **Verify (TDD Criteria)**:
      - 「必須フィールド（Status）が欠落している場合、`ValidationError` となること」
      - 「MarkdownのFront Matter以外（本文中の埋め込みメタデータ等）の解析ルールが明確か」

## 4. ブランチ戦略 (Branching Strategy)
- **ベースブランチ (Base Branch)**: `feature/spec-update-approval-flow`
- **作業ブランチ (Feature Branch)**: `feature/spec-01-domain`

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **レビュー**: `docs/specs/data/document_model.md` が作成され、Common Definitions と矛盾していないこと。
- [ ] **TDD準備**: 実装者がこの仕様書を見て `test_document_model.py` を書けること。

## 6. 成果物 (Deliverables)
- `docs/specs/data/document_model.md`