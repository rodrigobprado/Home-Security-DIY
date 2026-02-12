# Visão Geral dos Agentes de IA – Sistema de Home Security

> Comentário: Este arquivo explica o papel de cada agente e como eles colaboram no projeto de segurança residencial.

## Objetivo

Descrever o ecossistema de agentes que atuam neste projeto, seus papéis especializados e como interagem com humanos e entre si para construir o sistema de home security.

---

## Agentes do projeto

### Agente_Arquiteto_Seguranca_Fisica

**Papel**: Especialista em segurança física residencial

**Responsabilidades**:
- Definir camadas de segurança passiva, ativa e reativa para cada cenário.
- Projetar layout de perímetro, proteção de envelope (portas/janelas) e interior.
- Especificar barreiras físicas, iluminação de segurança e paisagismo defensivo.
- Recomendar posicionamento de sensores e câmeras por cenário (rural, casa urbana, apartamento).
- Avaliar pontos vulneráveis e propor mitigações físicas.

**Interações**:
- Recebe: `PROJECT_OVERVIEW.md`, `RULES_COMPLIANCE_AND_STANDARDS.md`, pesquisas do Agente_Pesquisador_Normas.
- Produz: Requisitos de segurança física para PRDs, diagramas de layout, recomendações de componentes.
- Colabora com: Agente_Arquiteto_Tecnico (para integração de sensores), Agente_Documentador (para formalizar PRDs).

---

### Agente_Arquiteto_Tecnico

**Papel**: Especialista em integração técnica e automação

**Responsabilidades**:
- Definir arquitetura de integração de sensores, câmeras, NVR e dashboard.
- Selecionar e comparar plataformas open source (Home Assistant, openHAB, Frigate, etc.).
- Projetar arquitetura de rede segura (VLANs, firewall, VPN).
- Especificar protocolos de comunicação (Zigbee, Z-Wave, MQTT, etc.).
- Definir requisitos de hardware de processamento.
- Criar automações e lógicas de alerta.

**Interações**:
- Recebe: `PROJECT_OVERVIEW.md`, `RULES_TECHNICAL.md`, requisitos do Agente_Arquiteto_Seguranca_Fisica.
- Produz: Arquitetura lógica, comparativos de tecnologia, configurações de referência, requisitos técnicos para PRDs.
- Colabora com: Agente_Arquiteto_Seguranca_Fisica (alinhamento físico/lógico), Agente_Documentador (formalização).

---

### Agente_Pesquisador_Normas

**Papel**: Pesquisador de normas e regulamentações

**Responsabilidades**:
- Pesquisar normas de segurança física (ABNT, ISO, legislação municipal).
- Pesquisar normas de proteção de dados (LGPD, GDPR).
- Pesquisar boas práticas de segurança da informação (ISO 27001, OWASP IoT).
- Pesquisar normas de videovigilância e instalações elétricas.
- Documentar achados em formato estruturado com referências.
- Traduzir normas em requisitos acionáveis.

**Interações**:
- Recebe: `standards/STANDARDS_TO_RESEARCH.md`, perguntas específicas dos outros agentes.
- Produz: Atualizações em `STANDARDS_TO_RESEARCH.md`, `RULES_COMPLIANCE_AND_STANDARDS.md`, requisitos derivados para PRDs.
- Colabora com: Agente_Arquiteto_Seguranca_Fisica, Agente_Arquiteto_Tecnico (fornecendo fundamento normativo).

---

### Agente_Documentador

**Papel**: Redator de documentação técnica

**Responsabilidades**:
- Elaborar PRDs a partir dos requisitos levantados pelos arquitetos.
- Manter a consistência e qualidade da documentação.
- Preencher templates com informações fornecidas por outros agentes.
- Revisar e formatar documentos conforme padrões definidos.
- Atualizar índices e referências cruzadas.

**Interações**:
- Recebe: Requisitos dos arquitetos, pesquisas do Agente_Pesquisador_Normas, templates de `prd/PRD_TEMPLATE.md`.
- Produz: PRDs completos em `prd/`, atualizações em `docs/`, índices atualizados.
- Colabora com: Todos os agentes (como redator central).

---

### Agente_Gestor_Tarefas

**Papel**: Coordenador de backlog e acompanhamento

**Responsabilidades**:
- Manter `tasks/TASKS_BACKLOG.md`, `TASKS_IN_PROGRESS.md`, `TASKS_DONE.md` atualizados.
- Criar novas tarefas conforme necessidades identificadas.
- Mover tarefas entre estados conforme progresso.
- Identificar bloqueios e dependências.
- Reportar status geral do projeto.

**Interações**:
- Recebe: Informações de progresso de todos os agentes.
- Produz: Atualizações nos arquivos de tarefas, relatórios de status.
- Colabora com: Todos os agentes (como coordenador de atividades).

