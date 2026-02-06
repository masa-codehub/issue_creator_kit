# 能動的偵察レポート (Reconnaissance Report)

## 1. 調査対象と意図 (Scope & Context)
- **ユーザー依頼のキーワード:** `[TDD] Infrastructure Implementation (Infra)`, `find_file_by_id`, `sync_issue`
- **調査の目的:** ADR-007に基づくインフラ層（FileSystemAdapter, GitHubAdapter）の未実装メソッドの特定と、既存コードおよびインターフェース（Protocol）との整合性の確認。

## 2. 収集された事実 (Evidence)

### A. ドキュメント上の規定 (SSOT)
- **[Source]:** `docs/specs/components/infra_adapters.md`
  - **事実・規定:** 
    - `GitHubAdapter`: `sync_issue(doc: Document) -> int` の実装。タイトル検索ロジック（`is:issue is:open in:title`）を含む。
    - `FileSystemAdapter`: `find_file_by_id(task_id: str, search_dirs: list[str]) -> Path` の実装。
    - 共通例外: `InfrastructureError`, `GitHubAPIError`, `GitHubRateLimitError`, `FileSystemError` 等の送出。
- **[Source]:** `src/issue_creator_kit/domain/interfaces.py`
  - **事実・規定:** `IGitHubAdapter`, `IFileSystemAdapter` Protocols が定義されており、`sync_issue` や `find_file_by_id` が含まれている。

### B. 実装の現状 (Codebase Reality)
- **[File]:** `src/issue_creator_kit/infrastructure/filesystem.py`
  - **事実:** `find_file_by_id` が未実装。既存メソッド（`read_document`, `update_metadata` 等）は引数に `Path` を期待しているが、インターフェースは `Path | str` を許容している可能性がある。
- **[File]:** `src/issue_creator_kit/infrastructure/github_adapter.py`
  - **事実:** `sync_issue`, `find_or_create_issue` が未実装。エラー時に `RuntimeError` を送出しており、独自例外（`GitHubAPIError` 等）を使用していない。

### C. 物理構造と依存関係 (Structure & Dependencies)
- **ディレクトリ:** `src/issue_creator_kit/infrastructure/`
- **テスト:** `tests/unit/infrastructure/`
- **依存関係:** `requests` (GitHub), `pathlib`, `shutil`, `yaml` (FileSystem).

## 3. 発見された制約と矛盾 (Constraints & Contradictions)
- **制約事項:** `interfaces.py` で定義されたメソッド名や引数の変更は禁止。
- **SSOTとの乖離:** `GitHubAdapter` の例外クラスが独自例外になっていない。
- **未実装機能:** 
    - `FileSystemAdapter`: `find_file_by_id` (IDベースのファイル検索)
    - `GitHubAdapter`: `sync_issue` (Documentオブジェクトとの同期), `find_or_create_issue` (重複防止検索)

## 4. 補足・未調査事項 (Notes & Unknowns)
- `find_file_by_id` の「高速なテキスト検索」が具体的にどの程度の規模（grep等を使うか、単に全読みするか）を想定しているか。現時点では `read_document` もしくは `re` による走査を想定。
- `GitHubAdapter` におけるリトライポリシー（指数バックオフ）の実装要否（仕様書には「推奨」とある）。
