#!/usr/bin/env bash
set -euo pipefail

OUT_FILE="tasks/NETWORK_SECURITY_AUDIT_$(date +%F).md"

emit() {
  local item="$1"
  local status="$2"
  local detail="$3"
  printf "| %s | %s | %s |\n" "$item" "$status" "$detail" >> "$OUT_FILE"
}

mkdir -p "$(dirname "$OUT_FILE")"
cat > "$OUT_FILE" <<'HEADER'
# Auditoria Técnica de Segurança de Rede

HEADER

echo "Data: $(date -Iseconds)" >> "$OUT_FILE"
echo "" >> "$OUT_FILE"
echo "| Item | Status | Evidência |" >> "$OUT_FILE"
echo "|------|--------|-----------|" >> "$OUT_FILE"

if grep -q '^allow_anonymous false' src/mosquitto/config/mosquitto.conf; then
  emit "Mosquitto sem acesso anônimo" "PASS" "allow_anonymous false"
else
  emit "Mosquitto sem acesso anônimo" "FAIL" "Diretiva não encontrada"
fi

if [ -s src/mosquitto/config/acl_file ]; then
  emit "ACL do Mosquitto" "PASS" "Arquivo ACL presente e não vazio"
else
  emit "ACL do Mosquitto" "FAIL" "Arquivo ACL ausente/vazio"
fi

if [ -x scripts/generate-mqtt-certs.sh ]; then
  emit "Script de certificados MQTT" "PASS" "scripts/generate-mqtt-certs.sh executável"
else
  emit "Script de certificados MQTT" "FAIL" "Script ausente ou não executável"
fi

if [ -f src/mosquitto/config/mosquitto.prod.conf ]; then
  emit "Perfil TLS-only de produção do Mosquitto" "PASS" "src/mosquitto/config/mosquitto.prod.conf presente"
else
  emit "Perfil TLS-only de produção do Mosquitto" "FAIL" "mosquitto.prod.conf ausente"
fi

if [ "${APP_ENV:-}" = "production" ]; then
  if grep -q '^listener 8883' src/mosquitto/config/mosquitto.prod.conf; then
    emit "MQTT TLS em produção (listener 8883)" "PASS" "listener 8883 encontrado"
  else
    emit "MQTT TLS em produção (listener 8883)" "FAIL" "listener 8883 não encontrado"
  fi

  if grep -q '^listener 1883' src/mosquitto/config/mosquitto.prod.conf; then
    emit "MQTT sem listener plaintext em produção" "FAIL" "listener 1883 presente em mosquitto.prod.conf"
  else
    emit "MQTT sem listener plaintext em produção" "PASS" "listener 1883 ausente em mosquitto.prod.conf"
  fi
fi

if grep -q '^permit_join:\s*false' src/zigbee2mqtt/configuration.yaml; then
  emit "Zigbee2MQTT com pareamento fechado por padrão" "PASS" "permit_join: false"
else
  emit "Zigbee2MQTT com pareamento fechado por padrão" "FAIL" "permit_join: false não encontrado"
fi

if grep -q 'VLAN30 → Internet: DENY ALL' docs/ARQUITETURA_TECNICA.md; then
  emit "Regra documental de isolamento VLAN 30" "PASS" "VLAN30 sem internet documentada"
else
  emit "Regra documental de isolamento VLAN 30" "WARN" "Regra não localizada na documentação"
fi

if grep -q 'VLAN20 → Internet: DENY ALL' docs/ARQUITETURA_TECNICA.md; then
  emit "Regra documental de isolamento VLAN 20" "PASS" "VLAN20 sem internet documentada"
else
  emit "Regra documental de isolamento VLAN 20" "WARN" "Regra não localizada na documentação"
fi

cat >> "$OUT_FILE" <<'MANUAL'

## Itens de validação manual obrigatória

- Confirmar regras ativas no roteador/switch (não apenas documentação)
- Confirmar UPnP desabilitado
- Confirmar ausência de port forwarding
- Confirmar MFA/TOTP para usuários administrativos do HA
- Confirmar hardening SSH/fail2ban no host de produção
- Confirmar porta 1883 não exposta externamente
MANUAL

echo "Relatório gerado em: $OUT_FILE"
