---
title: "マージ差分検知と一括起票（仮想キュー）の TDD 実装"
labels:
  - "task"
  - "P1"
  - "BACKENDCODER"
roadmap: "reqs/roadmap/active/roadmap-adr003-task-lifecycle.md"
task_id: "T2-2"
depends_on: ["issue-T2-1.md"]
next_phase_path: ""
status: "Draft"
---
# マージ差分検知と一括起票（仮想キュー）の TDD 実装

## 親Issue / ロードマップ (Context)
- **Roadmap**: reqs/roadmap/active/roadmap-adr003-task-lifecycle.md
- **Task ID**: T2-2

## 1. 目的と背景 (Goal & Context)
- **As-is (現状)**: 現在の ICK は物理ディレクトリ `_queue` を監視している。
- **To-be (あるべき姿)**: `git diff` を解析し、`archive/` への新規追加ファイルを検知して Issue を起票するロジックが実装されている。
- **Design Evidence (設計の根拠)**: `design-003-logic.md` (T1-3成果物)

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `reqs/design/_inbox/design-003-logic.md`
- [ ] `docs/specs/test-criteria.md`

## 3. 実装手順と制約 (Implementation Steps & Constraints)

### 3.1. 負の制約 (Negative Constraints)
- [ ] **変更禁止**: 既存の `GitHubAdapter` のインターフェース。

### 3.2. 実装手順 (Changes)
- [ ] **ファイル**: `src/issue_creator_kit/usecase/creation.py`
    - **処理内容**:
        - `DifferenceDetector` クラスの実装: `GitAdapter` を使用してマージコミット間の差分ファイルパスを取得。
        - `IssueFactory` クラスの実装 (または既存拡張): ファイル内容をパースし、Issue オブジェクトを生成。
        - メインロジック: 検知されたファイル群に対して `create_issue` をループ実行。
- [ ] **ファイル**: `tests/unit/usecase/test_creation.py`
    - **処理内容**: TDD によるテスト実装。ダミーの `GitAdapter` モックを使用。

### 3.3. 構成変更・削除 (Configuration / Cleanup)
- なし

## 4. ブランチ戦略 (Branching Strategy)
- **ベースブランチ (Base Branch)**: `feature/phase-2-foundation`
- **作業ブランチ (Feature Branch)**: `feature/T2-2-virtual-queue-impl`

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **自動テスト**: 単体テストがパスすること。
- [ ] **コード**: `creation.py` に `DifferenceDetector` クラスが存在すること。

## 6. 成果物 (Deliverables)
- `creation.py`