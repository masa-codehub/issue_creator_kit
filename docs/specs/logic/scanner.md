# File System Scanner Specification

## 1. Overview

- **Responsibility**: 物理ファイルシステムから ADR および Task のドラフト（Active ファイル）を検出し、ドメインモデルへと変換する。ADR-013 に基づき、アーカイブディレクトリの走査を完全に廃止し、Pure Active Git 状態を維持する。
- **Collaborators**: `DocumentParser`, `FileSystem`.

## 2. Data Structures (Models)

### 2.1. ScanConfig

- **Schema**:
  ```python
  class ScanConfig:
      root_path: Path
      include_dirs: List[str]  # e.g., ["design/_approved", "tasks"]
      exclude_patterns: List[str]  # e.g., ["**/_archive/**", "**/_inbox/**"]
  ```

## 3. Interfaces (API/Methods)

### 3.1. FileSystemScanner.scan()

- **Signature**: `scan(config: ScanConfig) -> List[Document]`
- **Contract**:
  - **Pre-conditions**: `root_path` が存在し、読み取り可能であること。
  - **Post-conditions**: 返却されるリストには、アーカイブディレクトリ内のファイルが含まれていないこと。
- **Exceptions**: `FileNotFoundError` (root_path 欠如), `PermissionError`.

## 4. Logic & Algorithms

### 4.1. Active File Scanning (Constraint 4)

1.  **ディレクトリ走査**: `config.root_path` を起点に、`include_dirs` で指定されたディレクトリを再帰的に走査する。
2.  **フィルタリング**:
    - **Physical Archive Exclusion**: パスに `_archive` が含まれる場合は、ADR-013 の「アーカイブ全廃」方針に基づき、**無条件にスキップ**する。
    - **Glob Exclusion**: `exclude_patterns` に一致するパスをスキップする。
3.  **モデル変換**:
    - 各 `.md` ファイルを `DocumentParser` でパースし、`Document` オブジェクトを生成。
    - パース失敗時は、そのファイルパスと行番号を含むエラーを上位（Validator等）へ報告する。
4.  **グローバル ID 重複チェック**:
    - スキャンされたドキュメント間で ID が重複している場合、`DUPLICATE_ID` エラーを送出する (Fail-fast)。

## 5. Traceability

- **Merged Files**:
  - `scanner_logic.md` (Legacy)
- **Handover Constraints**:
  - **Constraint 4**: アーカイブディレクトリのスキャン除外を 4.1 で担保。
