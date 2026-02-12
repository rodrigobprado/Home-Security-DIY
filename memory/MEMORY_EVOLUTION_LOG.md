# Log de Evolução do Projeto – Sistema de Home Security

> Comentário: Registro cronológico de mudanças importantes, experimentos e aprendizados.

---

## Entradas

### [2026-02-12 ~23:00] [Agente_Arquiteto_Drones] – Conclusão das tarefas T-042 e T-043

**Descrição**: Pesquisa completa de regulamentação para operação de drones no Brasil e legislação de defesa não letal.

**Tarefas concluídas**:

| Tarefa | Descrição | Principais achados |
|--------|-----------|-------------------|
| T-042 | Pesquisar normas ANAC/DECEA | RBAC-E nº 94, SISANT, classificação por peso, VLOS/BVLOS, altura máx. 120m |
| T-043 | Pesquisar legislação defesa não letal | Spray pimenta permitido em propriedade privada, verificar legislação estadual |

**Arquivos atualizados**:

| Arquivo | Descrição |
|---------|-----------|
| `standards/STANDARDS_TO_RESEARCH.md` | Seção 8 completa com ANAC, DECEA, ANATEL, defesa não letal, seguro |
| `rules/RULES_COMPLIANCE_AND_STANDARDS.md` | Seção 8 com 22 regras de drones (REGRA-DRONE-01 a 22) |
| `tasks/TASKS_DONE.md` | T-042 e T-043 registradas como concluídas |
| `tasks/TASKS_BACKLOG.md` | Atualizado com status (32/45 = 71%) |

**Principais descobertas**:

1. **Classificação ANAC**: Drones <250g dispensam registro; >250g requerem registro ANAC + SISANT
2. **Espaço aéreo**: Verificar zonas no AIS Web antes de operar; CTR requer autorização
3. **ANATEL**: Módulos ESP32 e LoRa já homologados podem ser usados sem nova homologação
4. **Spray pimenta**: Classificado como "arma menos letal", não é arma de fogo (Lei 10.826/2003 não se aplica)
5. **Seguro RETA**: Obrigatório para operações não recreativas (inclui segurança patrimonial)

**Progresso do projeto**: 71% (32/45 tarefas concluídas)

**Próximos passos recomendados**:
- T-031: Definir arquitetura de hardware UGV
- T-033: Desenvolver firmware de controle baixo nível
- T-034: Implementar stack ROS2 para navegação

---

### [2026-02-12 ~22:00] [Agente_Arquiteto_Drones] – Adição do módulo de drones autônomos

**Descrição**: Criação completa do módulo reativo avançado com frota de drones autônomos modulares (open hardware/open source).

**Arquivos criados**:

| Arquivo | Descrição |
|---------|-----------|
| `docs/ARQUITETURA_DRONES_AUTONOMOS.md` | Arquitetura completa: hardware (UGV/UAV/USV), software (ROS2), comunicação, IA, defesa não letal |
| `prd/PRD_AUTONOMOUS_DRONES.md` | PRD principal com 46 RF, 20 RNF, critérios de aceitação e métricas |

**Arquivos atualizados**:

| Arquivo | Descrição |
|---------|-----------|
| `PROJECT_OVERVIEW.md` | Seção de drones adicionada na camada reativa |
| `prd/PRD_INDEX.md` | 5 novos PRDs de drones adicionados |
| `tasks/TASKS_BACKLOG.md` | 15 novas tarefas (T-031 a T-045) |
| `memory/MEMORY_SHARED.md` | Decisões de drones registradas |

**Principais decisões técnicas**:

1. **Três categorias de drones**: UGV (terrestre), UAV (aéreo), USV (pluvial/aquático)
2. **Stack de software**: ROS2 Humble/Iron + Python/C++/Rust + TensorFlow Lite/YOLOv8
3. **Hardware de referência**: Raspberry Pi 5 / Jetson Nano (UGV), Jetson Orin Nano (UAV)
4. **Comunicação redundante**: Wi-Fi 5GHz (principal) → Wi-Fi 2.4GHz → LoRa/Meshtastic (fallback)
5. **Módulo de defesa**: CO₂ + OC (pimenta) com autenticação 2FA e auditoria completa
6. **Integração**: MQTT com Home Assistant, streaming para Frigate

**Estimativas de custo**:
- UGV básico: R$ 2.500-4.000
- UAV básico: R$ 5.000-9.000
- Frota inicial (1 UGV + 1 UAV): R$ 8.500-15.000

