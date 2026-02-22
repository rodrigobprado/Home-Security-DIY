#!/usr/bin/env bash
set -euo pipefail

OUT_FILE="tasks/INTEGRATION_SMOKE_$(date +%F).md"
API_KEY="${DASHBOARD_API_KEY:-}"

check_http() {
  local name="$1"
  local url="$2"
  local expected="$3"
  local extra_header="${4:-}"

  local code
  if [ -n "$extra_header" ]; then
    code="$(curl -sS -m 8 -o /tmp/integration_check_body.txt -w "%{http_code}" -H "$extra_header" "$url" || true)"
  else
    code="$(curl -sS -m 8 -o /tmp/integration_check_body.txt -w "%{http_code}" "$url" || true)"
  fi

  if [ "$code" = "$expected" ]; then
    printf "| %s | PASS | HTTP %s |\n" "$name" "$code" >> "$OUT_FILE"
  else
    printf "| %s | FAIL | HTTP %s (esperado %s) |\n" "$name" "$code" "$expected" >> "$OUT_FILE"
  fi
}

mkdir -p "$(dirname "$OUT_FILE")"
cat > "$OUT_FILE" <<'HEADER'
# Smoke Test de Integração

HEADER

echo "Data: $(date -Iseconds)" >> "$OUT_FILE"
echo "" >> "$OUT_FILE"
echo "| Item | Status | Evidência |" >> "$OUT_FILE"
echo "|------|--------|-----------|" >> "$OUT_FILE"

check_http "Home Assistant UI" "http://localhost:8123" "200"
check_http "Dashboard UI" "http://localhost:3000" "200"
check_http "Dashboard Kiosk" "http://localhost:3000/simplified" "200"
check_http "Dashboard API Health" "http://localhost:8000/health" "200"
check_http "Frigate UI" "http://localhost:5000" "200"

if [ -n "$API_KEY" ]; then
  check_http "Dashboard API Sensors (com API key)" "http://localhost:8000/api/sensors" "200" "X-API-Key: ${API_KEY}"
else
  printf "| Dashboard API Sensors (com API key) | WARN | DASHBOARD_API_KEY não definido no ambiente |\n" >> "$OUT_FILE"
fi

cat >> "$OUT_FILE" <<'MANUAL'

## Itens obrigatoriamente manuais

- Teste real de detecção Frigate com pessoa no frame
- Teste de acionamento de alarme/sirene
- Teste de notificação push e Telegram
- Teste de VPN remoto
- Teste de restauração de backup
MANUAL

echo "Relatório gerado em: $OUT_FILE"
