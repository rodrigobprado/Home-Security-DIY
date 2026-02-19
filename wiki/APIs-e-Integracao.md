# APIs e Integração

O sistema expõe APIs REST, WebSocket e MQTT para comunicação entre componentes. **Nenhuma API é exposta publicamente** — acesso remoto exclusivamente via VPN (WireGuard/Tailscale).

---

## Visão Geral

```
┌─────────────────────────────────────────────────────────────┐
│                    CAMADA DE API                            │
│                                                             │
│  Cliente (Dashboard / App / Automação)                      │
│       │ REST / WebSocket / MQTT                             │
├───────┼─────────────────────────────────────────────────────┤
│       │                                                     │
│  ┌────▼────┐   ┌────────┐   ┌─────────────┐   ┌──────────┐ │
│  │  Home   │   │Frigate │   │Zigbee2MQTT  │   │Dashboard │ │
│  │Assistant│   │  NVR   │   │             │   │   API    │ │
│  │:8123    │   │:5000   │   │:8080 / MQTT │   │:8000     │ │
│  └─────────┘   └────────┘   └─────────────┘   └──────────┘ │
│                      │             │                        │
│              ┌───────┴─────────────┘                        │
│              │         MQTT Broker (Mosquitto :1883)        │
│              └──────────────────────────────────────────────┤
└─────────────────────────────────────────────────────────────┘
```

| Serviço | Protocolo | Porta | Autenticação |
|---------|-----------|-------|--------------|
| Home Assistant REST | HTTP/JSON | 8123 | Bearer token |
| Home Assistant WebSocket | WebSocket | 8123 | Bearer token |
| Frigate REST | HTTP/JSON | 5000 | Nenhuma (VLAN) |
| Frigate RTSP restream | RTSP | 8554 | Nenhuma (VLAN) |
| Mosquitto MQTT | TCP | 1883 | Usuário/senha |
| Zigbee2MQTT REST | HTTP/JSON | 8080 | Nenhuma (VLAN) |
| Dashboard API | HTTP/JSON | 8000 | `X-API-Key` ou Bearer |

---

## Home Assistant REST API

**Base URL**: `http://<HA_IP>:8123/api/`
**Autenticação**: `Authorization: Bearer <LONG_LIVED_TOKEN>`

### Endpoints principais

#### Estados de entidades

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/states` | Lista todos os estados de entidades |
| `GET` | `/api/states/{entity_id}` | Estado de uma entidade específica |
| `POST` | `/api/states/{entity_id}` | Atualizar estado de uma entidade |

```bash
# Consultar sensor de porta
curl -H "Authorization: Bearer TOKEN" \
  http://192.168.10.10:8123/api/states/binary_sensor.porta_entrada
```

```json
{
  "entity_id": "binary_sensor.porta_entrada",
  "state": "off",
  "attributes": {
    "device_class": "door",
    "friendly_name": "Porta Entrada",
    "battery": 95
  },
  "last_changed": "2026-02-18T10:30:00+00:00"
}
```

#### Serviços (ações)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/services` | Lista todos os serviços disponíveis |
| `POST` | `/api/services/{domain}/{service}` | Executar um serviço |

```bash
# Armar alarme no modo ausente
curl -X POST \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "alarm_control_panel.alarmo", "code": "1234"}' \
  http://192.168.10.10:8123/api/services/alarm_control_panel/alarm_arm_away
```

#### Alarmo — serviços de alarme

| Serviço | Descrição |
|---------|-----------|
| `alarm_control_panel/alarm_arm_away` | Armar total (saída) |
| `alarm_control_panel/alarm_arm_home` | Armar parcial (noite) |
| `alarm_control_panel/alarm_arm_night` | Armar perímetro |
| `alarm_control_panel/alarm_disarm` | Desarmar |

