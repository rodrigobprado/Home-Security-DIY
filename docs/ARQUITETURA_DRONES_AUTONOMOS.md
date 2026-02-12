# Arquitetura de Drones Autônomos Modulares

> Sistema de Home Security – Open Source / Open Hardware
>
> Módulo Reativo Avançado
>
> Versão: 1.0 | Data: 2026-02-12

---

## 1. Visão Geral

### 1.1 Objetivo

Desenvolver um ecossistema open source/open hardware de **drones autônomos modulares** com IA embarcada, comunicação redundante e capacidade de operação independente para vigilância, segurança, inspeção e monitoramento ambiental.

### 1.2 Princípios do projeto

| Princípio | Descrição |
|-----------|-----------|
| **Open Source** | Todo software sob licenças abertas (MIT, Apache 2.0, GPL) |
| **Open Hardware** | Especificações abertas, componentes genéricos, fabricação própria possível |
| **Modularidade** | Hardware e software em camadas independentes e intercambiáveis |
| **Autonomia** | Capacidade de operação sem intervenção humana constante |
| **Segurança** | Protocolos de autenticação, criptografia e auditoria |
| **Não letalidade** | Módulos de defesa priorizando dissuasão sem danos permanentes |
| **Privacidade** | Processamento local, conformidade com LGPD |

