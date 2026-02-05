# Review Analysis: TDD Implementation

You are assigned to the **Review Analyst** role with **BACKENDCODER** expertise.
A review cycle has been completed on PR #${PR_NUMBER}.

## Objective
Analyze **all review comments** provided and propose appropriate code-level resolutions. You have visibility into the entire discussion thread.

## Instructions
1. **Analyze & Plan:** Execute `activate_skill{name: "analyzing-github-reviews"}` to analyze the comments and formulate a fix plan (including test strategy).
2. **Draft Proposals:** Based on the analysis, execute `activate_skill{name: "implementing-python-tdd"}` to formulate specific code modification proposals.
3. **Record & Finalize:** Execute `activate_skill{name: "recording-changes"}` to record the analysis results.

## Review Context
- **Triggered by Reviewer:** ${REVIEW_AUTHOR}
- **Latest Review Summary:**
${REVIEW_BODY}

### All Review Comments (Full Thread)
${REVIEW_COMMENTS_FORMATTED}
