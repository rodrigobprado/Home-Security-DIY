# Backlog de Tarefas – Sistema de Home Security

> Comentário: Tarefas ainda não iniciadas vão aqui. Organizadas por categoria para facilitar priorização.

## Legenda de prioridade
- **Crítica**: Bloqueia outras tarefas ou é pré-requisito fundamental.
- **Alta**: Importante para o progresso do projeto.
- **Média**: Necessária, mas pode aguardar tarefas de maior prioridade.
- **Baixa**: Desejável, mas não urgente.

---

## Categoria: Levantamento de requisitos

> **Tarefas T-001, T-002, T-003, T-007 concluídas em 2026-02-12** – Movidas para `TASKS_DONE.md`

| ID | Título | Descrição | Responsável | Prioridade | PRD relacionado |
|----|--------|-----------|-------------|------------|-----------------|
| T-004 | Levantar requisitos de segurança ativa – cenário rural | Definir sensores, câmeras e alarmes adequados para perímetros extensos e áreas abertas. | Agente_Arquiteto_Tecnico | Alta | PRD_PERIMETER_RURAL |
| T-005 | Levantar requisitos de segurança ativa – casa urbana | Definir sensores para muros, quintal, portas e janelas de casa urbana. | Agente_Arquiteto_Tecnico | Alta | PRD_PERIMETER_URBAN_HOUSE, PRD_HOUSE_ENVELOPE |
| T-006 | Levantar requisitos de segurança ativa – apartamento | Definir sensores e controle de acesso para porta de apartamento e janelas (se aplicável). | Agente_Arquiteto_Tecnico | Alta | PRD_APARTMENT_SECURITY |

---

## Categoria: Arquitetura e design

> **Tarefas T-008, T-009, T-010 concluídas em 2026-02-12** – Movidas para `TASKS_DONE.md`

| ID | Título | Descrição | Responsável | Prioridade | PRD relacionado |
|----|--------|-----------|-------------|------------|-----------------|
| T-011 | Desenhar arquitetura lógica de integração | Definir fluxo de dados entre sensores, câmeras, NVR, central de automação e dashboard. | Agente_Arquiteto_Tecnico | Alta | PRD_SENSORS_AND_ALARMS_PLATFORM, PRD_VIDEO_SURVEILLANCE_AND_NVR |
| T-012 | Definir arquitetura de rede segura | Projetar segmentação de rede (VLANs), firewall, VPN e isolamento de dispositivos IoT. | Agente_Arquiteto_Tecnico | Alta | PRD_NETWORK_SECURITY |

---

## Categoria: Seleção de tecnologias

| ID | Título | Descrição | Responsável | Prioridade | PRD relacionado |
|----|--------|-----------|-------------|------------|-----------------|
| T-013 | Avaliar plataformas de automação open source | Comparar Home Assistant, openHAB e outras plataformas. Documentar prós/contras, curva de aprendizado, comunidade. | Agente_Arquiteto_Tecnico | Alta | PRD_LOCAL_PROCESSING_HUB |
| T-014 | Avaliar NVRs open source | Comparar ZoneMinder, Frigate, Shinobi, Viseron. Avaliar detecção de objetos, consumo de recursos, facilidade de uso. | Agente_Arquiteto_Tecnico | Alta | PRD_VIDEO_SURVEILLANCE_AND_NVR |
| T-015 | Avaliar protocolos de sensores | Comparar Zigbee, Z-Wave, Wi-Fi, 433MHz, Thread/Matter. Documentar alcance, consumo, custo, disponibilidade. | Agente_Arquiteto_Tecnico | Média | PRD_SENSORS_AND_ALARMS_PLATFORM |
| T-016 | Pesquisar hardware de processamento acessível | Levantar opções de hardware (Raspberry Pi 4/5, mini PC, NUC, etc.) com requisitos e custos estimados. | Agente_Arquiteto_Tecnico | Média | PRD_LOCAL_PROCESSING_HUB |
| T-017 | Pesquisar câmeras IP compatíveis | Listar câmeras com suporte a RTSP/ONVIF, PoE, visão noturna, adequadas para uso residencial open source. | Agente_Arquiteto_Tecnico | Média | PRD_VIDEO_SURVEILLANCE_AND_NVR |