### 1.3 Categorias de drones

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     FROTA DE DRONES AUTÔNOMOS                           │
├─────────────────────┬─────────────────────┬─────────────────────────────┤
│    TERRESTRES       │      AÉREOS         │        PLUVIAIS             │
│                     │                     │                             │
│  ┌─────────────┐    │  ┌─────────────┐    │  ┌─────────────┐           │
│  │   Rodas     │    │  │ Multirrotor │    │  │  Barco RC   │           │
│  │   (UGV)     │    │  │   (UAV)     │    │  │  (USV)      │           │
│  └─────────────┘    │  └─────────────┘    │  └─────────────┘           │
│                     │                     │                             │
│  ┌─────────────┐    │  ┌─────────────┐    │  ┌─────────────┐           │
│  │  Esteiras   │    │  │  Asa fixa   │    │  │  Anfíbio    │           │
│  │   (UGV)     │    │  │   (UAV)     │    │  │  (UGV+USV)  │           │
│  └─────────────┘    │  └─────────────┘    │  └─────────────┘           │
│                     │                     │                             │
│  Aplicação:         │  Aplicação:         │  Aplicação:                │
│  - Patrulha         │  - Vigilância       │  - Monitoramento           │
│  - Inspeção         │  - Resposta rápida  │  - Áreas alagadas          │
│  - Perímetro        │  - Mapeamento       │  - Lagos/represas          │
└─────────────────────┴─────────────────────┴─────────────────────────────┘
```

---

## 2. Arquitetura de Hardware

### 2.1 Diagrama de camadas

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        CAMADA DE MISSÃO                                 │
│   Câmeras, microfones, alto-falantes, módulo de defesa, sensores        │
├─────────────────────────────────────────────────────────────────────────┤
│                        CAMADA DE IA                                     │
│   NVIDIA Jetson / Raspberry Pi 5 / ESP32-S3                             │
│   Visão computacional, reconhecimento, decisão autônoma                 │
├─────────────────────────────────────────────────────────────────────────┤
│                        CAMADA DE CONTROLE                               │
│   Controlador de voo (PX4/ArduPilot) / Controlador de movimento         │
│   IMU, GPS/RTK, barômetro, magnetômetro                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                        CAMADA DE COMUNICAÇÃO                            │
│   Wi-Fi (principal) + LoRa/Meshtastic (redundância)                     │
│   Módulos de rádio, antenas, protocolos seguros                         │
├─────────────────────────────────────────────────────────────────────────┤
│                        CAMADA DE ENERGIA                                │
│   Baterias LiPo/Li-Ion, BMS, carregamento, monitoramento                │
├─────────────────────────────────────────────────────────────────────────┤
│                        CAMADA MECÂNICA                                  │
│   Chassis, motores, ESCs, hélices/rodas/esteiras, estrutura             │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Especificações por tipo de drone

#### 2.2.1 Drone Terrestre (UGV - Unmanned Ground Vehicle)

| Componente | Especificação | Opções recomendadas |
|------------|---------------|---------------------|
| **Chassis** | 4WD ou esteiras, ~30-50cm | Chassis robótico open source |
| **Motores** | DC brushless com encoder | JGB37-520, N20 com encoder |
| **Controlador de motor** | Ponte H ou ESC | L298N, BTS7960, ODrive |
| **Computador principal** | SBC com GPU | Raspberry Pi 5, NVIDIA Jetson Nano |
| **Câmera principal** | Wide angle, visão noturna | Raspberry Pi Camera V3, OAK-D |
| **Câmera térmica** | LWIR 80x60 ou superior | Flir Lepton, MLX90640 |
| **Lidar** | 2D ou 3D | RPLidar A1/A2, Intel RealSense |
| **Ultrassônico** | Detecção de obstáculos | HC-SR04, TF-Luna |
| **GPS** | GPS/GLONASS, RTK opcional | u-blox NEO-M8N, ZED-F9P |
| **IMU** | 9-DOF | MPU9250, BNO055 |
| **Bateria** | LiPo 4S-6S, 5000-10000mAh | Autonomia: 2-4 horas |
| **Comunicação** | Wi-Fi + LoRa | ESP32, RFM95W |

#### 2.2.2 Drone Aéreo (UAV - Unmanned Aerial Vehicle)

| Componente | Especificação | Opções recomendadas |
|------------|---------------|---------------------|
| **Frame** | Quadcopter/Hexacopter, 450-550mm | F450, S500, X500 |
| **Motores** | Brushless outrunner | 2212-920KV, 2216-880KV |
| **ESCs** | 30A BLHeli_32 | Hobbywing, T-Motor |
| **Controlador de voo** | Autopilot open source | Pixhawk 6C, CUAV V5+, Holybro |
| **Firmware** | Open source | PX4, ArduPilot |
| **Computador de missão** | Edge computing | NVIDIA Jetson Orin Nano, Raspberry Pi 5 |
| **Câmera gimbal** | 3-axis estabilizado | Câmera 4K + gimbal BGC |
| **Câmera térmica** | LWIR | Flir Boson, DJI Zenmuse XT |
| **GPS** | RTK para precisão | HERE3+, ZED-F9P |
| **Telemetria** | Longo alcance | SiK Radio 915MHz, RFD900 |
| **Bateria** | LiPo 4S-6S, 5000-8000mAh | Autonomia: 20-40 min |

#### 2.2.3 Drone Pluvial (USV - Unmanned Surface Vehicle)

| Componente | Especificação | Opções recomendadas |
|------------|---------------|---------------------|
| **Casco** | Catamarã ou monocasco, ~60-100cm | Impressão 3D ou fibra |
| **Propulsão** | Motor brushless marítimo | Turnigy Aquastar, Blue Robotics T200 |
| **ESC** | À prova d'água | Hobbywing SeaKing |
| **Controlador** | Autopilot ou SBC | ArduRover, Raspberry Pi |
| **Câmera** | À prova d'água | GoPro ou câmera IP66+ |
| **Sonar** | Profundidade | Ping Sonar, Lowrance |
| **GPS** | Com antena elevada | u-blox com haste |
| **Bateria** | LiPo selada | Autonomia: 2-6 horas |

### 2.3 Módulos comuns

#### 2.3.1 Módulo de câmera e visão

| Sensor | Resolução | FPS | Aplicação |
|--------|-----------|-----|-----------|
| **Raspberry Pi Camera V3** | 12MP | 30-120 | Visão diurna |
| **Pi NoIR Camera** | 8MP | 30 | Visão noturna (com IR) |
| **OAK-D** | 4K + Depth | 30 | Visão estéreo + IA |
| **Flir Lepton 3.5** | 160x120 | 9 | Térmica |
| **IMX477** | 12.3MP | 30 | Alta qualidade |

#### 2.3.2 Módulo de áudio

| Componente | Especificação |
|------------|---------------|
| **Microfone** | MEMS array, I2S (SPH0645, INMP441) |
| **Alto-falante** | 3-5W, driver I2S (MAX98357A) |
| **Processamento** | VAD, cancelamento de ruído |
| **Uso** | Comunicação bidirecional, alertas sonoros |

#### 2.3.3 Módulo GPS/RTK

| Modo | Precisão | Aplicação |
|------|----------|-----------|
| **GPS padrão** | ±2-5m | Navegação geral |
| **DGPS** | ±0.5-1m | Navegação melhorada |
| **RTK** | ±2cm | Navegação de precisão |

---

## 3. Sistema de Defesa Não Letal

### 3.1 Especificação do módulo reativo

> **AVISO LEGAL**: O uso deste módulo deve estar em conformidade com todas as legislações locais, estaduais e federais aplicáveis. O sistema é projetado exclusivamente para defesa não letal e dissuasão.

#### 3.1.1 Componentes

| Componente | Especificação | Função |
|------------|---------------|--------|
| **Cilindro CO₂** | 12g ou 88g, descartável/recarregável | Propelente |
| **Câmara de disparo** | Alumínio anodizado, válvula solenóide | Mecanismo de disparo |
| **Munição** | Cápsulas de OC (pimenta) + gengibre | Agente dissuasório |
| **Mira** | Laser classe 2 + câmera | Alinhamento e registro |
| **Controlador** | Microcontrolador dedicado | Segurança e autenticação |

#### 3.1.2 Especificações técnicas

| Parâmetro | Valor |
|-----------|-------|
| **Alcance efetivo** | 3-10 metros |
| **Capacidade** | 5-10 disparos por cilindro |
| **Tempo de recarga** | Manual (troca de cilindro) |
| **Pressão de trabalho** | 50-60 bar |
| **Temperatura de operação** | 0°C a 45°C |

#### 3.1.3 Protocolos de segurança

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    PROTOCOLO DE DISPARO SEGURO                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  1. AUTENTICAÇÃO                                                        │
│     └── Token criptografado + certificado do drone + timestamp          │
│                                                                         │
│  2. AUTORIZAÇÃO                                                         │
│     └── Verificação em 2 níveis:                                        │
│         ├── Sistema central (Home Security)                             │
│         └── IA embarcada (confirmação de ameaça)                        │
│                                                                         │
│  3. CONFIRMAÇÃO                                                         │
│     └── Aviso sonoro prévio (3 segundos)                                │
│     └── Sinal visual (laser de aviso)                                   │
│                                                                         │
│  4. DISPARO                                                             │
│     └── Registro completo:                                              │
│         ├── Timestamp (NTP sincronizado)                                │
│         ├── Coordenadas GPS                                             │
│         ├── Vídeo 5s antes + 10s depois                                 │
│         ├── Identificação do alvo (se disponível)                       │
│         └── Hash SHA-256 do registro                                    │
│                                                                         │
│  5. PÓS-DISPARO                                                         │
│     └── Notificação imediata ao proprietário                            │
│     └── Alerta ao sistema central                                       │
│     └── Log imutável em blockchain local (opcional)                     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

#### 3.1.4 Modos de operação

| Modo | Descrição | Autorização necessária |
|------|-----------|------------------------|
| **Desativado** | Sistema de defesa completamente desligado | Nenhuma |
| **Standby** | Pronto, mas requer autorização manual | Autenticação 2FA |
| **Semi-automático** | IA detecta, humano autoriza | Confirmação via app |
| **Automático** | IA detecta e dispara autonomamente | Modo de emergência, logs extensivos |

> **RECOMENDAÇÃO**: O modo automático deve ser usado apenas em situações extremas e onde legalmente permitido.

---

## 4. Arquitetura de Software

### 4.1 Stack tecnológico

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         CAMADA DE APLICAÇÃO                             │
│   Dashboard Web │ App Mobile │ API REST │ Integração Home Assistant     │
├─────────────────────────────────────────────────────────────────────────┤
│                         CAMADA DE SERVIÇOS                              │
│   Planejamento │ Coordenação │ Telemetria │ Streaming │ Notificações   │
├─────────────────────────────────────────────────────────────────────────┤
│                         CAMADA DE IA                                    │
│   Visão computacional │ Detecção │ Tracking │ Decisão │ Navegação      │
├─────────────────────────────────────────────────────────────────────────┤
│                         CAMADA DE MIDDLEWARE                            │
│   ROS2 │ MQTT Broker │ Message Queue │ Estado distribuído              │
├─────────────────────────────────────────────────────────────────────────┤
│                         CAMADA DE FIRMWARE                              │
│   Controladores │ Drivers │ HAL │ RTOS                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                         CAMADA DE HARDWARE                              │
│   Sensores │ Atuadores │ Comunicação │ Energia                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Componentes de software

#### 4.2.1 Sistema operacional e framework

| Componente | Tecnologia | Plataforma |
|------------|------------|------------|
| **SO embarcado** | Linux (Ubuntu/Debian), FreeRTOS | Jetson, RPi, ESP32 |
| **Framework robótico** | ROS2 Humble/Iron | Todos |
| **Containerização** | Docker, Podman | Jetson, RPi |
| **Orquestração** | Docker Compose, K3s | Estação base |

#### 4.2.2 Linguagens de programação

| Linguagem | Uso |
|-----------|-----|
| **Python** | IA, visão computacional, scripts, integração |
| **C++** | Nós ROS2 de alto desempenho, drivers |
| **Rust** | Firmware seguro, componentes críticos |
| **C** | Drivers de baixo nível, microcontroladores |

#### 4.2.3 Bibliotecas e frameworks de IA

| Biblioteca | Uso |
|------------|-----|
| **OpenCV** | Processamento de imagem |
| **TensorFlow Lite** | Inferência em edge |
| **PyTorch Mobile** | Modelos customizados |
| **OpenVINO** | Aceleração Intel |
| **ONNX Runtime** | Interoperabilidade de modelos |
| **YOLOv8** | Detecção de objetos |
| **MiDaS** | Estimativa de profundidade |

### 4.3 Arquitetura ROS2

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           SISTEMA ROS2                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐                   │
│  │  /camera    │   │  /lidar     │   │  /imu       │                   │
│  │  _node      │   │  _node      │   │  _node      │                   │
│  └──────┬──────┘   └──────┬──────┘   └──────┬──────┘                   │
│         │                 │                 │                           │
│         ▼                 ▼                 ▼                           │
│  ┌─────────────────────────────────────────────────────────────┐       │
│  │                    /sensor_fusion                           │       │
│  │                    Fusão de dados sensoriais                │       │
│  └─────────────────────────┬───────────────────────────────────┘       │
│                            │                                            │
│         ┌──────────────────┼──────────────────┐                        │
│         ▼                  ▼                  ▼                        │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐                   │
│  │ /perception │   │ /localization│  │  /mapping   │                   │
│  │ Detecção IA │   │  SLAM/GPS   │   │  Mapeamento │                   │
│  └──────┬──────┘   └──────┬──────┘   └──────┬──────┘                   │
│         │                 │                 │                           │
│         ▼                 ▼                 ▼                           │
│  ┌─────────────────────────────────────────────────────────────┐       │
│  │                    /decision_maker                          │       │
│  │              Planejamento e tomada de decisão               │       │
│  └─────────────────────────┬───────────────────────────────────┘       │
│                            │                                            │
│         ┌──────────────────┼──────────────────┐                        │
│         ▼                  ▼                  ▼                        │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐                   │
│  │ /navigation │   │  /defense   │   │ /telemetry  │                   │
│  │ Nav2 Stack  │   │  _module    │   │  _bridge    │                   │
│  └──────┬──────┘   └──────┬──────┘   └──────┬──────┘                   │
│         │                 │                 │                           │
│         ▼                 ▼                 ▼                           │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐                   │
│  │ /motor      │   │ /actuator   │   │ /comm       │                   │
│  │ _controller │   │ _controller │   │ _manager    │                   │
│  └─────────────┘   └─────────────┘   └─────────────┘                   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 4.4 Tópicos e serviços principais

| Tópico/Serviço | Tipo | Descrição |
|----------------|------|-----------|
| `/camera/image_raw` | sensor_msgs/Image | Stream de câmera |
| `/camera/thermal` | sensor_msgs/Image | Imagem térmica |
| `/lidar/scan` | sensor_msgs/LaserScan | Varredura 2D |
| `/imu/data` | sensor_msgs/Imu | Dados de IMU |
| `/gps/fix` | sensor_msgs/NavSatFix | Posição GPS |
| `/perception/detections` | vision_msgs/Detection2DArray | Objetos detectados |
| `/cmd_vel` | geometry_msgs/Twist | Comandos de velocidade |
| `/defense/arm` | std_srvs/SetBool | Armar/desarmar defesa |
| `/defense/fire` | custom_msgs/FireCommand | Comando de disparo |
| `/telemetry/status` | custom_msgs/DroneStatus | Status completo |

---

## 5. Arquitetura de Comunicação

### 5.1 Diagrama de rede

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         ESTAÇÃO BASE                                    │
│   ┌─────────────────────────────────────────────────────────────┐      │
│   │                  HOME SECURITY SYSTEM                        │      │
│   │   Home Assistant + Frigate + NVR + Dashboard de drones      │      │
│   └─────────────────────────────────────────────────────────────┘      │
│                              │                                          │
│              ┌───────────────┼───────────────┐                         │
│              │               │               │                         │
│         ┌────▼────┐    ┌─────▼─────┐   ┌─────▼─────┐                  │
│         │ Wi-Fi   │    │  LoRa     │   │ Meshtastic│                  │
│         │ AP/Mesh │    │  Gateway  │   │  Gateway  │                  │
│         │ 5GHz    │    │  915MHz   │   │  915MHz   │                  │
│         └────┬────┘    └─────┬─────┘   └─────┬─────┘                  │
│              │               │               │                         │
└──────────────┼───────────────┼───────────────┼─────────────────────────┘
               │               │               │
               │      ÁREA DE COBERTURA        │
               │               │               │
     ┌─────────┴───────────────┴───────────────┴─────────┐
     │                                                    │
     │  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
     │  │  DRONE   │  │  DRONE   │  │  DRONE   │        │
     │  │ TERRESTRE│  │  AÉREO   │  │ PLUVIAL  │        │
     │  │          │  │          │  │          │        │
     │  │ Wi-Fi    │  │ Wi-Fi    │  │ Wi-Fi    │        │
     │  │ + LoRa   │  │ + LoRa   │  │ + LoRa   │        │
     │  └──────────┘  └──────────┘  └──────────┘        │
     │                                                    │
     └────────────────────────────────────────────────────┘
```

