# Drones Autônomos

O módulo de drones é uma **camada reativa avançada** e **completamente opcional**. O sistema Home Security DIY funciona integralmente sem UGV ou UAV.

> **Regulamentação brasileira**: O uso de UAV (drones aéreos) deve seguir ANAC (RBAC-E nº 94) e DECEA (ICA 100-40). A operação autônoma BVLOS (Beyond Visual Line of Sight) requer autorização especial. **Para o MVP, o UGV terrestre é a plataforma recomendada** — sem restrição aeronáutica. Ver análise legal abaixo.

---

## Visão Geral

### Categorias de plataformas

```
┌─────────────────────────────────────────────────────────────────┐
│                     FROTA DE DRONES                             │
├──────────────────┬──────────────────┬───────────────────────────┤
│   TERRESTRES     │     AÉREOS       │       AQUÁTICOS           │
│   (UGV)          │     (UAV)        │       (USV)               │
│                  │                  │                           │
│ • Patrulha       │ • Vigilância     │ • Monitoramento           │
│ • Inspeção       │ • Resposta rápida│ • Lagos/represas          │
│ • Perímetro      │ • Mapeamento     │ • Áreas alagadas          │
│                  │                  │                           │
│ ✅ MVP            │ ⚠️ Restrição     │ 🔮 Futuro                  │
│ Legal sem        │ regulatória      │                           │
│ restrições       │ (ANAC/DECEA)     │                           │
└──────────────────┴──────────────────┴───────────────────────────┘
```

### Princípios do projeto

| Princípio | Descrição |
|-----------|-----------|
| Open Source | Todo software sob MIT, Apache 2.0 ou GPL |
| Open Hardware | Componentes genéricos, especificações abertas |
| Modularidade | Camadas independentes; ~80% do software UGV é reutilizável no UAV |
| Não letalidade | Módulo de defesa prioriza dissuasão sem danos permanentes |
| Privacidade | Processamento local, conformidade com LGPD |

---

## Análise Regulatória — UAV no Brasil

### O conflito VLOS vs. BVLOS

| Aspecto | VLOS (obrigatório) | BVLOS (necessário para patrulha) |
|---------|-------------------|----------------------------------|
| Definição | Piloto mantém contato visual direto | Drone opera fora do alcance visual |
| Regulamentação | Operação padrão (Classe 3) | Requer autorização especial ANAC + DECEA |
| Compatibilidade com patrulha | **Inviável** | Compatível com a arquitetura proposta |

### Decisão: Estratégia em duas fases

```
FASE 1 (MVP): UGV terrestre — totalmente legal
  • Sem restrição da ANAC/DECEA
  • Toda a stack de IA e comunicação se aplica
  • Autonomia de bateria 2–4 horas (vs 20–40 min do UAV)
  • Custo ~50% menor (R$ 2.150–4.100 vs R$ 4.600–9.400)

FASE 2 (Futuro): UAV quando viabilizado legalmente
  • Monitorar evolução do RBAC-E nº 94 da ANAC
  • Consultar advogado aeronáutico antes de operar
  • ~80% do software UGV é reutilizável diretamente
```

### Roadmap legal para UAV

| Etapa | Ação |
|-------|------|
| 1 | Monitorar publicações da ANAC sobre regulamentação BVLOS simplificada |
| 2 | Consultar advogado especialista em direito aeronáutico |
| 3 | Obter registro ANAC e cadastro SISANT antes de qualquer voo outdoor |
| 4 | Desenvolver protótipo em ambiente controlado (indoor ou área restrita) |
| 5 | Solicitar autorização BVLOS com documentação completa de segurança |

---

## Hardware — UGV (Terrestre) — MVP

### Especificações recomendadas

| Componente | Especificação | Opções |
|------------|---------------|--------|
| Chassis | 4WD robótico, ~30–50 cm | Chassis open source |
| Motores | DC brushless com encoder | JGB37-520, ODrive |
| Computador | SBC com GPU | Raspberry Pi 5 8GB, NVIDIA Jetson Nano |
| Câmera principal | Wide angle, visão noturna | Raspberry Pi Camera V3, OAK-D |
| Câmera térmica | LWIR 80×60+ | Flir Lepton, MLX90640 |
| Lidar | 2D | RPLidar A1/A2 |
| GPS | GPS/GLONASS | u-blox NEO-M8N |
| IMU | 9-DOF | MPU9250, BNO055 |
| Bateria | LiPo 4S–6S, 5.000–10.000 mAh | Autonomia: **2–4 horas** |
| Comunicação | Wi-Fi + LoRa | ESP32 + RFM95W |
| **Custo total** | | **R$ 2.150–4.100** |

