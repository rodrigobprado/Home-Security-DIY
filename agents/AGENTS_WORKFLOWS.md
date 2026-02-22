
***

### `agents/AGENTS_WORKFLOWS.md`

```markdown
# Workflows de Agentes

> Comentário: Descreve fluxos de trabalho típicos para orquestração multiagente.

## Workflow 1 – Inicialização do Projeto

1. Agente Arquiteto:
   - Lê: `PROJECT_OVERVIEW.md`, `/rules/`, `/agents/`.
   - Gera/ajusta: árvore de pastas, templates adicionais se necessário.
2. Agente Documentador:
   - Lê: `PROJECT_OVERVIEW.md`, `/prd/PRD_TEMPLATE.md`.
   - Cria: PRDs iniciais.
3. Agente Gestor de Tarefas:
   - Lê: PRDs.
   - Gera: tarefas em `TASKS_BACKLOG.md`.

## Workflow 2 – Iteração de Desenvolvimento

1. Agente Desenvolvedor pega tarefas em `TASKS_IN_PROGRESS.md`.
2. Ao concluir, atualiza `TASKS_DONE.md` e registra decisões em `MEMORY_EVOLUTION_LOG.md`.
3. Agente Documentador atualiza documentação conforme necessário.

## Workflow 3 — Processo atual (2026-02)

### Planejamento
1. Identificar pendências via auditoria de TODOs/FIXMEs no repositório (SKILL_TASK_001).
2. Criar issues GitHub consolidadas por tema; adicionar ao `TASKS_BACKLOG.md`.
3. Priorizar por impacto (crítico/alto/médio/baixo) usando labels do GitHub.

### Desenvolvimento
1. Ao iniciar uma tarefa: mover para "In Progress" no GitHub, atualizar `TASKS_IN_PROGRESS.md`.
2. Implementar com commits convencionais (`feat:`, `fix:`, `docs:`, `test:`, `chore:`).
3. Abrir Pull Request com descrição do que foi feito e referência à issue.
4. CI/CD executa: testes unitários, cobertura (≥70% backend / ≥60% frontend), typecheck, linting.

### Qualidade e Merge
1. Revisão obrigatória via Pull Request antes de merge.
2. Cobertura mínima de testes deve passar no CI (gates definidos em `.github/workflows/`).
3. Squash merge para `main` — mensagem de commit deve referenciar a issue (`closes #NNN`).

### Documentação
1. Atualizar `docs/` a cada PR que altere arquitetura, APIs ou segurança.
2. Registrar decisões arquiteturais relevantes em `memory/MEMORY_SHARED.md`.
3. Fechar issue no GitHub com referência ao commit/PR.

