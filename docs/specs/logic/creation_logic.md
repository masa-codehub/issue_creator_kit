# Issue Creation Logic Specification (ADR-007)

## 1. Overview
Defines the detailed algorithm for `IssueCreationUseCase.create_issues()`.
This logic ensures metadata-driven Issue creation based on dependency resolution (DAG) and maintains SSOT integrity via "Atomic Move" and "Status Transition".

## 2. Input / Output

### Input
- `adr_id` (str): ADR ID to process (e.g., `adr-007`).
- `base_dir` (str): Root directory of the project.
- `before` (str): Base Git Ref for diff detection.
- `after` (str): Head Git Ref for diff detection.

### Output
- `None` (Success).
- Raises `RuntimeError` on failure (including `CycleError`, `MissingDependencyError`, or API errors).

## 3. Algorithm (Detailed Steps)

### Step 1: Git Diff-based Discovery (Virtual Queue)
1.  **Get Target Files**:
    - Use `GitAdapter.get_added_files(before, after, "reqs/tasks/")` to identify new files.
    - If `adr_id` filter is provided, keep only files within `reqs/tasks/<adr_id>/`.
2.  **Indexing**:
    - For each identified file, call `FileSystemAdapter.read_document(file_path)`.
    - Build an **In-Memory Index** (Map) of the target batch.
3.  **Context Loading**:
    - Load existing tasks from `reqs/tasks/_archive/` (optionally filtered by `adr_id`) to resolve cross-batch dependencies.
4.  **Final Queue**: Filter documents where `status` is NOT `Issued`, `Completed`, or `Cancelled`, AND `issue_id` is empty.

### Step 2: DAG Analysis & Ready Judgment
1.  Build a **Dependency Graph (DAG)** using the Virtual Queue and existing tasks in `reqs/tasks/_archive/`.
2.  **Circular Dependency Check**:
    - Perform a depth-first search or similar algorithm to detect cycles.
    - If a cycle is detected, raise `CycleError` and abort.
3.  **Ready Judgment Logic**:
    - For each task in the Virtual Queue, evaluate its `Ready` criteria:
        - A task is `Ready` if **ALL** its `depends_on` IDs satisfy one of the following:
            - The dependency has `status: Issued` (verified via metadata or GitHub API).
            - The dependency has `status: Completed` (verified via GitHub API).
            - The dependency is in `reqs/tasks/_archive/` with a valid `issue_id`.
    - If a dependency is missing from both the current ADR folder and the archive, raise `MissingDependencyError`.
4.  **Topological Sort**:
    - Sort the `Ready` tasks to determine the safe creation order.

### Step 3: Atomic Issue Creation (Fail-fast Zone)
1.  Initialize `creation_results` buffer.
2.  For each task in sorted order:
    - **A. Prepare Body**: 
        - Replace reference links `[Ref](ID)` with GitHub Issue numbers `#123`.
        - Use local index for tasks in the same batch or GitHub API for already issued tasks.
    - **B. Call API**: `GitHubAdapter.create_issue(title, body, labels)`.
    - **C. Handle Success**: 
        - Update status to `Issued`.
        - Record `issue_id` and store the link-replaced body for later write-back.
    - **D. Handle Failure**:
        - Stop immediately. Raise `RuntimeError`.

### Step 4: Atomic Move & Status Transition (Transaction Commit)
*Executed only if Step 3 succeeded for all target tasks.*

1.  For each task successfully created:
    - **A. Update Local File**:
        - Write back updated metadata (`status: Issued`, `issue_id: 123`).
        - Write back link-replaced body.
    - **B. Atomic Move**:
        - Move file from `reqs/tasks/<adr_id>/` to `reqs/tasks/_archive/`.
        - Use `git mv` equivalent to preserve history.
2.  **Roadmap Sync**: Best-effort sync as per ADR-007.

## 4. TDD Verification Criteria

| Scenario | Given | When | Then |
| :--- | :--- | :--- | :--- |
| **Dependency Ready** | `T2` depends on `T1`. `T1` is `Issued`. | Run `ick create` | `T2` is created. |
| **Dependency Not Ready** | `T2` depends on `T1`. `T1` is `Draft`. | Run `ick create` | `T2` is skipped (not in Ready queue). |
| **Circular Dependency** | `A -> B -> A` | Run `ick create` | `CycleError` raised. |
| **Atomic Move** | Issue created for `T1` | Success | `T1.md` moves to `_archive/` and has `issue_id`. |
| **Idempotency** | `T1` has `issue_id` in file | Run `ick create` | `T1` is skipped (No duplicate Issue). |

## 5. Constraints
- **Scope**: Supports cross-ADR dependencies if IDs are unique.
- **Fail-fast**: Any API error during Step 3 prevents Step 4 (Move) for the remaining batch.