---

## Categoria: Normas e compliance

> **Tarefas T-018 a T-021, T-028 a T-030 concluídas em 2026-02-12** – Movidas para `TASKS_DONE.md`

| ID | Título | Descrição | Responsável | Prioridade | PRD relacionado |
|----|--------|-----------|-------------|------------|-----------------|
| | | | | | |

> ✅ Todas as tarefas de pesquisa de normas foram concluídas.

---

## Categoria: Documentação e PRDs

> **Tarefas T-022, T-023, T-024, T-025 concluídas em 2026-02-12** – Movidas para `TASKS_DONE.md`

| ID | Título | Descrição | Responsável | Prioridade | PRD relacionado |
|----|--------|-----------|-------------|------------|-----------------|
| | | | | | |

> Todas as tarefas prioritárias de documentação foram concluídas. PRDs restantes podem ser criados conforme demanda.

---

## Categoria: Privacidade e segurança da informação

| ID | Título | Descrição | Responsável | Prioridade | PRD relacionado |
|----|--------|-----------|-------------|------------|-----------------|
| T-026 | Definir requisitos de privacidade por design | Documentar como garantir processamento local, criptografia, controle de acesso e minimização de dados. | Agente_Arquiteto_Tecnico | Alta | PRD_NETWORK_SECURITY, RULES_COMPLIANCE_AND_STANDARDS |
| T-027 | Definir política de retenção de gravações | Estabelecer períodos de retenção, rotação automática, backup seguro de evidências. | Agente_Arquiteto_Tecnico | Média | PRD_VIDEO_SURVEILLANCE_AND_NVR |

---

---

## Categoria: Drones autônomos (módulo reativo avançado)

> **NOVO**: Tarefas para desenvolvimento do sistema de drones autônomos modulares.

