---
title: "`Process Documents` のロジックをPythonスクリプト化"
labels:
  - "task"
  - "P1"
  - "SYSTEM_ARCHITECT"
  - "BACKENDCODER"
roadmap: "reqs/roadmap/active/roadmap-adr002-document-approval-flow.md"
task_id: "T4-3"
depends_on:
  - "issue-T4-1.md"
status: "Created"
issue: "#55"
---
# {{title}}

## 親Issue / ロードマップ (Context)
- **Roadmap**: {{roadmap}}
- **Task ID**: {{task_id}}

## 1. 目的と背景 (Goal & Context)
- **As-is (現状)**: GitHub Actions の YAML 内に、ファイルの変更検知、コミット、プッシュ判定などのロジックがシェルスクリプトとして記述されている。
- **To-be (あるべき姿)**: ワークフロー全体の流れ（オーケストレーション）を Python の **Usecase** として実装する。Git 操作は **Infrastructure** 層の Adapter を介して行い、YAML からは単一のコマンドを呼び出すだけにする。

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `.github/workflows/auto-approve-docs.yml`
- [ ] `src/issue_creator_kit/infrastructure/git_adapter.py` (T4-2で作成)
- [ ] `src/issue_creator_kit/usecase/approval.py` (T4-2で作成)

## 3. 実装手順 (Implementation Steps)

### 3.1. Usecase 実装 (Orchestration)
- [ ] **ファイル**: `src/issue_creator_kit/usecase/workflow.py`
    - **機能**: 
        1. `ApprovalUseCase` を呼び出してファイルを処理。
        2. 変更があった場合、`GitAdapter` を使用してコミットメッセージの作成、ブランチの準備を行う。
        3. 実行結果（変更の有無、PR作成が必要か等）を戻り値として返す。

### 3.2. CLI 統合 (CLI Entrypoint)
- [ ] **ファイル**: `src/issue_creator_kit/cli.py`
    - **変更**: `issue-kit run-workflow` コマンドを追加。
    - **処理**: 上記 Usecase を呼び出し、結果に応じて `GITHUB_OUTPUT` への書き込み等を行う。

## 4. ブランチ戦略 (Branching Strategy)
- **ベースブランチ**: `feature/phase-4-cleanup`
- **作業ブランチ**: `feature/T4-3-workflow-usecase`

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **動作確認**: `GitAdapter` をスタブに差し替えて、ワークフローの流れが正しく制御されることを確認する。
- [ ] **静的解析**: `ruff` / `mypy` エラーなし。


## 6. 成果物 (Deliverables)
- `src/issue_creator_kit/scripts/process_and_commit_approvals.py`
- `src/issue_creator_kit/cli.py` (更新)
