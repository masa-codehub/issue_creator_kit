# Goal Definition: Update Architecture Lifecycle (Physical State)

## 1. SMART Goal
- **Specific**: Update `docs/architecture/arch-state-007-lifecycle.md` to reflect the "Physical State Scanner" model from ADR-008.
- **Measurable**: 
    - Number of states in Mermaid diagram reduced to 3 (Draft/Inbox, Approved, Done/Archive).
    - Triggers updated to "Manual PR Merge" and "Task Completion".
- **Achievable**: The target file and reference definitions are already gathered.
- **Relevant**: Necessary for aligning architecture documentation with the implemented ADR-008 logic.
- **Time-bound**: To be completed in this turn.

## 2. Outcome (Final State)
- `docs/architecture/arch-state-007-lifecycle.md` accurately describes a lifecycle where the directory structure is the SSOT for document/task state.
- Obsolete CLI-driven triggers (`ick sync`, `ick create`) are removed from the lifecycle definition.

## 3. Verification Methods (DoD)
- **Visual Check**: Run `cat docs/architecture/arch-state-007-lifecycle.md` and verify Mermaid syntax.
- **Content Check**: Verify that "Ready" and "Issued" states are removed or consolidated into "Approved".
- **Alignment Check**: Compare with `docs/architecture/plans/adr-008-automation-cleanup/definitions.md` to ensure terminology match.
