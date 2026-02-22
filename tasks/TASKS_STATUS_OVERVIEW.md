# Visão Geral de Tarefas e Status

> Comentário: Este arquivo explica como usar os arquivos de tarefas como um “Kanban em Markdown”.

## Arquivos de tarefas

- `TASKS_BACKLOG.md` – Ideias e tarefas ainda não iniciadas.
- `TASKS_IN_PROGRESS.md` – Tarefas em andamento.
- `TASKS_DONE.md` – Tarefas concluídas.

## Convenções

- Cada tarefa deve ter um ID único.
- Atualizar status movendo a linha da tarefa para o arquivo correspondente.
- Registrar decisões relevantes em `MEMORY_SHARED.md` ou `MEMORY_EVOLUTION_LOG.md`.

## Fluxo de trabalho sugerido

1. Criar tarefas em `TASKS_BACKLOG.md`.
2. Ao iniciar o trabalho, mover a tarefa para `TASKS_IN_PROGRESS.md`.
3. Ao finalizar, mover para `TASKS_DONE.md`.

> **Fluxo atual (2026-02)**:
> - Tarefas criadas como issues GitHub + entradas em `TASKS_BACKLOG.md`
> - Ao iniciar: issue movida para "In Progress" no GitHub; `TASKS_IN_PROGRESS.md` atualizado
> - Revisão obrigatória via Pull Request antes de merge para `main`
> - CI/CD verifica cobertura de testes, typecheck e linting
> - Ao concluir: issue fechada com `closes #NNN` no commit; entrada movida para `TASKS_DONE.md`