| ID | Título | Descrição | Responsável | Prioridade | PRD relacionado |
|----|--------|-----------|-------------|------------|-----------------|
| T-031 | Definir arquitetura de hardware UGV | Especificar chassis, motores, controladores, sensores e computador embarcado para drone terrestre. | Agente_Arquiteto_Drones | Alta | PRD_AUTONOMOUS_DRONES |
| T-032 | Definir arquitetura de hardware UAV | Especificar frame, propulsão, flight controller, sensores e computador embarcado para drone aéreo. | Agente_Arquiteto_Drones | Média | PRD_AUTONOMOUS_DRONES |
| T-033 | Desenvolver firmware de controle baixo nível | Criar firmware ESP32/Arduino para controle de motores, leitura de sensores e comunicação serial. | Agente_Arquiteto_Drones | Alta | PRD_AUTONOMOUS_DRONES |
| T-034 | Implementar stack ROS2 para navegação | Configurar ROS2 Humble/Iron com Nav2, SLAM, localização e planejamento de trajetória. | Agente_Arquiteto_Drones | Alta | PRD_AUTONOMOUS_DRONES |
| T-035 | Implementar pipeline de visão computacional | Desenvolver detecção de pessoas/veículos, tracking e classificação com YOLOv8/TensorFlow Lite. | Agente_Arquiteto_Drones | Alta | PRD_DRONE_AI_VISION |
| T-036 | Implementar sistema de comunicação redundante | Desenvolver failover Wi-Fi → LoRa/Meshtastic com streaming de vídeo e telemetria. | Agente_Arquiteto_Drones | Alta | PRD_DRONE_COMMUNICATION |
| T-037 | Desenvolver módulo de defesa não letal | Especificar e implementar sistema CO₂ + OC com autenticação, auditoria e protocolos de segurança. | Agente_Arquiteto_Drones | Média | PRD_DRONE_DEFENSE_MODULE |
| T-038 | Integrar drones com Home Assistant | Implementar integração MQTT para controle, telemetria e disparo por eventos de alarme. | Agente_Arquiteto_Drones | Alta | PRD_AUTONOMOUS_DRONES |
| T-039 | Desenvolver dashboard de frota | Criar interface de monitoramento e controle para múltiplos drones no Home Assistant. | Agente_Arquiteto_Drones | Média | PRD_DRONE_FLEET_MANAGEMENT |
| T-040 | Elaborar PRD do módulo de defesa | Detalhar requisitos funcionais e não funcionais do sistema de defesa não letal. | Agente_Documentador | Média | PRD_DRONE_DEFENSE_MODULE |
| T-041 | Elaborar PRD de comunicação de drones | Detalhar requisitos de rede, protocolos, failover e streaming para drones. | Agente_Documentador | Média | PRD_DRONE_COMMUNICATION |
| ~~T-042~~ | ~~Pesquisar normas ANAC/DECEA para drones~~ | ~~Levantar requisitos legais para operação de drones no Brasil (RBAC-E nº 94, SISANT).~~ | ~~Agente_Arquiteto_Drones~~ | ~~Alta~~ | ✅ CONCLUÍDO 2026-02-12 |
| ~~T-043~~ | ~~Pesquisar legislação de defesa não letal~~ | ~~Levantar regulamentação estadual/federal para uso de spray de pimenta em propriedade privada.~~ | ~~Agente_Arquiteto_Drones~~ | ~~Média~~ | ✅ CONCLUÍDO 2026-02-12 |
| T-044 | Criar guia de montagem UGV | Documentar passo a passo de montagem do drone terrestre com BOM e instruções. | Agente_Documentador | Baixa | PRD_AUTONOMOUS_DRONES |
| T-045 | Criar guia de montagem UAV | Documentar passo a passo de montagem do drone aéreo com BOM e instruções. | Agente_Documentador | Baixa | PRD_AUTONOMOUS_DRONES |

---

## Resumo do backlog

| Categoria | Total de tarefas | Concluídas |
|-----------|-----------------|------------|
| Levantamento de requisitos | 7 | 7 (T-001 a T-007) |
| Arquitetura e design | 5 | 5 (T-008 a T-012) |
| Seleção de tecnologias | 5 | 5 (T-013 a T-017) |
| Normas e compliance | 7 | 7 (T-018 a T-021, T-028 a T-030) |
| Documentação e PRDs | 4 | 4 (T-022 a T-025) |
| Privacidade e segurança | 2 | 2 (T-026, T-027) |
| **Drones autônomos** | **15** | **2 (T-042, T-043)** |
| **Total** | **45** | **32 concluídas (71%)** |

---

## Próximas tarefas prioritárias

### Módulo de drones autônomos

| Ordem | ID | Título | Justificativa | Status |
|-------|----|----|---------------|--------|
| ~~1~~ | ~~T-042~~ | ~~Pesquisar normas ANAC/DECEA~~ | ~~Requisito legal~~ | ✅ Concluído |
| 1 | T-031 | Arquitetura de hardware UGV | Base para desenvolvimento de firmware e ROS2 | Pendente |
| 2 | T-033 | Firmware de controle baixo nível | Pré-requisito para navegação | Pendente |
| 3 | T-034 | Stack ROS2 para navegação | Core do sistema autônomo | Pendente |
| 4 | T-036 | Sistema de comunicação redundante | Crítico para operação remota | Pendente |
| 5 | T-035 | Pipeline de visão computacional | Essencial para detecção e tracking | Pendente |
| 6 | T-038 | Integração com Home Assistant | Conexão com sistema principal | Pendente |

---

> TODO (Agente_Gestor_Tarefas): Revisar e manter este backlog atualizado conforme novas necessidades surgirem.

> TODO (humano): Priorizar e aprovar a ordem de execução das tarefas de drones antes de iniciar o trabalho.

