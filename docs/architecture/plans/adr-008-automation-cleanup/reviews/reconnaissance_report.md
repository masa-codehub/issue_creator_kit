# Reconnaissance Report: Architecture Refactoring for ADR-008

## 1. Context & Objectives
- **Trigger**: Approval of ADR-008 (Cleanup & Scanner Foundation).
- **Goal**: Refactor architecture documentation (`docs/architecture/`) to align with ADR-008 and prepare for the roadmap (ADR-009 to ADR-012).
- **Core Strategy**: "Subtraction" (Remove debts from ADR-003) and "Scanner Foundation" (Physical state based detection).

## 2. Evidence (Current State)

### 2.1. New Standards (SSOT)
- **ADR-008**: `reqs/design/_approved/adr-008-automation-cleanup.md`
    - **Decision**: Remove `WorkflowUseCase`, `ApprovalUseCase`, `auto-approve-docs.yml`, and ID write-back logic.
    - **New Mechanism**: Physical file scanning (`reqs/` traversal), `dry-run`, `visualize` (Mermaid), and Pydantic-based domain guardrails.
- **Roadmap**: `reqs/design/_inbox/status-and-plan.md`
    - **Flow**: Manual PR/Merge for approval (No auto-move).
    - **Steps**: ADR-008 (Cleanup) -> ADR-009 (L1 Auto) -> ADR-010 (Task Activation) -> ...

### 2.2. Documentation Candidates for Refactoring
Located in `docs/architecture/`:

**To Be Removed/Archived (ADR-003 Debts):**
- `arch-behavior-003-autopr.md`: Related to auto-PR logic (deprecated).
- `arch-behavior-003-creation.md`: Related to old creation flow (deprecated).
- `arch-state-003-task-lifecycle.md`: Old task lifecycle (deprecated).
- `arch-structure-003-vqueue.md`: Virtual Queue concept (deprecated).

**To Be Updated/Consolidated (ADR-007/008 Alignment):**
- `arch-behavior-approval-flow.md`: Needs update to reflect "Manual PR/Merge" and removal of auto-approve.
- `arch-state-007-lifecycle.md`: Needs update to reflect new "Physical State" lifecycle.
- `arch-structure-007-metadata.md`: Needs update to include Pydantic domain guardrails.
- `arch-structure-issue-kit.md`: Needs update to remove `WorkflowUseCase`/`ApprovalUseCase` and add `Scanner` components.
- `arch-state-doc-lifecycle.md`: Needs verification (likely needs update regarding ID write-back removal).

## 3. Findings
- **Discrepancy**: The current architecture docs describe a "Virtual Queue" and "Auto-Approve" system (ADR-003) which contradicts the approved ADR-008 ("Physical Scanner" and "Manual Approval").
- **Gap**: There is no diagram describing the new "Scanner Foundation" or the "DAG Visualization" feature mentioned in ADR-008.
- **Opportunity**: The `_inbox` plans (ADR-009+) suggest a need for a "Metadata Integration" and "Gemini Relay" model, which should be kept in mind (extensibility) but not fully documented yet (YAGNI, focus on ADR-008 first).

## 4. Risks
- **Confusion**: Keeping ADR-003 docs active will confuse developers during the refactoring implementation.
- **Scope Creep**: Trying to document ADR-009~012 behavior now is premature. Focus strictly on ADR-008 (Cleanup & Scanner) as the foundation.
