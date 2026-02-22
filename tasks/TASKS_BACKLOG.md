# Backlog de Tarefas – Sistema de Home Security

> Comentário: Tarefas ainda não iniciadas vão aqui. Organizadas por categoria para facilitar priorização.

## Legenda de prioridade
- **Crítica**: Bloqueia outras tarefas ou é pré-requisito fundamental.
- **Alta**: Importante para o progresso do projeto.
- **Média**: Necessária, mas pode aguardar tarefas de maior prioridade.
- **Baixa**: Desejável, mas não urgente.

---

## Categoria: Levantamento de requisitos

> ✅ Todas as 7 tarefas concluídas em 2026-02-12 – Detalhes em `TASKS_DONE.md`

---

## Categoria: Arquitetura e design

> ✅ Todas as 5 tarefas concluídas em 2026-02-12 – Detalhes em `TASKS_DONE.md`

---

## Categoria: Seleção de tecnologias

> ✅ Todas as 5 tarefas concluídas em 2026-02-12 – Detalhes em `TASKS_DONE.md`

---

## Categoria: Normas e compliance

> ✅ Todas as 7 tarefas concluídas em 2026-02-12 – Detalhes em `TASKS_DONE.md`

---

## Categoria: Documentação e PRDs

> ✅ Todas as 4 tarefas prioritárias concluídas em 2026-02-12 – Detalhes em `TASKS_DONE.md`
>
> PRDs restantes podem ser criados conforme demanda.

---

## Categoria: Privacidade e segurança da informação

> ✅ Tarefas T-026, T-027 concluídas em 2026-02-12 – Detalhes em `TASKS_DONE.md`

---

## Categoria: Drones autônomos (módulo reativo avançado)

> Tarefas para desenvolvimento do sistema de drones autônomos modulares.

| ID | Título | Descrição | Responsável | Prioridade | PRD relacionado |
|----|--------|-----------|-------------|------------|-----------------|
| T-037 | Desenvolver módulo de defesa não letal | Especificar e implementar sistema CO₂ + OC com autenticação, auditoria e protocolos de segurança. | Agente_Arquiteto_Drones | Média | PRD_DRONE_DEFENSE_MODULE |
| T-040 | Elaborar PRD do módulo de defesa | Detalhar requisitos funcionais e não funcionais do sistema de defesa não letal. | Agente_Documentador | Média | PRD_DRONE_DEFENSE_MODULE |
| T-044 | Criar guia de montagem UGV | Documentar passo a passo de montagem do drone terrestre com BOM e instruções. | Agente_Documentador | Baixa | PRD_AUTONOMOUS_DRONES |
| T-045 | Criar guia de montagem UAV | Documentar passo a passo de montagem do drone aéreo com BOM e instruções. | Agente_Documentador | Baixa | PRD_AUTONOMOUS_DRONES |

> ✅ T-038 (Integração MQTT drones + Home Assistant) concluída em 2026-02-22
>
> ✅ T-039 (Dashboard de frota com mapa operacional e comandos) concluída em 2026-02-22
>
> ✅ T-041 (PRD de comunicação de drones, revisão v1.1 com rastreabilidade) concluída em 2026-02-22
>
> ✅ T-042 (Pesquisar normas ANAC/DECEA) e T-043 (Pesquisar legislação defesa não letal) concluídas em 2026-02-12

---

## Categoria: Revisão e melhorias (nova – identificadas na revisão de 2026-02-12)

> Tarefas originadas da revisão completa do projeto, cobrindo falhas, pontos cegos e melhorias.

### Correções

| ID | Título | Descrição | Prioridade | Status |
|----|--------|-----------|------------|--------|
| ~~T-046~~ | ~~Corrigir/remover dependabot.yml~~ | ~~Arquivo com package-ecosystem vazio~~ | ~~Média~~ | ✅ CONCLUÍDO |
| T-047 | Criar SECURITY.md funcional | Política de divulgação de vulnerabilidades para projeto open source | Média | ✅ CONCLUÍDO |
| T-048 | Reescrever README.md | README atual descreve template genérico, não o projeto real | Alta | ✅ CONCLUÍDO |
| ~~T-049~~ | ~~Corrigir "pluvial" → "aquático"~~ | ~~Termo semanticamente incorreto em múltiplos arquivos~~ | ~~Média~~ | ✅ CONCLUÍDO |
| T-050 | Resolver conflito legal VLOS vs. operação autônoma | REGRA-DRONE-02 exige VLOS mas arquitetura é BVLOS | Alta | ✅ CONCLUÍDO |

### Lacunas de segurança

