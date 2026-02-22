# 8. Adoção de PostgreSQL com Isolamento por Schema

Data: 2026-02-22

## Status

Aceito

## Contexto

Múltiplos componentes compartilham persistência e precisam de separação de privilégios.

## Decisão

Usar PostgreSQL 16 com schemas isolados (`homeassistant`, `dashboard`, `metrics`) e usuários dedicados.

## Consequências

### Positivas
- Menor impacto de comprometimento de credencial.
- Governança de acesso por domínio de serviço.
- Melhor suporte a backup/restore granular.

### Negativas
- Gestão de permissões mais complexa.
- Necessidade de disciplina em migrações.

## Mitigação
- Scripts de init versionados.
- Runbook de backup/restore validado periodicamente.
