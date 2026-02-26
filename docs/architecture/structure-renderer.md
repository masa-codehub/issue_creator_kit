# Issue Renderer Structure & Metadata Schema

## Context

- **Bounded Context:** Issue Lifecycle Management
- **System Purpose:** GitHub Actions が自律的に後続タスクを起動（Autonomous Relay）できるように、機械可読なメタデータを Issue 本文に統合し、レンダリングロジックを独立させる。

## Diagram (C4 Component & Metadata Flow)

### Component Diagram: Issue Rendering Service

```mermaid
C4Component
    title Component Diagram for Issue Rendering

    Container(usecase, "TaskActivationUseCase", "Python", "Orchestrates task activation flow")

    Container_Boundary(domain_service, "Domain Services") {
        Component(renderer, "IssueRenderer", "Domain Service", "Renders Tasks into GitHub Issue format")
        Component(vo, "RenderedIssue", "Value Object", "Structured output containing title, body, and labels")
    }

    Container(model, "Task", "Pydantic Model", "Task definition with metadata (role, phase, etc.)")

    Rel(usecase, renderer, "Uses", "render(task, id_map)")
    Rel(renderer, model, "Reads", "metadata & content")
    Rel(renderer, vo, "Creates", "Structured Result")
    Rel(usecase, vo, "Receives", "Structured Result")
```

### Metadata Integration Flow

```mermaid
graph TD
    A[Task Model] -->|Input| B[IssueRenderer]
    B --> C{Process}
    C -->|1. Resolve IDs| D[Body with #123]
    C -->|2. Format Metadata| E[JSON Block]
    C -->|3. Gen Dependencies| F[## Dependencies Checklist]
    D & E & F --> G[RenderedIssue.body]
```

## Element Definitions (SSOT)

### IssueRenderer

- **Type:** `Component (Domain Service)`
- **Code Mapping:** `src/issue_creator_kit/domain/services/renderer.py`
- **Role (Domain-Centric):** `Task` モデルを GitHub の Issue 形式（タイトル、本文、ラベル）に変換する。ID の解決とメタデータの埋め込みを統制する。
- **Layer (Clean Arch):** `Domain Services`
- **Dependencies:**
  - **Upstream:** `TaskActivationUseCase`
  - **Downstream:** `Task` (Model), `RenderedIssue` (VO)
- **Tech Stack:** Python 3.12, Pydantic
- **Data Reliability:** 冪等な文字列変換。副作用を持たない純粋な関数として振る舞う。
- **Trade-off:** UseCase に直接記述するよりもファイル数は増えるが、レンダリングロジックの単体テストが容易になり、メタデータ形式の変更に対する柔軟性が向上する。

### RenderedIssue

- **Type:** `Component (Value Object)`
- **Code Mapping:** `src/issue_creator_kit/domain/models/renderer.py`
- **Role (Domain-Centric):** レンダリング結果の構造化データ。GitHub API クライアントが必要とする全情報を保持する。
- **Layer (Clean Arch):** `Domain Models`
- **Tech Stack:** Python (Data Class or Pydantic)
- **Fields:**
  - `title`: str (例: "task-011-01: [Arch] ...")
  - `body`: str (Resolved ID + Metadata Block)
  - `labels`: list[str] (Generated based on task role/phase)

## Task Model Extension (ADR-011)

`src/issue_creator_kit/domain/models/document.py` の `Task` モデルに以下のフィールドを追加定義する。

| Field   | Type      | Description            | Values                                                |
| :------ | :-------- | :--------------------- | :---------------------------------------------------- |
| `role`  | `Literal` | 担当エージェントの役割 | `arch` \| `spec` \| `tdd`                             |
| `phase` | `Literal` | 工程ラベル             | `Architecture` \| `Specification` \| `Implementation` |

## Metadata Schema Definition

Issue 本文の末尾に埋め込む `<!-- metadata:{...} -->` 形式の JSON オブジェクト定義。

### JSON Schema

| Key          | Type           | Description                                  | Required |
| :----------- | :------------- | :------------------------------------------- | :------- |
| `id`         | `string`       | プロジェクト一意の Task ID                   | Yes      |
| `type`       | `string`       | ドキュメントタイプ (常に "task")             | Yes      |
| `parent`     | `string`       | 親 ADR ID                                    | Yes      |
| `title`      | `string`       | タスクタイトル                               | Yes      |
| `status`     | `string`       | タスクステータス                             | Yes      |
| `role`       | `string`       | 担当ロール: `arch`, `spec`, `tdd` のいずれか | Yes      |
| `phase`      | `string`       | 工程名                                       | Yes      |
| `depends_on` | `list[string]` | 依存先タスク ID リスト                       | Yes      |
| `labels`     | `list[string]` | 追加の静的ラベルリスト                       | No       |
| `issue_id`   | `integer`      | GitHub Issue 番号（未発行時は null）         | No       |

### Implementation Example (Body Content)

```markdown
# Issue Content Title

Actual content here...

## Dependencies

- [ ] #123 (Resolved from task-010-01)
- [ ] #124 (Resolved from task-010-02)

<!-- metadata:{"id": "task-011-01", "type": "task", "parent": "adr-011", "title": "Issue Content Title", "status": "Draft", "role": "arch", "phase": "Architecture", "depends_on": ["task-010-01", "task-010-02"], "labels": ["P1"], "issue_id": null} -->
```

## Quality Policy (Guardrails)

1. **ID Resolution Strategy:** 部分一致による誤置換を防ぐため、負の前後参照 (`lookaround`) を含む正規表現（例: `(?<![A-Za-z0-9_-])ID(?![A-Za-z0-9_-])`）を使用して、ID の境界を正確に判定し置換を行う。
2. **Metadata Integrity:** JSON メタデータ内の情報は、GitHub API で渡される実データ（Labels 等）と同期していなければならない。ただし、`labels` フィールドには追加の静的ラベルのみを格納し、`role` や `phase` から生成される動的ラベルは Actions 側で合成する。
3. **Invisible Metadata:** メタデータブロックは `<!-- ... -->` で囲み、GitHub のプレビュー上で人間に見えないようにする。
