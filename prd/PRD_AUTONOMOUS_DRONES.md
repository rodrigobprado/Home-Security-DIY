# PRD – Sistema de Drones Autônomos Modulares

> Sistema de Home Security – Open Source / Open Hardware
>
> Módulo Reativo Avançado
>
> Versão: 1.0 | Data: 2026-02-12 | Responsável: Agente_Documentador

---

## 1. Visão geral

- **Nome do produto/funcionalidade**: Frota de Drones Autônomos Modulares
- **Responsável**: A definir (Agente_Arquiteto_Drones)
- **Data**: 2026-02-12
- **PRDs relacionados**: PRD_DRONE_DEFENSE_MODULE, PRD_DRONE_COMMUNICATION, PRD_SENSORS_AND_ALARMS_PLATFORM

---

## 2. Problema e oportunidade

### 2.1 Problema

Sistemas de segurança residencial tradicionais são estáticos e reativos:
- **Câmeras fixas** têm pontos cegos e cobertura limitada
- **Sensores** apenas detectam, não respondem ativamente
- **Tempo de resposta** depende de intervenção humana ou policial
- **Áreas extensas** (rurais) são impossíveis de monitorar completamente
- **Intrusos** podem evitar zonas monitoradas conhecidas

### 2.2 Oportunidade

Criar uma frota de drones autônomos que:
- **Patrulham** ativamente perímetros e áreas críticas
- **Respondem** automaticamente a alertas do sistema de segurança
- **Seguem** e documentam intrusos com vídeo e geolocalização
- **Dissuadem** através de presença, alertas sonoros e defesa não letal
- **Operam** de forma coordenada como uma frota inteligente

---

## 3. Público-alvo

| Perfil | Necessidade principal |
|--------|----------------------|
| **Proprietário rural** | Cobertura de grandes áreas, patrulha de perímetro |
| **Proprietário urbano** | Resposta rápida a alertas, documentação de incidentes |
| **Entusiasta DIY** | Projeto open source para construção própria |
| **Empresa de segurança** | Solução customizável para clientes |

---

## 4. Requisitos funcionais

### 4.1 Tipos de drones

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-001 | Suportar drone terrestre (UGV) com rodas ou esteiras | Alta |
| RF-002 | Suportar drone aéreo (UAV) multirrotor | Média |
| RF-003 | Suportar drone pluvial (USV) para áreas aquáticas | Baixa |
| RF-004 | Arquitetura modular para troca de componentes | Alta |
| RF-005 | Design open hardware com peças acessíveis | Alta |

### 4.2 Navegação autônoma

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-006 | Navegação autônoma por waypoints | Alta |
| RF-007 | Desvio de obstáculos em tempo real | Alta |
| RF-008 | SLAM para mapeamento de ambiente | Média |
| RF-009 | Navegação GPS/RTK para precisão centimétrica | Média |
| RF-010 | Retorno automático à base em bateria baixa | Alta |
| RF-011 | Retorno automático em perda de sinal | Alta |
| RF-012 | Patrulha programada por horário/rota | Alta |

### 4.3 Percepção e sensoriamento

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-013 | Câmera visual HD/4K com streaming | Alta |
| RF-014 | Câmera térmica/infravermelha | Média |
| RF-015 | Visão noturna (IR ativo ou térmica) | Alta |
| RF-016 | Lidar ou ultrassônico para obstáculos | Alta |
| RF-017 | Microfone para captação de áudio | Média |
| RF-018 | Alto-falante para comunicação/alertas | Alta |

### 4.4 Inteligência artificial

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-019 | Detecção de pessoas em tempo real | Alta |
| RF-020 | Detecção de veículos | Alta |
| RF-021 | Tracking de objetos em movimento | Alta |
| RF-022 | Reconhecimento facial (whitelist) | Média |
| RF-023 | Detecção de comportamento suspeito | Média |
| RF-024 | Classificação de eventos (baixo/médio/alto risco) | Alta |
| RF-025 | Decisão autônoma de escalonamento | Média |

### 4.5 Comunicação

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-026 | Wi-Fi de longo alcance como canal principal | Alta |
| RF-027 | LoRa/Meshtastic como canal redundante | Alta |
| RF-028 | Streaming de vídeo em tempo real | Alta |
| RF-029 | Telemetria contínua (posição, bateria, status) | Alta |
| RF-030 | Comandos remotos bidirecionais | Alta |
| RF-031 | Failover automático entre canais | Alta |

### 4.6 Integração com Home Security

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-032 | Integração com Home Assistant via MQTT | Alta |
| RF-033 | Disparo automático por evento de alarme | Alta |
| RF-034 | Streaming para Frigate/NVR | Alta |
| RF-035 | Notificações via canais existentes | Alta |
| RF-036 | Dashboard unificado de drones | Alta |
| RF-037 | Histórico de patrulhas e eventos | Alta |

### 4.7 Módulo de defesa (opcional)

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-038 | Sistema de disparo CO₂ + OC (pimenta) | Baixa |
| RF-039 | Autenticação de 2 fatores para armamento | Alta* |
| RF-040 | Registro completo de cada disparo | Alta* |
| RF-041 | Aviso sonoro/visual antes do disparo | Alta* |
| RF-042 | Modos: desativado, standby, semi-auto, auto | Média* |

> *Prioridade alta se módulo de defesa for implementado.

### 4.8 Coordenação de frota

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-043 | Gerenciamento centralizado de múltiplos drones | Média |
| RF-044 | Divisão de áreas de patrulha | Média |
| RF-045 | Coordenação de resposta a incidentes | Média |
| RF-046 | Balanceamento de carga (substituição por bateria) | Baixa |

---

## 5. Requisitos não funcionais