#### Histórico e logs

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/history/period/{timestamp}` | Histórico de estados |
| `GET` | `/api/logbook/{timestamp}` | Log de eventos |
| `GET` | `/api/error_log` | Log de erros do sistema |

### WebSocket API

**URL**: `ws://<HA_IP>:8123/api/websocket`

Usada pelo dashboard para atualizações em tempo real sem polling.

```json
// Subscrever eventos de mudança de estado
{"type": "subscribe_events", "event_type": "state_changed"}
```

---

## Frigate REST API

**Base URL**: `http://<FRIGATE_IP>:5000/api/`
**Autenticação**: Nenhuma (acesso restrito por VLAN)

### Eventos de detecção

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/events` | Lista eventos detectados |
| `GET` | `/api/events/{event_id}` | Detalhes de um evento |
| `GET` | `/api/events/{event_id}/thumbnail.jpg` | Thumbnail do evento |
| `GET` | `/api/events/{event_id}/snapshot.jpg` | Snapshot do evento |
| `GET` | `/api/events/{event_id}/clip.mp4` | Vídeo clip do evento |
| `DELETE` | `/api/events/{event_id}` | Remover evento |

**Filtros para `/api/events`:**

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `cameras` | string | Filtrar por câmera (ex: `entrada`) |
| `labels` | string | Filtrar por label (ex: `person,car`) |
| `after` | timestamp | Eventos após data |
| `before` | timestamp | Eventos antes de data |
| `limit` | int | Limite de resultados |
| `has_clip` | bool | Apenas com vídeo clip |

### Câmeras e gravações

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/{camera_name}/latest.jpg` | Último frame da câmera |
| `GET` | `/api/{camera_name}/recordings/summary` | Resumo de gravações |
| `GET` | `/api/{camera_name}/start/{start}/end/{end}/clip.mp4` | Exportar período |
| `GET` | `/api/stats` | Estatísticas do sistema |
| `GET` | `/api/config` | Configuração atual |

### Streams

| Protocolo | URL | Uso |
|-----------|-----|-----|
| **RTSP** | `rtsp://<IP>:8554/{camera_name}` | Restream para outros clientes |
| **WebRTC** | `http://<IP>:8555/{camera_name}` | Baixa latência no browser |

---

## MQTT — Tópicos (Mosquitto)

**Broker**: `mqtt://<MQTT_IP>:1883`
**Autenticação**: Usuário/senha configurados em `src/mosquitto/config/`

### Zigbee2MQTT

| Tópico | Direção | Descrição |
|--------|---------|-----------|
| `zigbee2mqtt/bridge/state` | Pub | Estado da bridge (`online`/`offline`) |
| `zigbee2mqtt/bridge/devices` | Pub | Lista de dispositivos pareados |
| `zigbee2mqtt/{device_name}` | Pub | Estado de um dispositivo |
| `zigbee2mqtt/{device_name}/set` | Sub | Enviar comando a um dispositivo |
| `zigbee2mqtt/{device_name}/get` | Sub | Solicitar estado atualizado |

**Payload — sensor de porta:**
```json
{
  "contact": false,
  "battery": 95,
  "voltage": 3100,
  "linkquality": 120
}
```

**Payload — sensor PIR:**
```json
{
  "occupancy": true,
  "battery": 80,
  "illuminance_lux": 150,
  "linkquality": 85
}
```

### Frigate

| Tópico | Direção | Descrição |
|--------|---------|-----------|
| `frigate/available` | Pub | Disponibilidade do Frigate |
| `frigate/events` | Pub | Eventos de detecção (new/update/end) |
| `frigate/{camera_name}/person` | Pub | Contagem de pessoas na câmera |
| `frigate/{camera_name}/car` | Pub | Contagem de veículos na câmera |
| `frigate/{camera_name}/person/snapshot` | Pub | Snapshot JPEG de pessoa detectada |

