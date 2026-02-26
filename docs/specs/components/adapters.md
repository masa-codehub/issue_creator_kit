# Infrastructure Adapters Specification

## 1. Overview

- **Responsibility**: 外部リソース（FileSystem, Git, GitHub）との境界を抽象化し、UseCase 層へクリーンなインターフェースを提供する。
- **Collaborators**: 全ての UseCase 層。

## 2. Data Structures (Models)

### 2.1. Common Exceptions

| Name                  | Base Class            | Description            |
| :-------------------- | :-------------------- | :--------------------- |
| `InfrastructureError` | `RuntimeError`        | 基底クラス。           |
| `GitHubAPIError`      | `InfrastructureError` | GitHub API 連携失敗。  |
| `GitOperationError`   | `InfrastructureError` | Git コマンド実行失敗。 |
| `FileSystemError`     | `InfrastructureError` | ファイル操作失敗。     |

## 3. Interfaces (API/Methods)

### 3.1. GitAdapter

- `checkout(branch, create=False)`: ブランチ切り替え。
- `add(paths)`, `commit(message)`, `push()`: 標準的な Git 操作。
- `move_file(src, dst)`: `git mv` を用いた移動。

### 3.2. FileSystemAdapter

- `read_document(path) -> Document`: フロントマターを含むドキュメントの読み込み。
- `write_file(path, content)`: ファイル書き込み。
- `safe_move_file(src, dst_dir)`: 安全な物理移動。
- `find_file_by_id(task_id, search_dirs) -> Path`: メタデータの ID に基づくファイル検索。

## 4. Logic & Algorithms

### 4.1. Atomic Move Sequence

GitHub 同期 -> メタデータ更新 -> 物理アーカイブ移動 の一連のプロセスを原子的に扱うためのエラーハンドリングポリシー（詳細は各アダプターの実装に依存）。

### 4.2. File ID Lookup

`find_file_by_id` は高速なテキストスキャンまたは `read_document` を併用し、フロントマター内の `id:` フィールドを優先的に検索する。

## 5. Traceability

- **Merged Files**:
  - `infra_adapters.md` (Legacy)
- **Handover Constraints**:
  - N/A (GitHub specific parts moved to `github-adapter.md`)
