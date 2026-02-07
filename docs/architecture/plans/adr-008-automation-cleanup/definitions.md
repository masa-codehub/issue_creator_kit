# Common Definitions: ADR-008 Scanner Foundation

## 1. Core Concepts (Ubiquitous Language)

### Physical State Scanner (物理状態スキャナー)
- **Definition**: A mechanism that determines the state of a Task or ADR solely based on its physical location in the file system, ignoring Git history or diffs.
- **Rules**:
  - `_inbox/`: Draft state (ADR/Design Doc only).
  - `reqs/tasks/<ADR-ID>/` root: Draft state (Task only).
  - `_approved/`: Approved state (ready for processing).
  - `_archive/`: Processed/Done state.
  - **Scanning Strategy**: Recursively walk the `reqs/` directory and determine the "Done" state by checking whether each file has a corresponding entry in `_archive/`.
  - **SSOT**: The file system IS the truth.

### Manual Approval Flow (手動承認フロー)
- **Definition**: The process of moving a document from `_inbox` to `_approved` via a human-initiated Pull Request and Merge.
- **Constraint**: No automated script shall perform this move.
- **Trigger**: Merge to `main` triggers the scanner (in future ADRs), but strictly speaking, the *state change* happens at merge.

### Domain Guardrails (ドメイン・ガードレール)
- **Definition**: Invariant checks implemented in the Domain Layer (Pydantic Models) to prevent invalid states.
- **Checks**:
  - **ID Format**: Must match `adr-\d{3}-.*` for ADRs, or `task-\d{3}-\d{2,}` for Tasks (e.g., `task-008-01`).
  - **Dependency**: `depends_on` must reference valid IDs. No self-reference. No cycles.
- **Scope**: Applied during scanning and CLI execution.

### DAG Visualization (DAG可視化)
- **Definition**: A visual representation of the dependency graph derived from `depends_on` fields.
- **Format**: Mermaid JS.
- **Usage**: `visualize` command outputs this to stdout for human verification.

## 2. Directory Mapping

| Concept | Physical Path |
| :--- | :--- |
| **Scanner Logic** | `src/issue_creator_kit/domain/services/scanner.py` (New) |
| **Guardrails** | `src/issue_creator_kit/domain/models/` (Update) |
| **Old Workflow** | `src/issue_creator_kit/usecase/workflow.py` (Delete) |
| **Old CLI** | `src/issue_creator_kit/cli.py` (Update) |
