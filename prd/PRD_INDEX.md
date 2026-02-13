# Índice de PRDs – Sistema de Home Security

> Comentário: Mantenha aqui uma lista de todos os PRDs do projeto. Cada PRD deve detalhar requisitos específicos de um subsistema ou cenário.

## PRDs por cenário residencial

### Cenário 1: Propriedade Rural

| PRD | Título | Descrição |
|-----|--------|-----------|
| `PRD_PERIMETER_RURAL.md` | Segurança de perímetro rural | Requisitos para proteção de perímetros extensos em áreas rurais, incluindo cercas, sensores de longo alcance, câmeras com visão noturna, detecção de invasão em áreas abertas e integração com iluminação perimetral. |
| `PRD_RURAL_ACCESS_CONTROL.md` | Controle de acesso rural | Requisitos para controle de portões de entrada (veículos e pedestres), interfones remotos, câmeras de reconhecimento de placas e integração com automação de abertura. |

### Cenário 2: Casa urbana com quintal

| PRD | Título | Descrição |
|-----|--------|-----------|
| `PRD_PERIMETER_URBAN_HOUSE.md` | Perímetro de casa urbana | Requisitos para proteção de muros, grades, portões e quintal, incluindo sensores de movimento externos, câmeras de área, iluminação reativa e detecção de aproximação. |
| `PRD_HOUSE_ENVELOPE.md` | Envelope da casa (portas e janelas) | Requisitos para proteção de todas as aberturas da casa: sensores de abertura, detectores de quebra de vidro, reforço de fechaduras e monitoramento de pontos vulneráveis. |

### Cenário 3: Apartamento

| PRD | Título | Descrição |
|-----|--------|-----------|
| `PRD_APARTMENT_SECURITY.md` | Segurança de apartamento | Requisitos para proteção de porta principal, janelas de andar alto (quando aplicável), integração com portaria/interfone do condomínio e controle de acesso interno. |
| `PRD_APARTMENT_SMART_LOCK.md` | Fechadura inteligente para apartamento | Requisitos específicos para fechaduras eletrônicas em portas de apartamento, incluindo modos de acesso (senha, biometria, app, chave física), auditoria de acessos e integração com automação. |

## PRDs de subsistemas (aplicáveis a todos os cenários)

| PRD | Título | Descrição |
|-----|--------|-----------|
| `PRD_SENSORS_AND_ALARMS_PLATFORM.md` | Plataforma de sensores e alarmes | Requisitos da central de monitoramento de sensores: tipos de sensores suportados (movimento, abertura, vibração, vidro, fumaça, vazamento), protocolos de comunicação (Zigbee, Z-Wave, Wi-Fi, 433MHz), lógica de disparo de alarmes e integração com sirenes. |
| `PRD_VIDEO_SURVEILLANCE_AND_NVR.md` | Videovigilância e NVR | Requisitos do sistema de câmeras e gravação: resolução mínima, armazenamento local, retenção de imagens, detecção inteligente (pessoas, veículos, objetos abandonados), streaming ao vivo, acesso remoto seguro. |
| `PRD_MONITORING_DASHBOARD.md` | Dashboard de monitoramento | Requisitos da interface de controle: visualização de status de sensores e câmeras, mapa da residência, histórico de eventos, controles de armar/desarmar, configuração de zonas e perfis. |
| `PRD_NOTIFICATIONS_AND_ALERTS.md` | Notificações e alertas | Requisitos do sistema de notificações: canais suportados (push, SMS, e-mail, Telegram, chamada de voz), priorização de alertas, configuração de silenciamento, confirmação de recebimento. |
| `PRD_AUTOMATION_AND_SCENES.md` | Automações e cenas | Requisitos para automações de segurança: iluminação reativa, simulação de presença, travamento automático, cenas de "saindo de casa" e "chegando em casa", integração com rotinas diárias. |
| `PRD_ENVIRONMENTAL_SENSORS.md` | Sensores ambientais | Requisitos para detecção de incêndio (fumaça, calor), vazamento de gás, inundação, qualidade do ar, incluindo lógica de alerta e integração com sistema de segurança principal. |
| `PRD_BACKUP_AND_RESILIENCE.md` | Backup e resiliência | Requisitos para continuidade do sistema: nobreak/bateria, backup de configurações, redundância de comunicação (4G como failover), recuperação após falha de energia. |

## PRDs de infraestrutura

| PRD | Título | Descrição |
|-----|--------|-----------|
| `PRD_NETWORK_SECURITY.md` | Segurança de rede | Requisitos para proteção da rede local: segregação de VLANs (IoT, câmeras, gestão), firewall, VPN para acesso remoto, bloqueio de acesso à internet para dispositivos que não precisam. |
| `PRD_LOCAL_PROCESSING_HUB.md` | Hub de processamento local | Requisitos do hardware central: especificações mínimas (CPU, RAM, armazenamento), sistema operacional, instalação de plataformas (Home Assistant, Frigate), backup automatizado. |

