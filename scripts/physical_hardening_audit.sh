#!/usr/bin/env bash
set -euo pipefail

OUT_FILE="tasks/PHYSICAL_HARDENING_AUDIT_$(date +%F).md"

status() {
  local code="$1"
  case "$code" in
    PASS) echo "PASS" ;;
    FAIL) echo "FAIL" ;;
    WARN) echo "WARN" ;;
    *) echo "INFO" ;;
  esac
}

emit() {
  local item="$1"
  local code="$2"
  local detail="$3"
  printf "| %s | %s | %s |\n" "$item" "$(status "$code")" "$detail" >> "$OUT_FILE"
}

echo "# Auditoria Técnica de Hardening Físico" > "$OUT_FILE"
echo "" >> "$OUT_FILE"
echo "Data: $(date -Iseconds)" >> "$OUT_FILE"
echo "" >> "$OUT_FILE"
echo "| Item | Status | Evidência |" >> "$OUT_FILE"
echo "|------|--------|-----------|" >> "$OUT_FILE"

# LUKS (best-effort)
if lsblk -o TYPE 2>/dev/null | grep -q "crypt"; then
  emit "Criptografia de disco (LUKS)" "PASS" "Dispositivo TYPE=crypt detectado em lsblk."
else
  emit "Criptografia de disco (LUKS)" "WARN" "Nenhum TYPE=crypt detectado (validar manualmente no host alvo)."
fi

# Dropbear (best-effort)
if [ -f /etc/dropbear/initramfs/dropbear.conf ] || [ -f /etc/initramfs-tools/conf.d/dropbear ]; then
  emit "Dropbear para unlock remoto" "PASS" "Arquivo de configuração detectado."
else
  emit "Dropbear para unlock remoto" "WARN" "Configuração não detectada neste ambiente."
fi

# Backup script availability
if [ -x scripts/backup.sh ]; then
  emit "Backup automático off-site (script)" "PASS" "scripts/backup.sh presente e executável."
else
  emit "Backup automático off-site (script)" "FAIL" "scripts/backup.sh ausente ou sem permissão de execução."
fi

# Documentation links
for f in docs/HARDENING_ANTI_TAMPER.md docs/ARQUITETURA_SEGURANCA_FISICA.md docs/SEGURANCA_FISICA_HARDENING_CHECKLIST.md; do
  if [ -f "$f" ]; then
    emit "Documento ${f}" "PASS" "Presente no repositório."
  else
    emit "Documento ${f}" "FAIL" "Arquivo ausente."
  fi
done

echo "" >> "$OUT_FILE"
echo "## Itens obrigatoriamente manuais" >> "$OUT_FILE"
echo "" >> "$OUT_FILE"
cat >> "$OUT_FILE" <<'EOF'
- Verificação física do perímetro e fechamentos
- Medição de iluminação (lux) em entradas/perímetro
- Verificação de DPS e aterramento por profissional habilitado
- Teste de autonomia real do nobreak em carga
- Validação de proteção física do servidor (acesso restrito)
EOF

echo "Relatório gerado em: $OUT_FILE"
