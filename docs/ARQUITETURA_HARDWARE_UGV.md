# Arquitetura de Hardware - Drone Terrestre (UGV)

Data: 2026-02-17
Referência: **Tarefa T-031 (TASKS_BACKLOG)**

---

## 1. Visão Geral

Este documento define a arquitetura de hardware para o UGV (Unmanned Ground Vehicle) do projeto Home Security DIY. O objetivo é construir um robô móvel capaz de navegar autonomamente em ambientes externos (quintal, jardim), com capacidade de superar pequenos obstáculos, transmitir vídeo e executar patrulhas.

O design prioriza **custo-benefício**, **modularidade** e **facilidade de reparo**.

---

## 2. Diagrama de Blocos

```mermaid
graph TD
    subgraph "Power System"
        BAT[Bateria Li-Ion 3S/4S] --> PMS[Power Management Board]
        PMS --> |12V| MOTORS[Drivers de Motor]
        PMS --> |5V| SBC[Computador de Bordo - RPi4/5]
        PMS --> |5V/3.3V| MCU[Microcontrolador - ESP32]
    end

    subgraph "Computação & Controle"
        SBC <--> |Serial/USB| MCU
        SBC --> |CSI/USB| CAM_MAIN[Câmera Principal - Nav/Detecção]
        SBC --> |USB| CAM_DEPTH[Câmera de Profundidade/Lidar]
        MCU --> |PWM| MOTOR_L[Motor Esquerdo]
        MCU --> |PWM| MOTOR_R[Motor Direito]
        MCU <-- |Encoder| ENC_L[Encoder Esquerdo]
        MCU <-- |Encoder| ENC_R[Encoder Direito]
    end

    subgraph "Sensores & Periféricos"
        MCU <-- |I2C| IMU[IMU - Acelerômetro/Giroscópio]
        MCU <-- |ADC| BAT_SENSE[Sensor de Tensão]
        SBC --> |USB| GPS[GPS/GNSS (Opcional)]
        SBC --> |USB/SPI| LORA[Módulo LoRa (Backup Link)]
        SBC --> |Audio Out| SPEAKER[Alto-falante]
    end
```

---

## 3. Especificações de Hardware

### 3.1 Chassis e Locomoção
- **Tipo**: Diferencial (Skid-steer) ou Ackermann (Direção).
- **Escolha**: **Diferencial (Tank/Skid-steer)** pela simplicidade mecânica e capacidade de giro em torno do próprio eixo (zero turn radius).
- **Rodas**: 4 ou 6 rodas off-road grandes (120mm+) ou esteiras para terrenos irregulares (grama, terra).
- **Motores**: 2x ou 4x Motores DC com caixa de redução (Geared Motors). Torque priorizado sobre velocidade.
  - *Sugestão*: Motores de vidro elétrico de carro (baixo custo, alto torque) ou motores planetários 12V.

### 3.2 Computação (Cérebro)
Sistema híbrido com "Cérebro Alto" (Navegação/IA) e "Cérebro Baixo" (Controle de Hardware).

| Nível | Componente Recomendado | Função |
|-------|------------------------|--------|
| **High-Level** | Raspberry Pi 4 (4GB+) ou 5 | Rodar ROS2, Nav2, Visão Computacional, Streaming de Vídeo, Wi-Fi. |
| **Low-Level** | **ESP32** (DevKit V1) | Gerar PWM para motores, ler encoders, ler IMU, monitorar bateria, safety watchdog. |

### 3.3 Sensores

1. **Visão (Navegação/Detecção)**:
   - Câmera USB Grande Angular (160° FOV) ou Raspberry Pi Camera Module 3.
   - *Opcional*: Intel RealSense ou OAK-D Lite para navegação estéreo (profundidade).
2. **LiDAR (Mapeamento 2D)**:
   - **RPLidar A1** ou LD19. Custo acessível e suportado nativamente pelo ROS2 Nav2. Essencial para SLAM.
3. **IMU (Odometria)**:
   - **MPU6050** ou BNO055 (melhor, com fusão interna). Conectado ao ESP32.
4. **Odometria de Rodas**:
   - Encoders magnéticos de efeito Hall nos motores.

### 3.4 Sistema de Energia

- **Bateria**: Pack Li-Ion 3S (11.1V / 12.6V) ou 4S (14.8V). 5000mAh a 10000mAh.
- **BMS**: Placa de proteção obrigatória para carga/descarga.
- **Reguladores**:
  - DC-DC Step-Down (Buck) 12V -> 5V 5A (para Raspberry Pi).
  - DC-DC para Motores (direto da bateria ou regulado se sensível).

### 3.5 Drivers de Motor

- **Ponte H**: IBT-2 (BTS7960) para motores de alta corrente (>5A).
- L298N **NÃO RECOMENDADO** (muita perda de calor, baixa eficiência).

---

## 4. Lista de Materiais (BOM) Estimada - Versão MVP

| Componente | Modelo Sugerido | Custo Est. (BRL) |
|------------|-----------------|------------------|
| Computador | Raspberry Pi 4 4GB | R$ 500 - 800 |
| Microcontrolador | ESP32 DevKit V1 | R$ 40 - 60 |
| Lidar | RPLidar A1M8 | R$ 600 - 900 |
| Câmera | RPi Camera V3 Wide | R$ 200 - 300 |
| Motores (x2) | Motor DC Planetário 12V c/ Encoder | R$ 300 - 500 |
| Driver Motor (x2)| BTS7960 43A | R$ 60 - 100 |
| Bateria | Li-Ion 3S 3P (Custom) | R$ 200 - 400 |
| Chassis | Custom (Impressão 3D + Alumínio) | R$ 200 - 400 |
| **TOTAL** | | **R$ 2.100 - 3.460** |

---

## 5. Próximos Passos (Implementação)

1. **Firmware (T-033)**: Criar código para o ESP32 (`micro-ros` ou protocolo serial custom) para receber comandos de velocidade (`cmd_vel`) e enviar odometria.
2. **ROS2 Stack (T-034)**: Configurar Docker container com ROS2 Humble no Raspberry Pi.
3. **Integração**: Conectar ESP32 ao RPi via USB Serial.
