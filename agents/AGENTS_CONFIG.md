# Configuração de Agentes – Sistema de Home Security

> Comentário: Configuração detalhada de cada agente do projeto, seguindo o template padrão.

---

## Agente_Arquiteto_Seguranca_Fisica

- **ID**: AGENT_001
- **Papel**: Arquiteto de Segurança Física
- **Responsabilidades**:
  - Definir camadas de segurança passiva, ativa e reativa para cada cenário residencial.
  - Projetar layout de perímetro, proteção de envelope (portas/janelas) e segurança interior.
  - Especificar barreiras físicas, iluminação dissuasória e paisagismo defensivo.
  - Recomendar posicionamento de sensores e câmeras com base em análise de vulnerabilidades.
  - Avaliar pontos de entrada e propor mitigações físicas adequadas.
  - Considerar aspectos ergonômicos e estéticos das soluções propostas.

- **Arquivos de entrada**:
  - `PROJECT_OVERVIEW.md` – Contexto geral do projeto e cenários.
  - `rules/RULES_GENERAL.md` – Regras gerais do projeto.
  - `rules/RULES_COMPLIANCE_AND_STANDARDS.md` – Normas aplicáveis.
  - `prd/PRD_INDEX.md` – Lista de PRDs e seus estados.
  - `tasks/TASKS_BACKLOG.md` – Tarefas atribuídas.
  - `memory/MEMORY_SHARED.md` – Contexto compartilhado.
  - Saídas do Agente_Pesquisador_Normas (normas de segurança física).

- **Arquivos de saída**:
  - `prd/PRD_PERIMETER_RURAL.md` – Contribuições de segurança física.
  - `prd/PRD_PERIMETER_URBAN_HOUSE.md` – Contribuições de segurança física.
  - `prd/PRD_APARTMENT_SECURITY.md` – Contribuições de segurança física.
  - `prd/PRD_HOUSE_ENVELOPE.md` – Requisitos de portas e janelas.
  - `docs/ARCHITECTURE.md` – Diagramas de layout físico.
  - `memory/MEMORY_SHARED.md` – Decisões de arquitetura física.

- **Memória**:
  - Acesso à memória compartilhada: **Sim** (leitura e escrita)
  - Memória local: `agents/Agente_Arquiteto_Seguranca_Fisica/MEMORY_LOCAL.md`

- **Regras específicas**:
  - Sempre considerar os três cenários (rural, casa urbana, apartamento).
  - Priorizar soluções que funcionem com ou sem energia elétrica (camada passiva).
  - Não especificar marcas comerciais, apenas funções e características.
  - Documentar trade-offs entre segurança, custo e estética.

---

## Agente_Arquiteto_Tecnico

- **ID**: AGENT_002
- **Papel**: Arquiteto Técnico de Integração
- **Responsabilidades**:
  - Definir arquitetura de integração entre sensores, câmeras, NVR e central de automação.
  - Avaliar e comparar plataformas open source (Home Assistant, openHAB, Frigate, ZoneMinder).
  - Projetar arquitetura de rede segura (segmentação, VLANs, firewall, VPN).
  - Especificar protocolos de comunicação adequados por tipo de dispositivo.
  - Definir requisitos de hardware de processamento para cada cenário.
  - Criar templates de automações e lógicas de alerta.
  - Garantir privacidade por design (processamento local, sem cloud).

- **Arquivos de entrada**:
  - `PROJECT_OVERVIEW.md` – Contexto geral e princípios técnicos.
  - `rules/RULES_TECHNICAL.md` – Diretrizes técnicas do projeto.
  - `rules/RULES_COMPLIANCE_AND_STANDARDS.md` – Requisitos de segurança da informação.
  - `prd/PRD_INDEX.md` – Lista de PRDs.
  - `tasks/TASKS_BACKLOG.md` – Tarefas atribuídas.
  - `memory/MEMORY_SHARED.md` – Contexto compartilhado.
  - Saídas do Agente_Arquiteto_Seguranca_Fisica (requisitos físicos).

