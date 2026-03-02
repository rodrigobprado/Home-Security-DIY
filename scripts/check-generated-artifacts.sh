#!/usr/bin/env bash
set -euo pipefail

BASE_REF="${1:-}"

if [[ -z "${BASE_REF}" ]]; then
  if [[ -n "${GITHUB_BASE_REF:-}" ]]; then
    BASE_REF="origin/${GITHUB_BASE_REF}"
  elif git rev-parse --verify HEAD~1 >/dev/null 2>&1; then
    BASE_REF="HEAD~1"
  else
    BASE_REF="HEAD"
  fi
fi

changed_paths="$(git diff --name-only --diff-filter=ACMRT "${BASE_REF}"...HEAD || true)"

if [[ -z "${changed_paths}" ]]; then
  echo "No changed files to inspect."
  exit 0
fi

artifact_hits="$(echo "${changed_paths}" | grep -E '(^|/)(node_modules|coverage|__pycache__)(/|$)|(^|/)\.coverage$' || true)"

if [[ -n "${artifact_hits}" ]]; then
  echo "[FAIL] Generated artifacts detected in changed paths:"
  echo "${artifact_hits}" | sed 's/^/ - /'
  exit 1
fi

echo "Generated artifact check passed."