**Novas tarefas criadas**:

| Faixa | Categoria | Quantidade |
|-------|-----------|------------|
| T-031 a T-039 | Desenvolvimento técnico | 9 |
| T-040 a T-041 | Documentação (PRDs) | 2 |
| T-042 a T-043 | Pesquisa de normas | 2 |
| T-044 a T-045 | Guias de montagem | 2 |

**Próximos passos recomendados**:
1. Pesquisa de normas ANAC/DECEA (T-042) - requisito legal
2. Definição de arquitetura de hardware UGV (T-031)
3. Desenvolvimento de firmware de controle (T-033)
4. Implementação de stack ROS2 (T-034)

---

### [2026-02-12 ~21:00] [Agente_Pesquisador_Normas] – Conclusão das tarefas T-028 a T-030 (PROJETO 100% CONCLUÍDO)

**Descrição**: Pesquisas complementares de normas para fechaduras e iluminação de segurança.

**Tarefas concluídas**:

| Tarefa | Descrição | Principais entregas |
|--------|-----------|---------------------|
| T-028 | Classificação de fechaduras | NBR 14913 (embutir), EN 1303 (cilindros), graus de segurança |
| T-029 | Fechaduras eletrônicas | IP65, AES-128, chave backup, Zigbee/Z-Wave |
| T-030 | Níveis de iluminação | NBR 8995-1, IES; 50-100 lux entradas, 20 lux identificação |

**Arquivos atualizados**:

| Arquivo | Descrição |
|---------|-----------|
| `standards/STANDARDS_TO_RESEARCH.md` | Seções 6 e 7 adicionadas (fechaduras e iluminação) |
| `rules/RULES_COMPLIANCE_AND_STANDARDS.md` | REGRA-FECHADURA-01 a 11, REGRA-ILUM-01 a 10 |

**Progresso do projeto**: 100% (30/30 tarefas concluídas) 🎉

**Marco alcançado**: Planejamento completo do Sistema de Home Security.

**Próximos passos**:
1. Revisão humana dos PRDs e documentação
2. Aprovação para início da implementação
3. Compra de materiais conforme estimativas
4. Instalação piloto em um dos cenários

---

### [2026-02-12 ~20:00] [Agente_Documentador] – Conclusão das tarefas T-022 a T-025

**Descrição**: Elaboração dos PRDs principais de sensores, videovigilância, dashboard e cenários residenciais.

**Tarefas concluídas**:

| Tarefa | Descrição | Principais entregas |
|--------|-----------|---------------------|
| T-022 | PRD de plataforma de sensores e alarmes | 40 RF, 24 RNF, arquitetura Zigbee/Alarmo, lista de sensores |
| T-023 | PRD de videovigilância e NVR | 50 RF, 22 RNF, arquitetura Frigate/OpenVINO, lista de câmeras |
| T-024 | PRD de dashboard de monitoramento | 47 RF, 16 RNF, wireframes, cards HA recomendados |
| T-025 | PRDs dos três cenários | Rural, casa urbana e apartamento com diagramas e orçamentos |

**Arquivos criados**:

| Arquivo | Descrição |
|---------|-----------|
| `prd/PRD_SENSORS_AND_ALARMS_PLATFORM.md` | Plataforma de sensores Zigbee + Alarmo |
| `prd/PRD_VIDEO_SURVEILLANCE_AND_NVR.md` | NVR Frigate + detecção IA |
| `prd/PRD_MONITORING_DASHBOARD.md` | Dashboard Home Assistant |
| `prd/PRD_PERIMETER_RURAL.md` | Cenário propriedade rural |
| `prd/PRD_PERIMETER_URBAN_HOUSE.md` | Cenário casa urbana |
| `prd/PRD_APARTMENT_SECURITY.md` | Cenário apartamento |

**Decisões de documentação**:
1. **Estrutura padronizada**: Todos PRDs seguem template com RF, RNF, CA, métricas, riscos
2. **Estimativas de investimento**: Incluídas em todos os cenários com faixas de preço
3. **Diagramas ASCII**: Posicionamento de câmeras e sensores por cenário
4. **Referências cruzadas**: Normas (REGRA-XXX) e PRDs relacionados linkados

**Progresso do projeto**: 90% (27/30 tarefas concluídas)

