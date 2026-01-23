# CLI Interface Specification (ADR-003)

## 1. Overview
Defines the entry points and command structure for the `issue-kit` CLI.
The CLI serves as the Interface layer in the Clean Architecture, responsible for parsing user input and orchestrating UseCases.

## 2. Common Specifications

### 2.1. Exit Codes
| Code | Meaning | Description |
| :--- | :--- | :--- |
| `0` | Success | The command completed all operations successfully. |
| `1` | Error | General error (validation failure, missing environment variables, runtime error). |

### 2.2. Environment Variables
| Variable | Required | Description |
| :--- | :--- | :--- |
| `GITHUB_MCP_PAT` | Yes | Personal Access Token for GitHub API operations. |
| `GITHUB_REPOSITORY`| No | Target repository (`owner/repo`). Defaults to current context if not provided via args. |

## 3. Command Definitions

### 3.1. `process-diff`
Orchestrates the "Virtual Queue" processing logic triggered by a merge to the archive directory.

- **Usage**: `issue-kit process-diff --base-ref <ref> --head-ref <ref> [--archive-dir <path>]`
- **Arguments**:
    - `--base-ref` (Required): The base commit/branch for diffing (e.g., `HEAD~1` or `main`).
    - `--head-ref` (Required): The head commit/branch (e.g., `HEAD`).
    - `--archive-dir` (Optional): Path to the task archive (default: `reqs/tasks/archive`).
- **Logic Mapping**: Calls `IssueCreationUseCase.create_issues_from_virtual_queue()`.
- **Side Effects**: Creates GitHub Issues, updates local files, syncs roadmap, and pushes changes to origin.

### 3.2. `process-merge`
Orchestrates the "Auto-PR (Phase Chain)" logic triggered by a task PR merge.

- **Usage**: `issue-kit process-merge --pr-body <body> [--archive-dir <path>]`
- **Arguments**:
    - `--pr-body` (Required): The body text of the merged PR to extract issue numbers from.
    - `--archive-dir` (Optional): Path to the task archive to find task definitions (default: `reqs/tasks/archive`).
- **Logic Mapping**: Calls `WorkflowUseCase.promote_from_merged_pr()`.
- **Side Effects**: Creates a new foundation branch, moves files from `drafts/` to `archive/`, and opens a new PR on GitHub.

### 3.3. `run-workflow` (Integrated/Legacy)
A high-level command for backward compatibility or manual orchestration.

- **Usage**: `issue-kit run-workflow --branch <name> [--inbox-dir <path>] [--approved-dir <path>]`
- **Role**: In ADR-003 context, this may act as an alias that sequentially calls `process-diff` or simply executes the legacy ADR-002 approval flow. For ADR-003 projects, `process-diff` and `process-merge` are preferred.

## 4. Validation & Error Handling

### 4.1. Authentication Check
- If `GITHUB_MCP_PAT` is missing, the CLI must print an error to stderr and exit with code `1`.
- Error Message: `Error: GitHub token is required via GITHUB_MCP_PAT environment variable.`

### 4.2. Exception Handling
- UseCase exceptions (e.g., `RuntimeError` from Fail-fast) must be caught by the CLI.
- The CLI should log the error details clearly and exit with code `1`.
- **Constraint**: No direct usage of `subprocess` or `requests` in the CLI module. All I/O must be delegated to UseCases/Adapters.

## 5. Verification (TDD Criteria)

| Scenario | When | Then |
| :--- | :--- | :--- |
| Missing Base Ref | `issue-kit process-diff --head-ref main` | Exit 1, show help/error. |
| Missing Token | `GITHUB_MCP_PAT="" issue-kit process-diff ...` | Exit 1, show "token required". |
| UseCase Failure | `IssueCreationUseCase` raises `RuntimeError` | Exit 1, log the exception message. |
| Successful Promotion | `issue-kit process-merge --pr-body "Closes #1"` | Exit 0. |