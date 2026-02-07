# Goal Definition: Define Scanner Foundation Architecture

- **Date**: 2026-02-06
- **Strategist**: SYSTEM_ARCHITECT

## 1. SMART Goals

- **Specific**: Create `docs/architecture/arch-structure-008-scanner.md` that defines the Scanner Foundation architecture.
- **Measurable**: 
    - The file must contain at least three Mermaid diagrams: Component, Process (Sequence), and Data/Class view.
    - All components defined in `definitions.md` (`FileSystemScanner`, `TaskParser`, `GraphBuilder`, `Visualizer`) must be included.
- **Achievable**: Facts and requirements are already gathered from ADR-008 and `definitions.md`.
- **Relevant**: This is a direct requirement of Issue #305 and a prerequisite for implementing the Scanner Foundation.
- **Time-bound**: Complete within this session.

## 2. Verification Methods (DoD)

### 2.1 File Existence
- **Command**: `ls docs/architecture/arch-structure-008-scanner.md`
- **Expected**: File exists.

### 2.2 Content Validation
- **Command**: `grep -E "FileSystemScanner|TaskParser|GraphBuilder|Visualizer" docs/architecture/arch-structure-008-scanner.md`
- **Expected**: All core component names are present.
- **Command**: `grep "graph " docs/architecture/arch-structure-008-scanner.md && grep "sequenceDiagram" docs/architecture/arch-structure-008-scanner.md`
- **Expected**: Mermaid diagram blocks are present.

### 2.3 Compliance
- **Check**: No reference to "Virtual Queue" or "Auto-Approve".
- **Command**: `grep -E "Virtual Queue|Auto-Approve" docs/architecture/arch-structure-008-scanner.md`
- **Expected**: No matches (exit code 1).

## 3. Work Plan

1. **Setup**: Create and switch to branch `feature/task-008-04-scanner`.
2. **Drafting**:
    - Use `drafting-architecture/assets/arch-structure.md` as a base (or standard Markdown as requested).
    - Define Component View: Show the flow from File System to Graph.
    - Define Process View: Sequence diagram for `scan()` method.
    - Define Quality Policies: Validation (Guardrails) and Error Handling.
3. **Refining**: Visual refactoring of Mermaid diagrams for clarity.
4. **Audit**: Self-audit using `drafting-architecture/assets/drafting-audit-template.md`.
