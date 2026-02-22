# Estrutura de Documentação

> Comentário: Visão geral de como a documentação está organizada.

## Pastas principais

- `/docs/` – Documentos de arquitetura, APIs e guias gerais.
- `/rules/` – Regras e normas.
- `/prd/` – PRDs por funcionalidade.
- `/tasks/` – Tarefas e status.

## Documentos-chave

- `ARCHITECTURE.md` – Visão técnica do sistema.
- `API_DOCS.md` – Detalhes de APIs, se aplicável.

## Estrutura atual (2026-02)

### Diretórios

| Diretório | Conteúdo |
|---|---|
| `/docs/` | Arquitetura, hardware, segurança, drones, compliance (25+ documentos) |
| `/rules/` | Regras gerais, técnicas e de compliance |
| `/prd/` | Product Requirements Documents por subsistema |
| `/tasks/` | Backlog, em andamento, concluídas e visão geral de status |
| `/agents/` | Configuração e memória local dos 6 agentes de IA |
| `/skills/` | Definição de skills dos agentes |
| `/standards/` | Normas e padrões para pesquisa |
| `/src/` | Código-fonte (Docker Compose, backend FastAPI, frontend React, drones) |
| `/k8s/` | Manifests Kubernetes — `base/` + overlays `staging/` e `production/` |
| `/wiki/` | Documentação wiki do GitHub (cenários, operação, segurança) |
| `/scripts/` | Scripts de setup, geração de secrets e certificados MQTT |

### Documentos-chave

- `PROJECT_OVERVIEW.md` — Visão geral do projeto (raiz)
- `docs/ARQUITETURA_TECNICA.md` — Stack tecnológico e decisões de arquitetura
- `docs/ARQUITETURA_SEGURANCA_FISICA.md` — Camadas de segurança passiva/ativa/reativa
- `docs/ARQUITETURA_DRONES_AUTONOMOS.md` — Arquitetura UGV/UAV
- `docs/THREAT_MODEL.md` — Modelo de ameaças do sistema
- `docs/HARDENING_ANTI_TAMPER.md` — Guia de hardening e anti-tampering físico
- `docs/TESTING_STRATEGY.md` — Estratégia de testes (unitários, integração, E2E)
- `src/docs/QUICK_START.md` — Guia de início rápido para instalação

