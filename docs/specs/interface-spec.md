# 詳細設計: 共通ユーティリティ関数インターフェース (ADR-002)

## 1. 目的
ADR-002 の実装（Phase 2）に先立ち、共通で使用するユーティリティ関数のインターフェース（型、引数、戻り値）を定義する。
本仕様は、メタデータ管理に **YAML Frontmatter** を使用することを前提とする。

## 2. 関数定義

### 2.1. `load_document(file_path: Path) -> Tuple[Dict[str, Any], str]`
Markdownファイルを読み込み、メタデータと本文を分離して返す。

- **引数**: 
    - `file_path`: 読み込むファイルのパス
- **戻り値**: 
    - `(metadata, content)` のタプル
    - `metadata`: YAML Frontmatter から解析された辞書
    - `content`: Frontmatter を除いた本文
- **設計の根拠**: `python-frontmatter` をラップし、ファイルI/Oと解析を一括で行うことで呼び出し側のコードを簡素化する。

### 2.2. `save_document(file_path: Path, metadata: Dict[str, Any], content: str) -> None`
メタデータと本文を指定して、Markdownファイルとして保存（上書き）する。

- **引数**:
    - `file_path`: 保存先のパス
    - `metadata`: 更新後のメタデータ辞書
    - `content`: 本文（変更がない場合は元の本文を渡す）
- **戻り値**: なし
- **設計の根拠**: `frontmatter.dumps` を使用して正しい形式でファイルを再構築する。

### 2.3. `update_metadata(file_path: Path, updates: Dict[str, Any]) -> None`
指定されたファイルのメタデータのみを部分的に更新し、保存する。便利関数。

- **引数**:
    - `file_path`: 対象ファイルのパス
    - `updates`: 更新・追加したいキーと値の辞書
- **戻り値**: なし
- **設計の根拠**: `load_document` -> 辞書更新 -> `save_document` の一連の流れをカプセル化する。

### 2.4. `safe_move_file(src_path: Path, dst_dir: Path, overwrite: bool = False) -> Path`
ファイルを指定されたディレクトリへ安全に移動する。

- **引数**:
    - `src_path`: 移動元ファイルのパス
    - `dst_dir`: 移動先ディレクトリのパス
    - `overwrite`: 既存ファイルを上書きするかどうか
- **戻り値**:
    - 移動後のファイルパス
- **例外**:
    - `FileNotFoundError`: 移動元が存在しない場合
    - `FileExistsError`: 上書き禁止かつ移動先が既に存在する場合

## 3. 利用ライブラリ
- `typing`: 型ヒント
- `pathlib`: パス操作
- `frontmatter`: YAML Frontmatter 解析 (`python-frontmatter`)

## 4. 今後の予定
Phase 2 の実装において、これらの関数を `src/issue_creator_kit/utils.py` に実装する。