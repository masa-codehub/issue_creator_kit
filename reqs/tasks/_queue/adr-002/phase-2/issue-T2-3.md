---
title: "承認プロセッサ (process_approvals.py) の実装"
labels:
  - "task"
  - "P1"
  - "BACKENDCODER"
roadmap: "reqs/roadmap/active/roadmap-adr002-document-approval-flow.md"
task_id: "T2-3"
depends_on:
  - "issue-T2-2.md"
status: "Draft"
---
# {{title}}

## 親Issue / ロードマップ (Context)
- **Roadmap**: {{roadmap}}
- **Task ID**: {{task_id}}

## 1. 目的と背景 (Goal & Context)
- **As-is (現状)**: ユーティリティ関数 (`utils.py`) は実装されたが、それらを組み合わせてドキュメント承認フロー（移動->更新->Issue起票）を実行するロジックがない。
- **To-be (あるべき姿)**: `process_approvals.py` が実装され、指定されたドキュメントの承認処理を一括で行えるようになる。

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `reqs/design/_approved/adr-002-document-approval-flow.md` (承認フローの仕様)
- [ ] `src/issue_creator_kit/utils.py` (利用するユーティリティ)

## 3. 実装手順 (Implementation Steps)

### 3.1. テストコード作成 (TDD)
- [ ] **ファイル**: `tests/unit/test_process_approvals.py`
    - **処理内容**: 承認フローの正常系・異常系を検証するテストを作成する。
    - **要件**: GitHub API 呼び出しなどは `unittest.mock` でモック化すること。

### 3.2. 実装 (Implementation)
- [ ] **ファイル**: `src/issue_creator_kit/scripts/process_approvals.py`
    - **処理内容**:
        1. 引数で指定されたドキュメントを `utils.load_document` で読み込む。
        2. Status を `Approved` (または指定値) に更新する。
        3. `utils.safe_move_file` で `_approved/` ディレクトリへ移動する。
        4. GitHub Issue を起票する（既存の `create_issues` ロジックを再利用または呼び出す）。
        5. 起票された Issue 番号をドキュメント内に追記する (`Issue: #123`)。

## 4. ブランチ戦略 (Branching Strategy)
- **ベースブランチ (Base Branch)**: `feature/phase-2-implementation`
- **作業ブランチ (Feature Branch)**: `feature/T2-3-process-approvals`

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **自動テスト**: `pytest tests/unit/test_process_approvals.py` がパスすること。
- [ ] **ロジック検証**: 移動、更新、Issue起票のシーケンスが正しい順序で実行されること。

## 6. 成果物 (Deliverables)
- `src/issue_creator_kit/scripts/process_approvals.py`
- `tests/unit/test_process_approvals.py`