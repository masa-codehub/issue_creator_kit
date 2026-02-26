# Issue Renderer Specification

## 1. Overview

- **Responsibility**: `Task` ドメインモデルを GitHub Issue 形式（タイトル、本文、ラベル）に変換し、ID 置換およびメタデータ埋め込みを行うドメインサービス。
- **Collaborators**: `GitHubAdapter` (発行済み番号の取得), `OrchestratorService` (変換依頼)。

## 2. Data Structures (Models)

### 2.1. RenderedIssue (Value Object)

| Field    | Type        | Description                                           |
| :------- | :---------- | :---------------------------------------------------- |
| `title`  | `str`       | `{task.id}: {task.title}` 形式のタイトル。            |
| `body`   | `str`       | ID 置換済み、かつメタデータブロックが付与された本文。 |
| `labels` | `list[str]` | 合成されたラベルリスト。                              |

### 2.2. Metadata JSON Schema

`<!-- metadata: { ... } -->` 内に含まれる JSON の構造。

- `id`, `type` (常に "task"), `parent`, `title`, `status`, `role`, `phase`, `depends_on`, `labels`, `issue_id`.

## 3. Interfaces (API/Methods)

### 3.1. `IssueRenderer.render(task: Task, id_map: dict[str, int]) -> RenderedIssue`

- **Signature**: `render(task: Task, id_map: dict[str, int]) -> RenderedIssue`
- **Contract**:
  - `id_map` を用いて本文中の Task ID を GitHub リンク (`#123`) へ置換する。
  - `depends_on` に含まれる全ての ID が `id_map` に存在することを保証する。
- **Exceptions**: `DependencyResolutionError`, `MetadataSerializationError`.

## 4. Logic & Algorithms

### 4.1. Substring-Safe ID Resolution

1. **Sort**: `id_map` のキーを長さの降順でソート。
2. **Regex**: `(?<![A-Za-z0-9_-])(ID1|ID2)(?![A-Za-z0-9_-])` 形式の正規表現を使用し、部分一致を完全に防ぐ。

### 4.2. Metadata Block Generation

1. 本文末尾に改行を 2 つ (`\n\n`) 挿入。
2. HTML コメント `<!-- metadata: {JSON} -->` を生成。
3. **Safety Padding**: `<!--` と JSON、および JSON と `-->` の間に必ず 1 つ以上の半角スペースを挿入し、コメント破壊を防ぐ。

### 4.3. Label Synthesis

1. システムラベル: `task`, `adr:{num}` (num は ADR 番号 3桁)。
2. カスタムラベル: フロントマター由来の `task.labels`。
3. 除外: `role`, `phase` はラベルに含めない。

## 5. Traceability

- **Merged Files**:
  - `adr-011-renderer-api.md` (Legacy)
  - `adr-011-renderer-logic.md` (Legacy)
- **Handover Constraints**:
  - Substring safety during ID replacement.
  - Mandatory space padding in metadata HTML comments.
