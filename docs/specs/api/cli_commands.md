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
| `GITHUB_TOKEN` | Yes* | GitHub Personal Access Token. Can also use `GH_TOKEN`. |
| `GITHUB_REPOSITORY`| No | Target repository (`owner/repo`). Defaults to this env var if not provided via args. |

*\*Required if not provided via the `--token` argument.*

## 3. Command Definitions

### 3.1. `process-diff`
Orchestrates the "Virtual Queue" processing logic triggered by a merge to the archive directory.

- **Usage**: `issue-kit process-diff --before <ref> --after <ref> [options]`
- **Arguments**:
    - `--before` (Required): The base commit/branch for diffing (e.g., `HEAD~1` or `main`).
    - `--after` (Required): The head commit/branch (e.g., `HEAD`).
    - `--archive-dir` (Optional): Path to the task archive (default: `reqs/tasks/archive/`).
    - `--roadmap` (Optional): Path to the roadmap file to synchronize.
    - `--use-pr` (Optional): Create a PR for metadata updates instead of pushing directly to main.
    - `--base-branch` (Optional): Base branch for the metadata sync PR (default: `main`).
    - `--repo` (Optional): GitHub repository (`owner/repo`).
    - `--token` (Optional): GitHub token.
- **Logic Mapping**: Calls `IssueCreationUseCase.create_issues_from_virtual_queue()`.

### 3.2. `process-merge`
Orchestrates the "Auto-PR (Phase Chain)" logic triggered by a task PR merge.

- **Usage**: `issue-kit process-merge [options]`
- **Arguments**:
    - `--pr-body` (Optional): The body text of the merged PR to extract issue numbers from.
    - `--event-path` (Optional): Path to the GitHub event JSON file. Safer than `--pr-body`.
    - `--archive-dir` (Optional): Path to the task archive (default: `reqs/tasks/archive/`).
    - `--repo` (Optional): GitHub repository (`owner/repo`).
    - `--token` (Optional): GitHub token.
- **Note**: If neither `--pr-body` nor `--event-path` is provided, the PR body defaults to an empty string.
- **Logic Mapping**: Calls `WorkflowUseCase.promote_from_merged_pr()`.

### 3.3. `run-workflow` (Integrated/Legacy)
A high-level command for backward compatibility or manual orchestration (ADR-002 style).

- **Usage**: `issue-kit run-workflow --branch <name> [options]`
- **Role**: Orchestrates the document approval flow (Inbox -> Approved). In ADR-003 projects, `process-diff` and `process-merge` are preferred for automation.

## 4. Validation & Error Handling

### 4.1. Authentication Check
- If no token is provided via `--token` or environment variables (`GITHUB_TOKEN` / `GH_TOKEN`), the CLI must print an error and exit with code `1`.
- Error Message: `Error: GitHub token is required.`

### 4.2. Exception Handling
- UseCase exceptions (e.g., `RuntimeError` from Fail-fast) must be caught by the CLI.
- The CLI should log the error details clearly and exit with code `1`.
- **Constraint**: No direct usage of `subprocess` or `requests` in the CLI module. All I/O must be delegated to UseCases/Adapters.

## 5. Verification (TDD Criteria)

| Scenario | When | Then |
| :--- | :--- | :--- |
| Missing Before Ref | `issue-kit process-diff --after main` | Exit 1, show help/error. |
| Missing After Ref | `issue-kit process-diff --before main` | Exit 1, show help/error. |
| Missing Token | Unset token env vars and run `issue-kit process-diff ...` | Exit 1, show "token required". |
| UseCase Failure | `IssueCreationUseCase` raises `RuntimeError` | Exit 1, log the exception message. |
| Successful Promotion | `issue-kit process-merge --pr-body "Closes #1"` | Exit 0. |
