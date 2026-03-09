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

- `id`, `type`, `parent`, `title`, `status`, `role`, `phase`, `depends_on`, `labels`, `issue_id`.

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

### 4.3. Label Synthesis (Label Inference)

ADR-015 に基づき、`Task` または `ADR` モデルから GitHub ラベルを自動合成する。

#### 4.3.1. 抽出ルール (Extraction Rules)

- **Task ドキュメントの場合**:
  - `type`: 単一の文字列値（`task` または `integration`）をそのまま抽出。
  - `adr:{NNN}`: 親 ADR ID (`parent`) から 3 桁の番号（例: `adr-015` -> `adr:015`）を抽出。
  - `role`: 単一の文字列値（例: `arch`, `spec`, `tdd`）が存在する場合、そのまま抽出。
  - `phase`: 単一の文字列値（例: `plan`, `impl`, `audit`）が存在する場合、そのまま抽出。
- **ADR ドキュメントの場合**:
  - `adr` ラベルのみを付与し、属性抽出（role, phase 等）は行わない。
- **手動ラベル**: `doc.labels` に含まれる値をそのまま採用。

#### 4.3.2. 除外規則 (Exclusion Rules)

- **Exclusion Rule**: `gemini` ラベルは、起票時（`IssueRenderer` の処理範囲）には合成結果に含めてはならない。
- **Deduplication**: 重複するラベルは 1 つに統合する。

#### 4.3.3. ソート順 (Sorting Priority)

最終的なラベルリストは、以下の優先順位に従って構成する。同一カテゴリ内ではアルファベット順（A-Z）でソートする。

1. **システムラベル (System)**:
   - `type` (例: `task`), `adr:{NNN}` (例: `adr:015`)
   - ※システムラベル内に限り、`type` を必ず先頭とする固定順とする（`structure-renderer.md` 遵守）。
2. **属性ラベル (Attribute)**:
   - `role` (例: `arch`), `phase` (例: `plan`)
   - アルファベット順（例: `plan` -> `spec`）。
3. **手動指定ラベル (Manual)**:
   - 上記以外のラベル。
   - アルファベット順。

#### 4.3.4. 合成例

| 入力 (Task Metadata)                                                                  | 合成結果 (Sorted Labels)                           |
| :------------------------------------------------------------------------------------ | :------------------------------------------------- |
| `type: task`, `parent: adr-015`, `role: spec`, `phase: plan`, `labels: ["P1"]`        | `["task", "adr:015", "plan", "spec", "P1"]`        |
| `type: integration`, `parent: adr-012`, `role: tdd`, `phase: impl`, `labels: ["bug"]` | `["integration", "adr:012", "impl", "tdd", "bug"]` |
| ADR ドキュメント                                                                      | `["adr"]`                                          |

## 5. Traceability

- **Merged Files**:
  - `adr-011-renderer-api.md` (Legacy)
  - `adr-011-renderer-logic.md` (Legacy)
- **Handover Constraints**:
  - Substring safety during ID replacement.
  - Mandatory space padding in metadata HTML comments.
