# Analysis Report: Physical State Lifecycle Transition

## 1. Intent Analysis (Why)
- **Problem**: The current metadata-driven lifecycle (ADR-007) is complex and depends on CLI tools (`ick sync`, `ick create`) to manage states, which can be brittle and hard to verify physically.
- **Outcome**: A simplified, highly visible lifecycle where the physical location of a file (`_inbox`, `_approved`, `_archive`) is the Single Source of Truth for its state. This aligns with the "Physical State Scanner" concept in ADR-008.

## 2. Gap Analysis
- **Metadata vs. Physics**: ADR-007 uses `status` metadata. ADR-008 uses directory structure.
- **Automation vs. Manual**: ADR-007 implies automated moves via CLI. ADR-008 mandates "Manual PR Merge" for approval.
- **State Bloat**: ADR-007 has 5 states for tasks. ADR-008 suggests 3 physical states (Draft, Approved, Done).

## 3. Hypotheses

### Hypothesis 1: Grounded (Physical State Mapping)
- **Strategy**: Map the current 5 task states into the 3 physical buckets.
  - Draft -> `_inbox/`
  - Ready/Issued -> `_approved/` (Ready to be processed or already issued but not finished)
  - Completed/Cancelled -> `_archive/`
- **Verification**: Mermaid diagram shows only 3 physical states and transitions based on physical moves (Manual PR Merge, Task Completion).

### Hypothesis 2: Leap (Guardrail-Centric)
- **Strategy**: Completely remove `status` metadata from the documentation and focus entirely on "Physical Location + Domain Guardrails".
- **Outcome**: The lifecycle is no longer about "Status Updates" but about "Location Shifts and Invariant Checks".

### Hypothesis 3: Paradoxical (Hybrid Truth)
- **Strategy**: Keep the internal `status` as a "cache" but explicitly state it is NOT the SSOT.
- **Risk**: Potential confusion between metadata and physical location.

## 4. Proposed Approach (Grounded)
I will adopt Hypothesis 1. I will update `arch-state-007-lifecycle.md` to define 3 core states: `Draft (Inbox)`, `Approved`, and `Done (Archive)`. Transitions will be defined as Physical Movements triggered by Manual PR Merge or Task Completion.