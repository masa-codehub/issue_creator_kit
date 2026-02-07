---
id: task-008-05
parent: adr-008
type: task
title: "ADR-008: Integrate CLI with Scanner Foundation"
status: Draft
phase: interface
labels:
  - "gemini:spec"
  - "P1"
  - "BACKENDCODER"
roadmap: "docs/specs/plans/adr-008-automation-cleanup/definitions.md"
depends_on: ["task-008-02", "task-008-04"]
issue_id: 
---
# ADR-008: Integrate CLI with Scanner Foundation

## 1. 目的と背景 (Goal & Context)
- **As-is (現状)**: CLI (`cli.py`) は旧ロジックを使用しているか、機能が削除された状態（Task-02後）。
- **To-be (あるべき姿)**: `ick process --dry-run` および `ick visualize` コマンドが実装され、新しい Scanner Foundation を利用して動作する。
- **Design Evidence**: `docs/architecture/arch-structure-issue-kit.md` (CLI Entrypoint)

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `src/issue_creator_kit/cli.py`
- [ ] `src/issue_creator_kit/domain/services/` (Scanner, Builder, Visualizer)

## 3. 実装手順と制約 (Implementation Steps & Constraints)

### 3.1. 負の制約 (Negative Constraints)
- [ ] **変更禁止**: ドメインロジックの修正（CLIは呼び出しに徹する）。

### 3.2. 実装手順 (Changes)
#### 3.2.1. Update CLI Commands
- [ ] **ファイル**: `src/issue_creator_kit/cli.py`
    - **処理内容**: `process` コマンドの実装（`--dry-run` オプション対応）。
    - **処理内容**: `visualize` コマンドの実装（標準出力への Mermaid 出力）。
    - **処理内容**: 依存性の注入（ScannerService のインスタンス化）。

## 4. ブランチ戦略 (Branching Strategy)
- **ベースブランチ (Base Branch)**: feature/spec-update-adr008
- **作業ブランチ (Feature Branch)**: feature/task-008-05-cli

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **自動テスト**: `pytest tests/unit/test_cli.py` がパスすること。
- [ ] **統合テスト**: 実際にコマンドを実行し、期待通りの出力が得られること（`ick visualize` でグラフが出るか）。

## 6. 成果物 (Deliverables)
- `src/issue_creator_kit/cli.py`
- `tests/unit/test_cli.py`
