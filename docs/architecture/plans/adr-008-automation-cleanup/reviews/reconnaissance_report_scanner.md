# Reconnaissance Report: Define Scanner Foundation Architecture

- **Date**: 2026-02-06
- **Status**: Completed

## 1. Objective
Investigate the current state and requirements for the "Scanner Foundation" architecture as defined in ADR-008.

## 2. Evidence Gathered

### 2.1 ADR-008 ([reqs/design/_approved/adr-008-automation-cleanup.md](reqs/design/_approved/adr-008-automation-cleanup.md))
- **Key Decision**: Transition from Git-diff based detection to Physical File-system scanning.
- **Core Components**:
    - **Physical State Scanner**: Walks `reqs/` directory.
    - **Validation Mode**: `--dry-run` to list planned actions.
    - **Visualization**: Output dependency graph (DAG) in Mermaid format.
- **Guardrails**: Validation logic moved to Domain layer (Pydantic models).

### 2.2 Common Definitions ([docs/architecture/plans/adr-008-automation-cleanup/definitions.md](docs/architecture/plans/adr-008-automation-cleanup/definitions.md))
- **Concepts**:
    - **Physical State Scanner**: Determines state by physical location (`_inbox`, `_approved`, `_archive`).
    - **DAG Visualization**: Uses `depends_on` to create Mermaid JS output.
- **Directory Mapping**:
    - `src/issue_creator_kit/domain/services/scanner.py` (New)
    - `src/issue_creator_kit/domain/models/` (Update)

### 2.3 Current Codebase State
- Current branch: `feature/arch-update-adr008` (checked out during reconnaissance).
- `docs/architecture/template/arch-structure-template.md` is missing (confirmed by `ls`).
- `docs/architecture/arch-structure-008-scanner.md` does not exist yet (target of this task).

## 3. Discrepancies & Gaps
- **Lack of Diagram**: No visual representation of the Scanner service, its interaction with the file system, or the DAG generation process.
- **Obsolete Docs**: ADR-003 related documents still exist (per ADR-008 context, though not directly audited in this report's scope).

## 4. Conclusion
The requirements for the Scanner Foundation are well-defined in ADR-008 and the common definitions. The task is to translate these into a structural architecture document.
