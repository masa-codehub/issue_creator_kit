# Reconnaissance Report: Update Architecture Lifecycle

## 1. Context Analysis
- **Goal**: Update `docs/architecture/arch-state-007-lifecycle.md` to reflect Physical State Scanner (ADR-008).
- **As-is**:
    - ADR states: Draft, Approved, Postponed, Superseded.
    - Task states: Draft, Ready, Issued, Completed, Cancelled.
    - Triggers include `ick sync`, `ick create`, and automated side effects.
- **To-be**:
    - Simplified states: Draft (Inbox), Approved, Done (Archive).
    - Triggers limited to "Manual PR Merge" and "Task Completion".
    - Removal of automated script triggers for movement.

## 2. Key Evidence
- **ADR-008 Definitions**:
    - `_inbox/`: Draft state.
    - `_approved/`: Approved state.
    - `_archive/`: Processed/Done state.
    - SSOT: The file system IS the truth.
- **Target File**: `docs/architecture/arch-state-007-lifecycle.md`.

## 3. Findings
- The current lifecycle (ADR-007) relies heavily on internal metadata (`status`) and CLI commands (`ick sync`, `ick create`) for state transitions.
- The new model (ADR-008) prioritizes physical location in the file system.
- Transition from `Draft` to `Approved` is explicitly "Manual PR Merge".
- Transition to `Archive` happens when a task is "Completed".

## 4. Risks & Obstacles
- Need to ensure the Mermaid diagram accurately reflects these simplified physical states.
- Must ensure that "Invariants" section is also updated to align with ADR-008's "Domain Guardrails".