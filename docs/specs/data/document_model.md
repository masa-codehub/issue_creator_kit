# Document Domain Model Specification

## 1. Overview
Defines the `Document` object and its `Metadata` schema, which serve as the Single Source of Truth (SSOT) for managing task lifecycle (Draft -> Active -> Archived) as per ADR-003.
This model encapsulates normalization, validation, and status transition rules.

## 2. Domain Model (Classes)

### 2.1. Class Diagram
```mermaid
classDiagram
    class Document {
        +Path path
        +str content
        +Metadata metadata
        +validate() void
    }
    class Metadata {
        +str title
        +str status
        +str|int issue
        +list[str] depends_on
        +str next_phase_path
        +dict extra_fields
        +validate() void
    }
    class ValidationError {
        +str message
        +str field
    }

    Document *-- Metadata : contains
    ValidationError <.. Document : throws
```

### 2.2. Metadata Schema
Metadata manages key attributes of a task.
It enforces strict normalization and validation rules.

#### Normalization Rules
1.  **Lowercase Keys**: All keys are converted to lowercase (e.g., `Status` -> `status`).
2.  **Alias Mapping (Japanese Support)**:
    - `タイトル` -> `title`
    - `ラベル` -> `labels`
    - `ステータス` -> `status`
    - `依存` -> `depends_on`

| Field | Type | Required | Description | Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `title` | `str` | Yes | Task title for Issue creation. | Must not be empty. |
| `status` | `str` | Yes | Lifecycle status. | Must be one of `Draft`, `Active`, `Archived`. |
| `issue` | `str` \| `int` | No | GitHub Issue number (e.g., `#123`). | Required if status is `Active` or `Archived`. |
| `depends_on` | `list[str]` | No | List of dependent filenames. | Must be a list of strings. |
| `next_phase_path`| `str` | No | Path to next phase drafts. | Required for phase promotion trigger. |

### 2.3. Validation Rules
The `validate()` method enforces the following rules:

1.  **Required Fields**: `title` and `status` must exist.
2.  **Status Integrity**:
    - If `status` is `Active` or `Archived`, the `issue` field must represent a valid issue number (starting with `#` or pure digits).
    - If `path` is in `archive/` directory, `status` must NOT be `Draft`.
3.  **Type Consistency**: `depends_on` must be a list, `labels` must be a list.

## 3. Parsing & Serialization

### 3.1. Parsing Logic
Supports hybrid parsing (YAML Frontmatter priority).

1.  **YAML Frontmatter**:
    - If file starts with `---`, parse content between delimiters as YAML.
2.  **Markdown List (Fallback)**:
    - Scan lines matching `^- \*\*([^*]+)\*\*: (.*)$`.
    - Stop scanning after 15 lines or upon encountering an empty line after metadata.

### 3.2. Serialization Logic
- Always serialize as **YAML Frontmatter** when saving.
- If the original file used Markdown List format, convert it to YAML Frontmatter to standardize the codebase.

## 4. Edge Cases & Error Handling

| Scenario | Behavior |
| :--- | :--- |
| **Missing Status** | Raise `ValidationError(field="status")`. |
| **Invalid Status Value** | Raise `ValidationError("Invalid status: {value}. Must be Draft, Active, or Archived")`. |
| **Active but No Issue** | Raise `ValidationError("Active tasks must have an issue number")`. |
| **Japanese Key** | Normalize to English key internally. `metadata["title"]` returns value for `タイトル`. |