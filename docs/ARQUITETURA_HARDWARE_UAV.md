# Arquitetura de Hardware - Drone Aéreo (UAV)

Data: 2026-02-17
Referência: **Tarefa T-032 (TASKS_BACKLOG)**

---

## 1. Visão Geral

Este documento define a arquitetura de hardware para o UAV (Unmanned Aerial Vehicle) do projeto Home Security DIY. O objetivo é construir um quadricóptero autônomo capaz de realizar patrulhas rápidas, verificar perímetro e fornecer visão aérea em caso de alarme.

**Desafio Principal**: Autonomia vs. Peso. O hardware deve ser leve o suficiente para voar por 20+ minutos, mas robusto para carregar o "cérebro" de navegação (NVIDIA Jetson / RPi).

---

## 2. Diagrama de Blocos

```mermaid
graph TD
    subgraph "Power System"
        BAT[Bateria Li-Ion 4S/6S] --> PDB[Power Distribution Board]
        PDB --> |VBAT| ESCs[4-in-1 ESC]
        PDB --> |5V/12V| BEC[Reguladores de Tensão]
        BEC --> |5V| FC[Flight Controller - Pixhawk/Cube]
        BEC --> |5V| COMP[Companion Computer - RPi/Jetson]
    end

    subgraph "Propulsão & Controle"
        FC --> |DShot/PWM| ESCs
        ESCs --> |3-Phase| M1[Motor 1]
        ESCs --> |3-Phase| M2[Motor 2]
        ESCs --> |3-Phase| M3[Motor 3]
        ESCs --> |3-Phase| M4[Motor 4]
        RC[Rádio Controle - RX] --> |SBUS/CRSF| FC
    end

    subgraph "Navegação & Sensores"
        GPS[GPS/RTK + Bússola] --> |CAN/Serial| FC
        LIDAR[LiDAR Baixo Custo - TFMini] --> |I2C/Serial| FC (Altímetro)
        OPTICAL[Optical Flow] --> |Serial| FC (Posição Indoor)
    end

    subgraph "Computação & Visão (Companion)"
        COMP <--> |MAVLink/Serial| FC
        CAM_MAIN[Câmera CSI/USB] --> COMP
        WIFI[Dongle Wi-Fi Alta Potência] --> COMP
    end
```

---

## 3. Especificações de Hardware

### 3.1 Frame e Propulsão
- **Frame**: Fibra de carbono 7-10 polegadas (Long Range).
  - *Sugestão*: Mark4 7-inch ou Quadros estilo "Cinelifter".
- **Motores**: Brushless com baixo KV para eficiência (eficiência > potência).
  - *Exemplo*: 2806.5 1300KV (para 6S) ou 2306 1700KV (para 4S).
- **Hélices**: 7 ou 8 polegadas (bipá ou tripá).
- **ESC**: 4-in-1 45A com firmware BLHeli_32 ou Bluejay.

### 3.2 Controlador de Voo (FC)
O "Cérebro Baixo" que mantém o drone estável.
- **Hardware**: Pixhawk 6C, Cube Orange, ou Holybro Kakute H7 (rodando ArduPilot/PX4).
- **Firmware**: **PX4 Autopilot** (melhor integração com ROS2) ou ArduPilot (mais estável/features prontas).
  - *Decisão*: **PX4** pela compatibilidade nativa com MAVROS/ROS2.

### 3.3 Computador de Bordo (Companion)
O "Cérebro Alto" para visão e autonomia complexa.
- **Opção A (Performance)**: **NVIDIA Jetson Orin Nano**. Processamento de IA nativo (YOLO), mas caro e consome muito.
- **Opção B (Custo/Peso)**: **Raspberry Pi Zero 2 W** (apenas ponte MAVLink) ou **Raspberry Pi 4** (stripped down).
- *Recomendação*: Raspberry Pi Zero 2 W para MVP (telemetria/vídeo leve). Jetson para v2.0.

### 3.4 Sensores de Navegação
1. **GNSS (GPS)**: Módulo M8N ou M10 (Beitian BN-880). RTK opcional mas recomendado para pouso preciso na base de carga.
2. **Altímetro Laser**: TFMini-S ou VL53L1X para manter altura precisa em baixa altitude (voo de patrulha).
3. **Optical Flow**: PMW3901 para manter posição sem GPS (garagem/indoor).

### 3.5 Bateria
- **Tipo**: Li-Ion (VTC6 ou Molicel P42A pack) ao invés de LiPo.
- **Configuração**: 4S2P (8 células) ou 6S1P.
- **Vantagem**: Maior densidade energética para voos longos (20-30 min), descarga menor (não serve para acro/racing).

---

## 4. Lista de Materiais (BOM) Estimada - Versão MVP Long Range

| Componente | Modelo Sugerido | Custo Est. (BRL) |
|------------|-----------------|------------------|
| Frame | Mark4 7-inch Carbon | R$ 250 - 400 |
| Flight Controller | SpeedyBee F405 V3 (Stack) | R$ 350 - 500 |
| ESC | 50A 4-in-1 (no stack) | (Incluso) |
| Motores (x4) | EMAX ECO II 2807 1300KV | R$ 400 - 600 |
| Hélices | HQProp 7x4x3 | R$ 50 - 80 |
| GPS | Beitian BN-880 + Bússola | R$ 100 - 150 |
| Companion | Raspberry Pi Zero 2 W | R$ 150 - 250 |
| Câmera | RPi Camera V3 (CSI) | R$ 180 - 250 |
| Bateria | Li-Ion 4S2P 6000mAh (Custom) | R$ 300 - 500 |
| **TOTAL** | | **R$ 1.780 - 2.730** |

---

## 5. Próximos Passos (Implementação UAV)

1. **Firmware PX4**: Configurar ambiente de build do PX4.
2. **MAVLink Bridge**: Criar serviço no RPi para encaminhar MAVLink via Wi-Fi para o Home Assistant/ROS2.
3. **Integração ROS2**: Configurar `mavros` no Docker (no servidor, não no drone para economizar CPU) para controlar o drone via offboard mode.
