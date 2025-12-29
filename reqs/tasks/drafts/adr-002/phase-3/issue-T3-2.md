---
title: "CLI サブコマンド `approve` の実装"
labels:
  - "task"
  - "P1"
  - "BACKENDCODER"
roadmap: "reqs/roadmap/active/roadmap-adr002-document-approval-flow.md"
task_id: "T3-2"
depends_on:
  - "issue-T3-1.md"
status: "Draft"
---
# {{title}}

## 親Issue / ロードマップ (Context)
- **Roadmap**: {{roadmap}}
- **Task ID**: {{task_id}}

## 1. 目的と背景 (Goal & Context)
- **As-is (現状)**: 承認処理ロジック `process_approvals.py` は存在するが、CLI (`issue-kit`) から呼び出すインターフェースがない。
- **To-be (あるべき姿)**: `issue-kit approve <file_path>` コマンドで承認フローを実行できるようになる。

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `src/issue_creator_kit/cli.py` (CLIエントリポイント)
- [ ] `src/issue_creator_kit/scripts/process_approvals.py` (呼び出し先ロジック)

## 3. 実装手順 (Implementation Steps)

### 3.1. CLI実装 (Implementation)
- [ ] **ファイル**: `src/issue_creator_kit/cli.py`
    - **処理内容**: `approve` サブコマンドを追加し、`process_approvals.main` (または適切な関数) を呼び出す処理を実装する。
    - **引数**: 対象ファイルパス (`file_path`)。

### 3.2. テスト (Test)
- [ ] **ファイル**: `tests/unit/test_cli.py`
    - **処理内容**: `approve` コマンドが正しく引数を解析し、バックエンドロジックを呼び出しているか検証する。

## 4. ブランチ戦略 (Branching Strategy)
- **ベースブランチ (Base Branch)**: `feature/phase-3-integration`
- **作業ブランチ (Feature Branch)**: `feature/T3-2-cli-approve`

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **自動テスト**: `pytest tests/unit/test_cli.py` がパスすること。
- [ ] **手動検証**: `issue-kit approve --help` が表示されること。

## 6. 成果物 (Deliverables)
- 更新された `src/issue_creator_kit/cli.py`