# Runbook: Transição Mock -> Hardware Real (UGV/UAV)

## Objetivo
Migrar o módulo de drones de simulação para operação em hardware real com risco controlado.

## Fases
1. **Lab fechado**: validar sensores, atuadores e telemetria sem armamento real.
2. **Shadow mode**: hardware ligado, comandos reais bloqueados por política.
3. **Go-live restrito**: janela operacional limitada, geofence ativa.

## Checklist pré-transição
- [ ] HMAC habilitado para comandos (`COMMAND_HMAC_SECRET_*`).
- [ ] `ALLOW_UNSIGNED_HOMEASSISTANT_COMMANDS_*` desligado em produção.
- [ ] Geofence e limites de altitude definidos (UAV).
- [ ] Exclusão de zonas críticas configurada (UGV).
- [ ] Canal redundante de failover testado (`*/lora/command`).

## Procedimento
1. Subir serviços com profile de drones:
```bash
cd src
docker compose --profile drones up -d ugv uav
```
2. Validar telemetria:
- `ugv/status`
- `uav/status`
- `uav/location`
3. Executar comandos de teste assinados (`stop`, `return_home`).
4. Validar trilhas de auditoria de defesa (`ugv/defense/audit`).

## Critérios de go-live
- 0 comandos não assinados aceitos em produção.
- Failover Wi-Fi -> LoRa observado e funcional.
- Sem violação de geofence/altitude em 7 dias de shadow mode.

## Rollback
- Voltar para mock: desligar profile `drones`.
- Bloquear comandos em automações HA.
- Registrar incidente e lições aprendidas.
