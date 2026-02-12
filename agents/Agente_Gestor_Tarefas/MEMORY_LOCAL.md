# Memória Local – Agente_Gestor_Tarefas

## Contexto de trabalho atual

> Registre aqui o contexto da tarefa atual em andamento.

Backlog inicial criado com 27 tarefas. Aguardando priorização humana para iniciar movimentação de tarefas.

## Anotações e rascunhos

> Use esta seção para rascunhos, cálculos e anotações temporárias.

### Resumo do backlog (2026-02-12)

| Categoria | Quantidade | Prioridade dominante |
|-----------|------------|---------------------|
| Levantamento de requisitos | 7 | Alta |
| Arquitetura e design | 5 | Alta/Média |
| Seleção de tecnologias | 5 | Alta/Média |
| Normas e compliance | 4 | Média |
| Documentação e PRDs | 4 | Alta |
| Privacidade e segurança | 2 | Alta/Média |
| **Total** | **27** | - |

### Dependências identificadas

```
T-001, T-002, T-003 (requisitos passivos) → T-008, T-009, T-010 (arquitetura física)
T-004, T-005, T-006 (requisitos ativos) → T-011 (arquitetura lógica)
T-013, T-014, T-015, T-016, T-017 (seleção tecnologia) → T-022, T-023, T-024 (PRDs)
T-018, T-019, T-020 (normas) → PRDs que referenciam normas
```

### Sugestão de ordem de execução

**Fase 1 (paralelo)**:
- T-001, T-002, T-003 (requisitos passivos - Agente_Arquiteto_Seguranca_Fisica)
- T-013, T-014 (avaliação plataformas - Agente_Arquiteto_Tecnico)
- T-018, T-019 (pesquisa normas - Agente_Pesquisador_Normas)

**Fase 2 (após Fase 1)**:
- T-004, T-005, T-006 (requisitos ativos)
- T-008, T-009, T-010 (arquitetura física)
- T-011, T-012 (arquitetura lógica e rede)

**Fase 3 (após Fase 2)**:
- T-022, T-023, T-024, T-025 (elaboração de PRDs)

## Cache de pesquisas

> Registre resultados de pesquisas para evitar retrabalho.

(vazio)

## Pendências e dúvidas

> Liste aqui dúvidas para outros agentes ou para humanos.

- [ ] Humano deve aprovar ordem de execução sugerida
- [ ] Definir critério de "done" para cada tarefa
- [ ] Estabelecer cadência de revisão do backlog (semanal? quinzenal?)

