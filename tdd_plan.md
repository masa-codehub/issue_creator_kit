## TDD Plan

### 1. WorkflowUseCase Test
- **Goal:** Verify logic of `WorkflowUseCase.run`.
- **Tests:**
  1. `test_run_success`: Mock approval returns True -> verify git ops.
  2. `test_run_no_changes`: Mock approval returns False -> verify NO git ops.
  3. `test_run_error`: Mock approval raises Error -> verify propagation.

### 2. ApprovalUseCase Test
- **Goal:** Verify logic of `ApprovalUseCase.process_single_file` and `process_all_files`.
- **Tests:**
  1. `test_process_single_file_success`: Mock FS/GitHub -> verify sequence of updates/move/issue-creation.
  2. `test_process_single_file_rollback`: Mock Issue creation failure -> verify file move rollback.
  3. `test_process_all_files`: Verify iteration and return value.

### Constraint Check
- Code already exists, so tests might pass immediately (Green).
- This is acceptable as the goal is coverage.