### 5.1 Performance

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-001 | Latência de vídeo | < 500ms em Wi-Fi |
| RNF-002 | Latência de comando | < 200ms em Wi-Fi, < 2s em LoRa |
| RNF-003 | Taxa de detecção IA | > 10 FPS |
| RNF-004 | Autonomia UGV | > 2 horas |
| RNF-005 | Autonomia UAV | > 20 minutos |
| RNF-006 | Velocidade máxima UGV | 5-10 km/h |
| RNF-007 | Alcance de comunicação Wi-Fi | > 200m |
| RNF-008 | Alcance de comunicação LoRa | > 2km |

### 5.2 Confiabilidade

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-009 | Uptime do sistema | > 99% |
| RNF-010 | MTBF | > 1000 horas de operação |
| RNF-011 | Recuperação de falha | Retorno automático à base |
| RNF-012 | Redundância de comunicação | Mínimo 2 canais |

### 5.3 Segurança

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-013 | Autenticação | TLS 1.3, certificados mTLS |
| RNF-014 | Criptografia | AES-256 para dados sensíveis |
| RNF-015 | Integridade de firmware | Assinatura digital |
| RNF-016 | Auditoria | Logs imutáveis com hash |

### 5.4 Conformidade

| ID | Requisito | Referência |
|----|-----------|------------|
| RNF-017 | Registro ANAC | Drones >250g (RBAC-E nº 94) |
| RNF-018 | Espaço aéreo | Zonas permitidas (DECEA) |
| RNF-019 | LGPD | Processamento local, sem nuvem |
| RNF-020 | Defesa não letal | Legislação estadual aplicável |

---

## 6. Arquitetura técnica

### 6.1 Stack de software

| Camada | Tecnologia |
|--------|------------|
| **Framework robótico** | ROS2 Humble/Iron |
| **IA/ML** | TensorFlow Lite, ONNX, YOLOv8 |
| **Comunicação** | MQTT, WebSocket, gRPC |
| **SO embarcado** | Ubuntu 22.04, FreeRTOS |
| **Linguagens** | Python, C++, Rust |

### 6.2 Hardware de referência

| Componente | UGV | UAV |
|------------|-----|-----|
| **Computador** | Raspberry Pi 5 / Jetson Nano | Jetson Orin Nano |
| **Controlador** | ESP32 / Arduino | Pixhawk 6C |
| **Câmera** | Pi Camera V3 + Flir Lepton | IMX477 + gimbal |
| **Lidar** | RPLidar A1 | Opcional |
| **GPS** | u-blox NEO-M8N | HERE3+ RTK |
| **Comunicação** | ESP32 + RFM95W | SiK Radio + ESP32 |

---

## 7. Critérios de aceitação

| ID | Critério | Método de verificação |
|----|----------|----------------------|
| CA-001 | Drone navega autonomamente entre waypoints | Teste de rota programada |
| CA-002 | Drone desvia de obstáculos corretamente | Teste com obstáculos |
| CA-003 | Detecção de pessoas funciona com >90% precisão | Teste de detecção |
| CA-004 | Streaming de vídeo tem latência <500ms | Medição de latência |
| CA-005 | Drone retorna à base com bateria <20% | Teste de autonomia |
| CA-006 | Failover para LoRa funciona em perda de Wi-Fi | Teste de failover |
| CA-007 | Integração com Home Assistant funcional | Teste de integração |
| CA-008 | Dashboard exibe telemetria em tempo real | Verificação visual |

---

## 8. Métricas de sucesso

| Métrica | Alvo |
|---------|------|
| **Cobertura de patrulha** | 100% do perímetro em 30 min |
| **Tempo de resposta a alerta** | < 60 segundos |
| **Disponibilidade** | > 99% |
| **Falsos positivos de detecção** | < 5% |
| **Satisfação do usuário** | > 4/5 |

---

## 9. Riscos e mitigações

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Regulamentação de drones | Alta | Alto | Verificar ANAC/DECEA antes de operar |
| Autonomia insuficiente | Média | Médio | Baterias maiores, estações de carga |
| Falha de comunicação | Média | Alto | Redundância LoRa + modo autônomo |
| Vandalismo/roubo de drone | Média | Alto | Rastreamento GPS, alerta de movimento |
| Colisão com obstáculos | Média | Médio | Sensores redundantes, velocidade limitada |
| Condições climáticas | Alta | Médio | Classificação IP65+, limites de operação |

---

## 10. Dependências

| Dependência | Tipo | PRD relacionado |
|-------------|------|-----------------|
| Sistema de alarme | Integração | PRD_SENSORS_AND_ALARMS_PLATFORM |
| NVR/Frigate | Integração | PRD_VIDEO_SURVEILLANCE_AND_NVR |
| Dashboard | Interface | PRD_MONITORING_DASHBOARD |
| Rede Wi-Fi/LoRa | Infraestrutura | PRD_NETWORK_SECURITY |
| Módulo de defesa | Opcional | PRD_DRONE_DEFENSE_MODULE |

---

## 11. Estimativa de custos

| Configuração | Investimento |
|--------------|--------------|
| **UGV básico (1 unidade)** | R$ 2.500-4.000 |
| **UAV básico (1 unidade)** | R$ 5.000-9.000 |
| **Infraestrutura de comunicação** | R$ 1.000-2.000 |
| **Frota inicial (1 UGV + 1 UAV)** | R$ 8.500-15.000 |

---

## 12. Referências

- `docs/ARQUITETURA_DRONES_AUTONOMOS.md` - Arquitetura completa
- [PX4 Documentation](https://docs.px4.io/)
- [ROS2 Navigation](https://nav2.org/)
- [YOLOv8 Documentation](https://docs.ultralytics.com/)

---

> **Status**: Rascunho v1.0
>
> **Próxima revisão**: Após definição de agente responsável
