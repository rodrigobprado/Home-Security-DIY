# Changelog

Todas as mudanças relevantes deste projeto serão registradas neste arquivo.

O formato segue Keep a Changelog e versionamento semântico.

## [Unreleased]

### Added
- Runbook de backup e restore do PostgreSQL em `docs/POSTGRES_BACKUP_RESTORE_RUNBOOK.md`.
- Runbook de atualização do Home Assistant sem downtime em `docs/HOME_ASSISTANT_ZERO_DOWNTIME_UPDATE_RUNBOOK.md`.
- Runbook de transição mock -> hardware real para drones em `docs/DRONES_MOCK_TO_HARDWARE_RUNBOOK.md`.
- Política de SLO/SLA para serviços críticos em `docs/SLOS_SLAS_CRITICAL_SERVICES.md`.
- ADRs 005-010 em `docs/adr/`.
- Serviços opcionais `ugv`/`uav` no `docker-compose` com profile `drones`.
- Healthchecks adicionais no `docker-compose`.

### Changed
- `dashboard-api` agora faz bind em `127.0.0.1:8000` no `docker-compose`.
- `mosquitto` adiciona listener loopback para TLS em `127.0.0.1:8883` e seleção de configuração por `APP_ENV`.
- Dependências dos drones fixadas com versões exatas (`==`).
- Configuração do Dependabot atualizada para ecossistemas reais do repositório.