## PRDs de drones autônomos (módulo reativo avançado)

| PRD | Título | Descrição |
|-----|--------|-----------|
| `PRD_AUTONOMOUS_DRONES.md` | Drones autônomos modulares | PRD principal: requisitos para frota de drones terrestres (UGV), aéreos (UAV) e aquáticos (USV) com navegação autônoma, IA embarcada, sensoriamento e integração com Home Security. |
| `PRD_DRONE_DEFENSE_MODULE.md` | Módulo de defesa não letal | Requisitos para sistema de disparo CO₂ + OC (pimenta), autenticação de 2 fatores, auditoria completa, modos de operação e protocolos de segurança. |
| `PRD_DRONE_COMMUNICATION.md` | Comunicação de drones | Requisitos para rede de comunicação redundante: Wi-Fi longo alcance, LoRa/Meshtastic, failover automático, streaming de vídeo, telemetria e comandos. |
| `PRD_DRONE_FLEET_MANAGEMENT.md` | Gerenciamento de frota | Requisitos para coordenação de múltiplos drones: divisão de áreas, balanceamento de carga, substituição automática por bateria baixa, resposta coordenada a incidentes. |
| `PRD_DRONE_AI_VISION.md` | IA e visão computacional | Requisitos para processamento de visão embarcado: detecção de pessoas/veículos, tracking, reconhecimento facial (whitelist), classificação de comportamento e decisão autônoma. |

## Status de elaboração

### PRDs principais e cenários

| PRD | Status | Responsável | Data |
|-----|--------|-------------|------|
| `PRD_PERIMETER_RURAL.md` | ✅ CONCLUÍDO | Agente_Documentador | 2026-02-12 |
| `PRD_RURAL_ACCESS_CONTROL.md` | TODO | Agente_Documentador | - |
| `PRD_PERIMETER_URBAN_HOUSE.md` | ✅ CONCLUÍDO | Agente_Documentador | 2026-02-12 |
| `PRD_HOUSE_ENVELOPE.md` | TODO | Agente_Documentador | - |
| `PRD_APARTMENT_SECURITY.md` | ✅ CONCLUÍDO | Agente_Documentador | 2026-02-12 |
| `PRD_APARTMENT_SMART_LOCK.md` | TODO | Agente_Documentador | - |
| `PRD_SENSORS_AND_ALARMS_PLATFORM.md` | ✅ CONCLUÍDO | Agente_Documentador | 2026-02-12 |
| `PRD_VIDEO_SURVEILLANCE_AND_NVR.md` | ✅ CONCLUÍDO | Agente_Documentador | 2026-02-12 |
| `PRD_MONITORING_DASHBOARD.md` | ✅ CONCLUÍDO | Agente_Documentador | 2026-02-12 |
| `PRD_NOTIFICATIONS_AND_ALERTS.md` | TODO | Agente_Documentador | - |
| `PRD_AUTOMATION_AND_SCENES.md` | TODO | Agente_Documentador | - |
| `PRD_ENVIRONMENTAL_SENSORS.md` | TODO | Agente_Documentador | - |
| `PRD_BACKUP_AND_RESILIENCE.md` | TODO | Agente_Documentador | - |
| `PRD_NETWORK_SECURITY.md` | TODO | Agente_Documentador | - |
| `PRD_LOCAL_PROCESSING_HUB.md` | TODO | Agente_Documentador | - |

### PRDs de drones autônomos

| PRD | Status | Responsável | Data |
|-----|--------|-------------|------|
| `PRD_AUTONOMOUS_DRONES.md` | ✅ CONCLUÍDO | Agente_Arquiteto_Drones | 2026-02-12 |
| `PRD_DRONE_DEFENSE_MODULE.md` | TODO | Agente_Arquiteto_Drones | - |
| `PRD_DRONE_COMMUNICATION.md` | TODO | Agente_Arquiteto_Drones | - |
| `PRD_DRONE_FLEET_MANAGEMENT.md` | TODO | Agente_Arquiteto_Drones | - |
| `PRD_DRONE_AI_VISION.md` | TODO | Agente_Arquiteto_Drones | - |

### Resumo de progresso PRDs

| Status | Quantidade |
|--------|------------|
| Concluídos | 7 |
| Pendentes (principais) | 8 |
| Pendentes (drones) | 4 |
| **Total** | **20** |

> **Última atualização**: 2026-02-12 por Agente_Arquiteto_Drones

