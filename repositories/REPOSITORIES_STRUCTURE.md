# Estrutura de Repositórios

> Comentário: Descreve como o projeto pode ser dividido em repositórios ou módulos.

## Repositório principal

- Contém:
  - Estrutura de documentação em `.md`
  - Configuração de agentes
  - Templates de PRD e tarefas

## Possíveis repositórios adicionais

- `backend/` – Código do backend do sistema de gestão de tarefas.
- `frontend/` – Interface do usuário.
- `automation/` – Scripts de orquestração e execução de agentes.

## Relações e dependências

- O repositório principal é a fonte de verdade para regras, normas e documentação.
- Repositórios de código devem referenciar este repositório para alinhamento de padrões.

> **Arquitetura de repositório atual (2026-02)**: Monorepo único `Home-Security-DIY`.
>
> ```
> Home-Security-DIY/
> ├── src/              # Código-fonte: Docker Compose, backend FastAPI, frontend React, drones
> ├── k8s/              # Manifests Kubernetes (base/ + overlays staging/ e production/)
> ├── docs/             # Documentação técnica (arquitetura, hardware, compliance)
> ├── rules/            # Regras gerais, técnicas e de compliance
> ├── prd/              # Product Requirements Documents por subsistema
> ├── agents/           # Configuração e memória local dos 6 agentes de IA
> ├── skills/           # Definição de skills dos agentes
> ├── tasks/            # Backlog e status das tarefas
> ├── standards/        # Normas e padrões para pesquisa
> ├── scripts/          # Scripts de setup e geração de secrets
> ├── wiki/             # Documentação wiki do GitHub
> └── PROJECT_OVERVIEW.md  # Visão geral do projeto
> ```
>
> **Não há repositórios separados** — todo o código e documentação vivem neste monorepo.

