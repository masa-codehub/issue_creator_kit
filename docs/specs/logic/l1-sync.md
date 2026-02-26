# L1 Sync Service Specification

## 1. Overview

- **Responsibility**: 親 Issue (L1) の本文内にある一時 ID チェックリストを、起票された実 Issue 番号（`#123`）へと一括置換し、GitHub 上で進捗を可視化する。
- **Collaborators**: `IGitHubAdapter`, `TaskActivationUseCase`.

## 2. Data Structures (Models)

### 2.1. SyncContext

- **Schema**:
  ```python
  class SyncContext:
      l1_id: int
      id_map: Dict[str, int]  # task_id -> issue_number
      max_retries: int = 3
  ```

## 3. Interfaces (API/Methods)

### 3.1. L1SyncService.sync_checklist()

- **Signature**: `sync_checklist(l1_id: int, in_memory_map: Dict[str, int]) -> int`
- **Contract**:
  - **Pre-conditions**: `in_memory_map` が空でないこと。
  - **Post-conditions**: L1 Issue の本文が、可能な限り多くの置換を反映して更新されている。
- **Exceptions**: `GitHubAPIError` (通信不能または API エラー), `Exception` (予期せぬエラー).

## 4. Logic & Algorithms

### 4.1. Replacement Algorithm (apply_replacement)

1.  **Sorting (Longest Match First)**:
    - `in_memory_map` のキー（一時 ID）を文字列の**長さの降順**でソートする。
    - 理由: `task-010-01` が `task-010-011` の一部として誤置換されるのを防ぐため。
2.  **Regex Construction**:
    - パターン: `(- \[[ xX]\]\s+)(ID_1|ID_2|...)(?!\S)`
    - `(?!\S)` (Negative Lookahead) により、ID の直後に非空白文字が続かないことを保証。
3.  **[Planned] Atomic Read-Modify-Write (Concurrency Control)**:
    - _Note: 以下のステップは将来的な拡張予定であり、現在の実装には含まれていない。_
    - GitHub API から `body` と `etag` を取得。
    - ローカルで置換処理を実行。
    - `If-Match: {etag}` ヘッダーを付けて PATCH リクエスト。
    - 412 Conflict 時は指数バックオフ（1s, 2s...）を伴うリトライを実施。

## 5. Traceability

- **Merged Files**:
  - `adr-010-l1-sync-logic.md` (Legacy)
  - `adr-010-l1-sync-logic-audit.md` (Legacy)
  - `adr-l1-automation-core.md` (Legacy)
