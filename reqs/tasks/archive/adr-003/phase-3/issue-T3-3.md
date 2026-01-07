---
title: "Auto-PR ロジックの実装"
labels:
  - "task"
  - "P1"
  - "BACKENDCODER"
roadmap: "reqs/roadmap/active/roadmap-adr003-task-lifecycle.md"
task_id: "T3-3"
depends_on: ["issue-T3-2.md"]
next_phase_path: ""
status: "Draft"
issue: "#156"
---
# Auto-PR ロジックの実装

## 親Issue / ロードマップ (Context)
- **Roadmap**: reqs/roadmap/active/roadmap-adr003-task-lifecycle.md
- **Task ID**: T3-3
- **Depends on**: issue-T3-2.md

## 1. 目的と背景 (Goal & Context)
- **As-is (現状)**: Auto-PR のロジックが削除されており、完了時に次フェーズへ連鎖しない。
- **To-be (あるべき姿)**: `docs/specs/auto-pr-logic.md` の仕様に従い、PR マージをトリガーとした Auto-PR 作成機能が実装されている。
- **Design Evidence (設計の根拠)**: docs/specs/auto-pr-logic.md

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `docs/specs/auto-pr-logic.md`
- [ ] `src/issue_creator_kit/usecase/workflow.py`
- [ ] `src/issue_creator_kit/cli.py`

## 3. 実装手順と制約 (Implementation Steps & Constraints)

### 3.1. 負の制約 (Negative Constraints)
- [ ] **リファクタリング禁止**: 今回のロジック追加に関係のない既存コードの書き換えは行わないこと。
- [ ] **モックの徹底**: 外部 GitHub API (PR作成等) は、テストコード内では必ずモック化すること。

### 3.2. 実装手順 (Changes)
- [ ] **TDD (Red)**: `tests/unit/usecase/test_workflow.py` に、PRマージイベントから `next_phase_path` を抽出し PR を作成する期待動作のテストを追加。
- [ ] **UseCase 実装 (Green)**: `WorkflowUseCase` に `promote_from_merged_pr(pr_body)` 等のメソッドを実装。
- [ ] **CLI 実装**: ワークフローから呼び出すための新しいコマンド（例: `process-merge`）を `cli.py` に追加。
- [ ] **Refactor (Blue)**: コードの整理。

### 3.3. 構成変更・削除 (Configuration / Cleanup)
- なし

## 4. ブランチ戦略 (Branching Strategy)
- **Pattern**: Feature (Implementation)
- **Base Branch**: `feature/phase-3-foundation`
- **Head Branch**: `feature/task-T3-3-impl`

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **自動テスト**: `pytest tests/unit/usecase/test_workflow.py` がパスすること。
- [ ] **観測可能性**: 実行時に「Detected merged PR for Issue #XXX. Next phase found: YYY」というログが出力されること。

## 6. 成果物 (Deliverables)
- 実装コードおよびテストコード