**Próximos passos sugeridos**:
- Agente_Pesquisador_Normas: Concluir T-028, T-029, T-030 (baixa prioridade)
- Opcional: Criar PRDs complementares (PRD_NETWORK_SECURITY, PRD_LOCAL_PROCESSING_HUB)
- Humano: Revisar PRDs criados e aprovar para implementação

---

### [2026-02-12 ~18:30] [Agente_Arquiteto_Seguranca_Fisica] – Conclusão das tarefas T-001 a T-003, T-007 a T-010

**Descrição**: Levantamento completo de requisitos de segurança passiva para os três cenários residenciais, requisitos de segurança reativa e diagramas de posicionamento.

**Tarefas concluídas**:

| Tarefa | Descrição | Principais entregas |
|--------|-----------|---------------------|
| T-001 | Requisitos segurança passiva – rural | Cerca + cerca elétrica, iluminação solar, 4 zonas de proteção |
| T-002 | Requisitos segurança passiva – casa urbana | Muro + cerca elétrica, paisagismo defensivo, grades em janelas |
| T-003 | Requisitos segurança passiva – apartamento | Porta blindada, fechadura multiponto, foco em envelope |
| T-007 | Requisitos segurança reativa | Plano de resposta, notificações, evidências, continuidade |
| T-008 | Diagrama posicionamento – rural | Layout com 4-6 câmeras, sensores de perímetro |
| T-009 | Diagrama posicionamento – casa urbana | Layout com 3-5 câmeras, cobertura completa |
| T-010 | Diagrama posicionamento – apartamento | Foco em porta, olho mágico digital |

**Arquivos criados**:

| Arquivo | Descrição |
|---------|-----------|
| `docs/ARQUITETURA_SEGURANCA_FISICA.md` | Documento completo com fundamentos de defesa em profundidade, requisitos por cenário e zona, diagramas ASCII, plano de resposta a incidentes, checklist de implementação |

**Decisões de arquitetura**:
1. **4 zonas de proteção**: Perímetro → Área externa → Envelope → Interior
2. **Prioridade por cenário**: Rural (perímetro), Urbana (envelope), Apartamento (porta)
3. **Plano de resposta**: Detecção < 5s, notificação < 30s, múltiplos canais
4. **Nobreak obrigatório**: Mínimo 30 minutos de autonomia

**Recomendações para próximos agentes**:
- Agente_Arquiteto_Tecnico: Usar documento como base para seleção de sensores e câmeras
- Agente_Documentador: Usar documento como base para PRDs dos cenários
- Agente_Pesquisador_Normas: Pendente pesquisa de classificação de fechaduras

**Próximos passos sugeridos**:
- Agente_Arquiteto_Tecnico: Iniciar T-004, T-005, T-006 (requisitos de segurança ativa)
- Agente_Arquiteto_Tecnico: Iniciar T-013, T-014 (avaliação de plataformas)
- Agente_Documentador: Elaborar PRDs quando requisitos ativos estiverem prontos

---

### [2026-02-12 ~17:30] [Agente_Pesquisador_Normas] – Conclusão das tarefas T-018, T-019, T-020, T-021

**Descrição**: Pesquisa completa de normas de segurança física, proteção de dados (LGPD), videovigilância e instalações elétricas.

**Tarefas concluídas**:

| Tarefa | Descrição | Principais achados |
|--------|-----------|-------------------|
| T-018 | Normas de segurança física | NBR 10821 (esquadrias), NBR 7199 (vidros), NBR 15575 (desempenho), Lei 13.477/2017 (cercas elétricas) |
| T-019 | LGPD/GDPR para videovigilância | Exceção Art. 4º, I para uso pessoal; câmeras que captam via pública devem seguir LGPD |
| T-020 | Boas práticas CFTV | Retenção 30 dias; 1080p para identificação; visão noturna obrigatória em externas |
| T-021 | Instalações elétricas | NBR 5410 (DPS obrigatório), NBR 5419 (SPDA), nobreak mínimo 30min |

**Arquivos atualizados**:

| Arquivo | Descrição |
|---------|-----------|
| `standards/STANDARDS_TO_RESEARCH.md` | Documento completo com pesquisas, links e status |
| `rules/RULES_COMPLIANCE_AND_STANDARDS.md` | Regras derivadas por categoria (REGRA-XXX-NN) |
| `tasks/TASKS_DONE.md` | Tarefas movidas para concluídas |
| `tasks/TASKS_BACKLOG.md` | Atualizado com novas tarefas de pesquisa identificadas |
| `agents/Agente_Pesquisador_Normas/MEMORY_LOCAL.md` | Cache de pesquisas e anotações |
| `memory/MEMORY_SHARED.md` | Decisões importantes registradas |