### Hardware — UAV (Aéreo) — Fase 2

| Componente | Especificação | Opções |
|------------|---------------|--------|
| Frame | Quadcopter 450–550 mm | F450, S500, X500 |
| Motores | Brushless outrunner | 2212-920KV |
| Controlador de voo | Autopilot open source | Pixhawk 6C, Holybro |
| Firmware | Open source | PX4, ArduPilot |
| Computador de missão | Edge computing | NVIDIA Jetson Orin Nano |
| Câmera | 4K gimbal 3-eixos | Câmera + BGC |
| GPS | RTK precisão | HERE3+, ZED-F9P |
| Bateria | LiPo 4S, 5.000–8.000 mAh | Autonomia: **20–40 min** |
| **Custo total** | | **R$ 4.600–9.400** |

---

## Arquitetura de Software

### Stack tecnológico

| Camada | Tecnologia |
|--------|-----------|
| Framework robótico | ROS2 Humble/Iron |
| SO embarcado | Linux (Ubuntu/Debian), FreeRTOS |
| Containerização | Docker, Podman |
| Linguagens | Python (IA, scripts), C++ (ROS2 crítico), Rust (firmware seguro) |
| IA — detecção | YOLOv8n, MobileNet-SSD |
| IA — tracking | DeepSORT, ByteTrack |
| IA — navegação | Nav2, ORB-SLAM3 |
| Comunicação | MQTT, WebRTC, LoRaWAN |

### Arquitetura ROS2 (simplificada)

```
/camera_node ─┐
/lidar_node  ─┼─► /sensor_fusion ─► /perception ─┐
/imu_node    ─┘                  ─► /localization ─┼─► /decision_maker
                                 ─► /mapping      ─┘          │
                                                    ┌──────────┼──────────┐
                                                    ▼          ▼          ▼
                                              /navigation /defense /telemetry
                                                    │          │          │
                                                    ▼          ▼          ▼
                                             /motor_ctrl /actuator  /comm_mgr
```

### Integração com Home Security

| Integração | Protocolo | Dados |
|------------|-----------|-------|
| Home Assistant | MQTT, REST API | Status, comandos, automações |
| Frigate | MQTT, RTSP | Eventos de detecção, streaming |
| Dashboard | WebSocket | Telemetria em tempo real |
| Notificações | MQTT → Telegram/Push | Alertas, eventos |

---

## Comunicação — Redundância em 3 Camadas

```
PRIORIDADE 1: Wi-Fi 5 GHz (baixa latência, streaming)
      │ timeout 3s
      ▼
PRIORIDADE 2: Wi-Fi 2.4 GHz (maior alcance, MQTT)
      │ timeout 5s
      ▼
PRIORIDADE 3: LoRa / Meshtastic (ultra-longo alcance, telemetria crítica)
      │ modo degradado
      ▼
FALLBACK: Modo autônomo (retorno à base ou posição segura)
```

| Canal | Protocolo | Alcance |
|-------|-----------|---------|
| Wi-Fi 5 GHz | TCP/UDP, WebRTC | 100–500 m |
| Wi-Fi 2.4 GHz | MQTT | 200–1.000 m |
| LoRa 915 MHz | LoRaWAN, Meshtastic | 2–15 km |

## Hardening de Runtime (UGV/UAV)

Status atual da implementação:
- logs estruturados em runtime (substituindo `print` operacional);
- rejeição explícita de fallback mock em produção;
- fallback mock permitido apenas em `dev/test` com `DRONES_ALLOW_MOCK_IMPORTS=true`;
- tratamento de erros específicos para MQTT, serial, ROS2 e inferência.

Diretrizes de operação:
- produção deve usar `APP_ENV=production`;
- `ALLOW_UNSIGNED_HOMEASSISTANT_COMMANDS_*` deve permanecer `false`;
- comandos MQTT críticos devem manter assinatura HMAC válida.

---

## Módulo de Defesa Não Letal

> **AVISO LEGAL**: O uso requer conformidade com legislação local (federal, estadual e municipal). O modo automático foi **descontinuado permanentemente**. O modo máximo permitido é o **semi-automático** (humano confirma cada disparo).

### Modos de operação

| Modo | Descrição | Autorização |
|------|-----------|-------------|
| Desativado | Sistema completamente desligado | Nenhuma |
| Standby | Pronto, aguarda autorização manual | Autenticação 2FA |
| **Semi-automático** | IA detecta, humano confirma via app | **Modo máximo** |
| ~~Automático~~ | ~~IA decide e dispara~~ | **Descontinuado** |

