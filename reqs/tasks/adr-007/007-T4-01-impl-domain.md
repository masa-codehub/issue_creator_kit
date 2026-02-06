---
id: 007-T4-01
parent: adr-007
type: task
title: "[TDD] Data Model & Adapter Protocols (Domain)"
status: Draft
phase: domain
date: 2026-02-05
labels:
  - "gemini:tdd"
  - "P1"
  - "BACKENDCODER"
roadmap: "docs/specs/plans/adr-007-metadata-driven-lifecycle/tdd-plan.md"
depends_on: []
---
# [TDD] Data Model & Adapter Protocols (Domain)

## 1. 目的と背景 (Goal & Context)
- **Goal**: ADR-007 に準拠した `Document` / `Metadata` モデルを実装し、さらに Infra と UseCase の架け橋となる **Adapter Interface (Python Protocols)** を定義することで、後続タスクの並列開発を可能にする。
- **As-is (現状)**: 具象クラスが直接 UseCase に依存されており、インフラの実装が終わるまでロジックのテストが困難。メタデータバリデーションも不足している。
- **To-be (あるべき姿)**: 
    - `docs/specs/data/document_model.md` に準拠したモデル。
    - `FileSystemAdapter`, `GitHubAdapter`, `GitAdapter` の抽象インターフェースが定義され、UseCase がこれらに依存（DI）する準備が整っている。
- **Design Evidence (設計の根拠)**: 
    - `docs/specs/data/document_model.md`
    - `docs/specs/components/infra_adapters.md`

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `docs/specs/data/document_model.md`
- [ ] `docs/specs/components/infra_adapters.md`
- [ ] `src/issue_creator_kit/domain/document.py`

## 3. 実装手順と制約 (Implementation Steps & Constraints)

### 3.1. 負の制約 (Negative Constraints)
- [ ] **変更禁止**: 既存のインフラ層やユースケース層の「ロジック」の書き換え（インターフェースの定義に留める）。

### 3.2. 実装手順 (Changes)
- [ ] **ファイル**: `src/issue_creator_kit/domain/document.py`
    - **処理内容**: 
        - `Metadata` の実装とバリデーション、正規化（日本語キー対応）。
        - シリアライズ（YAML への統一）ロジック。
- [ ] **ファイル**: `src/issue_creator_kit/domain/interfaces.py` (新規作成)
    - **処理内容**: 
        - `IFileSystemAdapter`, `IGitHubAdapter`, `IGitAdapter` の `typing.Protocol` による定義。
        - 各仕様書 (`infra_adapters.md`) に基づくメソッドシグネチャの定義。
- [ ] **ファイル**: `tests/unit/domain/test_document.py`
    - **処理内容**: スキーマバリデーションと正規化の網羅的なテスト。

## 4. ブランチ戦略 (Branching Strategy)
- **ベースブランチ (Base Branch)**: feature/impl-adr007-lifecycle
- **作業ブランチ (Feature Branch)**: tdd/task-007-T4-01-impl-domain

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **自動テスト**: `pytest tests/unit/domain/test_document.py` がパスすること。
- [ ] **インターフェース確認**: `interfaces.py` に `find_file_by_id` や `sync_issue` の定義が存在すること。
- [ ] **静的解析**: `mypy` がパスすること。

## 6. 成果物 (Deliverables)
- `src/issue_creator_kit/domain/document.py`
- `src/issue_creator_kit/domain/interfaces.py`
- `tests/unit/domain/test_document.py`
