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
| *(sem pendências na categoria)* | — | — | — | — | — |

> ✅ T-038 (Integração MQTT drones + Home Assistant) concluída em 2026-02-22
>
> ✅ T-039 (Dashboard de frota com mapa operacional e comandos) concluída em 2026-02-22
>
> ✅ T-040 (PRD do módulo de defesa, revisão v1.1 com rastreabilidade e lacunas) concluída em 2026-02-22
>
> ✅ T-041 (PRD de comunicação de drones, revisão v1.1 com rastreabilidade) concluída em 2026-02-22
>
> ✅ T-037 (Módulo de defesa não letal com 2FA/TOTP, bloqueios de segurança e auditoria imutável) concluída em 2026-02-22
>
> ✅ T-044 (Guia de montagem UGV alinhado ao firmware atual e checklists de validação) concluída em 2026-02-22
>
> ✅ T-045 (Guia de montagem UAV consolidado com integração MAVLink/MQTT e restrições VLOS) concluída em 2026-02-22
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

## Categoria: Auditoria de qualidade (2026-02-22 — identificadas pela auditoria PM)

> Tarefas originadas da auditoria técnica completa do projeto como gerente de projeto de elite.
> Todas possuem issue correspondente no GitHub.

### P0 — Crítico (segurança e infraestrutura)

| ID | Título | Issue GitHub | Prioridade | Status |
|----|--------|-------------|------------|--------|
| T-069 | Adicionar healthchecks nos serviços Docker sem verificação | [#173](https://github.com/rodrigobprado/Home-Security-DIY/issues/173) | Alta | ⏳ Pendente |
| T-070 | Dashboard API exposta em 0.0.0.0 — restringir a 127.0.0.1 | [#174](https://github.com/rodrigobprado/Home-Security-DIY/issues/174) | Alta | ⏳ Pendente |
| T-071 | Portas Frigate (5000, 8554, 8555) expostas em todas as interfaces | [#175](https://github.com/rodrigobprado/Home-Security-DIY/issues/175) | Alta | ⏳ Pendente |
| T-072 | Ativar MQTT TLS (porta 8883) no docker-compose | [#176](https://github.com/rodrigobprado/Home-Security-DIY/issues/176) | Alta | ⏳ Pendente |

### P1 — Alto (documentação e infraestrutura críticas)

| ID | Título | Issue GitHub | Prioridade | Status |
|----|--------|-------------|------------|--------|
| T-073 | Criar README.md na raiz do repositório | [#177](https://github.com/rodrigobprado/Home-Security-DIY/issues/177) | Alta | ⏳ Pendente |
| T-074 | Adicionar UGV e UAV ao docker-compose (profile drone) | [#178](https://github.com/rodrigobprado/Home-Security-DIY/issues/178) | Alta | ⏳ Pendente |
| T-075 | Criar runbook de transição mock→hardware real para drones | [#179](https://github.com/rodrigobprado/Home-Security-DIY/issues/179) | Alta | ⏳ Pendente |
| T-076 | Revisar/completar SECURITY.md com responsible disclosure | [#190](https://github.com/rodrigobprado/Home-Security-DIY/issues/190) | Alta | ⏳ Pendente |

### P2 — Médio (qualidade e operações)

| ID | Título | Issue GitHub | Prioridade | Status |
|----|--------|-------------|------------|--------|
| T-077 | Aumentar cobertura de testes do frontend (≥60%) | [#180](https://github.com/rodrigobprado/Home-Security-DIY/issues/180) | Média | ⏳ Pendente |
| T-078 | Configurar Dependabot para atualizações automáticas de deps | [#181](https://github.com/rodrigobprado/Home-Security-DIY/issues/181) | Média | ⏳ Pendente |
| T-079 | Adotar SealedSecrets ou External Secrets para K8s | [#182](https://github.com/rodrigobprado/Home-Security-DIY/issues/182) | Média | ⏳ Pendente |
| T-080 | Mover ADRs 005-010 da wiki para docs/adr/ | [#183](https://github.com/rodrigobprado/Home-Security-DIY/issues/183) | Média | ⏳ Pendente |
| T-081 | Criar runbook de backup e restore do PostgreSQL | [#184](https://github.com/rodrigobprado/Home-Security-DIY/issues/184) | Média | ⏳ Pendente |
| T-082 | Documentar processo de atualização do Home Assistant sem downtime | [#185](https://github.com/rodrigobprado/Home-Security-DIY/issues/185) | Média | ⏳ Pendente |

### P3 — Baixo (melhorias de processo)

| ID | Título | Issue GitHub | Prioridade | Status |
|----|--------|-------------|------------|--------|
| T-083 | Fixar versões de dependências dos drones (>= → ==) | [#186](https://github.com/rodrigobprado/Home-Security-DIY/issues/186) | Baixa | ⏳ Pendente |
| T-084 | Criar CONTRIBUTING.md | [#187](https://github.com/rodrigobprado/Home-Security-DIY/issues/187) | Baixa | ⏳ Pendente |
| T-085 | Criar CHANGELOG.md | [#188](https://github.com/rodrigobprado/Home-Security-DIY/issues/188) | Baixa | ⏳ Pendente |
| T-086 | Definir SLOs e SLAs para os serviços críticos | [#189](https://github.com/rodrigobprado/Home-Security-DIY/issues/189) | Baixa | ⏳ Pendente |

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
| Drones autônomos | 15 | 15 | 0 |
| Revisão e melhorias | 23 | 23 | 0 |
| **Auditoria de qualidade** | **18** | **0** | **18** |
| **Total** | **86** | **68** | **18** |

---

## Próximas tarefas prioritárias

### P0 — Segurança e infraestrutura (executar primeiro)

| Ordem | ID | Título | Issue | Justificativa |
|-------|----|--------|-------|---------------|
| 1 | T-070 | Dashboard API em 127.0.0.1 | #174 | API acessível na LAN sem auth adicional |
| 2 | T-071 | Restringir portas Frigate | #175 | Streams de vídeo expostos sem autenticação |
| 3 | T-072 | Ativar MQTT TLS | #176 | Comandos de drones em plaintext na rede |
| 4 | T-069 | Healthchecks Docker | #173 | Falhas silenciosas nos serviços críticos |

### P1 — Alta prioridade (próximos passos)

| Ordem | ID | Título | Issue | Justificativa |
|-------|----|--------|-------|---------------|
| 5 | T-073 | README.md | #177 | Primeira impressão do repositório em branco |
| 6 | T-074 | UGV/UAV no docker-compose | #178 | Desenvolvimento local impossível sem K8s |
| 7 | T-075 | Runbook mock→hardware | #179 | Sem guia para ativar hardware real |
| 8 | T-076 | SECURITY.md | #190 | Responsible disclosure ausente |

---

> Última atualização: 2026-02-22
