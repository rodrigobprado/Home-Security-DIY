# Runbook: Rollout e Rollback do Catálogo de Ativos

> Versão: 1.0 | Data: 2026-02-23 | Issues: #334–#340

---

## 1. Pré-requisitos

- [x] `DASHBOARD_ADMIN_KEY` configurado em todos os ambientes de destino
- [x] Banco de dados acessível e migração prévia testada em staging
- [x] Backup do banco realizado (`scripts/backup.sh`) antes do deploy
- [x] Pipeline CI verde (todos os testes passando)
- [x] Stack do docker-compose ou K8s respondendo

---

## 2. Plano de Deploy Progressivo

### 2.1 Fase 1 — Banco de Dados (migration)

```bash
# Aplicar migração 20260223_0003 (non-destructive, sem downtime)
alembic upgrade 20260223_0003

# Verificar que as 3 tabelas foram criadas
psql -U dashboard_user -d homedb -c "\dt dashboard.*"
# Esperado: assets, asset_credentials, asset_audit (além das existentes)

# Verificar backfill de device_positions -> assets
psql -U dashboard_user -d homedb -c "SELECT count(*) FROM dashboard.assets;"
```

### 2.2 Fase 2 — Backend API

```bash
# Atualizar container/pod do backend
docker compose -f src/docker-compose.yml up -d --no-deps dashboard-api

# Smoke check dos novos endpoints
curl -s -o /dev/null -w "%{http_code}" \
  -H "X-API-Key: $DASHBOARD_API_KEY" \
  http://localhost:8000/api/assets
# Esperado: 200

# Verificar que /api/map/devices ainda responde
curl -s -H "X-API-Key: $DASHBOARD_API_KEY" \
  http://localhost:8000/api/map/devices | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'{len(d)} devices')"
```

### 2.3 Fase 3 — Frontend

```bash
# Atualizar container do frontend
docker compose -f src/docker-compose.yml up -d --no-deps dashboard-frontend

# Verificar que a rota admin está acessível
curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/admin/assets
# Esperado: 200 (SPA fallback para index.html)
```

### 2.4 Fase 4 — Smoke Test de Fluxo Completo

```bash
# 1. Cadastrar sensor
ASSET_ID=$(curl -s -X POST http://localhost:8000/api/assets \
  -H "X-API-Key: $DASHBOARD_API_KEY" \
  -H "X-Admin-Key: $DASHBOARD_ADMIN_KEY" \
  -H "Content-Type: application/json" \
  -d '{"asset_type":"sensor","name":"Smoke Test Sensor","entity_id":"test.smoke_sensor"}' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['id'])")

echo "Asset criado: $ASSET_ID"

# 2. Verificar no catálogo
curl -s -H "X-API-Key: $DASHBOARD_API_KEY" \
  "http://localhost:8000/api/assets/$ASSET_ID" | python3 -m json.tool

# 3. Verificar no mapa
curl -s -H "X-API-Key: $DASHBOARD_API_KEY" \
  http://localhost:8000/api/map/devices | python3 -c \
  "import sys,json; d=json.load(sys.stdin); print('OK' if any(x.get('entity_id')=='test.smoke_sensor' for x in d) else 'MISSING')"

# 4. Verificar trilha de auditoria
curl -s -H "X-API-Key: $DASHBOARD_API_KEY" \
  "http://localhost:8000/api/audit?asset_id=$ASSET_ID" | python3 -m json.tool

# 5. Limpar ativo de smoke test
curl -s -X DELETE \
  -H "X-API-Key: $DASHBOARD_API_KEY" \
  -H "X-Admin-Key: $DASHBOARD_ADMIN_KEY" \
  "http://localhost:8000/api/assets/$ASSET_ID"
```

---

## 3. Checklist de Observabilidade Pós-deploy

| Verificação | Comando | Esperado |
|-------------|---------|----------|
| Backend health | `GET /health` | `{"status":"ok"}` |
| Assets API | `GET /api/assets` | 200, JSON com `items` |
| Audit API | `GET /api/audit` | 200, JSON com `items` |
| Map devices | `GET /api/map/devices` | 200, lista de devices |
| Admin RBAC | `POST /api/assets` sem X-Admin-Key | 403 ou 503 |
| Logs backend | `docker logs dashboard-api` | Sem traceback |
| Logs frontend | `docker logs dashboard-frontend` | Sem erro nginx |

---

## 4. Rollback

### 4.1 Rollback rápido — reverter container

```bash
# Reverter imagens para versão anterior (tag anterior no registry)
docker compose -f src/docker-compose.yml up -d --no-deps \
  --pull never dashboard-api dashboard-frontend
```

### 4.2 Rollback completo — incluindo migração de banco

> **Atenção**: o rollback de migração remove as tabelas `assets`, `asset_credentials`
> e `asset_audit`. Dados cadastrados serão perdidos. Execute apenas se necessário.

```bash
# Reverter apenas a migration 0003
alembic downgrade 20260219_0002

# Verificar que tabelas assets foram removidas
psql -U dashboard_user -d homedb -c "\dt dashboard.*"
# Não deve aparecer: assets, asset_credentials, asset_audit

# Reverter containers backend e frontend
docker compose -f src/docker-compose.yml up -d --no-deps \
  --pull never dashboard-api dashboard-frontend
```

### 4.3 Validar rollback

```bash
# /api/assets deve retornar 404 após rollback completo do backend
curl -s -o /dev/null -w "%{http_code}" \
  -H "X-API-Key: $DASHBOARD_API_KEY" http://localhost:8000/api/assets
# Esperado: 404

# /api/map/devices deve continuar funcionando (usa device_positions legadas)
curl -s -o /dev/null -w "%{http_code}" \
  -H "X-API-Key: $DASHBOARD_API_KEY" http://localhost:8000/api/map/devices
# Esperado: 200
```

---

## 5. Estratégia de Feature Flag (opcional)

Para deploy gradual sem rollback de banco, pode-se usar a variável de ambiente:

```bash
# Desativar DASHBOARD_ADMIN_KEY = desabilita operações admin sem reverter código
DASHBOARD_ADMIN_KEY=""  # admin key vazia → endpoints admin retornam 503

# Isso mantém a API de leitura (/api/assets GET) funcional enquanto bloqueia escrita
```

---

## 6. Contato em caso de incidente

1. Verificar logs: `docker logs dashboard-api --tail 100`
2. Verificar alertas no dashboard de observabilidade
3. Se banco inacessível: consultar `docs/POSTGRES_BACKUP_RESTORE_RUNBOOK.md`
4. Se problema crítico de segurança: seguir `docs/INCIDENT_RESPONSE.md`
