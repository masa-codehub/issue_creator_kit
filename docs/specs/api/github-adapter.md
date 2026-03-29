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

### 3.5. `add_labels(issue_number: int, labels: list[str]) -> None`

- **Signature**: `add_labels(issue_number: int, labels: list[str]) -> None`
- **Contract**: 指定された Issue または Pull Request に `labels` リストを追加する。既存のラベルは保持される。
- **Method**: `POST /repos/{owner}/{repo}/issues/{issue_number}/labels`
- **Payload**: `{"labels": labels}`
- **Note**:
  - 既存のラベルを維持しつつ、新しいラベルのみを追加したい場合に使用する。

### 3.6. `update_issue_labels(issue_number: int, labels: list[str]) -> None`

- **Signature**: `update_issue_labels(issue_number: int, labels: list[str]) -> None`
- **Contract**: 指定された Issue または Pull Request のラベルを、提供された `labels` リストで完全に置き換える。
- **Method**: `PUT /repos/{owner}/{repo}/issues/{issue_number}/labels`
- **Payload**: `{"labels": labels}`
- **Constraint**: このメソッドは非追加的な（既存ラベルの削除を伴う）操作を行うため、呼び出し側は保持すべき全てのラベルを明示的に引数に含める必要がある。
- **Note**:
  - 既存のラベルセットを完全に上書きしたい場合に使用する。
  - フェーズ遷移など、特定のラベルを正確に入れ替えたい場合に適している。
  - **重要**: 空の `labels` リストを渡した場合、当該 Issue から全てのラベルが削除される。

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
