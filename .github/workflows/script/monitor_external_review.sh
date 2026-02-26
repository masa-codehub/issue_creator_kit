#!/bin/bash
set -e

# Monitor for NEW external review activity based on available PR data.
# Fallback to 'comments,reviews,commits' since 'timeline' might not be available in older gh CLI versions.

PR_NUMBER=$1
if [ -z "$PR_NUMBER" ]; then
  echo "Error: PR_NUMBER is required."
  exit 1
fi

TRIGGER_LABEL="${TRIGGER_LABEL:-gemini}"

echo "[INFO] Fetching labels for PR #$PR_NUMBER..."
LABELS=$(gh pr view "$PR_NUMBER" --json labels -q '.labels[].name' 2>/dev/null || echo "")

if ! echo "$LABELS" | grep -qE "(^|\s)(${TRIGGER_LABEL}|${TRIGGER_LABEL}:.*)($|\s)"; then
  echo "[SKIP] Trigger label '${TRIGGER_LABEL}' not found (Current labels: $(echo $LABELS | tr '\n' ' ')). Skipping monitoring."
  exit 0
fi

EXTERNAL_ACTORS=("copilot-pull-request-reviewer")
MARKER_PATTERNS=("Copilot started reviewing" "currently reviewing" "AI review requested")

# 0. Get current user
CURRENT_USER="${GITHUB_USER:-$(gh api user --jq .login 2>/dev/null || echo "")}"
echo "[INFO] Current runner identified as: '$CURRENT_USER'"

# 1. Fetch PR data (Use standard fields instead of timeline)
fetch_pr_data() {
  gh pr view "$PR_NUMBER" --json comments,reviews,commits,reviewRequests
}

# Epoch time helper
to_epoch() {
  date -d "$1" +%s 2>/dev/null || echo 0
}

check_status() {
  local data=$1
  
  # 最新コミット時刻 (構造揺らぎに対応: .committedDate or .commit.committedDate)
  T_COMMIT=$(echo "$data" | jq -r '
    (.commits // [])
    | map(.committedDate // .commit.committedDate // empty)
    | sort
    | .[-1] // "1970-01-01T00:00:00Z"
  ')
  
  # 最新の外部レビュー完了時刻 (Strict author whitelist match)
  T_REVIEW_END=$(echo "$data" | jq -r --argjson actors "$(printf '%s\n' "${EXTERNAL_ACTORS[@]}" | jq -R . | jq -s .)" '
    (.reviews // [])
    | map(select(.author.login as $login | $actors | any(. == $login)))
    | sort_by(.submittedAt) | .[-1].submittedAt // "1970-01-01T00:00:00Z"
  ')

  # 自分の最新トリガーコメント時刻 (Null-safe collections)
  T_TRIGGER=$(echo "$data" | jq -r \
    --arg user "$CURRENT_USER" \
    --argjson patterns "$(printf '%s\n' "${MARKER_PATTERNS[@]}" | jq -R . | jq -s .)" '
    (
      [(.comments // [])[] | select(.author.login == $user and ((.body // "") as $b | $patterns | any($b | contains(.)))) | {createdAt: .createdAt}]
      +
      [(.reviews // [])[] | select(.author.login == $user and ((.body // "") as $b | $patterns | any($b | contains(.)))) | {createdAt: .submittedAt}]
    )
    | sort_by(.createdAt)
    | .[-1].createdAt // "1970-01-01T00:00:00Z"
  ')

  # マーカーコメントの最新時刻
  T_MARKER=$(echo "$data" | jq -r --argjson patterns "$(printf '%s\n' "${MARKER_PATTERNS[@]}" | jq -R . | jq -s .)" '
    [(.comments // [])[] | select((.body // "") as $b | $patterns | any($b | contains(.)))]
    | sort_by(.createdAt) | .[-1].createdAt // "1970-01-01T00:00:00Z"
  ')

  # レビューリクエスト
  HAS_NEW_REQUEST=$(echo "$data" | jq -r --argjson actors "$(printf '%s\n' "${EXTERNAL_ACTORS[@]}" | jq -R . | jq -s .)" '
    (.reviewRequests // [])
    | map(
        .requestedReviewer.login // .login // empty
        | as $login
        | ($actors | any(. == $login))
      )
    | any
    | if . then "yes" else "no" end
  ')

  # エポック秒に変換して比較
  E_COMMIT=$(to_epoch "$T_COMMIT")
  E_REVIEW_END=$(to_epoch "$T_REVIEW_END")
  E_TRIGGER=$(to_epoch "$T_TRIGGER")
  E_MARKER=$(to_epoch "$T_MARKER")

  echo "[DEBUG] Commit: $T_COMMIT, ReviewEnd: $T_REVIEW_END, Trigger: $T_TRIGGER, Marker: $T_MARKER, Request: $HAS_NEW_REQUEST" >&2

  # A. 【発火】最新の外部レビュー完了が、コミットおよび前回のトリガーよりも新しい
  if [ "$E_REVIEW_END" -gt "$E_TRIGGER" ] && [ "$E_REVIEW_END" -ge "$E_COMMIT" ]; then
    echo "READY"
    return
  fi

  # B. 【待機】レビューは終わっていないが、最新コミット以降に「開始」の兆候がある
  if { [ "$E_MARKER" -ge "$E_COMMIT" ] && [ "$E_MARKER" -gt "$E_TRIGGER" ]; } || [ "$HAS_NEW_REQUEST" = "yes" ]; then
    echo "WAITING"
    return
  fi

  # C. 【スキップ】何も始まっていない、または現在の状態は処理済み
  echo "SKIP"
}

echo "[INFO] Analyzing PR #$PR_NUMBER activity for external review status..."

MAX_RETRIES=30
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
  DATA=$(fetch_pr_data)
  STATUS=$(check_status "$DATA")

  case "$STATUS" in
    "READY")
      echo "[DONE] New completed external review detected."
      gh pr review "$PR_NUMBER" --comment -b "New external review results detected. Activating automated analysis workflow."
      exit 0
      ;;
    "WAITING")
      echo "[WAIT] External review is in progress (marker or request detected). Waiting... ($((RETRY_COUNT+1))/$MAX_RETRIES)"
      sleep 30
      ;;
    "SKIP")
      if [ $RETRY_COUNT -lt 4 ]; then
        echo "[INFO] No activity yet. Waiting for potential external tool startup... ($((RETRY_COUNT+1))/5)"
        sleep 15
      else
        echo "[SKIP] No new external review activity detected since last commit or trigger."
        exit 0
      fi
      ;;
  esac
  RETRY_COUNT=$((RETRY_COUNT+1))
done

echo "[TIMEOUT] Monitor timed out. No new review activity finished within the time limit."
exit 0
