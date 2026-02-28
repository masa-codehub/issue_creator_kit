#!/bin/bash
set -e

TARGET_KEY="${SYNC_TARGET_KEY:-public_repo}"

# 1. Try to read from pyproject.toml
PYPROJECT_REPO=""
if [ -f "dev-repo/pyproject.toml" ]; then
  PYPROJECT_REPO=$(grep -A 10 "\[tool\.sync\]" dev-repo/pyproject.toml | grep "^${TARGET_KEY}\s*=" | cut -d'"' -f2 || true)
fi

# 2. Determine final REPO and OWNER
# pyproject.toml takes precedence if it contains a full owner/repo string
if [[ "$PYPROJECT_REPO" == *"/"* ]]; then
  # Split the string by /
  OWNER="${PYPROJECT_REPO%%/*}"
  REPO="${PYPROJECT_REPO#*/}"
else
  OWNER="$FALLBACK_OWNER"
  # If pyproject has a value but no slash, assume it's just the repo name
  if [ -n "$PYPROJECT_REPO" ]; then
    REPO="$PYPROJECT_REPO"
  else
    REPO="$FALLBACK_REPO"
  fi
fi

if [ -z "$REPO" ]; then
  echo "Target repository is not set in pyproject.toml or variables. Skipping synchronization."
  echo "skip=true" >> "$GITHUB_OUTPUT"
  exit 0
fi

echo "skip=false" >> "$GITHUB_OUTPUT"
echo "SYNC_OWNER=$OWNER" >> "$GITHUB_ENV"
echo "SYNC_REPO=$REPO" >> "$GITHUB_ENV"