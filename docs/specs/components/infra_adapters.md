# Infrastructure Adapters Specification

## 1. 概要
Infrastructure 層における各 Adapter（GitHub, Git, FileSystem）のインターフェースと期待される振る舞いを定義する。
本仕様は、外部システムとの境界を明確にし、UseCase 層が特定のライブラリや実装詳細に依存せずに、これらの機能を利用できるようにすることを目的とする。

## 2. 共通例外 (Common Exceptions)

インフラ層でのエラーは、標準の例外を継承した以下の独自例外（またはそのエイリアス）として送出されることを期待する。

| 例外名 | 親クラス | 説明 |
| :--- | :--- | :--- |
| `InfrastructureError` | `RuntimeError` | 全てのインフラ層エラーの基底クラス。 |
| `GitHubAPIError` | `InfrastructureError` | GitHub API 呼び出し失敗（4xx, 5xx）時に送出される。 |
| `GitOperationError` | `InfrastructureError` | Git コマンド実行失敗（非ゼロ終了）時に送出される。 |
| `FileSystemError` | `InfrastructureError` | ファイル操作失敗（権限不足等）時に送出される。 |

## 3. GitHubAdapter

### 3.2. `find_or_create_issue(title: str, body: str) -> int`
同一タイトルの Open 状態の Issue を検索し、存在すればその番号を、存在しなければ新規作成してその番号を返す。
- **検索ロジック**: `is:issue is:open in:title "{title}"` をクエリとして検索を実行する。
- **複数ヒット時**: 最も新しく作成された Issue を採用する。
- **戻り値**: Issue 番号
- **例外**: `GitHubAPIError`

## 4. GitAdapter

### 4.2. `commit(message: str) -> None`
ステージングされた変更をコミットする。
- **引数**: `message`: コミットメッセージ
- **特殊挙動**: ステージングされた変更が一切ない場合、例外を送出せず、何もしない（Success扱い）。
- **例外**: コミットメッセージが空の場合や、その他の Git エラー時は `GitOperationError` を送出する。

### 4.3. `push(remote: str = "origin", branch: str = "main") -> None`
リモートへプッシュする。
- **例外**: `GitOperationError`

## 5. FileSystemAdapter

ローカルファイルシステム上の操作を担当する。

### 5.1. `read_document(file_path: Path) -> Document`
ファイルを読み込み、`Document` ドメインオブジェクトとして返す。
- **例外**: ファイル不在時は `FileNotFoundError`

### 5.2. `update_metadata(file_path: Path, updates: dict[str, Any]) -> None`
ファイルのメタデータ部分のみを更新する。既存のファイル形式（YAML Frontmatter または Markdown List）を維持すること。
- **例外**: `FileSystemError`

### 5.3. `safe_move_file(src_path: Path, dst_dir: Path, overwrite: bool = False) -> Path`
ファイルを安全に移動する。
- **引数**:
  - `src_path`: 移動元パス
  - `dst_dir`: 移動先ディレクトリ
  - `overwrite`: 既存ファイルがある場合に上書きするかどうか
- **戻り値**: 移動後のファイルパス
- **例外**: `src_path` 不在時は `FileNotFoundError`。移動先が重複し `overwrite=False` の場合は `FileExistsError`。

### 5.4. `write_file(path: Path | str, content: str) -> None`
指定した内容をファイルに書き込む。
- **例外**: `FileSystemError`

## 6. 検証手順 (Verification)

### 6.1. エラーハンドリングの検証 (TDD Criteria)
- GitHub API が 500 エラーを返した際、`GitHubAPIError` が送出されること。
- Git コマンドが非ゼロの終了コードを返した際、`GitOperationError` が送出されること。
- ディレクトリ作成権限がない場所への `write_file` 実行時に `FileSystemError` が送出されること。

### 6.2. Mock 可能性
- 全てのインターフェースが純粋な Python メソッドとして定義されており、`unittest.mock` 等で容易にスタブ/モック化できること。
- `read_document` の戻り値が `Document` オブジェクトであり、その内部状態を Mock で検証できること。