**Descobertas importantes**:
1. **LGPD - Exceção pessoal**: Câmeras em residência que captam apenas área privada estão FORA do escopo da LGPD
2. **OWASP IoT**: Senhas padrão são a principal vulnerabilidade (caso Mirai 2016)
3. **Cerca elétrica**: Legislação municipal pode variar - verificar antes de especificar
4. **Retenção**: 30 dias é padrão de mercado para residências

**Novas tarefas criadas**: T-028, T-029, T-030 (pesquisas complementares de menor prioridade)

**Próximos passos sugeridos**:
- Agente_Arquiteto_Seguranca_Fisica pode iniciar levantamento de requisitos (T-001 a T-003)
- Agente_Arquiteto_Tecnico pode iniciar avaliação de plataformas (T-013, T-014)
- PRDs devem referenciar as regras derivadas (REGRA-XXX-NN)

---

### [2026-02-12 ~16:00] [Agente_Arquiteto_Projeto] – Especialização do template para Home Security

**Descrição**: Template de documentação multiagente especializado para o projeto de Sistema de Home Security Open Source e Open Hardware.

**Arquivos criados/atualizados**:

| Arquivo | Ação | Descrição |
|---------|------|-----------|
| `PROJECT_OVERVIEW.md` | Atualizado | Contexto completo do projeto: três cenários (rural, casa urbana, apartamento), três camadas de segurança (passiva, ativa, reativa), princípios técnicos (open source, open hardware, privacidade local). |
| `prd/PRD_INDEX.md` | Atualizado | Lista inicial de 15 PRDs organizados por cenário e subsistema, com descrições e status. |
| `tasks/TASKS_BACKLOG.md` | Atualizado | Backlog inicial com 27 tarefas macro cobrindo levantamento de requisitos, arquitetura, seleção de tecnologias, normas e documentação. |
| `rules/RULES_TECHNICAL.md` | Atualizado | Seção "Stack e diretrizes técnicas" adicionada: plataformas open source (Home Assistant, Frigate), protocolos (Zigbee, Z-Wave, Wi-Fi), hardware acessível, boas práticas de segurança de rede. |
| `rules/RULES_COMPLIANCE_AND_STANDARDS.md` | Atualizado | Normas categorizadas: segurança física, LGPD/GDPR, segurança da informação, videovigilância, instalações elétricas. Regras derivadas documentadas. |
| `standards/STANDARDS_TO_RESEARCH.md` | Atualizado | Lista organizada de normas a pesquisar com template de documentação de pesquisa. |
| `agents/AGENTS_OVERVIEW.md` | Atualizado | Cinco agentes definidos: Arquiteto_Seguranca_Fisica, Arquiteto_Tecnico, Pesquisador_Normas, Documentador, Gestor_Tarefas. Fluxo de colaboração documentado. |
| `agents/AGENTS_CONFIG.md` | Atualizado | Configuração detalhada de cada agente: responsabilidades, arquivos de entrada/saída, memória, regras específicas. |
| `memory/MEMORY_SHARED.md` | Atualizado | Resumo do projeto e decisões iniciais registradas. |
| `memory/MEMORY_EVOLUTION_LOG.md` | Atualizado | Esta entrada. |

**Decisões tomadas**:
1. Projeto organizado em três cenários residenciais distintos com requisitos específicos.
2. Abordagem de defesa em profundidade com camadas passiva/ativa/reativa.
3. Privacidade por design: processamento e armazenamento 100% local.
4. Foco em plataformas open source maduras: Home Assistant, Frigate, ZoneMinder.
5. Hardware acessível como alvo: Raspberry Pi, mini PC.

**TODOs gerados**:
- Humano deve validar cenários e priorizar tarefas do backlog.
- Humano deve definir plataforma de automação primária.
- Agentes devem iniciar execução das tarefas priorizadas.

**Próximos passos sugeridos**:
1. Priorização humana das tarefas em `TASKS_BACKLOG.md`.
2. Início da pesquisa de normas (Agente_Pesquisador_Normas).
3. Levantamento de requisitos por cenário (Agente_Arquiteto_Seguranca_Fisica + Agente_Arquiteto_Tecnico).

---

> Nota: Adicionar novas entradas acima desta linha, mantendo ordem cronológica reversa (mais recente primeiro).