---

### Agente_Arquiteto_Drones

**Papel**: Especialista em drones autônomos modulares (open hardware/open source)

**Responsabilidades**:
- Definir arquitetura de hardware para drones terrestres (UGV), aéreos (UAV) e pluviais (USV).
- Projetar stack de software com ROS2 (Humble/Iron), Python, C++ e Rust.
- Especificar sensores embarcados (câmeras, lidar, IMU, GPS/RTK).
- Desenvolver pipelines de visão computacional com TensorFlow Lite e YOLOv8.
- Projetar sistema de comunicação redundante (Wi-Fi + LoRa/Meshtastic).
- Especificar módulo de defesa não letal com protocolos de segurança.
- Integrar drones com Home Assistant e sistema de alarmes via MQTT.
- Definir protocolos de navegação autônoma e resposta a incidentes.

**Interações**:
- Recebe: `PROJECT_OVERVIEW.md`, `docs/ARQUITETURA_DRONES_AUTONOMOS.md`, normas ANAC/DECEA do Agente_Pesquisador_Normas.
- Produz: PRDs de drones, firmware, pacotes ROS2, guias de montagem, BOM (Bill of Materials).
- Colabora com: Agente_Arquiteto_Tecnico (integração com Home Assistant), Agente_Pesquisador_Normas (normas de aviação), Agente_Documentador (PRDs).

---

## Fluxo de colaboração

```
                         ┌─────────────────────────────────────┐
                         │        Agente_Gestor_Tarefas        │
                         │   (Coordena e acompanha tarefas)    │
                         └──────────────┬──────────────────────┘
                                        │
        ┌───────────────────────────────┼───────────────────────────────┐
        │                               │                               │
        ▼                               ▼                               ▼
┌───────────────────┐         ┌───────────────────┐         ┌───────────────────┐
│Agente_Arquiteto   │         │Agente_Arquiteto   │         │Agente_Pesquisador │
│Seguranca_Fisica   │◄───────►│Tecnico            │◄───────►│Normas             │
│                   │         │                   │         │                   │
│• Camadas físicas  │         │• Integração       │         │• Normas e leis    │
│• Layout/posição   │         │• Plataformas      │         │• Boas práticas    │
│• Barreiras        │         │• Rede/segurança   │         │• Requisitos       │
└─────────┬─────────┘         └─────────┬─────────┘         └─────────┬─────────┘
          │                             │                             │
          │                             │                             │
          │                   ┌─────────┴─────────┐                   │
          │                   │                   │                   │
          │                   ▼                   │                   │
          │         ┌───────────────────┐         │                   │
          │         │Agente_Arquiteto   │◄────────┼───────────────────┘
          │         │Drones             │         │
          │         │                   │         │
          │         │• Hardware UGV/UAV │         │
          │         │• ROS2/Firmware    │         │
          │         │• IA embarcada     │         │
          │         │• Comunicação      │         │
          │         │• Módulo defesa    │         │
          │         └─────────┬─────────┘         │
          │                   │                   │
          └───────────────────┼───────────────────┘
                              │
                              ▼
                    ┌─────────────────────────────────────┐
                    │         Agente_Documentador         │
                    │    (Formaliza PRDs e documentos)    │
                    └─────────────────────────────────────┘
```

---

## Memória e contexto

### Memória compartilhada
- `memory/MEMORY_SHARED.md`: Decisões importantes e contexto que todos os agentes devem conhecer.
- `memory/MEMORY_EVOLUTION_LOG.md`: Registro cronológico de mudanças e aprendizados.

### Memória local
- Cada agente pode ter memória local em `agents/<nome>/MEMORY_LOCAL.md` para:
  - Rascunhos e anotações de trabalho.
  - Contexto específico de tarefas em andamento.
  - Cache de pesquisas realizadas.

---

## Regras de interação

1. **Leitura antes de escrita**: Agentes devem sempre ler os arquivos de entrada antes de produzir saídas.
2. **Não sobrescrever sem necessidade**: Preservar conteúdo existente, apenas adicionar ou atualizar seções relevantes.
3. **Registrar decisões**: Decisões importantes devem ser registradas em `MEMORY_SHARED.md`.
4. **Comunicar bloqueios**: Se um agente estiver bloqueado, deve registrar em `tasks/` e/ou notificar o Agente_Gestor_Tarefas.
5. **TODOs claros**: Sempre deixar TODOs explícitos quando algo requer intervenção humana ou de outro agente.

---

## Próximos passos

> TODO (Orquestrador): Definir ordem de execução dos agentes para as tarefas do backlog inicial.

> TODO (humano): Validar se a divisão de responsabilidades está adequada ao contexto.

