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

changed_files="$(git diff --name-only --diff-filter=ACMRT "${BASE_REF}"...HEAD || true)"
target_files="$(echo "${changed_files}" | grep -E '^k8s/.*\.ya?ml$' || true)"

if [[ -z "${target_files}" ]]; then
  echo "No changed K8s YAML files to scan."
  exit 0
fi

echo "Scanning changed K8s manifests for runAsNonRoot policy..."
echo "${target_files}" | sed 's/^/ - /'

failed=0
while IFS= read -r file; do
  [[ -z "${file}" ]] && continue
  [[ -f "${file}" ]] || continue

  if grep -nE '^[[:space:]]*runAsNonRoot:[[:space:]]*false[[:space:]]*$' "${file}" >/dev/null; then
    if grep -q "SECURITY_EXCEPTION_RUN_AS_NON_ROOT_FALSE" "${file}"; then
      echo "[WARN] runAsNonRoot=false found with documented exception in ${file}"
      continue
    fi
    echo "[FAIL] runAsNonRoot=false without documented exception in ${file}:"
    grep -nE '^[[:space:]]*runAsNonRoot:[[:space:]]*false[[:space:]]*$' "${file}" || true
    failed=1
  fi
done <<< "${target_files}"

if [[ "${failed}" -ne 0 ]]; then
  echo "K8s non-root policy check failed."
  exit 1
fi

echo "K8s non-root policy check passed."
