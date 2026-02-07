# 目標定義書 (Goal Definition) - PR #292

## 1. SMARTゴール (Specific, Measurable, Achievable, Relevant, Time-bound)

- **Specific:**
  - `FileSystemAdapter`: `find_file_by_id` の実装（正規表現による高速検索）。全メソッドの `Path | str` 引数対応。
  - `GitHubAdapter`: `sync_issue`, `find_or_create_issue` の実装。独自例外（`GitHubAPIError`等）の導入。
- **Measurable:**
  - `pytest tests/unit/infrastructure/` でカバレッジ 90% 以上を達成。
  - `mypy .` および `ruff check .` が警告なしでパス。
  - `IGitHubAdapter` / `IFileSystemAdapter` の Protocol を完全に満たす（`test_protocol_conformance` の追加）。
- **Achievable:** 既存の `requests` および `pathlib` の知識で実装可能。モック（`pyfakefs`, `unittest.mock`）により外部依存なしでテスト可能。
- **Relevant:** ADR-007 のタスクライフサイクル（GitHub同期と物理移動）を成立させるための必須要件。
- **Time-bound:** このセッション内で実装、テスト、PR作成までを完了。

## 2. 成果物 (Deliverables)

- `src/issue_creator_kit/infrastructure/filesystem.py`
- `src/issue_creator_kit/infrastructure/github_adapter.py`
- `tests/unit/infrastructure/test_filesystem.py` (更新・追加)
- `tests/unit/infrastructure/test_github_adapter.py` (更新・追加)

## 3. 検証方法 (Verification Methods)

- **DoD (Definition of Done) チェックリスト:**

  - [ ] `FileSystemAdapter.find_file_by_id` が `_archive/` を含む複数ディレクトリから ID 指定でファイルを特定できる。
  - [ ] `GitHubAdapter.sync_issue` が `Document` オブジェクトからタイトル・本文・ラベルを正しくマッピングし、必要に応じて更新または作成を行う。
  - [ ] GitHub API エラー時に `GitHubAPIError` または `GitHubRateLimitError` が送出される。
  - [ ] すべてのインフラ操作が `InfrastructureError` のサブクラスとして定義された例外を投げる。

- **検証コマンド:**

  ```bash
  # テスト実行
  pytest tests/unit/infrastructure/ --cov=src/issue_creator_kit/infrastructure/

  # 静的解析
  ruff check src/issue_creator_kit/infrastructure/
  mypy src/issue_creator_kit/infrastructure/
  ```

## 4. 依存関係とリスク (Risks)

- **リスク:** `GitHubAdapter` の `sync_issue` におけるタイトル検索が、非常に似たタイトルの Issue を誤検知する可能性。
- **対策:** 検索クエリを厳密に（IDプレフィックスを含めて）構成し、ヒットしない場合は新規作成に倒す。
