#!/usr/bin/env bash
set -euo pipefail

ENV_FILE="${1:-src/.env}"
OUT_DIR="k8s/generated/secrets"
NAMESPACE="home-security"

if [[ ! -f "$ENV_FILE" ]]; then
  echo "Env file not found: $ENV_FILE" >&2
  exit 1
fi

set -a
# shellcheck disable=SC1090
source "$ENV_FILE"
set +a

required_vars=(
  MQTT_USER
  MQTT_PASSWORD
  POSTGRES_USER
  POSTGRES_PASSWORD
  POSTGRES_DB
  POSTGRES_HA_PASSWORD
  POSTGRES_DASHBOARD_PASSWORD
  POSTGRES_METRICS_PASSWORD
  HA_TOKEN
  HA_HOST
  DASHBOARD_API_KEY
)

for var_name in "${required_vars[@]}"; do
  if [[ -z "${!var_name:-}" ]]; then
    echo "Missing required env var in $ENV_FILE: $var_name" >&2
    exit 1
  fi
done

mkdir -p "$OUT_DIR"

kubectl create namespace "$NAMESPACE" --dry-run=client -o yaml > "$OUT_DIR/00-namespace.yaml"

kubectl create secret generic mqtt-credentials \
  -n "$NAMESPACE" \
  --from-literal=MQTT_USER="$MQTT_USER" \
  --from-literal=MQTT_PASSWORD="$MQTT_PASSWORD" \
  --dry-run=client -o yaml > "$OUT_DIR/mqtt-credentials.yaml"

kubectl create secret generic postgres-credentials \
  -n "$NAMESPACE" \
  --from-literal=POSTGRES_USER="$POSTGRES_USER" \
  --from-literal=POSTGRES_PASSWORD="$POSTGRES_PASSWORD" \
  --from-literal=POSTGRES_DB="$POSTGRES_DB" \
  --from-literal=POSTGRES_HA_PASSWORD="$POSTGRES_HA_PASSWORD" \
  --from-literal=POSTGRES_DASHBOARD_PASSWORD="$POSTGRES_DASHBOARD_PASSWORD" \
  --from-literal=POSTGRES_METRICS_PASSWORD="$POSTGRES_METRICS_PASSWORD" \
  --from-literal=POSTGRES_HA_URL="postgresql+psycopg2://ha_user:${POSTGRES_HA_PASSWORD}@postgres.home-security.svc.cluster.local:5432/${POSTGRES_DB}?options=-csearch_path%3Dhomeassistant" \
  --dry-run=client -o yaml > "$OUT_DIR/postgres-credentials.yaml"

DASHBOARD_ALLOWED_ORIGINS_VAL="${DASHBOARD_ALLOWED_ORIGINS:-https://dashboard.home.local}"

kubectl create secret generic dashboard-credentials \
  -n "$NAMESPACE" \
  --from-literal=ha-token="$HA_TOKEN" \
  --from-literal=ha-url="http://${HA_HOST}:8123" \
  --from-literal=database-url="postgresql+asyncpg://dashboard_user:${POSTGRES_DASHBOARD_PASSWORD}@postgres:5432/${POSTGRES_DB}?options=-csearch_path%3Ddashboard" \
  --from-literal=dashboard-api-key="$DASHBOARD_API_KEY" \
  --from-literal=dashboard-allowed-origins="$DASHBOARD_ALLOWED_ORIGINS_VAL" \
  --dry-run=client -o yaml > "$OUT_DIR/dashboard-credentials.yaml"

echo "Generated secrets in $OUT_DIR"
echo "Apply with:"
echo "  kubectl apply -f $OUT_DIR/"
