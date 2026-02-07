# [Specification Plan] ADR-008 Scanner Foundation

## 1. SSOT Audit Log

- **Source Design Doc:** `reqs/design/_approved/adr-008-automation-cleanup.md`
- **System Context:** `docs/system-context.md`
- **Common Definitions (Arch):** `docs/architecture/plans/adr-008-automation-cleanup/definitions.md`
- **Architecture Handover:** `docs/architecture/plans/adr-008-automation-cleanup/arch-to-spec.md`

## 2. Common Definitions & Standards (Critical)

### 2.1. Ubiquitous Language (Naming)

- **Physical State Scanner:** Git差分ではなくファイルシステム上の位置（`_inbox`, `_approved`, `_archive`）で状態を判定する機構。
- **Domain Guardrails:** Pydanticモデルで実装される不変条件（ID形式、依存関係の健全性）。
- **DAG Visualization:** 依存関係を有向非巡回グラフとして可視化すること。

### 2.2. Common Data Types

| Type Name  | Base Type | Constraints (Min, Max, Regex)                                                                                                              |
| :--------- | :-------- | :----------------------------------------------------------------------------------------------------------------------------------------- |
| _TaskID_   | _String_  | `task-\d{3}-\d{2,}` (e.g., `task-008-01`) ※ADR-008配下の新規タスクに適用。既存の `007-T3-*` 形式等はレガシーとして読み取り専用で許容する。 |
| _ADRID_    | _String_  | `adr-\d{3}-.*` (e.g., `adr-008-cleanup`)                                                                                                   |
| _PathLike_ | _Path_    | Absolute or Relative path to `reqs/`                                                                                                       |

### 2.3. Error Handling Policy

| Error Code          | Exception Class   | Description                                         |
| :------------------ | :---------------- | :-------------------------------------------------- |
| _INVALID_METADATA_  | _ValidationError_ | ID format or required fields missing                |
| _DUPLICATE_ID_      | _ValidationError_ | Same ID found in multiple files (including archive) |
| _CYCLE_DETECTED_    | _GraphError_      | Circular dependency found in DAG                    |
| _ORPHAN_DEPENDENCY_ | _GraphError_      | `depends_on` ID not found in scan scope             |

### 2.4. Cleanup Targets (Legacy Code)

- `src/issue_creator_kit/usecase/workflow.py`
- `src/issue_creator_kit/usecase/approval.py`
- `.github/workflows/auto-approve-docs.yml`

## 3. Directory Structure & Naming

- **Spec File Naming (this directory):** `{component}-{slug}.md` （例: `scanner-foundation.md`）
- **Task Directory & File Naming (implementation):** `reqs/tasks/adr-008/task-{NN}-{slug}.md` （例: `reqs/tasks/adr-008/task-07-arch-fix.md`）

## 4. Issue Slicing Strategy

- **Policy:** 1 Spec File per Component / Core Feature.

## 5. Dependency & Parallelization Strategy (Critical)

- **Core Tasks:**
  1. **Domain Models (Guardrails):** 全ての基礎となるため最優先。
  2. **Cleanup:** 既存の干渉を防ぐため早期に実施。
- **Parallel Tasks:**
  - **Scanner Implementation:** Domain Model 完成後に着手。
  - **Graph Builder & Visualizer:** Domain Model 完成後に着手。
- **DAG Diagram:**

```mermaid
graph TD
    Cleanup[Cleanup Legacy Code]
    Domain[Domain Models & Guardrails]
    Scanner[FileSystem Scanner Logic]
    Graph[Graph Builder & Visualizer]
    CLI[CLI Integration]

    Cleanup --> CLI
    Domain --> Scanner
    Domain --> Graph
    Scanner --> Graph
    Graph --> CLI
```
