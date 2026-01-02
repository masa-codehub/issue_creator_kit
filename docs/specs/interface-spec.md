# 詳細設計: インフラストラクチャ層インターフェース (ADR-002)

## 1. 目的
本ドキュメントは、`issue_creator_kit` におけるインフラストラクチャ層（ファイルシステム、外部API）およびドメインモデル（ドキュメント）のインターフェース定義である。
実装は `src/issue_creator_kit/infrastructure/` および `src/issue_creator_kit/domain/` に配置される。

## 2. ドメインモデル

### 2.1. `Document` (`src/issue_creator_kit/domain/document.py`)
Markdownファイルの構造（メタデータと本文）を表現するドメインオブジェクト。

#### プロパティ
- `content: str`: ドキュメントの本文（Markdown形式）
- `metadata: dict[str, Any]`: ドキュメントのメタデータ（タイトル、ステータス等）

#### メソッド

##### `parse(cls, text: str) -> "Document"`
テキスト（ファイル内容）を解析し、`Document` オブジェクトを生成する。
- **引数**:
    - `text`: ファイルの全文
- **戻り値**: `Document` インスタンス
- **仕様**:
    - YAML Frontmatter (`---` 区切り) に対応する。
    - Markdown List Metadata (`- **Key**: Value`) にも対応する（後方互換性のため）。

##### `to_string(self, use_frontmatter: bool = True) -> str`
`Document` オブジェクトを文字列（ファイル保存用フォーマット）に変換する。
- **引数**:
    - `use_frontmatter`: `True` の場合、YAML Frontmatter 形式を使用する。 `False` の場合、Markdown List Metadata 形式を使用する。
- **戻り値**: 文字列化されたドキュメント

## 3. インフラストラクチャ

### 3.1. `FileSystemAdapter` (`src/issue_creator_kit/infrastructure/filesystem.py`)
ローカルファイルシステムへのアクセスを抽象化するアダプター。

#### メソッド

##### `read_document(self, file_path: Path) -> Document`
Markdownファイルを読み込み、`Document` オブジェクトとして返す。
- **引数**:
    - `file_path`: 読み込むファイルのパス
- **戻り値**: `Document` インスタンス
- **例外**:
    - `FileNotFoundError`: 指定されたファイルが存在しない場合

##### `save_document(self, file_path: Path, document: Document, use_frontmatter: bool = True) -> None`
`Document` オブジェクトを指定されたパスに保存する。
- **引数**:
    - `file_path`: 保存先のパス
    - `document`: 保存するドキュメントオブジェクト
    - `use_frontmatter`: Frontmatter形式を使用するかどうか（デフォルト: `True`）
- **戻り値**: なし

##### `update_metadata(self, file_path: Path, updates: dict[str, Any]) -> None`
指定されたファイルのメタデータのみを部分的に更新し、保存する。同時実行制御（排他ロック）を行う。
- **引数**:
    - `file_path`: 対象ファイルのパス
    - `updates`: 更新・追加したいキーと値の辞書
- **戻り値**: なし
- **例外**:
    - `FileNotFoundError`: 指定されたファイルが存在しない場合
- **仕様**:
    - `fcntl` が利用可能な環境ではファイルロックを使用し、競合を防ぐ。

##### `safe_move_file(self, src_path: Path, dst_dir: Path, overwrite: bool = False) -> Path`
ファイルを指定されたディレクトリへ安全に移動する。
- **引数**:
    - `src_path`: 移動元ファイルのパス
    - `dst_dir`: 移動先ディレクトリのパス
    - `overwrite`: 既存ファイルを上書きするかどうか
- **戻り値**: 移動後のファイルパス
- **例外**:
    - `FileNotFoundError`: 移動元が存在しない場合
    - `FileExistsError`: 上書き禁止かつ移動先が既に存在する場合

##### `list_files(self, dir_path: Path, pattern: str = "*") -> list[Path]`
指定されたディレクトリ内のファイルをリストアップする。
- **引数**:
    - `dir_path`: 対象ディレクトリのパス
    - `pattern`: 検索するglobパターン（デフォルト: `*`）
- **戻り値**: 見つかったファイルのパスリスト（`Path` オブジェクト）

### 3.2. `GitHubAdapter` (`src/issue_creator_kit/infrastructure/github_adapter.py`)
GitHub API へのアクセスを抽象化するアダプター。

#### 初期化
`__init__(self, token: str | None = None, repo: str | None = None)`
- **引数**:
    - `token`: GitHub Personal Access Token (省略時は環境変数 `GH_TOKEN` または `GITHUB_TOKEN` を使用)
    - `repo`: リポジトリ名 (例: `owner/repo`, 省略時は環境変数 `GITHUB_REPOSITORY` を使用)

#### メソッド

##### `create_issue(self, title: str, body: str, labels: list[str] | None = None) -> int`
GitHub Issue を新規作成する。
- **引数**:
    - `title`: Issue のタイトル
    - `body`: Issue の本文
    - `labels`: 付与するラベルのリスト（オプション）
- **戻り値**: 作成された Issue の番号 (number)
- **例外**:
    - `ValueError`: リポジトリ情報が未設定の場合
    - `RuntimeError`: API呼び出しが失敗した場合（ステータスコードが 201 以外）

## 4. 利用ライブラリ
- `typing`: 型ヒント
- `pathlib`: パス操作
- `shutil`: ファイル移動
- `PyYAML`: YAML解析 (`yaml`)
- `requests`: HTTPクライアント
- `fcntl`: ファイルロック (Unix系のみ)
