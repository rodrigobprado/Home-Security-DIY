#!/usr/bin/env bash
# =============================================================================
# Home Security DIY - Local Config Validation
# =============================================================================
# Runs all configuration validations locally before commit.
#
# Usage:
#   ./scripts/validate-configs.sh
#
# Requirements:
#   - yamllint (pip install yamllint)
#   - docker compose
#   - shellcheck (apt install shellcheck)
#   - kustomize or kubectl (optional, for K8s validation)
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="${SCRIPT_DIR}/.."

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

ERRORS=0

log_info()  { echo -e "${BLUE}[INFO]${NC} $*"; }
log_ok()    { echo -e "${GREEN}[PASS]${NC} $*"; }
log_warn()  { echo -e "${YELLOW}[SKIP]${NC} $*"; }
log_fail()  { echo -e "${RED}[FAIL]${NC} $*"; ERRORS=$((ERRORS + 1)); }

echo "=============================================="
echo " Home Security DIY - Config Validation"
echo "=============================================="
echo ""

# ---------------------------------------------------------------------------
# 1. YAML Lint
# ---------------------------------------------------------------------------
log_info "1/5 YAML Lint..."

if command -v yamllint &>/dev/null; then
    if yamllint -c "${PROJECT_DIR}/.yamllint.yml" \
        "${PROJECT_DIR}/src/docker-compose.yml" \
        "${PROJECT_DIR}/k8s/base/" \
        "${PROJECT_DIR}/k8s/overlays/" 2>&1; then
        log_ok "YAML lint passed"
    else
        log_fail "YAML lint failed"
    fi
else
    log_warn "yamllint not installed (pip install yamllint)"
fi

echo ""

# ---------------------------------------------------------------------------
# 2. Docker Compose validation
# ---------------------------------------------------------------------------
log_info "2/5 Docker Compose validation..."

if command -v docker &>/dev/null; then
    # Create temporary .env if not exists
    ENV_FILE="${PROJECT_DIR}/src/.env"
    TEMP_ENV=0
    if [[ ! -f "$ENV_FILE" ]]; then
        cp "${PROJECT_DIR}/src/.env.example" "$ENV_FILE"
        TEMP_ENV=1
    fi

    if docker compose -f "${PROJECT_DIR}/src/docker-compose.yml" config --quiet 2>&1; then
        log_ok "Docker Compose config valid"
    else
        log_fail "Docker Compose config invalid"
    fi

    # Cleanup temp .env
    if [[ $TEMP_ENV -eq 1 ]]; then
        rm -f "$ENV_FILE"
    fi
else
    log_warn "docker not installed"
fi

echo ""

# ---------------------------------------------------------------------------
# 3. Kubernetes manifests validation
# ---------------------------------------------------------------------------
log_info "3/5 Kubernetes manifests validation..."

if command -v kubectl &>/dev/null; then
    for overlay in staging production; do
        overlay_dir="${PROJECT_DIR}/k8s/overlays/${overlay}"
        if [[ -d "$overlay_dir" ]]; then
            if kubectl kustomize "$overlay_dir" >/dev/null 2>&1; then
                log_ok "Kustomize build (${overlay}) passed"
            else
                log_fail "Kustomize build (${overlay}) failed"
            fi
        fi
    done
else
    log_warn "kubectl not installed (K8s validation skipped)"
fi

echo ""

# ---------------------------------------------------------------------------
# 4. Shell scripts lint
# ---------------------------------------------------------------------------
log_info "4/5 Shell scripts lint..."

if command -v shellcheck &>/dev/null; then
    SHELL_OK=1
    for script in "${PROJECT_DIR}"/scripts/*.sh; do
        if [[ -f "$script" ]]; then
            if shellcheck "$script" 2>&1; then
                log_ok "shellcheck: $(basename "$script")"
            else
                log_fail "shellcheck: $(basename "$script")"
                SHELL_OK=0
            fi
        fi
    done
    if [[ $SHELL_OK -eq 1 ]]; then
        log_ok "All shell scripts passed"
    fi
else
    log_warn "shellcheck not installed (apt install shellcheck)"
fi

echo ""

# ---------------------------------------------------------------------------
# 5. Environment variables check
# ---------------------------------------------------------------------------
log_info "5/5 Environment variables check..."

COMPOSE_FILE="${PROJECT_DIR}/src/docker-compose.yml"
ENV_EXAMPLE="${PROJECT_DIR}/src/.env.example"

if [[ -f "$COMPOSE_FILE" && -f "$ENV_EXAMPLE" ]]; then
    MISSING=0
    while IFS= read -r var; do
        # Extract variable name from ${VAR:-default} or ${VAR}
        var_name=$(echo "$var" | grep -oP '(?<=\$\{)\w+' | head -1)
        if [[ -n "$var_name" && "$var_name" != "SYS" ]]; then
            if ! grep -q "^${var_name}=" "$ENV_EXAMPLE" 2>/dev/null && \
               ! grep -q "^#.*${var_name}=" "$ENV_EXAMPLE" 2>/dev/null; then
                log_fail "Variable ${var_name} used in compose but missing from .env.example"
                MISSING=1
            fi
        fi
    done < <(grep -oP '\$\{[^}]+\}' "$COMPOSE_FILE" | sort -u)

    if [[ $MISSING -eq 0 ]]; then
        log_ok "All compose variables found in .env.example"
    fi
else
    log_warn "docker-compose.yml or .env.example not found"
fi

echo ""
echo "=============================================="
if [[ $ERRORS -eq 0 ]]; then
    echo -e "${GREEN}All checks passed!${NC}"
else
    echo -e "${RED}${ERRORS} check(s) failed.${NC}"
fi
echo "=============================================="

exit $ERRORS
