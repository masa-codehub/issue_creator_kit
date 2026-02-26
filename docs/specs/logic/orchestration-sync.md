# Orchestration & L1 Sync Specification

## Overview

外部リポジトリの走査に対応した `OrchestratorService` の拡張と、冪等性を担保した `L1SyncService` の置換ロジック、および GitHub API の楽観的ロック（Optimistic Locking）を用いた同期フローを定義する。

## 1. OrchestratorService Interface

### 1.1. Method: execute

将来的な拡張性（カスタムラベル、除外ディレクトリ設定等）を考慮し、`config` 引数を追加する。

#### Signature

```python
def execute(
    self,
    root_path: Path | str,
    dry_run: bool = False,
    config: Optional[Config] = None
) -> OrchestrationResult:
    ...
```

#### Input

| Name        | Type               | Description                                  |
| :---------- | :----------------- | :------------------------------------------- |
| `root_path` | `Path \| str`      | 走査対象のルートディレクトリ。               |
| `dry_run`   | `bool`             | True の場合、GitHub への書き込みを行わない。 |
| `config`    | `Optional[Config]` | 実行オプション（将来の拡張用）。             |

## 2. L1SyncService Logic

### 2.1. Method: sync_checklist

L1 Issue の本文内にある一時IDチェックリストを、実Issue番号へ一括更新する。

#### Algorithm: Idempotent Replacement

`re.sub` とコールバック関数（`repl`）を用いて、1回のスキャンで安全に置換を行う。

1. **Regex Pattern**: `r"(- \[[ xX]\]\s+)(task-\d{3}-\d{2,})(?!\S)"`
   - プレフィックスとしてチェックリスト構文 (`- [ ]`, `- [x]`) を必須とする。
   - すでに `#123` のように置換済みの箇所は、このパターンにマッチしないためスキップされる（冪等性の担保）。
2. **Replacement Strategy**:
   - プレフィックスを保持し、後続の `task-XXX-NN` を `#<issue_no>` に置換する。

#### Algorithm: Read-Modify-Write with Retry

ETag を用いた楽観的ロックにより、データの喪失（Lost Update）を防ぐ。

1. **GitHubAdapter 拡張要件**:
   - `get_issue(l1_id)` は `body` と共に `etag` を返却すること。
   - `patch_issue(l1_id, body, etag)` は、`If-Match: <etag>` ヘッダーを付けてリクエストすること。
2. **Retry Flow**:
   - GitHub API が `409 Conflict` または `412 Precondition Failed` を返した場合、リトライを実行する。
   - **リトライ回数**: 最大 3 回。
   - **Exponential Backoff**:
     - Base: 1.0s
     - Factor: 2.0
     - 待機時間: 1s -> 2s -> 4s

## 3. Data Structures

### 3.1. Config (Optional)

将来的な拡張のためのプレースホルダ。

```python
class Config(TypedDict, total=False):
    labels: list[str]
    exclude_patterns: list[str]
```

## 4. Test Cases (TDD Criteria)

### 4.1. Replacement Idempotency

| Input Body                            | ID Map                 | Expected Output Body           |
| :------------------------------------ | :--------------------- | :----------------------------- |
| `- [ ] task-010-01`                   | `{"task-010-01": 123}` | `- [ ] #123`                   |
| `- [x] #123` (既に置換済み)           | `{"task-010-01": 123}` | `- [x] #123` (変化なし)        |
| `- [ ] task-010-01<br><br>- [x] #590` | `{"task-010-01": 124}` | `- [ ] #124<br><br>- [x] #590` |

### 4.2. Conflict Handling

- **Scenario**: `patch_issue` で 409 Conflict が発生。
- **Expected Behavior**:
  1. 1s 待機。
  2. `get_issue` を再実行して最新の `body` と `etag` を取得。
  3. 置換を再実行。
  4. `patch_issue` を再試行。
  5. 3回失敗した場合は `SyncError` を送出。
