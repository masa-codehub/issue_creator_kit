# Reconnaissance Report - Update Infrastructure Adapter Specifications

## 1. 調査目的
FileSystem (Atomic Move) および GitHub API (Issue/Status Sync) との連携インターフェース仕様を更新するための現状把握。

## 2. 収集した事実 (Collected Facts)

### 2.1. 現状の仕様 (`docs/specs/components/infra_adapters.md`)
- **FileSystemAdapter**: `safe_move_file` (shutil.move 使用), `update_metadata` (fcntl ロック使用) が定義されている。
- **GitHubAdapter**: `create_issue`, `find_or_create_issue`, `create_pull_request` などが定義されている。共通例外として `GitHubAPIError`, `GitHubRateLimitError` が定義されているが、実装との乖離がある。

### 2.2. ADR-007 の要件 (`reqs/design/_approved/adr-007-metadata-driven-lifecycle.md`)
- **ディレクトリ構造**: `reqs/tasks/<ADR-ID>/` から `reqs/tasks/_archive/` へのフラットな移動。
- **メタデータ**: `issue_id` の自動追記が必要。
- **ステータス遷移**: `Ready -> Issued` 時に「起票成功 -> メタデータ更新 -> アーカイブ移動」を原子的に行う必要がある。

### 2.3. 現状の実装 (`src/issue_creator_kit/infrastructure/`)
- **`filesystem.py`**: `shutil.move` を使用。メタデータ更新は `fcntl` を使用した書き戻し。
- **`github_adapter.py`**: `requests` を直接使用。リトライロジックや `GitHubAPIError` 等の独自例外は未実装。

### 2.4. 現状のテスト (`tests/unit/infrastructure/test_github_adapter.py`)
- 基本的な成功ケースと初期化エラーのテストのみ。APIエラー時の上位層への波及（ファイル移動の抑止）を検証するテストはない。

## 3. ギャップ分析 (Gap Analysis)
- **FileSystem**: `id` をキーとしたファイル検索ロジックが仕様に未定義。アーカイブ移動の「原子性」の定義が曖昧（ shutil.move だけで十分か、OSレベルの atomic rename を意識するか）。
- **GitHub**: メタデータのどのフィールドを Issue のどの項目（Title, Body, Labels）にマッピングするかの定義が不足。`issue_id` を抽出してメタデータに書き戻す際の一貫性保証が未定義。

## 4. 参照エビデンス
- `reqs/design/_approved/adr-007-metadata-driven-lifecycle.md` (Decision 4: ステータス遷移と自動移動ルール)
- `docs/specs/components/infra_adapters.md` (Section 3 & 5)
