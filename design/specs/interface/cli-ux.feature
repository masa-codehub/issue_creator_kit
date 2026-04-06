Feature: CLI User Experience (ADR-017)
  As a developer using the Issue Creator Kit
  I want a consistent and informative CLI experience
  So that I can safely automate document management and issue creation.

  Background:
    Given the environment is set up with a valid GitHub token
    And the project root contains ADRs and Task drafts

  Scenario: Successful issue processing in execute mode
    When I run "issue-kit process --execute"
    Then the exit code should be 0
    And the output should contain "Created L1 Issue for"
    And the output should contain "Task activation complete"

  Scenario: Previewing changes in dry-run mode
    When I run "issue-kit process --dry-run"
    Then the exit code should be 0
    And the output should contain "[INFO] Detected"
    And the output should contain "Dry-run summary:"

  Scenario: Failing due to missing safety flag
    When I run "issue-kit process"
    Then the exit code should be 2
    And the output should contain "[FAIL]"
    And the output should contain "Either --execute or --dry-run must be specified"

  Scenario: Validation failure during check
    Given a task file with an invalid ID format
    When I run "issue-kit check"
    Then the exit code should be 1
    And the output should contain "[FAIL]"
    And the output should contain "ID 形式が不正です。期待される形式: task-XXX-NN"

  Scenario: Handling multiple validation errors
    Given multiple files with validation errors
    When I run "issue-kit check"
    Then the output should list all validation errors without stopping early
    And the exit code should be 1
