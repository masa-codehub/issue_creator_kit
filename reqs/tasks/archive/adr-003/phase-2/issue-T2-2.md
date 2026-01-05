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
- **As-is (現状)**: 現在の ICK は物理ディレクトリ `_queue` を監視しているが、ADR-003 で「仮想キュー」への移行が決定された。
- **To-be (あるべき姿)**: `git diff-tree` を用いて `archive/` への新規追加ファイルを検知し、アトミックに Issue を一括起票するロジックが実装されている。
- **Design Evidence (設計の根拠)**: `design-003-logic.md` 第 1 項および第 2 項

## 2. 参照資料・入力ファイル (Input Context)
- [ ] `reqs/design/_inbox/design-003-logic.md` (詳細ロジック)
- [ ] `docs/specs/infra-interface.md` (IGitAdapter, IGitHubAdapter)
- [ ] `docs/specs/test-criteria.md` (テストシナリオ)

## 3. 実装手順と制約 (Implementation Steps & Constraints)

### 3.1. 負の制約 (Negative Constraints)
- [ ] **仕様遵守**: 部分失敗時のロールバック（Issue削除）は実装せず、二重起票を許容する Fail-Fast 戦略を維持すること（ADR-003 補足参照）。
- [ ] **変更禁止**: `IGitAdapter` などの既存インターフェースのシグネチャ変更（必要な場合は抽象クラスに追加）。

### 3.2. 実装手順 (Changes)
- [ ] **UseCase実装**: `src/issue_creator_kit/usecase/creation.py`
    - **DifferenceDetector**: `GitAdapter.get_added_files` を用いて、`archive/` 配下の新規 `.md` ファイルを特定する。
    - **AtomicBatchCreator**: `design-003-logic.md` 第 2 項に基づき、全件成功時のみメタデータ書き戻しコミットを実行するフローを実装。
- [ ] **テスト実装**: `tests/unit/usecase/test_creation.py`
    - **Scenario**: `docs/specs/test-criteria.md` の `VQ-001`〜`VQ-004`, `BC-001`〜`BC-005` をカバーするテストを記述。

### 3.3. 構成変更・削除 (Configuration / Cleanup)
- なし

## 4. ブランチ戦略 (Branching Strategy)
- **ベースブランチ (Base Branch)**: `feature/phase-2-foundation`
- **作業ブランチ (Feature Branch)**: `feature/task-T2-2-virtual-queue`

## 5. 検証手順・完了条件 (Verification & DoD)
- [ ] **自動テスト**: `pytest tests/unit/usecase/test_creation.py` がパスすること（TC: VQ-001〜BC-005）。
- [ ] **観測される挙動**: 1件でも Issue 作成に失敗した場合、ファイルへの `issue` 番号書き戻しが発生しないこと（Fail-Fast の確認）。

## 6. 成果物 (Deliverables)
- `src/issue_creator_kit/usecase/creation.py`
- `tests/unit/usecase/test_creation.py`
