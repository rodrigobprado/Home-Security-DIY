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
target_files="$(echo "${changed_files}" | grep -E '\.(ya?ml|conf|template)$' || true)"

if [[ -z "${target_files}" ]]; then
  echo "No changed YAML/CONF/template files to scan."
  exit 0
fi

echo "Scanning changed files for hardcoded secrets..."
echo "${target_files}" | sed 's/^/ - /'

failed=0
while IFS= read -r file; do
  [[ -z "${file}" ]] && continue
  [[ -f "${file}" ]] || continue

  if grep -nE 'CHANGE_ME|HomeSec-[A-Za-z0-9._-]+' "${file}" >/dev/null; then
    echo "[FAIL] Placeholder or inline credential marker in ${file}:"
    grep -nE 'CHANGE_ME|HomeSec-[A-Za-z0-9._-]+' "${file}" || true
    failed=1
  fi

  if grep -nE 'proxy_set_header[[:space:]]+X-(API|Admin)-Key[[:space:]]+"[^"$]+' "${file}" >/dev/null; then
    echo "[FAIL] Hardcoded API/Admin key header in ${file}:"
    grep -nE 'proxy_set_header[[:space:]]+X-(API|Admin)-Key[[:space:]]+"[^"$]+' "${file}" || true
    failed=1
  fi

  if [[ "${file}" == *.yml || "${file}" == *.yaml ]]; then
    if awk '
      BEGIN { sensitive = ""; bad = 0 }
      /^[[:space:]]*-[[:space:]]*name:[[:space:]]*(HA_TOKEN|DATABASE_URL|DASHBOARD_API_KEY|DASHBOARD_ADMIN_KEY)[[:space:]]*$/ {
        sensitive = $0
        next
      }
      sensitive != "" && /^[[:space:]]*value:[[:space:]]*/ {
        print "[FAIL] Sensitive env uses value instead of valueFrom in '"${file}"': " $0
        bad = 1
        sensitive = ""
        next
      }
      sensitive != "" && /^[[:space:]]*valueFrom:[[:space:]]*$/ {
        sensitive = ""
        next
      }
      sensitive != "" && /^[[:space:]]*$/ { next }
      sensitive != "" && /^[[:space:]]*#/ { next }
      sensitive != "" { sensitive = "" }
      END { exit bad }
    ' "${file}"; then
      :
    else
      failed=1
    fi
  fi
done <<< "${target_files}"

if [[ "${failed}" -ne 0 ]]; then
  echo "Hardcoded secret scan failed."
  exit 1
fi

echo "Hardcoded secret scan passed."
