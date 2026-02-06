# Goal Definition - [TDD] CLI Integration (Interface)

## 1. 具体的目標 (Specific Goal)
- `src/issue_creator_kit/cli.py` を更新し、`process-diff` コマンドが `--adr-id` 引数を受け取れるようにする。
- `--adr-id` の入力値が `adr-XXX` (XXX は 3 桁の数字) 形式であることをバリデーションし、不正な場合はエラーメッセージを出力して終了コード `1` で終了する。
- UseCase 呼び出しを `IssueCreationUseCase.create_issues()` に変更し、適切な引数を渡す。
- `process-diff` および `process-merge` の `--archive-dir` デフォルト値を `reqs/tasks/_archive/` に変更する。

## 2. 完了条件 (Definition of Done)
- [ ] `tests/unit/test_cli.py` に `process-diff` 用のテストケース（正常系・異常系）が追加され、すべてパスする。
- [ ] `issue-kit process-diff --help` で新しい引数とデフォルト値が表示される。
- [ ] 静的解析 (`ruff`, `mypy`) でエラーが出ない。
- [ ] 自己監査レポートが作成され、全項目をパスしている。

## 3. 検証方法 (Verification Methods)
- **単体テスト**: `pytest tests/unit/test_cli.py`
- **ヘルプ表示**: `python -m issue_creator_kit.cli process-diff --help`
- **バリデーション確認**:
    - `python -m issue_creator_kit.cli process-diff --before HEAD~1 --after HEAD --adr-id adr-007` (UseCase 呼び出し確認)
    - `python -m issue_creator_kit.cli process-diff --before HEAD~1 --after HEAD --adr-id invalid` (終了コード 1 の確認)
- **静的解析**: `ruff check src/issue_creator_kit/cli.py` / `mypy src/issue_creator_kit/cli.py`
