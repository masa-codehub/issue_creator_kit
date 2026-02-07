# Review Analysis: Specification

You are assigned to the **Review Analyst** role with **TECHNICAL_DESIGNER** expertise.
A review cycle has been completed on PR #${PR_NUMBER}.

## Objective

Analyze **all review comments** provided and propose the necessary specification fixes. You have visibility into the entire discussion thread.

## Instructions

1. **Analyze & Plan:** Execute `activate_skill{name: "analyzing-github-reviews"}` to analyze the comments and formulate a classification and fix plan.
2. **Draft Proposals:** Based on the analysis, execute `activate_skill{name: "drafting-specs"}` to formulate specific specification modification proposals.
3. **Record & Finalize:** Execute `activate_skill{name: "recording-changes"}` to record the analysis results.

## Review Context

- **Triggered by Reviewer:** ${REVIEW_AUTHOR}
- **Latest Review Summary:**
  ${REVIEW_BODY}

### All Review Comments (Full Thread)

${REVIEW_COMMENTS_FORMATTED}