| ID | Título | Descrição | Prioridade | Status |
|----|--------|-----------|------------|--------|
| T-051 | Criar threat model formal (STRIDE) | Enumerar adversários, vetores e cenários de ataque | Alta | ✅ CONCLUÍDO |
| T-052 | Detecção/proteção contra jamming de RF | Jammer de Zigbee/Wi-Fi derruba todos os sensores wireless | Alta | ✅ CONCLUÍDO |
| T-053 | Proteção contra tamper/destruição do servidor | Mini PC é ponto único de falha; 4G como requisito | Alta | ✅ CONCLUÍDO |
| T-054 | Engenharia social e ameaças internas | Pretextos, insiders, duress code | Média | ✅ CONCLUÍDO |
| T-055 | Gestão de falsos positivos e fadiga de alerta | Confirmação multi-sensor, auto-tuning | Média | ✅ CONCLUÍDO |
| T-056 | Modos de operação degradada | Comportamento quando componentes falham | Alta | ✅ CONCLUÍDO |
| T-057 | Plano de resposta a incidentes cibernéticos | IR plan para hack do sistema, camera comprometida | Alta | ✅ CONCLUÍDO |

### Ética e legal

| ID | Título | Descrição | Prioridade | Status |
|----|--------|-----------|------------|--------|
| T-058 | Reavaliar módulo de defesa autônoma | Remover/restringir modo automático; risco legal grave | Alta | ✅ CONCLUÍDO |

### Operação e usabilidade

| ID | Título | Descrição | Prioridade | Status |
|----|--------|-----------|------------|--------|
| T-059 | Plano de manutenção e ciclo de vida | Calendário de manutenção, EOL de hardware, troca de baterias | Média | ✅ CONCLUÍDO |
| T-060 | Requisitos de acessibilidade e usabilidade (via Security Center) | Dashboard unificado e simplificado | Média | ✅ CONCLUÍDO |
| T-061 | Análise de custos operacionais | Custos mensais/anuais por cenário (energia, internet, baterias) | Média | ✅ CONCLUÍDO |

### Documentação e processo

| ID | Título | Descrição | Prioridade | Status |
|----|--------|-----------|------------|--------|
| T-062 | Criar ADRs (Architecture Decision Records) | Formalizar decisões já tomadas (HA, Frigate, Zigbee, etc.) | Média | ✅ CONCLUÍDO |
| T-063 | Estratégia de backup do NVR | RAID, edge recording, backup offsite (Script Implementado) | Média | ✅ CONCLUÍDO |
| T-064 | Criar CONTRIBUTING.md | Guia de contribuição para projeto open source | Baixa | ✅ CONCLUÍDO |
| T-065 | Avaliar adoção Matter/Thread | Plano de migração futuro Zigbee → Matter | Baixa | ✅ CONCLUÍDO (2026-02-18) |
| T-066 | Converter diagramas ASCII → Mermaid | GitHub renderiza Mermaid nativamente | Baixa | ✅ CONCLUÍDO |
| T-067 | Criar risk matrix (prob. × impacto) | Complemento ao threat model | Baixa | ✅ CONCLUÍDO |
| T-068 | Documentar alternativas comerciais compatíveis | Fallback quando DIY não funciona | Baixa | ✅ CONCLUÍDO (2026-02-18) |

---

## Resumo do backlog

| Categoria | Total de tarefas | Concluídas | Pendentes |
|-----------|-----------------|------------|-----------|
| Levantamento de requisitos | 7 | 7 | 0 |
| Arquitetura e design | 5 | 5 | 0 |
| Seleção de tecnologias | 5 | 5 | 0 |
| Normas e compliance | 7 | 7 | 0 |
| Documentação e PRDs | 4 | 4 | 0 |
| Privacidade e segurança | 2 | 2 | 0 |
| Drones autônomos | 15 | 11 | 4 |
| **Revisão e melhorias** | **23** | **23** | **0** |
| **Total** | **68** | **64** | **4** |

---

## Próximas tarefas prioritárias

### 1. Revisão e melhorias (alta prioridade)

| Ordem | ID | Título | Justificativa |
|-------|----|--------|---------------|
| 1 | T-051 | Threat model formal | Desbloqueia T-052, T-054, T-067 |
| 2 | T-048 | Reescrever README.md | Primeira impressão do repositório |
| 3 | T-050 | Resolver conflito VLOS/BVLOS | Viabilidade legal de drones aéreos |
| 4 | T-058 | Reavaliar defesa autônoma | Risco legal e ético grave |
| 5 | T-053 | Proteção contra tamper | Ponto único de falha |
| 6 | T-056 | Modos degradados | Resiliência do sistema |
| 7 | T-057 | Resposta a incidentes ciber | Complemento ao IR físico |

### 2. Módulo de drones autônomos

| Ordem | ID | Título | Justificativa |
|-------|----|--------|---------------|
| 1 | T-037 | Módulo de defesa não letal | Depende de base de comunicação e segurança operacional |
| 2 | T-040 | PRD do módulo de defesa | Formalização de requisitos e riscos legais |
| 3 | T-044 | Guia de montagem UGV | Habilita replicabilidade do hardware terrestre |
| 4 | T-045 | Guia de montagem UAV | Replicabilidade da plataforma aérea |

---

> Última atualização: 2026-02-22
