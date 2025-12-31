---
title: "GitHub Actions ワークフローの刷新"
labels:
  - "task"
  - "P1"
  - "SYSTEM_ARCHITECT" # or BACKENDCODER with CI knowledge
roadmap: "reqs/roadmap/active/roadmap-adr002-document-approval-flow.md"
task_id: "T3-3"
depends_on:
  - "issue-T3-2.md"
status: "Draft"
---
# {{title}}

## 親Issue / ロードマップ (Context)
- **Roadmap**: {{roadmap}}
- **Task ID**: {{task_id}}

## 1. 目的と背景 (Goal & Context)
- **As-is (現状)**: 既存の `.github/workflows/auto-approve-docs.yml` はシェルスクリプト (`sed`, `mv`) で承認処理を行っており、脆弱である。
- **To-be (あるべき姿)**: 実装された `issue-kit approve` コマンドを使用する安全なワークフローに置き換わる。

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `.github/workflows/auto-approve-docs.yml` (修正対象)
- [ ] `src/issue_creator_kit/cli.py` (使用するコマンド)

## 3. 実装手順 (Implementation Steps)

### 3.1. ワークフロー修正 (Workflow Update)
- [ ] **ファイル**: `.github/workflows/auto-approve-docs.yml`
    - **処理内容**:
        - Python 環境のセットアップ (`actions/setup-python`) を追加。
        - パッケージのインストール (`pip install .`) を追加。
        - 承認ステップを `issue-kit approve <file>` の実行に変更。

## 4. ブランチ戦略 (Branching Strategy)
- **ベースブランチ (Base Branch)**: `feature/phase-3-integration`
- **作業ブランチ (Feature Branch)**: `feature/T3-3-workflow-update`

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **ローカル検証**: `act` コマンド（利用可能な場合）でワークフローが正常終了すること。または、PR作成後のCI実行でエラーが出ないこと（Dry-run的な確認）。
- [ ] **構文チェック**: YAML構文エラーがないこと。

## 6. 成果物 (Deliverables)
- 更新された `.github/workflows/auto-approve-docs.yml`

---
**Created Issue**: #46
