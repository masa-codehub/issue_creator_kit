---
depends_on:
- spec-03-usecase.md
issue: '#217'
labels:
- task
- P2
- TECHNICAL_DESIGNER
roadmap: reqs/roadmap/archive/roadmap-adr002-document-approval-flow.md
status: Draft
task_id: SPEC-04
title: '[Spec] Define CLI Interface'
---
# [Spec] Define CLI Interface

## 親Issue / ロードマップ (Context)
- **Roadmap**: reqs/roadmap/archive/roadmap-adr002-document-approval-flow.md
- **Task ID**: SPEC-04
- **Common Definitions**: docs/specs/plans/20260120-approval-flow.md

## 1. 目的と背景 (Goal & Context)
- **As-is (現状)**: CLIのエントリポイント仕様が未定義。
- **To-be (あるべき姿)**: コマンド名、引数、環境変数、終了コードが定義される。
- **Design Evidence**: `docs/system-context.md`

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `docs/specs/plans/20260120-approval-flow.md`

## 3. 実装手順と制約 (Implementation Steps & Constraints)

### 3.1. 負の制約 (Negative Constraints)
- [ ] **ロジック混入禁止**: CLI層にはビジネスロジックを書かず、Usecaseへの委譲のみを行う仕様とする。

### 3.2. 実装手順 (Changes)
- [ ] **ファイル**: `docs/specs/api/cli_commands.md`
    - **処理内容**:
      - コマンド: `issue-kit run-workflow`
      - 引数: なし（ ワークフローの詳細な挙動・パラメータは別仕様で定義）
      - 環境変数: `GITHUB_MCP_PAT` (必須)
    - **Verify (TDD Criteria)**:
      - 「`GITHUB_MCP_PAT` がない場合、エラーメッセージを表示して終了コード 1 を返すこと」

## 4. ブランチ戦略 (Branching Strategy)
- **ベースブランチ (Base Branch)**: `feature/spec-update-approval-flow`
- **作業ブランチ (Feature Branch)**: `feature/spec-04-cli`

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **レビュー**: `docs/specs/api/cli_commands.md` が作成されていること。

## 6. 成果物 (Deliverables)
- `docs/specs/api/cli_commands.md`