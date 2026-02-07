# ADR-008 Domain Models Specification

## Overview
ADR-008「Scanner Foundation」において使用されるドメインモデルのデータ構造と制約を定義する。
本仕様は Pydantic v2 を用いた実装の設計図となり、物理ファイルからパースされたメタデータの整合性を保証するガードレールとして機能する。

## Data Types (Value Objects)

### TaskID
- **Base Type**: `str`
- **Regex**: `^task-\d{3}-\d{2,}$` (例: `task-008-01`)
- **Legacy Support**: `^\d{3}-T\d+(-[A-Z0-9-]+)?$` (例: `007-T3-01`) は読み取り専用で許容する。

### ADRID
- **Base Type**: `str`
- **Regex**: `^adr-\d{3}-[a-z0-9-]+$` (例: `adr-008-cleanup`)

## Schema Definition

### ADR Model
ADR（Architecture Decision Record）のメタデータを表現する。

| Field | Type | Required | Description | Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `id` | `ADRID` | Yes | ユニーク識別子 | `adr-\d{3}-.*` |
| `title` | `str` | Yes | ADR のタイトル | |
| `status` | `str` | Yes | ステータス | `Draft`, `Approved`, `Postponed`, `Superseded` |
| `date` | `str` | No | 作成日 | ISO 8601 (`YYYY-MM-DD`) |

### Task Model
タスク（Issue Draft）のメタデータを表現する。

| Field | Type | Required | Description | Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `id` | `TaskID` | Yes | ユニーク識別子 | `task-\d{3}-\d{2,}` |
| `title` | `str` | Yes | タスクのタイトル | |
| `status` | `str` | Yes | ステータス | `Draft`, `Ready`, `Issued`, `Completed`, `Cancelled` |
| `parent` | `ADRID` | Yes | 親 ADR の ID | 有効な ADRID 形式であること |
| `depends_on` | `List[TaskID]` | Yes | 依存するタスク ID | |
| `issue_id` | `int` | No | GitHub Issue 番号 | `status` が `Issued` 以上で必須 |

## Verify Criteria (TDD)

### Happy Path
| Input ID | Expected Result | Reason |
| :--- | :--- | :--- |
| `adr-008-test` | Success | Valid ADRID format |
| `task-008-01` | Success | Valid TaskID format |
| `007-T3-01` | Success | Legacy format (ReadOnly) |

### Error Path
| Input ID | Expected Result | Reason |
| :--- | :--- | :--- |
| `TASK-001-01` | ValidationError | Uppercase not allowed |
| `adr-8-test` | ValidationError | Must have 3 digits for ADR number |
| `task-008-1` | ValidationError | Task sequence must be at least 2 digits |
| `adr-008_test` | ValidationError | Underscore not allowed |

### Business Logic Guardrails
- `status='Issued'` かつ `issue_id=None` の場合、`ValidationError` を送出すること。
- `parent` に自分自身の ID を指定した場合（自己参照）、`ValidationError` を送出すること。