### Protocolo de disparo seguro

```
1. AUTENTICAÇÃO  → Token criptografado + certificado do drone
2. AUTORIZAÇÃO   → Confirmação em 2 níveis (sistema + humano via app)
3. AVISO         → Alerta sonoro 3 s + laser de aviso visual
4. DISPARO       → Registro: timestamp, GPS, vídeo ±5/10 s, hash SHA-256
5. PÓS-DISPARO   → Notificação ao proprietário + log imutável
```

### Salvaguardas obrigatórias

| Salvaguarda | Implementação |
|-------------|---------------|
| Bloqueio automático — crianças | Classificação etária por pose + proporções |
| Bloqueio automático — animais | YOLOv8 com classes de animais |
| Cooldown mínimo | 30 s entre disparos (timer hardware) |
| Limite diário | Máximo 3 disparos em 24 h |
| Zona de exclusão | Geofence permanente (calçada, entradas de serviço) |
| Registro audiovisual | Buffer circular 30 s antes + 60 s após |

### Responsabilidade legal

O proprietário é **civil e criminalmente responsável** por todos os danos causados, independente do modo de operação (Código Civil Art. 927, Código Penal Art. 129). **Consulte um advogado antes de instalar ou operar o módulo de defesa.**

---

## IA Embarcada

| Capacidade | Modelo/Técnica | Plataforma |
|------------|----------------|------------|
| Detecção de pessoas | YOLOv8n | Jetson, RPi 5 |
| Detecção de veículos | YOLOv8n | Jetson, RPi 5 |
| Reconhecimento facial | FaceNet, ArcFace | Jetson |
| Tracking de objetos | DeepSORT, ByteTrack | Jetson, RPi 5 |
| Estimativa de pose | MoveNet, MediaPipe | Jetson |
| Navegação autônoma | Nav2 | ROS2 |
| SLAM (mapeamento) | ORB-SLAM3, RTAB-Map | Jetson |

**Latência alvo**: < 100 ms (detecção), < 500 ms (decisão).

---

## Regras Derivadas

```
REGRA-DRONE-01: Drones aéreos >250g devem ser registrados na ANAC.
REGRA-DRONE-02: Voos devem respeitar altitude máxima de 120m e zonas restritas.
REGRA-DRONE-03: Operação noturna requer luzes de navegação visíveis.
REGRA-DRONE-04: Módulo de defesa requer autenticação 2FA para armamento.
REGRA-DRONE-05: Todo disparo deve ser registrado com vídeo, GPS e timestamp.
REGRA-DRONE-06: Drones devem ter fail-safe (retorno à base) em perda de sinal.
REGRA-DRONE-07: Firmware deve ser assinado digitalmente.
REGRA-DRONE-08: Comunicação deve usar criptografia end-to-end.
REGRA-DRONE-09: Vídeo armazenado localmente — nunca em nuvem.
REGRA-DRONE-10: Whitelist de pessoas autorizadas deve ser configurável.
```

---

## MVP — O que está no escopo imediato

1. Drone terrestre (UGV) com câmera
2. Detecção básica de pessoas (YOLO)
3. Comunicação Wi-Fi com Home Assistant via MQTT
4. Dashboard de telemetria em tempo real
5. Alertas via Telegram

### Estado atual dos comandos UGV (MVP)

- `move`: implementado
- `defense_arm` / `defense_disarm`: implementados com validações de saúde
- `patrol`: **ainda não implementado**; o controlador publica status explícito `not_implemented` no tópico `ugv/status` para evitar falso positivo operacional
- Bootstrap MQTT: o monitor de saúde tem heartbeat resetado imediatamente após `client.connect()` para evitar alerta espúrio de timeout no primeiro ciclo

---

## Referências

- `docs/ARQUITETURA_DRONES_AUTONOMOS.md` — fonte principal desta página
- `docs/ARQUITETURA_HARDWARE_UGV.md` — especificações detalhadas do UGV
- `docs/ARQUITETURA_HARDWARE_UAV.md` — especificações detalhadas do UAV
- `docs/DRONES_MOCK_TO_HARDWARE_RUNBOOK.md` — transição segura de mock para hardware real
- `docs/ARQUITETURA_DRONES_AUTONOMOS.md` — inclui status de execução das tasks T-031 a T-045
- `docs/LEGAL_AND_ETHICS.md` — aspectos legais e éticos
- `prd/PRD_AUTONOMOUS_DRONES.md` — requisitos detalhados
- [PX4 Autopilot](https://px4.io/) | [ROS2](https://docs.ros.org/) | [Nav2](https://nav2.org/)
