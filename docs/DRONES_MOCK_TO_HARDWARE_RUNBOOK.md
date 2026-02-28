# Runbook: Transição Mock -> Hardware Real (UGV/UAV)

## Objetivo
Migrar o módulo de drones de simulação para operação em hardware real com risco controlado.

## Fases
1. **Lab fechado**: validar sensores, atuadores e telemetria sem armamento real.
2. **Shadow mode**: hardware ligado, comandos reais bloqueados por política.
3. **Go-live restrito**: janela operacional limitada, geofence ativa.
4. **Operação assistida**: liberar comandos críticos apenas com observador humano.

## Checklist pré-transição
- [x] HMAC habilitado para comandos (`COMMAND_HMAC_SECRET_*`).
- [x] `ALLOW_UNSIGNED_HOMEASSISTANT_COMMANDS_*` desligado em produção.
- [x] Geofence e limites de altitude definidos (UAV).
- [x] Exclusão de zonas críticas configurada (UGV).
- [x] Canal redundante de failover testado (`*/lora/command`).
- [x] Runtime sem fallback mock silencioso em produção (`DRONES_ALLOW_MOCK_IMPORTS=false`).
- [x] Logging estruturado ativo (UGV/UAV) para comandos, failover e falhas de integração.

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

## Procedimento (K3s / Produção)
1. Confirmar deployment de UGV/UAV no namespace `home-security`.
2. Aplicar configuração de hardware real (sem mocks) com rollout controlado.
3. Executar smoke test operacional:
   - publicação de `status` periódica em `ugv/status` e `uav/status`
   - comando assinado `return_home` com confirmação de execução
   - telemetria mínima: bateria, posição e modo de operação
4. Monitorar 30 minutos sem perda de heartbeat antes de liberar operação assistida.

## Critérios de go-live
- 0 comandos não assinados aceitos em produção.
- Failover Wi-Fi -> LoRa observado e funcional.
- Sem violação de geofence/altitude em 7 dias de shadow mode.
- Observabilidade ativa (logs + eventos MQTT + dashboard).
- Sem `print` operacional em runtime crítico; logs devem conter evento + contexto.

## Variáveis de runtime (hardening)

Obrigatórias para segurança:
- `APP_ENV=production`
- `COMMAND_HMAC_SECRET_UGV`, `COMMAND_HMAC_SECRET_UAV`
- `DEFENSE_PIN_UGV`, `DEFENSE_PIN_UAV`
- `ALLOW_UNSIGNED_HOMEASSISTANT_COMMANDS_UGV=false`
- `ALLOW_UNSIGNED_HOMEASSISTANT_COMMANDS_UAV=false`

Somente diagnóstico em dev/test:
- `DRONES_ALLOW_MOCK_IMPORTS=true` (proibido em produção)

Níveis de log:
- `UGV_LOG_LEVEL` (default `INFO`)
- `UAV_LOG_LEVEL` (default `INFO`)
- `UAV_VISION_LOG_LEVEL` (default `INFO`)

## Rollback
- Voltar para mock: desligar profile `drones`.
- Bloquear comandos em automações HA.
- Registrar incidente e lições aprendidas.

## Evidência obrigatória
- Data/hora da mudança e responsáveis.
- Resultado de smoke tests (comandos assinados e failover).
- Registro de geofence/altitude sem violação durante shadow mode.
- Plano executado de rollback (quando aplicável).