### 5.2 Protocolos de comunicação

| Canal | Protocolo | Uso | Alcance |
|-------|-----------|-----|---------|
| **Wi-Fi 5GHz** | TCP/UDP, WebRTC | Streaming de vídeo, comandos rápidos | 100-500m |
| **Wi-Fi 2.4GHz** | MQTT | Telemetria, comandos | 200-1000m |
| **LoRa** | LoRaWAN, Meshtastic | Telemetria crítica, fallback | 2-15km |
| **Bluetooth** | BLE 5.0 | Configuração, diagnóstico local | 50m |

### 5.3 Redundância e failover

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    MATRIZ DE REDUNDÂNCIA                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  PRIORIDADE 1: Wi-Fi 5GHz (baixa latência)                             │
│       │                                                                 │
│       ├── Falha detectada (timeout 3s)                                 │
│       │                                                                 │
│       ▼                                                                 │
│  PRIORIDADE 2: Wi-Fi 2.4GHz (maior alcance)                            │
│       │                                                                 │
│       ├── Falha detectada (timeout 5s)                                 │
│       │                                                                 │
│       ▼                                                                 │
│  PRIORIDADE 3: LoRa/Meshtastic (ultra-longo alcance)                   │
│       │                                                                 │
│       ├── Modo degradado: apenas telemetria e comandos críticos        │
│       │                                                                 │
│       ▼                                                                 │
│  FALLBACK: Modo autônomo (retorno à base ou posição segura)            │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 5.4 Integração com Home Security

