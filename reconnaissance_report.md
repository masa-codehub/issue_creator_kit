# Reconnaissance Report - [TDD] CLI Integration (Interface)

## 1. 調査目的
- CLI サブコマンド `process-diff` への `--adr-id` 引数の追加およびバリデーション実装。
- `IssueCreationUseCase.create_issues()` へのパラメータ受け渡しの確認。
- 既存のテストコードの状況確認。

## 2. 収集された事実 (Facts)

### 2.1. CLI 実装 (`src/issue_creator_kit/cli.py`)
- `process-diff` サブコマンドに `--adr-id` 引数が存在しない。
- `run_automation` 関数内で `usecase.create_issues_from_virtual_queue` を呼び出しているが、UseCase 側は `create_issues` に名称変更されている。
- `--archive-dir` のデフォルト値が `reqs/tasks/archive/` になっているが、ADR-007 仕様では `reqs/tasks/_archive/` (アンダースコア付き) が推奨されている。

### 2.2. UseCase 実装 (`src/issue_creator_kit/usecase/creation.py`)
- `create_issues` メソッドが存在し、`adr_id` 引数を受け取れるようになっている。
- 引数のシグネチャ: `create_issues(self, before: str, after: str, adr_id: str | None = None, archive_path: str = "reqs/tasks/_archive/")`

### 2.3. 仕様書 (`docs/specs/api/cli_commands.md`)
- `process-diff` は `--adr-id` (形式: `adr-XXX`) を受け取り、バリデーションを行う必要がある。
- バリデーション失敗時は終了コード `1` を返す。
- デフォルトの `archive-dir` は `reqs/tasks/_archive/`。

### 2.4. テストコード (`tests/unit/test_cli.py`)
- `run-workflow` のテストは存在するが、`process-diff` のテストは存在しない。

## 3. 依存関係と制約
- CLI 層は UseCase 層に依存している。
- バリデーションは CLI 層で行う必要がある（仕様書に明記）。

## 4. 結論
- `cli.py` の `process-diff` サブパーサーおよび `run_automation` 関数を更新し、新しい UseCase インターフェースに適合させる必要がある。
- 引数バリデーションの実装と、それを確認するテストの追加が必要。