**Payload — evento de detecção:**
```json
{
  "type": "new",
  "after": {
    "id": "1708246800.123456-abcdef",
    "camera": "entrada",
    "label": "person",
    "score": 0.92,
    "start_time": 1708246800.0,
    "end_time": null
  }
}
```

### Home Assistant

| Tópico | Direção | Descrição |
|--------|---------|-----------|
| `homeassistant/status` | Pub | Estado do HA (`online`/`offline`) |
| `homeassistant/+/+/config` | Pub | Auto-discovery de dispositivos |
| `homeassistant/+/+/state` | Pub | Estado de entidades |

---

## Zigbee2MQTT REST API

**Base URL**: `http://<Z2M_IP>:8080/api/`

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/devices` | Lista de dispositivos pareados |
| `GET` | `/api/groups` | Lista de grupos |
| `POST` | `/api/permit_join` | Habilitar pareamento |
| `POST` | `/api/device/{id}/rename` | Renomear dispositivo |
| `POST` | `/api/device/{id}/remove` | Remover dispositivo |

---

## Dashboard API

**Base URL**: `http://<HOST>:8000`
**Autenticação obrigatória**:
- `X-API-Key: <DASHBOARD_API_KEY>`
- ou `Authorization: Bearer <DASHBOARD_API_KEY>`

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/health` | Healthcheck (Docker/K8s probe) |
| `WS` | `/ws` | WebSocket — fan-out de eventos HA |
| `GET` | `/api/sensors` | Todos os estados de entidades HA |
| `GET` | `/api/sensors/{entity_id}` | Estado de uma entidade |
| `GET` | `/api/cameras/{name}/snapshot` | Snapshot Frigate (proxy) |
| `GET` | `/api/alerts` | Histórico paginado (PostgreSQL) |
| `GET` | `/api/services/status` | Health dos serviços |
| `GET` | `/api/services/ws-metrics` | Métricas operacionais de WebSocket |
| `GET` | `/api/map/devices` | Posições dos dispositivos no mapa |

### Exemplos de acesso

```bash
curl -H "X-API-Key: ${DASHBOARD_API_KEY}" \
  http://localhost:8000/api/services/status
```

```bash
# WebSocket autenticado por query string
ws://localhost:8000/ws?api_key=${DASHBOARD_API_KEY}
```

Em ambiente Docker, o frontend injeta `X-API-Key` no proxy Nginx para `/api/*` e `/ws`.

---

## Nomenclatura de Entidades

### Padrões de nomes no Home Assistant

| Tipo | Formato | Exemplo |
|------|---------|---------|
| Sensor de porta | `binary_sensor.porta_{local}` | `binary_sensor.porta_entrada` |
| Sensor de janela | `binary_sensor.janela_{local}` | `binary_sensor.janela_sala` |
| Sensor PIR | `binary_sensor.pir_{local}` | `binary_sensor.pir_corredor` |
| Câmera | `camera.cam_{local}` | `camera.cam_entrada` |
| Sirene | `switch.sirene_{local}` | `switch.sirene_interna` |
| Alarme | `alarm_control_panel.alarmo` | `alarm_control_panel.alarmo` |

### Padrões de tópicos MQTT

| Tipo | Formato | Exemplo |
|------|---------|---------|
| Sensor Zigbee | `zigbee2mqtt/sensor_{tipo}_{local}` | `zigbee2mqtt/sensor_porta_entrada` |
| Câmera Frigate | `frigate/{local}` | `frigate/entrada` |

---

## Referências

- `docs/API_DOCS.md` — fonte principal desta página
- [Home Assistant REST API](https://developers.home-assistant.io/docs/api/rest)
- [Home Assistant WebSocket API](https://developers.home-assistant.io/docs/api/websocket)
- [Frigate HTTP API](https://docs.frigate.video/integrations/api)
- [Zigbee2MQTT MQTT Topics](https://www.zigbee2mqtt.io/guide/usage/mqtt_topics_and_messages.html)
- [Arquitetura](Arquitetura) — visão geral do stack
