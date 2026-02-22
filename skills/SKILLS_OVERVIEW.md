# Visão Geral de Skills

> Comentário: “Skills” aqui são capacidades específicas que agentes ou sistemas podem executar (ex.: gerar PRD, revisar código, pesquisar normas).

## Objetivo

Listar e organizar as skills necessárias para operar este projeto de forma semi ou totalmente automatizada.

## Tipos de skills

- Skills de documentação (ex.: gerar resumos, criar PRDs).
- Skills de desenvolvimento (ex.: gerar código, criar testes).
- Skills de pesquisa (ex.: buscar normas, tendências, requisitos legais).
- Skills de gestão (ex.: organizar tarefas, atualizar status).

## Skills implementadas

### Documentação
- **SKILL_DOC_001** — Elaborar PRD de subsistema (entrada: requisitos → saída: PRD estruturado)
- **SKILL_DOC_002** — Criar guia de instalação/montagem (entrada: especificação → saída: guia passo a passo)
- **SKILL_DOC_003** — Atualizar documentação técnica (entrada: mudança de código → saída: docs atualizados)
- **SKILL_DOC_004** — Auditoria de TODOs e criação de issues GitHub

### Desenvolvimento
- **SKILL_DEV_001** — Gerar serviço FastAPI com autenticação (entrada: spec → saída: endpoint + testes)
- **SKILL_DEV_002** — Criar testes unitários e de integração (entrada: módulo → saída: test suite)
- **SKILL_DEV_003** — Gerar manifesto Kubernetes/Docker Compose (entrada: serviço → saída: YAML)

### Pesquisa e Normas
- **SKILL_NORM_001** — Pesquisar e resumir normas técnicas ABNT/LGPD/ANATEL/ANAC
- **SKILL_NORM_002** — Criar checklist de compliance por domínio

### Gestão
- **SKILL_TASK_001** — Auditar TODOs do projeto e criar issues GitHub consolidadas
- **SKILL_TASK_002** — Atualizar status do backlog de tarefas
- **SKILL_TASK_003** — Triagem e priorização de pendências por severidade

## Como usar este diretório

- Definir modelos de skill em `SKILL_TEMPLATES.md`.
- Criar listas específicas por domínio em `SKILLS_DEV.md`, `SKILLS_DOCS.md` etc.

