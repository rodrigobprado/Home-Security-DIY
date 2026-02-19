#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   ./scripts/pr_flow.sh --title "fix: ..." --issues "7 8 9" [--base main] [--summary-file /tmp/summary.md]

BASE_BRANCH="main"
PR_TITLE=""
ISSUES=""
SUMMARY_FILE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --title)
      PR_TITLE="${2:-}"
      shift 2
      ;;
    --issues)
      ISSUES="${2:-}"
      shift 2
      ;;
    --base)
      BASE_BRANCH="${2:-main}"
      shift 2
      ;;
    --summary-file)
      SUMMARY_FILE="${2:-}"
      shift 2
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

if [[ -z "$PR_TITLE" ]]; then
  echo "Missing required argument: --title" >&2
  exit 1
fi

if [[ -z "$ISSUES" ]]; then
  echo "Missing required argument: --issues \"7 8 ...\"" >&2
  exit 1
fi

CURRENT_BRANCH="$(git branch --show-current)"
if [[ "$CURRENT_BRANCH" == "$BASE_BRANCH" ]]; then
  echo "Refusing to create PR from base branch '$BASE_BRANCH'. Create/use a feature branch first." >&2
  exit 1
fi

TMP_BODY="$(mktemp)"
trap 'rm -f "$TMP_BODY"' EXIT

{
  echo "## Summary"
  if [[ -n "$SUMMARY_FILE" ]]; then
    cat "$SUMMARY_FILE"
  else
    echo "- describe the main code changes here"
  fi
  echo
  echo "## Validation Checklist"
  echo "- [ ] tests added/updated where applicable"
  echo "- [ ] local validation executed (lint/tests/build)"
  echo "- [ ] no secrets/tokens/real IPs committed"
  echo "- [ ] docs/config examples updated when needed"
  echo
  echo "## Operational Checklist"
  echo "- [ ] backward-compatibility impact reviewed"
  echo "- [ ] rollout/rollback considerations reviewed"
  echo
  echo "## Linked Issues"
  for issue in $ISSUES; do
    echo "- Closes #$issue"
  done
} > "$TMP_BODY"

gh pr create \
  --base "$BASE_BRANCH" \
  --head "$CURRENT_BRANCH" \
  --title "$PR_TITLE" \
  --body-file "$TMP_BODY"

