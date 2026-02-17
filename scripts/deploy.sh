#!/usr/bin/env bash
# =============================================================================
# Home Security DIY - K3s Deployment Script
# =============================================================================
# Usage:
#   ./deploy.sh staging    # Deploy to staging
#   ./deploy.sh production # Deploy to production
#   ./deploy.sh teardown staging     # Remove staging
#   ./deploy.sh teardown production  # Remove production
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
K8S_DIR="${SCRIPT_DIR}/../k8s"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info()  { echo -e "${BLUE}[INFO]${NC} $*"; }
log_ok()    { echo -e "${GREEN}[OK]${NC} $*"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC} $*"; }
log_error() { echo -e "${RED}[ERROR]${NC} $*"; }

# ---------------------------------------------------------------------------
# Pre-flight checks
# ---------------------------------------------------------------------------
check_prerequisites() {
    local missing=0

    if ! command -v kubectl &>/dev/null; then
        log_error "kubectl not found. Install K3s first: curl -sfL https://get.k3s.io | sh -"
        missing=1
    fi

    if ! kubectl cluster-info &>/dev/null 2>&1; then
        log_error "Cannot connect to Kubernetes cluster. Is K3s running?"
        missing=1
    fi

    if ! command -v kustomize &>/dev/null && ! kubectl kustomize --help &>/dev/null 2>&1; then
        log_warn "kustomize not found, using 'kubectl apply -k' instead."
    fi

    if [[ $missing -eq 1 ]]; then
        exit 1
    fi
}

# ---------------------------------------------------------------------------
# Label nodes
# ---------------------------------------------------------------------------
label_nodes() {
    log_info "Labeling nodes for hardware affinity..."

    local node
    node=$(kubectl get nodes -o jsonpath='{.items[0].metadata.name}')

    # Label for Zigbee USB coordinator
    kubectl label node "$node" home-security/zigbee-coordinator=true --overwrite 2>/dev/null || true
    log_ok "Node '$node' labeled: zigbee-coordinator=true"

    # Label for Intel GPU (OpenVINO)
    if [[ -d /dev/dri ]]; then
        kubectl label node "$node" home-security/intel-gpu=true --overwrite 2>/dev/null || true
        log_ok "Node '$node' labeled: intel-gpu=true"
    else
        log_warn "No /dev/dri found. Frigate will not have GPU acceleration."
    fi
}

# ---------------------------------------------------------------------------
# Deploy
# ---------------------------------------------------------------------------
deploy() {
    local env="$1"
    local overlay_dir="${K8S_DIR}/overlays/${env}"

    if [[ ! -d "$overlay_dir" ]]; then
        log_error "Overlay directory not found: $overlay_dir"
        log_error "Valid environments: staging, production"
        exit 1
    fi

    log_info "Deploying Home Security DIY to ${env}..."

    # Label nodes for hardware affinity
    label_nodes

    # Apply with kustomize
    log_info "Applying Kustomize overlay: ${env}"
    kubectl apply -k "$overlay_dir"

    # Wait for rollout
    local namespace="home-security"
    if [[ "$env" == "staging" ]]; then
        namespace="home-security-staging"
    fi

    log_info "Waiting for deployments to be ready..."
    for deployment in mosquitto zigbee2mqtt frigate homeassistant; do
        local full_name="$deployment"
        if [[ "$env" == "staging" ]]; then
            full_name="stg-${deployment}"
        fi

        log_info "  Waiting for ${full_name}..."
        kubectl rollout status deployment/"$full_name" \
            -n "$namespace" \
            --timeout=120s 2>/dev/null || \
            log_warn "  ${full_name} not ready yet (may need hardware or config)"
    done

    echo ""
    log_ok "Deployment to ${env} complete!"
    echo ""

    # Show status
    log_info "Current status:"
    kubectl get pods -n "$namespace" -o wide
    echo ""
    kubectl get svc -n "$namespace"
    echo ""

    if [[ "$env" == "production" ]]; then
        kubectl get ingress -n "$namespace" 2>/dev/null || true
        echo ""
        log_info "Access points:"
        echo "  Home Assistant: http://security.home.local  (or http://<NODE_IP>:8123)"
        echo "  Frigate NVR:    http://frigate.home.local   (or http://<NODE_IP>:5000)"
        echo "  Zigbee2MQTT:    http://zigbee.home.local    (or http://<NODE_IP>:8080)"
        echo "  MQTT Broker:    mqtt://<NODE_IP>:31883"
    else
        local node_ip
        node_ip=$(kubectl get nodes -o jsonpath='{.items[0].status.addresses[?(@.type=="InternalIP")].address}')
        log_info "Access via NodePort or port-forward:"
        echo "  kubectl port-forward svc/stg-homeassistant 8123:8123 -n $namespace"
        echo "  kubectl port-forward svc/stg-frigate 5000:5000 -n $namespace"
        echo "  kubectl port-forward svc/stg-zigbee2mqtt 8080:8080 -n $namespace"
    fi
}

# ---------------------------------------------------------------------------
# Teardown
# ---------------------------------------------------------------------------
teardown() {
    local env="$1"
    local overlay_dir="${K8S_DIR}/overlays/${env}"

    if [[ ! -d "$overlay_dir" ]]; then
        log_error "Overlay directory not found: $overlay_dir"
        exit 1
    fi

    log_warn "This will DELETE all Home Security resources in ${env}!"
    read -rp "Are you sure? (yes/N): " confirm
    if [[ "$confirm" != "yes" ]]; then
        log_info "Cancelled."
        exit 0
    fi

    log_info "Tearing down ${env}..."
    kubectl delete -k "$overlay_dir" --ignore-not-found=true

    log_ok "Teardown of ${env} complete."
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
main() {
    if [[ $# -lt 1 ]]; then
        echo "Usage: $0 <staging|production>"
        echo "       $0 teardown <staging|production>"
        exit 1
    fi

    check_prerequisites

    case "$1" in
        staging|production)
            deploy "$1"
            ;;
        teardown)
            if [[ $# -lt 2 ]]; then
                log_error "Usage: $0 teardown <staging|production>"
                exit 1
            fi
            teardown "$2"
            ;;
        *)
            log_error "Unknown command: $1"
            echo "Usage: $0 <staging|production>"
            echo "       $0 teardown <staging|production>"
            exit 1
            ;;
    esac
}

main "$@"
