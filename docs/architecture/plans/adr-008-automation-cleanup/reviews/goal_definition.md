# Goal Definition: Architecture Refactoring Plan for ADR-008

## 1. Objective (Outcome)
- **Goal**: Establish a concrete execution plan for updating the architecture documentation to reflect ADR-008 (Cleanup & Scanner Foundation).
- **Scope**:
  - Archive/Remove obsolete ADR-003 documents.
  - Update ADR-007 documents to match the new "Manual Approval" and "Physical State" model.
  - Define new architecture components (Scanner, Visualizer) in documentation.
  - Generate GitHub Issues to delegate the actual drafting/updating work.

## 2. Deliverables
1.  **Design Brief Update**: `docs/architecture/plans/adr-008-automation-cleanup/design-brief.md` updated with specific doc refactoring scope.
2.  **Common Definitions**: `docs/architecture/plans/adr-008-automation-cleanup/definitions.md` defining "Physical State Scanner", "Domain Guardrails", etc.
3.  **Issue Drafts**: A set of JSON/Markdown drafts for:
    - Archiving 4 obsolete docs.
    - Updating 4 existing docs.
    - Creating 1 new doc (`arch-structure-008-scanner.md`).
    - 1 Integration Issue.
4.  **Pull Request**: A PR containing the above plan artifacts.

## 3. Verification Methods (DoD)
- **File Existence**:
  - `ls docs/architecture/plans/adr-008-automation-cleanup/definitions.md` returns success.
  - `ls .gemini/tmp/issues/*.json` (or similar) confirms draft generation.
- **Content Check**:
  - `grep "Physical State" docs/architecture/plans/adr-008-automation-cleanup/definitions.md`
- **Integration**:
  - The Integration Issue draft lists all other generated issue drafts as dependencies.

## 4. Constraints
- **SSOT**: Strictly follow `reqs/design/_approved/adr-008-automation-cleanup.md`.
- **No Direct Editing**: I am *planning* the changes, not making the final edits to the architecture docs themselves (except the plan files).
