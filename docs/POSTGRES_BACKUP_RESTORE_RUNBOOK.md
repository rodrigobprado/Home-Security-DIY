# Runbook: Backup e Restore do PostgreSQL

## Objetivo
Garantir backup consistente e restauração validada do banco PostgreSQL do projeto.

## Escopo
- Banco: `${POSTGRES_DB}`
- Schemas críticos: `homeassistant`, `dashboard`, `metrics`

## Pré-requisitos
- Stack em execução (`docker compose` ou K8s)
- Acesso ao usuário administrador do PostgreSQL
- Chave de criptografia configurada (`BACKUP_ENCRYPTION_PASSPHRASE`)
- Espaço em disco local >= 2x tamanho estimado do dump

## Backup (Docker Compose)
1. Executar dump completo:
```bash
cd src
docker compose exec -T postgres pg_dump -U "${POSTGRES_USER:-postgres}" -d "${POSTGRES_DB:-homedb}" -Fc > /tmp/homedb_$(date +%F_%H%M).dump
```
2. Gerar checksum:
```bash
sha256sum /tmp/homedb_*.dump > /tmp/homedb_*.dump.sha256
```
3. Criptografar artefato:
```bash
openssl enc -aes-256-cbc -salt -pbkdf2 -in /tmp/homedb_*.dump -out /tmp/homedb_*.dump.enc -pass env:BACKUP_ENCRYPTION_PASSPHRASE
```
4. Copiar para armazenamento externo/offsite.

## Backup (K3s)
1. Executar dump no pod PostgreSQL:
```bash
kubectl -n home-security exec -i statefulset/postgres -- \
  pg_dump -U "${POSTGRES_USER:-postgres}" -d "${POSTGRES_DB:-homedb}" -Fc > /tmp/homedb_$(date +%F_%H%M).dump
```
2. Gerar checksum e criptografar (mesmos comandos da seção Docker).
3. Publicar artefato em armazenamento externo versionado.

## Restore (ambiente de teste)
1. Subir banco limpo.
2. Restaurar dump:
```bash
cd src
docker compose exec -T postgres createdb -U "${POSTGRES_USER:-postgres}" restore_validation || true
docker compose exec -T postgres pg_restore -U "${POSTGRES_USER:-postgres}" -d restore_validation < /tmp/homedb_YYYY-MM-DD_HHMM.dump
```
3. Validar tabelas esperadas:
```bash
docker compose exec -T postgres psql -U "${POSTGRES_USER:-postgres}" -d restore_validation -c "\dn"
```

## Restore (K3s em homologação)
1. Criar banco de validação:
```bash
kubectl -n home-security exec -i statefulset/postgres -- \
  createdb -U "${POSTGRES_USER:-postgres}" restore_validation || true
```
2. Restaurar dump:
```bash
kubectl -n home-security exec -i statefulset/postgres -- \
  pg_restore -U "${POSTGRES_USER:-postgres}" -d restore_validation < /tmp/homedb_YYYY-MM-DD_HHMM.dump
```
3. Validar schemas:
```bash
kubectl -n home-security exec -i statefulset/postgres -- \
  psql -U "${POSTGRES_USER:-postgres}" -d restore_validation -c "\dn"
```

## Guardrails de restauração em produção
- Restore direto em produção exige aprovação explícita e janela de manutenção.
- Antes do restore, capturar snapshot atual para rollback.
- Após restore, executar smoke test da Dashboard API e integrações MQTT.

## RPO/RTO alvo
- RPO: até 24h
- RTO: até 60 minutos

## Frequência recomendada
- Backup diário incremental + semanal completo.
- Teste de restore trimestral obrigatório.

## Critérios de sucesso
- Dump criado sem erro.
- Checksum válido.
- Restore executado e schemas visíveis.
- Evidência registrada em `tasks/` com data/hora.

## Evidência mínima a registrar
- Data/hora de início e término.
- Nome do artefato de backup e hash SHA-256.
- Ambiente validado (Compose/K3s) e resultado de restore.
- Desvio de RPO/RTO (se houver) e ação corretiva.
