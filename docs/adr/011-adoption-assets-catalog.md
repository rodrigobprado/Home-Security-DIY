# ADR 011 — Catálogo Dinâmico de Ativos no Dashboard

**Data**: 2026-02-23
**Status**: Aceito
**Issues**: #334, #335, #336, #337, #338, #339, #340

---

## Contexto

O dashboard original usava listas hardcoded em `SensorGrid.jsx`, `CameraGrid.jsx` e `config.py` para determinar quais dispositivos exibir. Isso criava fricção operacional ao adicionar novos sensores ou câmeras (requeria deploy de código), além de impossibilitar rastreabilidade de mudanças.

## Decisão

Implementar um catálogo dinâmico de ativos com:
1. **Modelo de dados normalizado** (`dashboard.assets` + `asset_credentials` + `asset_audit`) com UUID pk, constraint de tipo e status
2. **API CRUD REST** (`/api/assets`) com paginação, busca e soft delete
3. **RBAC por nível de operação**: leitura via `X-API-Key`, escrita via `X-Admin-Key` separado
4. **Trilha de auditoria transacional** em toda operação de escrita (before/after JSON + actor + IP)
5. **Frontend com fallback**: SensorGrid/CameraGrid usam catálogo dinâmico, com fallback para listas estáticas se vazio
6. **Migração não-destrutiva**: backfill de `device_positions` → `assets` no upgrade, rollback seguro no downgrade

## Alternativas consideradas

- **Configuração via arquivo YAML**: rejeitado — sem trilha de auditoria, requer deploy para mudanças
- **Integração direta com Home Assistant entity registry**: rejeitado — acoplamento forte com HA, não suporta ativos não-HA (câmeras offline, sensores de terceiros)
- **CRUD no frontend sem backend**: rejeitado — sem persistência, sem auditoria, sem RBAC

## Consequências

**Positivas**:
- Cadastro de ativos sem deploy de código
- Auditoria completa de quem/quando/o-que mudou
- RBAC separado: operadores podem monitorar, só admins cadastram
- SensorGrid/CameraGrid passam a ser data-driven (não hardcoded)

**Negativas**:
- Dependência de `DASHBOARD_ADMIN_KEY` configurado para operações de escrita
- Curva de aprendizado para operadores (nova UI em `/admin/assets`)
- Backfill inicial pode criar ativos duplicados se `device_positions` já contiver dados

## Referências

- [SECURITY.md](../../SECURITY.md) — hardening e RBAC
- [ASSETS_CATALOG_ROLLOUT_RUNBOOK.md](../ASSETS_CATALOG_ROLLOUT_RUNBOOK.md) — deploy e rollback
- [API_DOCS.md](../API_DOCS.md) — documentação de endpoints
