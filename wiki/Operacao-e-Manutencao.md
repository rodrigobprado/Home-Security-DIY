# Operação e Manutenção

## Rotina operacional

- Verificar saúde dos serviços (Home Assistant, Frigate, MQTT, Zigbee2MQTT).
- Revisar eventos críticos e falsos positivos.
- Validar gravação/retenção de vídeo.

## Backup e recuperação

- Script disponível: `scripts/backup.sh`.
- Armazenar backup fora do host principal.
- Testar restauração periodicamente.

## Hardening e resiliência

- Aplicar recomendações de `docs/HARDENING_ANTI_TAMPER.md`.
- Revisar `docs/RESILIENCIA_E_MODOS_DEGRADADOS.md`.
- Manter atualização controlada de imagens e dependências.
