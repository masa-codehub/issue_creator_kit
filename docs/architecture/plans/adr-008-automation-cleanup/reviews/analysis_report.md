# Analysis Report: Architecture Refactoring for ADR-008

## 1. Intent Analysis (5W1H)
- **Why**: To eliminate technical debt (ADR-003 auto-logic) and build a stable foundation (Scanner) for future automation (ADR-009+).
- **What**: Refactor architecture documentation (`docs/architecture/`).
- **Where**: `docs/architecture/` and `issue-kit` design.
- **Who**: Architect (Me) planning for Developers/Implementers.
- **When**: Now (ADR-008 is approved).
- **How**: By archiving obsolete docs and updating/creating docs to reflect the "Physical State" model.

## 2. Gap Analysis
- **Current State**: Documentation describes a "Virtual Queue" and "Auto-Merge" system.
- **Desired State**: System behaves based on "Physical File Presence" and "Manual Merge".
- **Risk**: If docs aren't updated clearly, developers might accidentally reimplement the "Auto-Merge" logic or get confused by the mixed signals.

## 3. Hypotheses
- **Option A (Grounded - Recommended)**:
    - **Strategy**: Strictly follow ADR-008.
    - **Actions**: Archive `arch-*-003-*`. Update `arch-*-007-*`. Create `arch-structure-008-scanner.md`.
    - **Pros**: Clear, focused, complies with "Subtraction" philosophy.
    - **Cons**: None.
- **Option B (Leap)**:
    - **Strategy**: Pre-optimize for ADR-009/010.
    - **Actions**: Add detailed specs for "L1 Automation" and "Task Activation" now.
    - **Pros**: Less updates later.
    - **Cons**: Speculative. Violates YAGNI. ADR-008 focuses on *cleanup*.
- **Option C (Paradoxical)**:
    - **Strategy**: Delete all existing architecture docs and write one single "Current Architecture" file.
    - **Pros**: Extreme simplicity.
    - **Cons**: Loss of granular context (Structure vs State vs Behavior). Too radical.

## 4. Conclusion
Adopt **Option A**. Focus on removing the old (ADR-003) and defining the new foundation (Scanner) as per ADR-008.
