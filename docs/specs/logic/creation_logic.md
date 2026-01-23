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
- `None` (Success) or raises `RuntimeError` on failure.

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
    - If a circular dependency is detected, raise `CycleError` and abort immediately.
3.  Ensure all dependencies (even those already processed or outside the queue) are validated (exist in `archive/`).

### Step 3: Atomic Issue Creation (Fail-fast Zone)
1.  Initialize an empty memory buffer `creation_results` (mapping file path -> issue number).
2.  For each file in the sorted order:
    - **A. Prepare Body**: 
        - Replace any references to dependent files in the `content` with their actual Issue numbers (e.g., `[Task](issue-T1.md)` -> `#123`).
        - Use the memory buffer `creation_results` for files in the same batch, or check filesystem for already採番済みの files.
    - **B. Call API**: Call `GitHubAdapter.create_issue(title, body, labels)`.
    - **C. Handle Success**: Store the returned `issue_number` in the `creation_results` buffer.
    - **D. Handle Failure**:
        - If any API call fails (4xx/5xx/Timeout), **Stop immediately**.
        - Do NOT write anything back to Git.
        - Raise `RuntimeError` to abort the workflow.

### Step 4: Git Write-back (Transaction Commit)
*This step only executes if ALL issues were created successfully.*

1.  For each file path in `creation_results`:
    - **A. Update Metadata**: Call `FileSystemAdapter.update_metadata(file_path, {"issue": issue_number, "status": "Active"})`.
    - **B. Update Body**: Call `FileSystemAdapter.write_file` with the link-replaced content (standardizing SSOT as per decision).
2.  **Roadmap Synchronization**:
    - Call `RoadmapSyncUseCase.sync_all(creation_results)`.
3.  **Finalize Git**:
    - `GitAdapter.add(all_modified_files)`.
    - `GitAdapter.commit("docs: create issues for virtual queue and sync links")`.
    - `GitAdapter.push()`.

## 4. TDD Verification Criteria

| Scenario | Given | When | Then (Expectation) |
| :--- | :--- | :--- | :--- |
| **Normal Batch** | 3 new files in `archive/` | Execute `create_issues_from_virtual_queue` | All 3 issues created, files updated with #No, status is `Active`. |
| **Dependency Order** | `A.md` depends on `B.md` | Execute | `B` is created first. `A`'s body contains `#<B_No>`. |
| **API Failure (Partial)** | `A` success, `B` fails | Execute | `A` remains successfully created on GitHub, but `A.md` on Git is **NOT** updated (no issue number). Process exits with 1. |
| **Redundant Run** | File in `archive/` already has `issue: #123` | Execute | File is skipped (no duplicate Issue). |
| **Link Replacement** | Body has `[Ref](./issue-T1.md)` | Execute | Body in file and GitHub is updated to `#<No>`. |

## 5. Constraints & Edge Cases
- **1 PR = 1 Task**: Although the logic supports batches, implementations should assume the trigger is typically a single task promotion for simplicity in initial phase.
- **Max Batch Size**: Implementers MAY impose a limit (e.g., 50 files) to avoid GitHub API rate limits in a single run.