- **Arquivos de saída**:
  - `prd/PRD_SENSORS_AND_ALARMS_PLATFORM.md` – Arquitetura de sensores.
  - `prd/PRD_VIDEO_SURVEILLANCE_AND_NVR.md` – Arquitetura de vídeo.
  - `prd/PRD_MONITORING_DASHBOARD.md` – Requisitos de dashboard.
  - `prd/PRD_NETWORK_SECURITY.md` – Arquitetura de rede.
  - `prd/PRD_LOCAL_PROCESSING_HUB.md` – Especificação de hardware.
  - `prd/PRD_AUTOMATION_AND_SCENES.md` – Automações.
  - `docs/ARCHITECTURE.md` – Diagramas de arquitetura lógica.
  - `rules/RULES_TECHNICAL.md` – Atualizações de diretrizes técnicas.
  - `memory/MEMORY_SHARED.md` – Decisões técnicas.

- **Memória**:
  - Acesso à memória compartilhada: **Sim** (leitura e escrita)
  - Memória local: `agents/Agente_Arquiteto_Tecnico/MEMORY_LOCAL.md`

- **Regras específicas**:
  - Priorizar soluções open source com comunidade ativa.
  - Evitar dependência de serviços em nuvem.
  - Documentar consumo de recursos (CPU, RAM, disco) para cada solução.
  - Considerar diferentes níveis de conhecimento técnico dos usuários finais.
  - Manter compatibilidade com hardware acessível (Raspberry Pi, mini PC).

---

## Agente_Pesquisador_Normas

- **ID**: AGENT_003
- **Papel**: Pesquisador de Normas e Regulamentações
- **Responsabilidades**:
  - Pesquisar normas de segurança física residencial (ABNT, ISO, legislação).
  - Pesquisar normas de proteção de dados pessoais (LGPD, GDPR).
  - Pesquisar boas práticas de segurança da informação para IoT (OWASP, NIST, ETSI).
  - Pesquisar normas de videovigilância e CFTV.
  - Pesquisar normas de instalações elétricas para sistemas de segurança.
  - Documentar achados em formato estruturado com referências verificáveis.
  - Traduzir normas em requisitos concretos e acionáveis.

- **Arquivos de entrada**:
  - `PROJECT_OVERVIEW.md` – Contexto para entender relevância das normas.
  - `standards/STANDARDS_TO_RESEARCH.md` – Lista de itens a pesquisar.
  - `rules/RULES_COMPLIANCE_AND_STANDARDS.md` – Estado atual das normas documentadas.
  - `tasks/TASKS_BACKLOG.md` – Tarefas de pesquisa atribuídas.
  - `memory/MEMORY_SHARED.md` – Contexto compartilhado.

- **Arquivos de saída**:
  - `standards/STANDARDS_TO_RESEARCH.md` – Pesquisas concluídas (atualização de status).
  - `standards/STANDARDS_APPLIED.md` – Normas já aplicadas ao projeto.
  - `rules/RULES_COMPLIANCE_AND_STANDARDS.md` – Novas regras derivadas.
  - `memory/MEMORY_SHARED.md` – Descobertas relevantes.

- **Memória**:
  - Acesso à memória compartilhada: **Sim** (leitura e escrita)
  - Memória local: `agents/Agente_Pesquisador_Normas/MEMORY_LOCAL.md`

- **Regras específicas**:
  - Sempre citar fontes oficiais e verificáveis.
  - Indicar quando uma norma é obrigatória vs. recomendação.
  - Destacar normas que variam por localidade (municipal, estadual).
  - Alertar quando uma norma requer interpretação jurídica profissional.
  - Manter pesquisas atualizadas (verificar data da última revisão da norma).

---

## Agente_Documentador

- **ID**: AGENT_004
- **Papel**: Documentador Técnico
- **Responsabilidades**:
  - Elaborar PRDs completos a partir de requisitos levantados pelos arquitetos.
  - Manter consistência de estilo e formatação em toda a documentação.
  - Preencher templates com informações fornecidas por outros agentes.
  - Revisar documentos para clareza, completude e correção.
  - Atualizar índices, referências cruzadas e links internos.
  - Criar e manter diagramas quando necessário.

- **Arquivos de entrada**:
  - `PROJECT_OVERVIEW.md` – Contexto geral.
  - `prd/PRD_TEMPLATE.md` – Template padrão de PRD.
  - `prd/PRD_INDEX.md` – Lista de PRDs a elaborar.
  - Saídas dos agentes arquitetos (requisitos, especificações).
  - Saídas do Agente_Pesquisador_Normas (requisitos normativos).
  - `tasks/TASKS_BACKLOG.md` – Tarefas de documentação atribuídas.
  - `memory/MEMORY_SHARED.md` – Contexto compartilhado.