| Integração | Protocolo | Dados |
|------------|-----------|-------|
| **Home Assistant** | MQTT, REST API | Status, comandos, automações |
| **Frigate** | MQTT, RTSP | Eventos de detecção, streaming |
| **Dashboard** | WebSocket | Telemetria em tempo real |
| **Notificações** | MQTT → Telegram/Push | Alertas, eventos, disparos |

---

## 6. IA Embarcada

### 6.1 Capacidades de IA

| Capacidade | Modelo/Técnica | Plataforma |
|------------|----------------|------------|
| **Detecção de pessoas** | YOLOv8n, MobileNet-SSD | Jetson, RPi5 |
| **Detecção de veículos** | YOLOv8n | Jetson, RPi5 |
| **Reconhecimento facial** | FaceNet, ArcFace | Jetson |
| **Tracking de objetos** | DeepSORT, ByteTrack | Jetson, RPi5 |
| **Estimativa de pose** | MoveNet, MediaPipe | Jetson |
| **Detecção de anomalias** | Autoencoder, Isolation Forest | Todos |
| **Navegação autônoma** | Nav2, comportamentos reativos | ROS2 |
| **SLAM** | ORB-SLAM3, RTAB-Map | Jetson |

### 6.2 Pipeline de visão computacional

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    PIPELINE DE VISÃO COMPUTACIONAL                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐            │
│  │ Captura  │──►│ Pré-proc │──►│ Inferência│──►│ Pós-proc │            │
│  │ Imagem   │   │ (resize, │   │ (YOLO,    │   │ (NMS,    │            │
│  │ 30 FPS   │   │ normalize│   │ tracking) │   │ filter)  │            │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘            │
│                                                       │                 │
│                                                       ▼                 │
│                                              ┌──────────────┐          │
│                                              │  Decisão     │          │
│                                              │  - Alerta    │          │
│                                              │  - Seguir    │          │
│                                              │  - Defesa    │          │
│                                              └──────────────┘          │
│                                                                         │
│  Latência alvo: < 100ms (detecção) < 500ms (decisão)                   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 6.3 Árvore de decisão autônoma

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    ÁRVORE DE DECISÃO AUTÔNOMA                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│                         ┌─────────────┐                                │
│                         │  Detecção   │                                │
│                         │  de pessoa  │                                │
│                         └──────┬──────┘                                │
│                                │                                        │
│                    ┌───────────┴───────────┐                           │
│                    │                       │                           │
│              ┌─────▼─────┐           ┌─────▼─────┐                     │
│              │ Conhecido │           │Desconhecido│                    │
│              │(whitelist)│           │           │                     │
│              └─────┬─────┘           └─────┬─────┘                     │
│                    │                       │                           │
│              ┌─────▼─────┐           ┌─────▼─────┐                     │
│              │  Ignorar  │           │  Seguir   │                     │
│              │  ou Log   │           │  e alertar│                     │
│              └───────────┘           └─────┬─────┘                     │
│                                            │                           │
│                              ┌─────────────┴─────────────┐             │
│                              │                           │             │
│                        ┌─────▼─────┐               ┌─────▼─────┐       │
│                        │Comportam. │               │Comportam. │       │
│                        │ Normal    │               │ Suspeito  │       │
│                        └─────┬─────┘               └─────┬─────┘       │
│                              │                           │             │
│                        ┌─────▼─────┐               ┌─────▼─────┐       │
│                        │ Monitorar │               │  Escalar  │       │
│                        │           │               │  alerta   │       │
│                        └───────────┘               └─────┬─────┘       │
│                                                          │             │
│                                            ┌─────────────┴──────┐      │
│                                            │                    │      │
│                                      ┌─────▼─────┐        ┌─────▼─────┐│
│                                      │ Aviso     │        │ Invasão  ││
│                                      │ sonoro    │        │ confirmada││
│                                      └───────────┘        └─────┬─────┘│
│                                                                 │      │
│                                                           ┌─────▼─────┐│
│                                                           │  Defesa   ││
│                                                           │(se autoriz)││
│                                                           └───────────┘│
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Segurança e Compliance

### 7.1 Requisitos de segurança

| Categoria | Requisito |
|-----------|-----------|
| **Autenticação** | TLS 1.3, certificados mTLS, tokens JWT |
| **Criptografia** | AES-256-GCM para dados, ChaCha20 para telemetria |
| **Integridade** | Assinatura de firmware, verificação de boot |
| **Auditoria** | Logs imutáveis, timestamps NTP, hash chain |
| **Privacidade** | Processamento local, dados criptografados em repouso |

### 7.2 Conformidade legal

| Aspecto | Requisito | Referência |
|---------|-----------|------------|
| **LGPD** | Processamento local, sem envio para nuvem | Lei 13.709/2018 |
| **Uso de drones** | Registro na ANAC para drones >250g | RBAC-E nº 94 |
| **Espaço aéreo** | Respeitar zonas restritas | DECEA |
| **Armas não letais** | Verificar legislação estadual | Varia por estado |
| **Gravação de vídeo** | Não capturar áreas públicas/vizinhos | LGPD |

### 7.3 Regras derivadas

```
REGRA-DRONE-01: Drones aéreos >250g devem ser registrados na ANAC.

REGRA-DRONE-02: Voos devem respeitar altitude máxima de 120m e zonas restritas.

REGRA-DRONE-03: Operação noturna requer luzes de navegação visíveis.

REGRA-DRONE-04: Módulo de defesa requer autenticação de 2 fatores para armamento.

REGRA-DRONE-05: Todo disparo deve ser registrado com vídeo, GPS e timestamp.

REGRA-DRONE-06: Drones devem ter modo fail-safe (retorno à base) em perda de sinal.

REGRA-DRONE-07: Firmware deve ser assinado digitalmente para evitar adulteração.

REGRA-DRONE-08: Comunicação deve usar criptografia end-to-end.

REGRA-DRONE-09: Dados de vídeo devem ser armazenados localmente, nunca em nuvem.

REGRA-DRONE-10: Whitelist de pessoas autorizadas deve ser configurável.
```

---

## 8. Estimativa de Custos

### 8.1 Drone terrestre (UGV)

| Componente | Custo estimado |
|------------|----------------|
| Chassis 4WD | R$ 200-400 |
| Motores + drivers | R$ 150-300 |
| Raspberry Pi 5 8GB | R$ 500-700 |
| Câmera + térmica | R$ 300-800 |
| Lidar RPLidar A1 | R$ 400-600 |
| GPS + IMU | R$ 200-400 |
| Bateria + BMS | R$ 200-400 |
| Estrutura + impressão 3D | R$ 100-300 |
| Comunicação (ESP32 + LoRa) | R$ 100-200 |
| **Total** | **R$ 2.150-4.100** |

### 8.2 Drone aéreo (UAV)

| Componente | Custo estimado |
|------------|----------------|
| Frame + motores + ESCs | R$ 600-1.200 |
| Controlador Pixhawk | R$ 600-1.500 |
| NVIDIA Jetson Orin Nano | R$ 2.000-3.000 |
| Câmera + gimbal | R$ 500-1.500 |
| GPS RTK | R$ 400-1.200 |
| Bateria 4S 5000mAh (x2) | R$ 300-600 |
| Telemetria + LoRa | R$ 200-400 |
| **Total** | **R$ 4.600-9.400** |

### 8.3 Drone pluvial (USV)

| Componente | Custo estimado |
|------------|----------------|
| Casco (impressão 3D ou fibra) | R$ 300-800 |
| Motor + ESC marítimo | R$ 300-600 |
| Raspberry Pi 5 | R$ 500-700 |
| Câmera IP66 | R$ 200-500 |
| GPS + sonar | R$ 300-600 |
| Bateria selada | R$ 200-400 |
| **Total** | **R$ 1.800-3.600** |

### 8.4 Infraestrutura de comunicação

| Componente | Custo estimado |
|------------|----------------|
| AP Wi-Fi longo alcance | R$ 300-800 |
| Gateway LoRa | R$ 200-500 |
| Nós Meshtastic (x3) | R$ 150-300 |
| Antenas externas | R$ 100-300 |
| **Total** | **R$ 750-1.900** |

---

## 9. Roadmap de Desenvolvimento

### 9.1 Fases do projeto

| Fase | Duração | Entregas |
|------|---------|----------|
| **Fase 1: Fundação** | - | Arquitetura, documentação, seleção de hardware |
| **Fase 2: Prototipagem** | - | Drone terrestre básico, comunicação Wi-Fi |
| **Fase 3: IA básica** | - | Detecção de pessoas, navegação autônoma |
| **Fase 4: Integração** | - | Integração com Home Security |
| **Fase 5: Comunicação** | - | Rede LoRa/Meshtastic redundante |
| **Fase 6: Defesa** | - | Módulo reativo (onde legalmente permitido) |
| **Fase 7: Frota** | - | Coordenação multi-drone |
| **Fase 8: Aéreo** | - | Drone aéreo com VTOL |

### 9.2 MVP (Minimum Viable Product)

O MVP consiste em:
1. Um drone terrestre com câmera
2. Detecção básica de pessoas (YOLO)
3. Comunicação Wi-Fi com Home Assistant
4. Dashboard de telemetria
5. Alertas via Telegram

---

## 10. Referências

### Projetos open source relacionados

- [PX4 Autopilot](https://px4.io/)
- [ArduPilot](https://ardupilot.org/)
- [ROS2](https://docs.ros.org/)
- [Meshtastic](https://meshtastic.org/)
- [OpenCV](https://opencv.org/)
- [YOLOv8](https://docs.ultralytics.com/)
- [Nav2](https://nav2.org/)

### Hardware open source

- [Open Source Rover (NASA JPL)](https://github.com/nasa-jpl/open-source-rover)
- [Duckietown](https://www.duckietown.org/)
- [OpenPilot](https://github.com/commaai/openpilot)

### Documentação adicional

- `prd/PRD_AUTONOMOUS_DRONES.md` - PRD detalhado
- `prd/PRD_DRONE_DEFENSE_MODULE.md` - Módulo de defesa
- `prd/PRD_DRONE_COMMUNICATION.md` - Rede de comunicação

---

> **Status**: Documento de arquitetura v1.0
>
> **Próximos passos**: Criar PRDs detalhados, definir tarefas de implementação
>
> **Aviso legal**: O desenvolvimento e uso de drones e módulos de defesa devem seguir todas as regulamentações locais aplicáveis.
