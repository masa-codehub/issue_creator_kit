# 詳細設計: 共通ユーティリティ関数インターフェース (ADR-002)

## 1. 目的
ADR-002 の実装（Phase 2）に先立ち、共通で使用するユーティリティ関数のインターフェース（型、引数、戻り値）を定義し、一貫性を確保する。

## 2. 関数定義

### 2.1. `parse_metadata(content: str) -> Dict[str, str]`
Markdownコンテンツからメタデータセクションを解析し、辞書形式で返す。

- **引数**: 
    - `content`: Markdown形式の文字列
- **戻り値**: 
    - キーと値のペアを含む辞書
- **設計の根拠**: 既存の `create_issues.py` のロジックを一般化し、`docs/specs/metadata-logic-spec.md` で定義された正規表現パターンをサポートする。

### 2.2. `update_metadata(content: str, updates: Dict[str, str]) -> str`
Markdownコンテンツ内の既存のメタデータを指定された値で更新し、更新後のコンテンツを返す。

- **引数**:
    - `content`: 元のMarkdown文字列
    - `updates`: 更新したいキーと値の辞書
- **戻り値**:
    - 更新後のMarkdown文字列
- **設計の根拠**: `metadata-logic-spec.md` で確立された置換用正規表現を使用して、メタデータの値を安全に書き換える。

### 2.3. `safe_move_file(src_path: Path, dst_dir: Path, overwrite: bool = False) -> Path`
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
- **設計の根拠**: InboxからApprovedへの移動やアーカイブ処理を、例外処理を含めて共通化する。

## 3. 利用ライブラリ
- `typing`: 型ヒントの提供
- `pathlib`: オブジェクト指向なパス操作
- `re`: 正規表現によるテキスト処理

## 4. 今後の予定
本定義に基づき、Phase 2 において `pytest` によるテスト駆動開発（TDD）で実装を行う。
