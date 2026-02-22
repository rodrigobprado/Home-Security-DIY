# Integração MQTT Drones + Home Assistant (T-038)

Este documento descreve os tópicos MQTT usados para integração entre Home Assistant e os módulos UGV/UAV.

## Objetivo

- Controle manual no Home Assistant (`start_patrol`, `return_home`, `stop`, `inspect_zone`)
- Telemetria de status e bateria para entidades HA
- Disparo automático por evento de alarme
- Notificação push quando há detecção no pipeline de visão dos drones

## Tópicos de comando (HA -> Drones)

- `ugv/command`
- `uav/command`

Payloads suportados:

```json
{"cmd":"patrol","route":"perimeter_day","source_id":"homeassistant"}
{"cmd":"return_home","source_id":"homeassistant"}
{"cmd":"stop","source_id":"homeassistant"}
{"cmd":"inspect_zone","source_id":"homeassistant"}
```

## Tópicos de telemetria (Drones -> HA)

- `ugv/status`
  - Campos relevantes: `state`, `battery`, `wifi_signal`, `comm.mode`
- `uav/status`
  - Campos relevantes: `mode`, `armed`, `battery`, `heading`, `comm.mode`
- `uav/location`
  - Campos relevantes: `latitude`, `longitude`, `altitude`
- `ugv/vision/detections`
- `uav/vision/detections`
- `ugv/vision/safety`
- `uav/vision/safety`

## Entidades e botões no Home Assistant

Arquivo: `src/homeassistant/mqtt.yaml`

- Sensores:
  - `sensor.ugv_battery`
  - `sensor.ugv_status`
  - `sensor.uav_battery`
  - `sensor.uav_status`
- Botões:
  - `button.ugv_start_patrol`
  - `button.ugv_return_home`
  - `button.ugv_emergency_stop`
  - `button.uav_inspect_zone`
  - `button.uav_return_home`
  - `button.uav_stop`

## Automações no Home Assistant

Arquivo: `src/homeassistant/automations.yaml`

- `alarm_triggered_dispatch_uav`
  - Alarme disparado -> publica `inspect_zone` em `uav/command`
- `alarm_triggered_dispatch_ugv`
  - Alarme disparado -> publica `patrol` em `ugv/command`
- `drone_intrusion_notification`
  - Deteções em `ugv/vision/detections` ou `uav/vision/detections` -> `notify.notify`

## Segurança de comandos MQTT

Por padrão, os bridges UGV/UAV validam comandos por HMAC:

- `COMMAND_HMAC_SECRET_UGV`
- `COMMAND_HMAC_SECRET_UAV`

Para integração rápida com botões do Home Assistant sem assinatura HMAC, habilitar explicitamente:

- `ALLOW_UNSIGNED_HOMEASSISTANT_COMMANDS_UGV=true`
- `ALLOW_UNSIGNED_HOMEASSISTANT_COMMANDS_UAV=true`

Recomendação para produção:

- Usar assinatura HMAC e timestamp para todos os emissores
- Restringir `COMMAND_ALLOWED_SOURCES_*`
- Separar broker MQTT em rede/VLAN de automação
