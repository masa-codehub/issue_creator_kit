---
id: task-008-01
parent: adr-008
type: task
title: "ADR-008: Implement Domain Guardrails & Models"
status: Draft
phase: domain
labels:
  - "gemini:spec"
  - "P1"
  - "BACKENDCODER"
roadmap: "docs/specs/plans/adr-008-automation-cleanup/definitions.md"
depends_on: []
issue_id: 
---
# ADR-008: Implement Domain Guardrails & Models

## 1. 目的と背景 (Goal & Context)
- **As-is (現状)**: Scanner Foundation に必要な Pydantic モデル (`Task`, `ADR`, `Graph`) や不変条件（Guardrails）が実装されていない。
- **To-be (あるべき姿)**: `src/issue_creator_kit/domain/models/` 配下に、`definitions.md` で定義された型制約と Guardrails を満たすドメインモデルが実装され、単体テストが通っている。
- **Design Evidence**: `docs/architecture/arch-structure-008-scanner.md` (SSOT), `docs/specs/plans/adr-008-automation-cleanup/definitions.md` (Spec Plan)

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `docs/specs/plans/adr-008-automation-cleanup/definitions.md`
- [ ] `docs/architecture/arch-structure-008-scanner.md`

## 3. 実装手順と制約 (Implementation Steps & Constraints)

### 3.1. 負の制約 (Negative Constraints)
- [ ] **変更禁止**: `src/issue_creator_kit/cli.py` (CLIへの統合は別タスク)
- [ ] **スコープ外**: ファイルシステムへのアクセスロジック (`FileSystemScanner`)

### 3.2. 実装手順 (Changes)
#### 3.2.1. Define Domain Models
- [ ] **ファイル**: `src/issue_creator_kit/domain/models/core.py` (新規作成)
    - **処理内容**: `TaskID`, `ADRID` などの基本型を定義（Regex検証含む）。
- [ ] **ファイル**: `src/issue_creator_kit/domain/models/task.py` (新規作成)
    - **処理内容**: `Task`, `ADR` モデルを Pydantic で定義。
- [ ] **ファイル**: `src/issue_creator_kit/domain/models/graph.py` (新規作成)
    - **処理内容**: `TaskNode`, `TaskGraph` クラスと循環参照検知ロジックの実装。

#### 3.2.2. Implement Guardrails
- [ ] **ファイル**: `src/issue_creator_kit/domain/models/validators.py` (新規作成)
    - **処理内容**: `ID Format`, `No Self-Reference`, `No Cycles` のバリデーションロジックを実装。

## 4. ブランチ戦略 (Branching Strategy)
- **ベースブランチ (Base Branch)**: feature/spec-update-adr008 (統合ブランチ)
- **作業ブランチ (Feature Branch)**: feature/task-008-01-domain

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **自動テスト**: `pytest tests/unit/domain/models` がパスすること。
- [ ] **TDD Criteria (Happy Path)**: 正しいフォーマットの ID と DAG 構造を受け入ること。
- [ ] **TDD Criteria (Error Path)**: 循環参照、不正な ID フォーマット、自己参照に対して `ValidationError` または `GraphError` を送出すること。
- [ ] **静的解析**: `ruff check .` および `mypy .` がパスすること。

## 6. 成果物 (Deliverables)
- `src/issue_creator_kit/domain/models/*.py`
- `tests/unit/domain/models/*.py`
