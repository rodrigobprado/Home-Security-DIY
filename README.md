# Sistema de Gestão de Tarefas com IA Multiagente – Template em Markdown

Este repositório é um **template de projeto em Markdown** pensado para ser usado por humanos e múltiplos agentes de IA, com foco em gestão de tarefas, documentação estruturada e execução incremental até a finalização do projeto.

> Use este template como base para **qualquer projeto**, não apenas sistemas de tarefas: basta adaptar os arquivos `.md` ao seu domínio.

---

## Objetivos do template

- Fornecer uma **estrutura padrão e flexível** de pastas e arquivos em Markdown.
- Permitir que **humanos preencham lacunas críticas** antes da execução automática por agentes.
- Facilitar o trabalho de **múltiplos agentes de IA** com memória compartilhada e memória local por agente.
- Servir de base para orquestradores (n8n, LangGraph, scripts próprios, etc.) que operem sobre arquivos `.md`.

---

## Estrutura de diretórios

```bash
project-root/
  PROJECT_OVERVIEW.md

  rules/
    RULES_GENERAL.md
    RULES_TECHNICAL.md
    RULES_COMPLIANCE_AND_STANDARDS.md

  skills/
    SKILLS_OVERVIEW.md
    SKILL_TEMPLATES.md
    SKILLS_DEV.md
    SKILLS_DOCS.md

  prd/
    PRD_TEMPLATE.md
    PRD_INDEX.md

  tasks/
    TASKS_STATUS_OVERVIEW.md
    TASKS_BACKLOG.md
    TASKS_IN_PROGRESS.md
    TASKS_DONE.md

  memory/
    MEMORY_SHARED.md
    MEMORY_EVOLUTION_LOG.md

  quality/
    IMPROVEMENTS.md
    PENDING_ITEMS.md
    TECH_DEBT.md

  standards/
    STANDARDS_TO_RESEARCH.md
    STANDARDS_APPLIED.md

  docs/
    DOCS_STRUCTURE.md
    DOCS_TODO.md
    ARCHITECTURE.md
    API_DOCS.md

  agents/
    AGENTS_OVERVIEW.md
    AGENTS_CONFIG.md
    AGENTS_WORKFLOWS.md
    AGENTS_LOCAL_MEMORY_TEMPLATE.md

  repositories/
    REPOSITORIES_STRUCTURE.md
