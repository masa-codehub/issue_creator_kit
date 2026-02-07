# Promotion Logic (Metadata-Driven) Specification

## 1. Overview

Defines the logic for `WorkflowUseCase.promote_tasks()`.
This logic handles the "Phase Chain" (dependency propagation) by re-evaluating the `Ready` status of dependent tasks when a task is merged and closed (`Completed`).

## 2. Input

| Name               | Type      | Description                                                  |
| :----------------- | :-------- | :----------------------------------------------------------- |
| `closed_issue_ids` | List[int] | IDs of GitHub Issues that were just closed (merged).         |
| `tasks_dir`        | Path      | Root directory where task files are located (`reqs/tasks/`). |

## 3. Logic Details

### 3.1. Completed Task Identification

1.  Scan `reqs/tasks/_archive/` for files where `issue_id` matches any of `closed_issue_ids`.
2.  Update the `status` of these files to `Completed` if they are not already.

### 3.2. Dependency Re-evaluation (Promotion)

1.  Identify **Candidate Tasks**:
    - Scan all ADR folders `reqs/tasks/<ADR-ID>/` for tasks that list the `Completed` tasks' `id` in their `depends_on`.
2.  For each Candidate Task:
    - Call the **Ready Judgment Logic** (defined in `creation_logic.md`).
    - If the criteria are met:
      - Update `status` to `Ready`.
3.  **Idempotency Check**:
    - Do not update if the status is already `Ready`, `Issued`, or `Completed`.

### 3.3. Automatic Sync PR (Optional / Workflow Trigger)

If any tasks were promoted to `Ready`:

1.  Create a new branch: `feat/promote-ready-tasks-<timestamp>`.
2.  Commit the updated task files (status change).
3.  Create a Pull Request to `main` with the title `feat: promote tasks to Ready status`.
4.  Rationale: This alerts the team that new tasks are ready for issue creation (via `ick create`).

## 4. Safety Mechanisms

### 4.1. Conflict Prevention

- If the file is already being modified in another active PR, skip the update to avoid merge conflicts.

### 4.2. Cycle Protection

- Reuse the DAG analysis from `creation_logic.md` to ensure that promotion doesn't happen in a way that violates DAG principles.

## 5. Edge Cases

| Case                                                  | Expected Behavior                                        |
| :---------------------------------------------------- | :------------------------------------------------------- |
| Issue closed but not merged (Cancelled)               | Update status to `Cancelled`. Do not promote dependents. |
| Dependency is outside current ADR                     | Supported (Global ID lookup).                            |
| All dependencies are met but task is already `Issued` | Skip (Idempotency).                                      |