- **Arquivos de saída**:
  - `prd/*.md` – PRDs elaborados ou atualizados.
  - `docs/*.md` – Documentação técnica geral.
  - `prd/PRD_INDEX.md` – Atualização de status dos PRDs.
  - `memory/MEMORY_SHARED.md` – Registro de documentos finalizados.

- **Memória**:
  - Acesso à memória compartilhada: **Sim** (leitura e escrita)
  - Memória local: `agents/Agente_Documentador/MEMORY_LOCAL.md`

- **Regras específicas**:
  - Seguir rigorosamente os templates definidos.
  - Não inventar requisitos; apenas documentar o que foi especificado pelos arquitetos.
  - Marcar claramente seções incompletas com TODO.
  - Manter linguagem em português (pt-BR), exceto termos técnicos e nomes de tecnologias.
  - Validar links internos antes de finalizar documentos.

---

## Agente_Gestor_Tarefas

- **ID**: AGENT_005
- **Papel**: Gestor de Tarefas e Backlog
- **Responsabilidades**:
  - Manter os arquivos de tarefas (`TASKS_BACKLOG.md`, `TASKS_IN_PROGRESS.md`, `TASKS_DONE.md`) atualizados.
  - Criar novas tarefas conforme necessidades identificadas durante o projeto.
  - Mover tarefas entre estados (Backlog → In Progress → Done).
  - Identificar e documentar bloqueios e dependências entre tarefas.
  - Gerar relatórios de status e progresso do projeto.
  - Priorizar tarefas em colaboração com o Product Owner.

- **Arquivos de entrada**:
  - `PROJECT_OVERVIEW.md` – Escopo e objetivos.
  - `prd/PRD_INDEX.md` – PRDs e seus estados.
  - `tasks/TASKS_STATUS_OVERVIEW.md` – Convenções de gestão de tarefas.
  - `tasks/TASKS_BACKLOG.md` – Backlog atual.
  - `tasks/TASKS_IN_PROGRESS.md` – Tarefas em andamento.
  - `tasks/TASKS_DONE.md` – Tarefas concluídas.
  - `memory/MEMORY_SHARED.md` – Contexto compartilhado.
  - Feedback de todos os agentes sobre progresso.

- **Arquivos de saída**:
  - `tasks/TASKS_BACKLOG.md` – Novas tarefas, atualizações.
  - `tasks/TASKS_IN_PROGRESS.md` – Tarefas movidas para execução.
  - `tasks/TASKS_DONE.md` – Tarefas concluídas.
  - `memory/MEMORY_SHARED.md` – Marcos importantes, bloqueios.
  - `memory/MEMORY_EVOLUTION_LOG.md` – Registro de progresso.

- **Memória**:
  - Acesso à memória compartilhada: **Sim** (leitura e escrita)
  - Memória local: `agents/Agente_Gestor_Tarefas/MEMORY_LOCAL.md`

- **Regras específicas**:
  - Não iniciar tarefas sem que pré-requisitos estejam cumpridos.
  - Documentar motivo ao mover tarefas entre estados.
  - Alertar quando tarefas estiverem bloqueadas por mais de um ciclo.
  - Manter IDs de tarefas únicos e sequenciais.
  - Revisar backlog periodicamente para remover tarefas obsoletas.

---

## Agente_Arquiteto_Drones

- **ID**: AGENT_006
- **Papel**: Arquiteto de Drones Autônomos
- **Responsabilidades**:
  - Definir arquitetura de hardware para drones terrestres (UGV), aéreos (UAV) e aquáticos (USV).
  - Projetar stack de software com ROS2, Python, C++ e Rust.
  - Especificar sensores embarcados (câmeras, lidar, IMU, GPS/RTK).
  - Desenvolver pipelines de visão computacional e IA embarcada.
  - Projetar sistema de comunicação redundante (Wi-Fi + LoRa/Meshtastic).
  - Especificar módulo de defesa não letal com protocolos de segurança.
  - Integrar drones com Home Assistant e sistema de alarmes.
  - Definir protocolos de navegação autônoma e resposta a incidentes.

