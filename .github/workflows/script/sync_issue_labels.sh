#!/bin/bash
set -e

# Sync labels from linked issues to the pull request.
# This ensures that metadata-driven automation (like Gemini analyzer) has the correct context.

PR_NUMBER=$1
if [ -z "$PR_NUMBER" ]; then
  echo "Error: PR_NUMBER is required."
  exit 1
fi

# Ensure gh CLI is available
if ! command -v gh >/dev/null 2>&1; then
  echo "Error: GitHub CLI (gh) is not installed."
  exit 1
fi

echo "[INFO] Syncing labels for PR #$PR_NUMBER..."

# 1. Get linked issue numbers (Closing issues)
# closingIssuesReferences is the standard way GitHub links PRs to issues (via "Fixes #123" etc.)
ISSUE_NUMBERS=$(gh pr view "$PR_NUMBER" --json closingIssuesReferences -q '.closingIssuesReferences[].number' 2>/dev/null || echo "")

# 2. Fallback: Extract issue numbers from PR body if closingIssuesReferences is empty
# This is useful for non-standard links or if the API doesn't populate it yet.
if [ -z "$ISSUE_NUMBERS" ]; then
  echo "[INFO] No issues linked via closingIssuesReferences. Checking PR body..."
  BODY=$(gh pr view "$PR_NUMBER" --json body -q '.body' 2>/dev/null || echo "")
  # Match "Fixes #123", "Closes #123", "Fixes#123", etc. (case-insensitive, POSIX-compatible)
  ISSUE_NUMBERS=$(echo "$BODY" | grep -Ei '(close|closes|closed|fix|fixes|fixed|resolve|resolves|resolved)[[:space:]]*#[0-9]+' | sed -E 's/.*#([0-9]+).*/\1/' | sort -u | tr '\n' ' ' || echo "")
fi

if [ -z "$ISSUE_NUMBERS" ] || [ "$ISSUE_NUMBERS" = " " ]; then
  echo "[INFO] No linked issues found for PR #$PR_NUMBER. Skipping label sync."
  exit 0
fi

echo "[INFO] Linked issues found: $ISSUE_NUMBERS"

ALL_LABELS=""

# 3. Fetch labels from each linked issue
for ISSUE_NUMBER in $ISSUE_NUMBERS; do
  echo "[INFO] Fetching labels from Issue #$ISSUE_NUMBER..."
  LABELS=$(gh issue view "$ISSUE_NUMBER" --json labels -q '.labels[].name' 2>/dev/null || echo "")
  if [ -n "$LABELS" ]; then
    if [ -z "$ALL_LABELS" ]; then
      ALL_LABELS="$LABELS"
    else
      ALL_LABELS="$ALL_LABELS"$'\n'"$LABELS"
    fi
  fi
done

if [ -z "$ALL_LABELS" ]; then
  echo "[INFO] No labels found in linked issues."
  exit 0
fi

# 4. Get current PR labels to avoid redundant updates
CURRENT_PR_LABELS=$(gh pr view "$PR_NUMBER" --json labels -q '.labels[].name' 2>/dev/null || echo "")

# 5. Get unique labels from issues, and filter out those already on the PR
MISSING_LABELS_STR=""
UNIQUE_ISSUE_LABELS=$(echo "$ALL_LABELS" | sort -u)

LABEL_ARGS=()
while IFS= read -r label; do
  if [ -n "$label" ]; then
    if ! echo "$CURRENT_PR_LABELS" | grep -qx "$label"; then
      LABEL_ARGS+=(--add-label "$label")
      if [ -z "$MISSING_LABELS_STR" ]; then
        MISSING_LABELS_STR="$label"
      else
        MISSING_LABELS_STR="$MISSING_LABELS_STR, $label"
      fi
    fi
  fi
done <<< "$UNIQUE_ISSUE_LABELS"

if [ "${#LABEL_ARGS[@]}" -eq 0 ]; then
  echo "[INFO] All labels from issues are already present on PR #$PR_NUMBER."
  exit 0
fi

# 6. Apply labels safely
echo "[INFO] Adding missing labels to PR #$PR_NUMBER: $MISSING_LABELS_STR"
if ! gh pr edit "$PR_NUMBER" "${LABEL_ARGS[@]}" > /dev/null; then
  echo "[ERROR] Failed to add labels to PR #$PR_NUMBER"
  exit 1
fi
echo "[DONE] Labels synced successfully."
