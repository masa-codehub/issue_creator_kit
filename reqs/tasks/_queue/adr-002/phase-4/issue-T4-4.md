---
title: "新規スクリプトの単体テストを実装"
labels:
  - "task"
  - "P1"
  - "BACKENDCODER"
roadmap: "reqs/roadmap/active/roadmap-adr002-document-approval-flow.md"
task_id: "T4-4"
depends_on:
  - "issue-T4-3.md"
status: "Draft"
---
# {{title}}

## 親Issue / ロードマップ (Context)
- **Roadmap**: {{roadmap}}
- **Task ID**: {{task_id}}

## 1. 目的と背景 (Goal & Context)
- **As-is (現状)**: 新規アーキテクチャに移行した Usecase 群のテストが存在しない。
- **To-be (あるべき姿)**: `Infrastructure` 層の Adapter（Git, FileSystem）をモックに差し替えることで、実際の IO を発生させずに Usecase のロジック（条件分岐や順序）を 100% 検証できている状態。

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `src/issue_creator_kit/usecase/workflow.py`
- [ ] `src/issue_creator_kit/usecase/approval.py`

## 3. 実装手順 (Implementation Steps)

### 3.1. Usecase テスト (Unit Test)
- [ ] **ファイル**: `tests/unit/test_usecase_workflow.py`
    - **テスト内容**: 
        - `process_all_files` が成功したとき、`GitAdapter.commit` が呼ばれるか。
        - エラー発生時に適切にロールバック（または停止）指示が出るか。
- [ ] **ファイル**: `tests/unit/test_usecase_approval.py`
    - **テスト内容**: メタデータ更新ロジックの正当性を、ファイル IO をモックして検証。

## 4. ブランチ戦略 (Branching Strategy)
- **ベースブランチ**: `feature/phase-4-cleanup`
- **作業ブランチ**: `feature/T4-4-test-usecases`

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **テスト実行**: `pytest tests/unit/` がパスすること。
- [ ] **モック活用**: `subprocess` や `requests` を直接触らず、Adapter インターフェースをモックしていること。

