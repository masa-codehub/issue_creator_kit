---
id: task-008-04
parent: adr-008
type: task
title: "ADR-008: Implement Graph Builder & Visualizer"
status: Draft
phase: domain
labels:
  - "gemini:spec"
  - "P1"
  - "BACKENDCODER"
roadmap: "docs/specs/plans/adr-008-automation-cleanup/definitions.md"
depends_on: ["task-008-01", "task-008-03"]
issue_id: 
---
# ADR-008: Implement Graph Builder & Visualizer

## 1. 目的と背景 (Goal & Context)
- **As-is (現状)**: 依存関係の整合性検証（DAG構築）と可視化ロジックが存在しない。
- **To-be (あるべき姿)**: `Task` リストから依存関係グラフを構築し、循環参照を検知するとともに、Mermaid 形式で出力できる。
- **Design Evidence**: `docs/architecture/arch-structure-008-scanner.md` (GraphBuilder, Visualizer)

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `src/issue_creator_kit/domain/models/` (Task-01 成果物)
- [ ] `src/issue_creator_kit/domain/services/scanner.py` (Task-03 成果物)

## 3. 実装手順と制約 (Implementation Steps & Constraints)

### 3.1. 負の制約 (Negative Constraints)
- [ ] **変更禁止**: `FileSystemScanner` のロジック（入力として使うのみ）。

### 3.2. 実装手順 (Changes)
#### 3.2.1. Implement Graph Builder
- [ ] **ファイル**: `src/issue_creator_kit/domain/services/builder.py` (新規作成)
    - **処理内容**: `List[Task]` を受け取り、`TaskGraph` (DAG) を構築する。
    - **処理内容**: 依存関係の解決（IDルックアップ）と循環参照チェックの実行。

#### 3.2.2. Implement Visualizer
- [ ] **ファイル**: `src/issue_creator_kit/domain/services/visualizer.py` (新規作成)
    - **処理内容**: `TaskGraph` を受け取り、Mermaid 記法の文字列を生成する。

## 4. ブランチ戦略 (Branching Strategy)
- **ベースブランチ (Base Branch)**: feature/spec-update-adr008
- **作業ブランチ (Feature Branch)**: feature/task-008-04-graph

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **自動テスト**: `pytest tests/unit/domain/services/test_builder.py` 等がパスすること。
- [ ] **TDD Criteria (Happy Path)**: 正常な依存関係を持つタスク群から、正しい Mermaid 文字列が生成されること。
- [ ] **TDD Criteria (Error Path)**: 循環参照を含むタスク群を渡した際に例外が発生すること。

## 6. 成果物 (Deliverables)
- `src/issue_creator_kit/domain/services/builder.py`
- `src/issue_creator_kit/domain/services/visualizer.py`
