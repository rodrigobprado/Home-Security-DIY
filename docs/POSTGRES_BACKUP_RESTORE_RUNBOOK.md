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
