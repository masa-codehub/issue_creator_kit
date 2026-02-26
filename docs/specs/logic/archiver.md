# File Archiver (Physical Removal) Specification

## 1. Overview

- **Responsibility**: 起票が完了したドラフトファイルをローカルの Git リポジトリから物理的に削除し、Pure Active Git 状態を維持する。
- **Responsibility Shift**: ADR-013 により、`_archive/` ディレクトリへの「移動・固定」から、GitHub を SSOT とした「物理削除」へと責務が変更された。

## 2. Data Structures (Models)

### 2.1. RemovalTarget

- **Schema**:
  ```python
  class RemovalTarget:
      task_id: str
      file_path: Path
      is_processed: bool
  ```

## 3. Interfaces (API/Methods)

### 3.1. FileArchiver.remove_processed_file()

- **Signature**: `remove_processed_file(target: RemovalTarget) -> bool`
- **Contract**:
  - **Pre-conditions**: `is_processed` が `True` であり、対応する Issue が GitHub 上に実在すること。
  - **Post-conditions**: `file_path` が存在しなくなる。
- **Exceptions**: `OSError` (Permission denied).

## 4. Logic & Algorithms

### 4.1. Physical Removal Flow

1.  **Safety Check**: 指定された `file_path` が実際に存在し、かつその内容（ID）が `target.task_id` と一致することを再確認する。
2.  **Deletion**:
    - `os.remove(file_path)` を実行。
    - ディレクトリが空になった場合、`.gitkeep` が存在しない限りディレクトリ自体の削除も検討する（オプション）。
3.  **Logging**: 削除されたタスク ID とファイルパスをログに出力する。

### 4.2. Error Handling

- **Missing File**: 削除対象のファイルが既に存在しない場合、他のプロセスまたは手動で削除されたものと見なし、成功として扱う（Idempotency）。
- **Dry Run Support**: `dry-run` モード時は削除を行わず、削除予定のログ出力のみに留める。

## 5. Traceability

- **Merged Files**:
  - `adr-010-physical-fixation.md` (Legacy)
- **Handover Constraints**:
  - ADR-013: 「物理アーカイブの全廃」方針を直接具現化。