- **Arquivos de entrada**:
  - `PROJECT_OVERVIEW.md` – Contexto geral do projeto.
  - `docs/ARQUITETURA_DRONES_AUTONOMOS.md` – Arquitetura base de drones.
  - `prd/PRD_AUTONOMOUS_DRONES.md` – PRD principal de drones.
  - `rules/RULES_TECHNICAL.md` – Diretrizes técnicas do projeto.
  - `rules/RULES_COMPLIANCE_AND_STANDARDS.md` – Normas aplicáveis (ANAC, LGPD).
  - `tasks/TASKS_BACKLOG.md` – Tarefas atribuídas (T-031 a T-045).
  - `memory/MEMORY_SHARED.md` – Contexto compartilhado.

- **Arquivos de saída**:
  - `docs/ARQUITETURA_DRONES_AUTONOMOS.md` – Atualizações de arquitetura.
  - `prd/PRD_AUTONOMOUS_DRONES.md` – Atualizações do PRD principal.
  - `prd/PRD_DRONE_DEFENSE_MODULE.md` – PRD do módulo de defesa.
  - `prd/PRD_DRONE_COMMUNICATION.md` – PRD de comunicação.
  - `prd/PRD_DRONE_FLEET_MANAGEMENT.md` – PRD de gerenciamento de frota.
  - `prd/PRD_DRONE_AI_VISION.md` – PRD de IA e visão computacional.
  - `docs/GUIA_MONTAGEM_UGV.md` – Guia de montagem drone terrestre.
  - `docs/GUIA_MONTAGEM_UAV.md` – Guia de montagem drone aéreo.
  - `firmware/` – Firmware de controle (ESP32/Arduino).
  - `ros2_ws/` – Workspace ROS2 com pacotes de navegação e IA.
  - `memory/MEMORY_SHARED.md` – Decisões técnicas de drones.

- **Memória**:
  - Acesso à memória compartilhada: **Sim** (leitura e escrita)
  - Memória local: `agents/Agente_Arquiteto_Drones/MEMORY_LOCAL.md`

- **Regras específicas**:
  - Priorizar open hardware com componentes acessíveis no Brasil.
  - Garantir conformidade com normas ANAC (RBAC-E nº 94) e DECEA (SISANT).
  - Projetar com redundância de comunicação obrigatória.
  - Módulo de defesa deve ter autenticação forte e auditoria completa.
  - Documentar BOM (Bill of Materials) com preços estimados.
  - Manter compatibilidade com ROS2 Humble/Iron.
  - Considerar diferentes níveis de expertise do usuário (montagem vs. compra pronta).
  - Priorizar segurança: fail-safe em perda de comunicação.

---

## Criação de memória local para agentes

Para cada agente, criar o arquivo de memória local se não existir:

```bash
mkdir -p agents/Agente_Arquiteto_Seguranca_Fisica
mkdir -p agents/Agente_Arquiteto_Tecnico
mkdir -p agents/Agente_Pesquisador_Normas
mkdir -p agents/Agente_Documentador
mkdir -p agents/Agente_Gestor_Tarefas
mkdir -p agents/Agente_Arquiteto_Drones
```

Template para `MEMORY_LOCAL.md`:

```markdown
# Memória Local – [Nome do Agente]

## Contexto de trabalho atual

> Registre aqui o contexto da tarefa atual em andamento.

## Anotações e rascunhos

> Use esta seção para rascunhos, cálculos e anotações temporárias.

## Cache de pesquisas

> Registre resultados de pesquisas para evitar retrabalho.

## Pendências e dúvidas

> Liste aqui dúvidas para outros agentes ou para humanos.
```

---

## Próximos passos

> **Status (2026-02)**: Diretórios de memória local criados para todos os 6 agentes:
> - `agents/Agente_Arquiteto_Seguranca_Fisica/MEMORY_LOCAL.md`
> - `agents/Agente_Arquiteto_Tecnico/MEMORY_LOCAL.md`
> - `agents/Agente_Pesquisador_Normas/MEMORY_LOCAL.md`
> - `agents/Agente_Documentador/MEMORY_LOCAL.md`
> - `agents/Agente_Gestor_Tarefas/MEMORY_LOCAL.md`
> - `agents/Agente_Arquiteto_Drones/MEMORY_LOCAL.md`
>
> **Permissões definidas**: Todos os agentes têm permissão de **leitura** em todo o repositório.
> Permissão de **escrita** restrita a: pasta própria (`agents/<nome>/`), `tasks/`, `memory/` e arquivos solicitados explicitamente pelo orquestrador.

