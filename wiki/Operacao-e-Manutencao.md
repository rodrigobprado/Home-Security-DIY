# Operação e Manutenção

## Monitoramento diário

### Dashboard operacional

Acesse `http://localhost:3000` (ou `dashboard.home.local` em produção):

- **Modo completo (`/`)**: visão completa com alarme, sensores, mapa, câmeras, drones e status dos serviços
- **Modo kiosk (`/simplified`)**: tela de TV/monitor dedicado — barra de alarme, mapa e grid de câmeras

O dashboard atualiza em tempo real via WebSocket (fan-out do Home Assistant).

### Checklist operacional

- [ ] Verificar status dos serviços em `http://localhost:3000` → widget **ServiceStatus**
- [ ] Revisar alertas recentes no widget **AlertFeed**
- [ ] Confirmar câmeras com snapshot atualizado no widget **CameraGrid**
- [ ] Checar estado do alarme (Alarmo) no widget **AlarmStatus**

## Backup e recuperação

O script `scripts/backup.sh` realiza backup automático com retenção em múltiplos níveis:

```bash
# Executar backup manualmente
./scripts/backup.sh

# Configurar via cron (diário às 3h)
0 3 * * * /path/to/Home-Security-DIY/scripts/backup.sh
```

### O que é salvo

| Item | Retenção |
|---|---|
| Dump PostgreSQL completo (diário) | 7 dias |
| Dump PostgreSQL por schema (diário) | 7 dias |
| Cópia semanal (domingo) | 28 dias |
| Cópia mensal (dia 1) | 365 dias |
| Config Home Assistant | Incluída no backup |
| Gravações Frigate | Gerenciado pelo próprio Frigate |

### Restauração do banco

```bash
# Docker
docker exec -i home-security-postgres psql -U postgres homedb < backup.sql

# K3s
kubectl exec -n home-security postgres-0 -- psql -U postgres homedb < backup.sql
```

Runbook detalhado: `docs/POSTGRES_BACKUP_RESTORE_RUNBOOK.md`

## Atualização de serviços

```bash
# Docker Compose
docker compose pull
docker compose up -d

# K3s
kubectl rollout restart deployment/dashboard-api -n home-security
kubectl rollout restart deployment/dashboard-frontend -n home-security
```

Atualização controlada do Home Assistant: `docs/HOME_ASSISTANT_ZERO_DOWNTIME_UPDATE_RUNBOOK.md`

Transição de drones mock -> hardware: `docs/DRONES_MOCK_TO_HARDWARE_RUNBOOK.md`

Metas operacionais (SLO/SLA): `docs/SLOS_SLAS_CRITICAL_SERVICES.md`

## Hardening e resiliência

- Consulte `docs/HARDENING_ANTI_TAMPER.md` para configurações de segurança
- Consulte `docs/RESILIENCIA_E_MODOS_DEGRADADOS.md` para comportamento em falhas
- Mantenha imagens Docker atualizadas com Dependabot (já configurado no repositório)
- Rotacione credenciais periodicamente (HA_TOKEN, senhas PostgreSQL, MQTT)

## Logs e diagnóstico

```bash
# Ver logs da API do dashboard
docker compose logs -f dashboard-api

# Ver logs do Home Assistant
docker compose logs -f homeassistant

# Ver conexão WebSocket ativa
curl http://localhost:8000/api/services/status
```
