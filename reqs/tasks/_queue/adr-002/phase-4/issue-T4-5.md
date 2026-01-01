---
title: "ワークフローYAMLをリファクタリングし、新規スクリプトを呼び出すように変更"
labels:
  - "task"
  - "P1"
  - "SYSTEM_ARCHITECT"
roadmap: "reqs/roadmap/active/roadmap-adr002-document-approval-flow.md"
task_id: "T4-5"
depends_on:
  - "issue-T4-4.md"
status: "Draft"
---
# {{title}}

## 親Issue / ロードマップ (Context)
- **Roadmap**: {{roadmap}}
- **Task ID**: {{task_id}}

## 1. 目的と背景 (Goal & Context)
- **As-is (現状)**: `.github/workflows/auto-approve-docs.yml` が複雑なシェルスクリプトを含んでいる。
- **To-be (あるべき姿)**: T4-3 で作成した Python コマンドを呼び出すだけのシンプルな形にし、メンテナンス性を向上させる。

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `.github/workflows/auto-approve-docs.yml`
- [ ] `src/issue_creator_kit/cli.py`

## 3. 実装手順 (Implementation Steps)

### 3.1. ワークフロー修正 (Workflow Update)
- [ ] **ファイル**: `.github/workflows/auto-approve-docs.yml`
    - **変更**:
        - `Process Documents` ステップのシェルスクリプトを削除。
        - 代わりに `issue-kit run-workflow ...` (T4-3で定義した新コマンド) を実行する。
        - Output (`has_changes` 等) の受け渡し方法を調整（Python スクリプトが GITHUB_OUTPUT に書き込む形にするか、終了コードで判定するか）。

## 4. ブランチ戦略 (Branching Strategy)
- **ベースブランチ**: `feature/phase-4-cleanup`
- **作業ブランチ**: `feature/T4-5-refactor-yaml`

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **構文チェック**: YAML の構文エラーがないこと。
- [ ] **動作確認**: (可能であれば) `act` 等でローカル実行し、エラーにならないこと。または PR マージ後の動作確認計画を立てる。

## 6. 成果物 (Deliverables)
- `.github/workflows/auto-approve-docs.yml`
