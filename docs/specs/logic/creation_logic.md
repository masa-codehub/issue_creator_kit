# Issue Creation Logic Specification (ADR-003)

## 1. Overview
Defines the detailed algorithm for `IssueCreationUseCase.create_issues_from_virtual_queue()`.
This logic ensures atomic Issue creation from the "Virtual Queue" (newly added files in `archive/` without an issue number) and maintains SSOT integrity via a Fail-fast approach.

## 2. Input / Output

### Input
- `base_ref` (str): Base branch or commit SHA for diff comparison (typically `HEAD~1` or `main`).
- `head_ref` (str): Head branch or commit SHA (typically `HEAD`).
- `archive_dir` (str): Path to the task archive directory (default: `reqs/tasks/archive`).

### Output
- `None` (Success).
- Raises `RuntimeError` on failure (including `CycleError` or validation errors).

## 3. Algorithm (Detailed Steps)

### Step 1: Queue Detection
1.  Call `GitAdapter.get_added_files(base_ref, head_ref, archive_dir)`.
2.  For each file found:
    - Call `FileSystemAdapter.read_document(file_path)`.
    - Filter out files that already have an `issue` field in metadata.
3.  The remaining files constitute the **Virtual Queue**.

### Step 2: Dependency Resolution
1.  Extract `depends_on` list from each document in the queue.
2.  Perform a **Topological Sort** to determine the creation order.
    - If a circular dependency is detected, raise `CycleError` (or wrap it in `RuntimeError`) and abort immediately.
3.  Ensure all dependencies (even those already processed or outside the queue) are validated:
    - Each entry in `depends_on` MUST refer to either:
        - a file within the same Virtual Queue batch, or
        - an existing task file under `archive/` whose metadata status is `Active` or `Archived`.
    - If any dependency does not satisfy the above (e.g., file not found in `archive/`, invalid path, or inconsistent metadata), **abort immediately** following the Fail-fast policy of ADR-003:
        - Stop the process before Step 3.
        - Raise `RuntimeError` to fail the workflow.

### Step 3: Atomic Issue Creation (Fail-fast Zone)
1.  Initialize an empty memory buffer `creation_results`.
    - **Schema**: List of objects containing `{file_path: Path, issue_number: str, updated_content: str}`.
2.  For each file in the sorted order:
    - **A. Prepare Body**: 
        - Replace any references to dependent files in the `content` with their actual Issue numbers (e.g., `[Task](issue-T1.md)` -> `#123`).
        - Use the memory buffer `creation_results` for files in the same batch, or check filesystem for already-numbered files.
    - **B. Call API**: Call `GitHubAdapter.create_issue(title, body, labels)`.
    - **C. Handle Success**: 
        - Store the returned `issue_number` (formatted as a string, e.g., `"#123"`) and the link-replaced body in the `creation_results` buffer.
    - **D. Handle Failure**:
        - If any API call fails (4xx/5xx/Timeout), **Stop immediately**.
        - Note: For 403 Forbidden errors, retry only if the error is identified as a rate limit (via headers/body).
        - Do NOT write anything back to Git.
        - Raise `RuntimeError` to abort the workflow.

### Step 4: Git Write-back (Transaction Commit)
*This step only executes if ALL issues were created successfully.*

1.  For each entry in `creation_results`:
    - **A. Update Metadata**: Call `FileSystemAdapter.update_metadata(file_path, {"issue": issue_number, "status": "Active"})`.
    - **B. Update Body**: Call `FileSystemAdapter.write_file` with the `updated_content` stored in the buffer.
2.  **Roadmap Synchronization (Best-effort, Non-fatal)**:
    - Call `RoadmapSyncUseCase.sync_all(creation_results)`.
    - If roadmap synchronization fails (exception or error response), **do not abort** the workflow:
        - Log a warning (including affected files / issue numbers).
        - Do **not** roll back metadata or file updates already applied in this step.
        - Continue to finalize the process.
    - Rationale: As defined in `docs/architecture/arch-behavior-003-creation.md`, roadmap sync is treated as a best-effort operation separate from the Fail-fast Zone (Step 3).
3.  **Finalize Git**:
    - Define `all_modified_files` as the set of all task files and roadmap files updated in this step.
    - `GitAdapter.add(all_modified_files)`.
    - `GitAdapter.commit("docs: create issues for virtual queue and sync links")`.
    - `GitAdapter.push()`.

## 4. TDD Verification Criteria

| Scenario | Given | When | Then (Expectation) |
| :--- | :--- | :--- | :--- |
| **Normal Batch** | 3 new files in `archive/` | Execute `create_issues_from_virtual_queue` | All 3 issues created. Metadata is updated with issue numbers (e.g., `#123`) and status is `Active`. |
| **Dependency Order** | `A.md` depends on `B.md` | Execute | `B` is created first. `A`'s body (GitHub and Git) contains `#<B_No>`. |
| **API Failure (Partial)** | `A` success, `B` fails | Execute | `A` remains on GitHub, but `A.md` on Git is **NOT** updated (no issue number). A `RuntimeError` is raised. |
| **Redundant Run** | File in `archive/` already has `issue: #123` | Execute | File is skipped (no duplicate Issue). |
| **Link Replacement** | Body has `[Ref](./issue-T1.md)` | Execute | Body in file and GitHub is updated to the corresponding issue number (e.g., `#123`). |

## 5. Constraints & Edge Cases
- **Implementation Scope**: Although the trigger is typically a single task promotion (1 PR = 1 Task), the logic MUST handle multiple files if they are merged into `archive/` simultaneously.
- **Max Batch Size**: Implementers MAY impose a limit (e.g., 50 files) to avoid GitHub API rate limits in a single run.
- **Cycle Detection**: Circular dependencies MUST be detected during Step 2, resulting in an immediate abort.
