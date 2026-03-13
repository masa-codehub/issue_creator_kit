# Document Models Specification

## 1. Overview

- **Responsibility**: システム全体で扱われる設計ドキュメント（ADR）およびタスク（Issue Draft）のデータ構造、バリデーションルール、およびライフサイクル状態を定義する。
- **Collaborators**:
  - `Scanner`: 物理ファイルから本モデルへのパースを担当。
  - `TaskGraphValidator`: モデル間の依存関係（`depends_on`）の検証を担当。
  - `Renderer`: 本モデルから GitHub Issue 本文への変換を担当。
  - `GitHubAdapter`: `Registered` 状態 host ID 解決（Issue 番号取得）を担当。

## 2. Data Structures (Models)

### 2.1. Value Objects

| Term              | Base Type | Regex / Constraints                                                      | Description                             |
| :---------------- | :-------- | :----------------------------------------------------------------------- | :-------------------------------------- |
| **ADRID**         | `str`     | `^(adr&#124;design)-\d{3}(?:-[a-z0-9-]+)?$`                              | ADR または DesignDoc のユニーク識別子。 |
| **TaskID**        | `str`     | `^task-\d{3}-\d{2,}$`                                                    | タスクのユニーク識別子。                |
| **LegacyTaskID**  | `str`     | `^\d{3}-T\d+(-[A-Z0-9-]+)?$`                                             | 読み取り専用でサポートされる旧形式 ID。 |
| **Status (ADR)**  | `str`     | `Literal['Draft', 'Approved', 'Postponed', 'Superseded', 'Implemented']` | ADR のライフサイクル状態。              |
| **Status (Task)** | `str`     | `Literal['Draft', 'Ready', 'Issued', 'Completed', 'Cancelled']`          | タスクのライフサイクル状態。            |

### 2.2. Schema Definitions (Pydantic V2)

#### Common Constraints (ADR-013 Compliance)

- **`type` Field**: `Literal` 型で定義され、**デフォルト値を持ってはならない**。フロントマターでの明示が必須。
- **Discrimination**: `Annotated` と `Union` を用い、`type` フィールドを判別子（Discriminator）として使用する。

#### ADR Model

| Field        | Type                                    | Required | Description                          |
| :----------- | :-------------------------------------- | :------- | :----------------------------------- |
| `id`         | `ADRID`                                 | Yes      | ADR / DesignDoc 識別子。             |
| `type`       | `Literal["adr", "design-doc"]`          | Yes      | **必須**（デフォルト値禁止）。       |
| `title`      | `str`                                   | Yes      | ドキュメントのタイトル。             |
| `status`     | `Status (ADR)`                          | Yes      | 現在の状態。                         |
| `date`       | `str`                                   | No       | ISO 8601 形式の作成/更新日。         |
| `depends_on` | `list[TaskID \| ADRID \| LegacyTaskID]` | Yes      | 依存先リスト（デフォルトは空配列）。 |
| `labels`     | `list[str]`                             | No       | GitHub ラベルリスト。                |

#### Task Model

| Field        | Type                             | Required | Description                                            |
| :----------- | :------------------------------- | :------- | :----------------------------------------------------- |
| `id`         | `TaskID`                         | Yes      | タスク識別子。                                         |
| `type`       | `Literal["task", "integration"]` | Yes      | **必須**（デフォルト値禁止）。                         |
| `title`      | `str`                            | Yes      | タスクのタイトル。                                     |
| `status`     | `Status (Task)`                  | Yes      | 現在の状態。                                           |
| `parent`     | `ADRID`                          | Yes      | 親となる ADR / DesignDoc の ID。                       |
| `role`       | `str`                            | No       | 担当ロール（`arch`, `spec`, `tdd`）。                  |
| `phase`      | `str`                            | No       | 工程フェーズ。                                         |
| `depends_on` | `list[TaskID]`                   | Yes      | 依存先タスク ID リスト。                               |
| `issue_id`   | `int`                            | No       | GitHub Issue 番号（`status` が `Issued` 以降で必須）。 |
| `labels`     | `list[str]`                      | No       | GitHub ラベルリスト。                                  |

#### Derived Properties (Read-only)

| Property     | Return Type   | Logic / Description                                                                                                                                                        |
| :----------- | :------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `adr_number` | `int \| None` | parent（Task）または id（ADR）から 3 桁の数値を抽出 し、整数として返す。 `adr-016` -> `16`, `design-001` -> `1`。 パースに失敗した場合は `None` を返し、例外を送出しない。 |

