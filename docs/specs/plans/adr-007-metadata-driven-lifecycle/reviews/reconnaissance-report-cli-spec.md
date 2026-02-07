# Reconnaissance Report - CLI Specification Update (ADR-007)

## 1. 調査目的

`issue-kit` CLI の仕様定義を ADR-007（メタデータ駆動型ライフサイクル管理）に適合させるための現状把握。

## 2. 調査結果 (事実)

### 2.1. 現状の仕様定義 (`docs/specs/api/cli_commands.md`)

- **`run-workflow`**:
  - `--inbox-dir` デフォルト: `reqs/design/_inbox`
  - `--approved-dir` デフォルト: `reqs/design/_approved`
- **`process-diff`**:
  - `--archive-dir` デフォルト: `reqs/tasks/archive/` (ADR-007 では `reqs/tasks/_archive/` が正)
- **`process-merge`**:
  - `--archive-dir` デフォルト: `reqs/tasks/archive/`

### 2.2. ADR-007 での決定事項 (`reqs/design/_approved/adr-007-metadata-driven-lifecycle.md`)

- タスク下書きの配置場所: `reqs/tasks/<ADR-ID>/`
- アーカイブ場所: `reqs/tasks/_archive/` (フラット配置)
- ステータス遷移: `Draft -> Ready -> Issued -> Completed -> Cancelled`
- 自動移動: 起票成功時に `reqs/tasks/_archive/` へ移動。

### 2.3. Common Definitions (`docs/specs/plans/adr-007-metadata-driven-lifecycle/definitions.md`)

- `ick create` (Issue #283 では `process-diff` 相当と思われる) の冪等性、DAG 解析ロジックが定義されている。
- CLI Spec (007-T3-04) は `007-T3-01` (Model) に依存。

### 2.4. 現状の実装 (`src/issue_creator_kit/cli.py`)

- `process-diff` サブコマンドが存在し、`--archive-dir` のデフォルトは `reqs/tasks/archive/` となっている。
- `--adr-id` フィルタは未実装。

### 2.5. 現状のテスト (`tests/unit/test_cli.py`)

- `run-workflow` の引数解析テストが存在する。
- `process-diff` のテストは不足している可能性がある（要確認だが、今回のタスクは Spec 更新なので、検証基準の記述が重要）。

## 3. ギャップ分析

- デフォルトのアーカイブパスが古い (`archive/` vs `_archive/`)。
- タスク探索の開始ディレクトリが不明確（ADR-007 では `reqs/tasks/` 全体を再帰探索すべき）。
- `--adr-id` によるフィルタリングオプションが定義されていない。

## 4. 証拠 (Evidence)

- `docs/specs/api/cli_commands.md` line 38, 52
- `adr-007-metadata-driven-lifecycle.md` Section "Directory Structure"
- `cli.py` line 147, 169
