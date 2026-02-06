# Analysis Report: Define Scanner Foundation Architecture

- **Date**: 2026-02-06
- **Analyst**: SYSTEM_ARCHITECT

## 1. Intent Analysis (Why)
The user wants to establish a visual and structural Single Source of Truth (SSOT) for the newly defined Scanner Foundation. This is critical because the project is shifting its core state management philosophy from Git-diff tracking (fragile) to Physical File-system scanning (robust). Without this document, future implementation tasks will lack a clear design to follow, leading to potential fragmentation in how the scanner is implemented.

## 2. Gap Analysis
- **Current**: Textual definitions in `definitions.md` and high-level goals in ADR-008.
- **Missing**: 
    - A **Component View** showing how `FileSystemScanner` interacts with `TaskParser` and `GraphBuilder`.
    - A **Process View** (Sequence) showing the flow from scanning a file to generating a `Graph` object.
    - Clear definition of the **Visualizer**'s role in the DAG generation.
- **Constraint**: Must avoid any reference to the deprecated "Virtual Queue" or "Auto-Approve" flow from ADR-003.

## 3. Hypotheses

### Hypothesis A: Grounded (Grounded) - Focus on core flow
- **Approach**: Directly translate the definitions from ADR-008 and `definitions.md` into a single file with three Mermaid diagrams (Component, Sequence, and a simple Class/Model view).
- **Benefit**: High certainty, matches exactly what's requested in Issue #305.

### Hypothesis B: Leap (Leap) - Extensibility for Remote Repos
- **Approach**: Design the `FileSystemScanner` with an interface that could potentially allow for other "Scanners" (e.g., a Remote Git Scanner) in the future, even if currently only FileSystem is implemented.
- **Risk**: Might be premature (YAGNI), but ADR-008's "Physical State" focus suggests local-first.

### Hypothesis C: Paradoxical (Paradoxical) - Pure Data Flow
- **Approach**: Instead of focusing on "Services", focus entirely on the transformation of "Raw Path Data" -> "Domain Task Objects" -> "DAG Graph". Architecture revolves around data pipelines.
- **Benefit**: Extremely clean separation of data and side-effects.

## 4. Proposed Strategy
Adopt **Hypothesis A** as the primary strategy to ensure the immediate needs of ADR-008 are met without over-engineering. However, incorporate elements of **Hypothesis C** by clearly defining the data structures (Task, Graph) to ensure robust Pydantic validation as per ADR-008 "Guardrails".
