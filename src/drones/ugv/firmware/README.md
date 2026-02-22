# UGV Firmware (ESP32) - T-033

## Objetivo
Firmware de baixo nivel para controle de motores, leitura de encoders/bateria e comunicacao serial com o computador embarcado.

## Hardware mapeado (sem conflito GPIO)

- Motores BTS7960:
  - `RPWM_L=GPIO16`
  - `LPWM_L=GPIO17`
  - `RPWM_R=GPIO25`
  - `LPWM_R=GPIO26`
- Encoders:
  - `ENC_L_A=GPIO34`, `ENC_L_B=GPIO35`
  - `ENC_R_A=GPIO32`, `ENC_R_B=GPIO33`
- Bateria (ADC): `GPIO39`
- LoRa SX1276 (HSPI):
  - `SS=GPIO5`, `RST=GPIO27`, `DIO0=GPIO2`
  - `SCK=GPIO14`, `MISO=GPIO12`, `MOSI=GPIO13`

> GPIO 18/19 nao sao usados no firmware para evitar conflito historico com SPI/LoRa (issue #30).

## Protocolo serial (115200 bps)

### Comandos recebidos (RX)

- `M <left_pwm> <right_pwm>`
  - Exemplo: `M 120 -80`
  - Faixa: `-255..255`
- `STOP`
  - Parada imediata dos motores

### Telemetria enviada (TX)

- `O <left_ticks> <right_ticks>`
  - Odometria por encoder
- `B <battery_percent>`
  - Percentual de bateria calibrado
- `W <watchdog_ok>`
  - `1` se recebendo comandos dentro do timeout
  - `0` se watchdog acionado (fail-safe)

## Controle

- Loop PID de velocidade (20 Hz) por roda.
- PWM via LEDC (20 kHz, resolucao 8 bits).
- Watchdog de comando serial (timeout 800 ms) com fail-safe para `STOP`.

## Testes unitarios

Rodar em host (sem ESP32):

```bash
pio test -e native
```

Cobertura atual de teste:
- saturacao de PWM
- resposta de sinal do PID para erro positivo/negativo
