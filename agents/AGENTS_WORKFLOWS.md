
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

> TODO: Adaptar e expandir workflows de acordo com o processo real da equipe.

