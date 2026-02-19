#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ERRORS=0

check_file_links() {
    local md_file="$1"
    local md_dir
    md_dir="$(cd "$(dirname "$md_file")" && pwd)"

    while IFS= read -r link; do
        [[ -z "$link" ]] && continue
        [[ "$link" =~ ^https?:// ]] && continue
        [[ "$link" =~ ^mailto: ]] && continue
        [[ "$link" =~ ^# ]] && continue

        local target="${link%%#*}"
        [[ -z "$target" ]] && continue

        if [[ "$target" = /* ]]; then
            target_path="${ROOT_DIR}${target}"
        elif [[ "$target" =~ ^(README\.md|CONTRIBUTING\.md|SECURITY\.md|LICENSE|docs/|k8s/|src/|scripts/|tests/|tasks/|prd/) ]]; then
            target_path="${ROOT_DIR}/${target}"
        else
            target_path="${md_dir}/${target}"
        fi

        if [[ ! -e "$target_path" ]]; then
            echo "[FAIL] $md_file -> $link"
            ERRORS=$((ERRORS + 1))
        fi
    done < <(grep -oP '\[[^]]+\]\(\K[^)]+' "$md_file" || true)
}

while IFS= read -r md; do
    check_file_links "$md"
done < <(
    find "$ROOT_DIR" -maxdepth 3 -type f -name "*.md" \
        ! -path "$ROOT_DIR/wiki/*" \
        ! -path "$ROOT_DIR/.github/ISSUE_TEMPLATE/*" \
        | sort
)

if [[ $ERRORS -gt 0 ]]; then
    echo "Found $ERRORS broken local markdown links."
    exit 1
fi

echo "All local markdown links are valid."
