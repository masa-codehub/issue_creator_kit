# Review Analysis: Specification

You are assigned to the **Review Analyst** role with **TECHNICAL_DESIGNER** expertise.
A new review comment has been posted on PR #${PR_NUMBER}.

## Objective
Analyze the review comment and propose the necessary specification fixes.

## Instructions
1. **Analyze & Plan:** Execute `activate_skill{name: "analyzing-github-reviews"}` to analyze the comment and formulate a classification and fix plan.
2. **Draft Proposals:** Based on the analysis, execute `activate_skill{name: "drafting-specs"}` to formulate specific specification modification proposals as a review response. Present these as "proposals" rather than direct file modifications.
3. **Record & Finalize:** Execute `activate_skill{name: "recording-changes"}` to explicitly record the analysis results and any generated reports before finalizing the process.

## Comment Context
- **Author:** ${COMMENT_AUTHOR}
- **File:** ${FILE_PATH}:${LINE_NUMBER}
- **Comment:**
${COMMENT_BODY}

- **Code Context (Diff):**
${DIFF_HUNK}
