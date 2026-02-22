#!/usr/bin/env bash
set -euo pipefail

OUT="${1:-tasks/COMPLIANCE_CHECKLIST_AUDIT_$(date +%F).md}"

pass=0
fail=0

check() {
  local description="$1"
  local cmd="$2"
  if eval "$cmd" >/dev/null 2>&1; then
    printf -- "- [x] %s\n" "$description" >>"$OUT"
    pass=$((pass + 1))
  else
    printf -- "- [ ] %s\n" "$description" >>"$OUT"
    fail=$((fail + 1))
  fi
}

manual() {
  local description="$1"
  printf -- "- [ ] %s *(validação manual necessária)*\n" "$description" >>"$OUT"
}

mkdir -p "$(dirname "$OUT")"

cat >"$OUT" <<'HEADER'
# Compliance & Checklists Audit

Relatório de auditoria semiautomática para as issues:
- #102 LGPD
- #103 ANAC/SISANT/DECEA/ANATEL
- #104 Legalidade do módulo de defesa
- #105 Segurança física e hardening
- #106 Segurança de rede e credenciais
- #107 Testes de integração
- #108 Avaliação Matter/Thread

HEADER

echo "## #102 LGPD (câmeras, dados e retenção)" >>"$OUT"
check "Frigate com retenção contínua de 30 dias" "grep -Eq '^\s*days:\s*30\b' src/frigate/config.yml"
check "Retenção padrão de alertas no backend em 30 dias" "grep -Eq '^\s*alert_retention_days:\s*int\s*=\s*30\b' src/dashboard/backend/app/config.py"
check "Regras LGPD documentadas (REGRA-LGPD-01..05)" "grep -q 'REGRA-LGPD-05' rules/RULES_COMPLIANCE_AND_STANDARDS.md"
manual "Validar se ângulos das câmeras captam somente área privada"
manual "Instalar placas físicas de aviso nas áreas monitoradas (quando aplicável)"
manual "Validar log de acesso às gravações em ambiente operacional"

echo >>"$OUT"
echo "## #103 Regulamentação de drones (ANAC/SISANT/DECEA/ANATEL)" >>"$OUT"
check "Documentação regulatória ANAC/DECEA presente" "grep -q 'RBAC-E nº 94' standards/STANDARDS_TO_RESEARCH.md"
check "Regras operacionais de drones publicadas" "grep -q 'REGRA-DRONE-20' rules/RULES_COMPLIANCE_AND_STANDARDS.md"
manual "Confirmar peso real do UAV e exigência de registro (>250g)"
manual "Realizar cadastro do operador e da aeronave no SISANT/DECEA"
manual "Verificar zona aérea local (CTR/NOTAM) antes de operação"
manual "Configurar geofence e limite de altitude no firmware/software de voo"

echo >>"$OUT"
echo "## #104 Legalidade do módulo de defesa não letal" >>"$OUT"
check "Restrições legais e éticas do módulo documentadas" "grep -q 'Human-in-the-Loop' docs/LEGAL_AND_ETHICS.md"
check "Regra de bloqueio de disparo automático documentada" "grep -q 'REGRA-DRONE-23' rules/RULES_COMPLIANCE_AND_STANDARDS.md"
manual "Consulta jurídica formal sobre uso de OC em SP/RJ/MG"
manual "Implementar e validar 2FA para armamento (PIN + TOTP)"
manual "Validar bloqueio por detecção de crianças/animais em ambiente real"
manual "Configurar e testar zonas de exclusão de disparo"

echo >>"$OUT"
echo "## #105 Segurança física e hardening" >>"$OUT"
check "Guia de hardening anti-tamper disponível" "test -f docs/HARDENING_ANTI_TAMPER.md"
check "Checklist de segurança física documentado" "grep -q 'Perímetro fechado e em bom estado' docs/ARQUITETURA_SEGURANCA_FISICA.md"
manual "Validar perímetro físico, portas, janelas, iluminação e paisagismo em campo"
manual "Aplicar LUKS + Dropbear no servidor instalado"
manual "Validar nobreak real e backup off-site funcional"
manual "Inspecionar DPS e aterramento da instalação elétrica"

echo >>"$OUT"
echo "## #106 Segurança de rede, VLANs e credenciais" >>"$OUT"
check "Mosquitto com autenticação obrigatória (allow_anonymous false)" "grep -q '^allow_anonymous false' src/mosquitto/config/mosquitto.conf"
check "ACL do Mosquitto configurada" "test -s src/mosquitto/config/acl_file"
check "Script de geração de certificados MQTT disponível" "test -x scripts/generate-mqtt-certs.sh"
check "Zigbee2MQTT com permit_join false por padrão" "grep -q '^permit_join:\s*false' src/zigbee2mqtt/configuration.yaml"
manual "Confirmar VLAN 20/30 isoladas no roteador/switch"
manual "Habilitar TLS MQTT em produção e bloquear 1883 externo"
manual "Validar TOTP em Home Assistant para todos os usuários"
manual "Validar hardening SSH (PasswordAuthentication no / PermitRootLogin no / fail2ban)"

echo >>"$OUT"
echo "## #107 Testes de integração" >>"$OUT"
check "Estratégia de testes documentada" "test -f docs/TESTING_STRATEGY.md"
check "Checklist de validação documentado na wiki" "test -f wiki/Testes-e-Validacao.md"
manual "Executar smoke tests dos serviços em ambiente ativo (HA, Dashboard, Frigate, API)"
manual "Executar testes de sensores, sirene, notificações e VPN"
manual "Executar teste de restauração de backup"

echo >>"$OUT"
echo "## #108 Avaliação Matter/Thread" >>"$OUT"
check "Documento de avaliação Matter/Thread presente" "test -f docs/MATTER_THREAD_EVALUATION.md"
manual "Validar disponibilidade real de sirenes/sensores Matter no mercado BR"
manual "Comparar preços Matter vs Zigbee com fornecedores atuais"
manual "Verificar suporte estável Matter no Home Assistant/Alarmo na versão em uso"
manual "Registrar decisão de adoção/rejeição com data"

echo >>"$OUT"
echo "## Resumo" >>"$OUT"
echo "- Itens verificados automaticamente (PASS): $pass" >>"$OUT"
echo "- Itens verificados automaticamente (FAIL): $fail" >>"$OUT"
echo "- Itens dependentes de validação manual: 25" >>"$OUT"

echo "Audit report generated: $OUT"
