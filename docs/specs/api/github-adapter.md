# GitHub Adapter Specification

## 1. Overview

- **Responsibility**: GitHub API を介した Issue および Pull Request の操作を担当するインフラ層のアダプター。
- **Collaborators**: `ScannerService`, `RelayUseCase`, `OrchestratorService` 等、外部連携を必要とする全ての UseCase/Domain Service。

## 2. Data Structures (Models)

### 2.1. TaskStatus (Data Class)

- **Schema**:
  ```python
  @dataclass
  class TaskStatus:
      number: int
      state: str  # "open" | "closed"
      is_completed: bool
      updated_at: datetime
      metadata: dict[str, Any]
  ```

### 2.2. GitHub Label Attributes

| Label Name  | Color     | Description                                           |
| :---------- | :-------- | :---------------------------------------------------- |
| `adr:{NNN}` | `#0052cc` | ADR IDを一意に識別する。`{NNN}` は3桁ゼロ埋めの数値。 |
| `task`      | `#d4c5f9` | タスクであることを示すシステムラベル。                |

## 3. Interfaces (API/Methods)

### 3.1. `get_issue(number: int) -> dict[str, Any]`

- **Signature**: `get_issue(number: int) -> dict[str, Any]`
- **Contract**: 指定された番号の Issue 情報を取得する。レスポンスには `body` と `etag` を含めること。
- **Exceptions**: `GitHubAPIError` (404等)

### 3.2. `patch_issue(number: int, body: str, etag: str | None = None) -> None`

- **Signature**: `patch_issue(number: int, body: str, etag: str | None = None) -> None`
- **Contract**: Issue の本文を更新する。`etag` が指定されている場合は `If-Match` ヘッダーを使用し、楽観的ロックを行う。
- **Exceptions**: `GitHubAPIError` (412 Precondition Failed 等)

### 3.3. `search_issues(query: str) -> list[dict[str, Any]]`

- **Signature**: `search_issues(query: str) -> list[dict[str, Any]]`
- **Constraint (Mandatory)**: **Constraint 2**: 検索において、メタデータクエリ (`""id": "task-A""`) を優先し、ラベル検索をフォールバックまたはフィルタ条件として併用しなければならない。
- **Contract**: 指定された条件に一致する Issue を検索する。
- **Pagination**: 最大 10 ページまで走査する Safety Limit を設ける。

### 3.4. `check_task_status(task_id: str) -> TaskStatus | None`

- **Contract**: 指定された `task_id` を持つ Issue の状態を確認する。

## 4. Logic & Algorithms

### 4.1. Deterministic Selection

検索結果に複数の Issue が含まれる場合、Issue 番号 (`number`) が最大のもの（最新）を正本として採用する。

### 4.2. ETag Extraction

レスポンスヘッダーの `ETag` から取得し、Weak ETag (`W/"..."`) もそのまま文字列として扱う。

### 4.3. Metadata Extraction (Regex)

Issue 本文からメタデータ JSON 文字列を抽出する際は、以下の正規表現を用いる。

- **Pattern**: `<!--\s*metadata:(.*?)\s*-->`
- **Logic**: マッチしたグループ 1 の文字列を JSON としてパースする。

### 4.4. Retry Policy

- **Target**: `429`, `403` (Rate Limit), `502`, `503`, `504`
- **Config**: 最大 3 回、初回 5 秒、指数係数 2 のバックオフ。

### 4.5. Session Caching

- **Policy**: 同一セッション内での重複した API コールを避けるため、`task_id` に紐づく検索結果や Issue 状態をメモリ内にキャッシュする。
- **Scope**: 単一のコマンド実行（`process`, `relay` 等）のライフサイクル内。

## 5. Traceability

- **Merged Files**:
  - `adr-010-github-adapter-ext.md` (Legacy)
  - `github-issue-api-spec.md` (Legacy)
  - `infra_adapters.md` (Legacy) (GitHubAdapter part)
- **Handover Constraints**:
  - [Constraint 2] Metadata query priority in `IGitHubAdapter`.