### 2.3. Example Implementation (Python)

```python
import re
from typing import Annotated, Literal, Union, Optional
from pydantic import BaseModel, Field, TypeAdapter

# Value Objects with strict validation (ADR-013 Compliance)
ADRID = Annotated[str, Field(pattern=r"^(adr|design)-\d{3}(?:-[a-z0-9-]+)?$")]
TaskID = Annotated[str, Field(pattern=r"^task-\d{3}-\d{2,}$")]
LegacyTaskID = Annotated[str, Field(pattern=r"^\d{3}-T\d+(-[A-Z0-9-]+)?$")]

class ADR(BaseModel):
    id: ADRID
    type: Literal["adr", "design-doc"]  # No default value (Strict)
    title: str
    status: Literal["Draft", "Approved", "Postponed", "Superseded", "Implemented"]
    date: Optional[str] = None
    depends_on: list[Union[TaskID, ADRID, LegacyTaskID]] = Field(default_factory=list)
    labels: list[str] = Field(default_factory=list)

    @property
    def adr_number(self) -> Optional[int]:
        match = re.search(r"(?:adr|design)-(\d{3})", self.id)
        return int(match.group(1)) if match else None

class Task(BaseModel):
    id: TaskID
    type: Literal["task", "integration"]  # No default value (Strict)
    title: str
    status: Literal["Draft", "Ready", "Issued", "Completed", "Cancelled"]
    parent: ADRID
    role: Optional[str] = None
    phase: Optional[str] = None
    depends_on: list[Union[TaskID, LegacyTaskID]] = Field(default_factory=list)
    issue_id: Optional[int] = Field(None, gt=0)
    labels: list[str] = Field(default_factory=list)

    @property
    def adr_number(self) -> Optional[int]:
        match = re.search(r"(?:adr|design)-(\d{3})", self.parent)
        return int(match.group(1)) if match else None

# Discriminated Union for strict validation
DocumentType = Annotated[Union[Task, ADR], Field(discriminator="type")]
DocumentAdapter = TypeAdapter(DocumentType)
```

## 3. Interfaces (ID Lifecycle)

### 3.1. ID Lifecycle States

| State          | Format              | Context                                      |
| :------------- | :------------------ | :------------------------------------------- |
| **Temporary**  | `task-\d{3}-\d{2,}` | ローカルのドラフトおよび `id` フィールド。   |
| **Registered** | `int (> 0)`         | GitHub 起票成功後に取得される実 Issue 番号。 |
| **Rendered**   | `#\d+`              | GitHub Issue 本文内での相互参照形式。        |

### 3.2. IDMap Structure

起票済みタスクの解決に使用されるメモリ内キャッシュ。

- **Structure**: `dict[TaskID, int]`
- **Validation**: すべての Value は `1` 以上である必要がある。

## 4. Logic & Algorithms

### 4.1. Normalization Rules

- **Key Normalization**: YAML フロントマターのキーはすべて小文字として扱う。
- **Alias Support**: `ID` -> `id`, `ステータス` -> `status`, `型` -> `type`, `依存` -> `depends_on` などの日本語エイリアスをパース時に正規化する。

### 4.2. SSOT Guardrail (Sync Logic)

`docs/definitions.md` 内の定義と Pydantic モデルの `Literal` 値は、以下のマーカーを用いて整合性が自動検証される。

- `<!-- guardrail-sync: ADR.status -->`
- `<!-- guardrail-sync: Task.status -->`
- `<!-- guardrail-sync: Task.phase -->`
- `<!-- guardrail-sync: Task.role -->`

### 4.3. Phase Compatibility

`Task.phase` においては、新標準（`architecture`, `spec`, `tdd`）に加え、以下の `LEGACY_PHASES` を互換性のために許容する。

- `domain`, `infrastructure`, `usecase`, `interface`, `cleanup`, `test`, `refactor` 等。

## 5. Traceability

### 5.1. Merged Files

本仕様書は以下の旧ドキュメントを統合・廃止したものである。

- `document_model.md` (Legacy)
- `domain_models_adr008.md` (Legacy)
- `adr-010-id-model.md` (Legacy)
- `adr-011-ssot-guardrail.md` (Legacy)

### 5.2. Handover Constraints

- **Constraint 3 (ADR-013)**: Pydantic モデルの `type` フィールドはデフォルト値を持たず、パース失敗時に明示的なエラーメッセージを返さなければならない。

  - **Status**: **Fulfilled** (See Section 2.2).
