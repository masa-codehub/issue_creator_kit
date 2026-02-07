# Review Analysis Report: PR #328

## 1. Summary
- **Total Comments:** 10
- **Accept (修正受諾):** 10
- **Discuss (議論/確認):** 0
- **Explain (現状維持/説明):** 0

## 2. Analysis Details

### [Accept] docs/specs/logic/graph_and_validators.md
- **Reviewer's Comment:**
  - Multiple comments (Copilot, gemini-code-assist) regarding clarity, deterministic behavior, and interface consistency.
- **Context Analysis:**
  - The specification for GraphBuilder and Visualizer was too abstract in some areas, leading to potential implementation ambiguity and TDD instability.
- **Proposed Action:**
  - **Terminology:** Align with ADR-008 and ADR-007 by using `DocumentNode` (or clarifying `TaskNode` holds `Document`) and `Document` instead of `Task`.
  - **Interface:** Update `build_graph(documents)` to `build_graph(documents, archived_ids)` to allow `ORPHAN_DEPENDENCY` check against `_archive/`.
  - **ORPHAN_DEPENDENCY:** Clarify that dependencies in `_archive/` are valid.
  - **Mermaid Rules:**
    - Arrow direction: `From --> To` (Depends on).
    - Empty graph: Always return `graph TD`.
    - Deterministic order: Nodes by ID asc, Edges by (From, To) asc.
    - Title resolution: `metadata.extra["title"]` -> H1 -> ID.
    - Escaping: `"` -> `"`, `[` -> `(`, `]` -> `)`, `
` -> `<br/>`.
  - **TDD:** Use realistic IDs (`task-008-a` etc.) in examples to match `Metadata.id` regex.
- **Verification Plan:**
  - Update specification and verify alignment with ADR-008.
  - Self-audit using `auditing-ssot`.

---

## 3. Execution Plan
- [ ] Update `docs/specs/logic/graph_and_validators.md` based on accepted comments.
- [ ] Update `docs/architecture/arch-structure-008-scanner.md` if terminology alignment is needed.
- [ ] Record changes and push.
