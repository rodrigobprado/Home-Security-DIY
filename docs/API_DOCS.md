# Documentacao de APIs e Interfaces

> Sistema de Home Security – Open Source / Open Hardware
>
> Versao: 1.1 | Data: 2026-02-23 | Adicionado: Catálogo de Ativos e Trilha de Auditoria (Issues #336, #339)

---

## 1. Visao geral

O sistema utiliza APIs REST, WebSocket e MQTT para comunicacao entre componentes. Nenhuma API e exposta publicamente — acesso remoto exclusivamente via VPN (WireGuard).

### Convencoes

- **Formato**: JSON para APIs REST, JSON para MQTT payloads
- **Autenticacao**:
  - Home Assistant: Bearer token (Long-Lived Access Token)
  - Dashboard API (operador): `X-API-Key` header ou `Authorization: Bearer <key>`
  - Dashboard API (admin): `X-Admin-Key` header (necessário para CRUD de ativos)
  - MQTT: usuario/senha
- **Codigos de erro**: Padrao HTTP para REST APIs

---

## 2. Home Assistant REST API

**Base URL**: `http://<HA_IP>:8123/api/`
**Autenticacao**: Header `Authorization: Bearer <LONG_LIVED_TOKEN>`

### Endpoints principais

#### Estado dos sensores

| Metodo | Endpoint | Descricao |
|--------|----------|-----------|
| `GET` | `/api/states` | Lista todos os estados de entidades |
| `GET` | `/api/states/{entity_id}` | Estado de uma entidade especifica |
| `POST` | `/api/states/{entity_id}` | Atualizar estado de uma entidade |

**Exemplo — consultar sensor de porta:**

```bash
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

#### Servicos (acoes)

| Metodo | Endpoint | Descricao |
|--------|----------|-----------|
| `GET` | `/api/services` | Lista todos os servicos disponiveis |
| `POST` | `/api/services/{domain}/{service}` | Executar um servico |

**Exemplo — armar alarme:**

```bash
curl -X POST \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "alarm_control_panel.alarmo", "code": "1234"}' \
  http://192.168.10.10:8123/api/services/alarm_control_panel/alarm_arm_away
```

#### Alarmo (sistema de alarme)

| Servico | Descricao |
|---------|-----------|
| `alarm_control_panel/alarm_arm_away` | Armar total |
| `alarm_control_panel/alarm_arm_home` | Armar parcial (noite) |
| `alarm_control_panel/alarm_arm_night` | Armar perimetro |
| `alarm_control_panel/alarm_disarm` | Desarmar |

#### Historico e logs

| Metodo | Endpoint | Descricao |
|--------|----------|-----------|
| `GET` | `/api/history/period/{timestamp}` | Historico de estados |
| `GET` | `/api/logbook/{timestamp}` | Log de eventos |
| `GET` | `/api/error_log` | Log de erros do sistema |

### WebSocket API

**URL**: `ws://<HA_IP>:8123/api/websocket`

Usada para atualizacoes em tempo real no dashboard. Permite subscribe a mudancas de estado sem polling.

```json
{"type": "subscribe_events", "event_type": "state_changed"}
```

---

## 3. Frigate API

**Base URL**: `http://<FRIGATE_IP>:5000/api/`
**Autenticacao**: Nenhuma (acesso restrito por VLAN)

### Endpoints principais

#### Eventos de deteccao

| Metodo | Endpoint | Descricao |
|--------|----------|-----------|
| `GET` | `/api/events` | Lista eventos detectados |
| `GET` | `/api/events/{event_id}` | Detalhes de um evento |
| `GET` | `/api/events/{event_id}/thumbnail.jpg` | Thumbnail do evento |
| `GET` | `/api/events/{event_id}/snapshot.jpg` | Snapshot do evento |
| `GET` | `/api/events/{event_id}/clip.mp4` | Video clip do evento |
| `DELETE` | `/api/events/{event_id}` | Remover evento |

**Filtros para `/api/events`:**

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `cameras` | string | Filtrar por camera (ex: `entrada`) |
| `labels` | string | Filtrar por label (ex: `person,car`) |
| `after` | timestamp | Eventos apos data |
| `before` | timestamp | Eventos antes de data |
| `limit` | int | Limite de resultados |
| `has_clip` | bool | Apenas com video clip |
| `has_snapshot` | bool | Apenas com snapshot |

#### Cameras

| Metodo | Endpoint | Descricao |
|--------|----------|-----------|
| `GET` | `/api/stats` | Estatisticas do sistema |
| `GET` | `/api/config` | Configuracao atual |
| `GET` | `/api/{camera_name}/latest.jpg` | Ultimo frame da camera |

#### Gravacoes

| Metodo | Endpoint | Descricao |
|--------|----------|-----------|
| `GET` | `/api/{camera_name}/recordings/summary` | Resumo de gravacoes |
| `GET` | `/api/{camera_name}/start/{start}/end/{end}/clip.mp4` | Exportar periodo |

#### Streams

| Protocolo | URL | Uso |
|-----------|-----|-----|
| **RTSP** | `rtsp://<IP>:8554/{camera_name}` | Restream para outros clientes |
| **WebRTC** | `http://<IP>:8555/{camera_name}` | Baixa latencia no browser |

---

## 4. Topicos MQTT (Mosquitto)

**Broker**: `mqtt://<MQTT_IP>:1883`
**Autenticacao**: Usuario/senha configurados em `mosquitto/config/`

### Topicos do Zigbee2MQTT

| Topico | Direcao | Descricao |
|--------|---------|-----------|
| `zigbee2mqtt/bridge/state` | Pub | Estado da bridge (`online`/`offline`) |
| `zigbee2mqtt/bridge/devices` | Pub | Lista de dispositivos pareados |
| `zigbee2mqtt/bridge/log` | Pub | Logs da bridge |
| `zigbee2mqtt/{device_name}` | Pub | Estado de um dispositivo |
| `zigbee2mqtt/{device_name}/set` | Sub | Enviar comando a um dispositivo |
| `zigbee2mqtt/{device_name}/get` | Sub | Solicitar estado atualizado |

**Exemplo de payload — sensor de porta:**

```json
// zigbee2mqtt/sensor_porta_entrada
{
  "contact": false,
  "battery": 95,
  "voltage": 3100,
  "linkquality": 120
}
```

**Exemplo de payload — sensor PIR:**

```json
// zigbee2mqtt/sensor_pir_sala
{
  "occupancy": true,
  "battery": 80,
  "illuminance_lux": 150,
  "linkquality": 85
}
```

### Topicos do Frigate

| Topico | Direcao | Descricao |
|--------|---------|-----------|
| `frigate/available` | Pub | Disponibilidade do Frigate |
| `frigate/stats` | Pub | Estatisticas de processamento |
| `frigate/events` | Pub | Eventos de deteccao (novo/update/end) |
| `frigate/{camera_name}/person` | Pub | Contagem de pessoas na camera |
| `frigate/{camera_name}/car` | Pub | Contagem de veiculos na camera |
| `frigate/{camera_name}/person/snapshot` | Pub | Snapshot JPEG de pessoa detectada |

**Exemplo de payload — evento de deteccao:**

```json
// frigate/events
{
  "type": "new",
  "before": {},
  "after": {
    "id": "1708246800.123456-abcdef",
    "camera": "entrada",
    "label": "person",
    "score": 0.92,
    "start_time": 1708246800.0,
    "end_time": null,
    "thumbnail": "/9j/4AAQSkZJRg..."
  }
}
```

### Topicos do Home Assistant

| Topico | Direcao | Descricao |
|--------|---------|-----------|
| `homeassistant/status` | Pub | Estado do HA (`online`/`offline`) |
| `homeassistant/+/+/config` | Pub | Auto-discovery de dispositivos |
| `homeassistant/+/+/state` | Pub | Estado de entidades |

---

## 5. Zigbee2MQTT REST API

**Base URL**: `http://<Z2M_IP>:8080/api/`

| Metodo | Endpoint | Descricao |
|--------|----------|-----------|
| `GET` | `/api/devices` | Lista de dispositivos pareados |
| `GET` | `/api/groups` | Lista de grupos |
| `POST` | `/api/permit_join` | Habilitar pareamento |
| `POST` | `/api/device/{id}/rename` | Renomear dispositivo |
| `POST` | `/api/device/{id}/remove` | Remover dispositivo |

---

## 6. Dashboard API

**Base URL**: `http://<HOST>:8000`
**Autenticacao**:
- `X-API-Key: <DASHBOARD_API_KEY>`
- ou `Authorization: Bearer <DASHBOARD_API_KEY>`
- Proteção anti-bruteforce: tentativas inválidas são rate-limited por IP (HTTP e WS).

| Metodo | Endpoint | Descricao |
|--------|----------|-----------|
| `GET` | `/health` | Healthcheck da API |
| `WS` | `/ws` | Fan-out WebSocket de eventos do Home Assistant |
| `GET` | `/api/sensors` | Lista estados de entidades |
| `GET` | `/api/sensors/{entity_id}` | Estado de entidade especifica |
| `GET` | `/api/cameras/{name}/snapshot` | Snapshot JPEG (proxy Frigate) |
| `GET` | `/api/cameras/events` | Eventos recentes de deteccao |
| `GET` | `/api/alerts` | Historico de alertas (PostgreSQL) |
| `GET` | `/api/services/status` | Saude de servicos principais |
| `GET` | `/api/services/ws-metrics` | Metricas operacionais de WebSocket |
| `GET` | `/api/map/devices` | Posicao dos dispositivos no mapa |

Notas de segurança para configuração de mapa:
- `floorplan_image_data_url` deve ser `data:image/*;base64,...`
- tamanho máximo aceito: 2 MB

**Exemplo REST:**

```bash
curl -H "X-API-Key: ${DASHBOARD_API_KEY}" \
  http://localhost:8000/api/services/status
```

**Exemplo WebSocket:**

```bash
websocat \
  -H "X-API-Key: ${DASHBOARD_API_KEY}" \
  ws://localhost:8000/ws
```

---

## 7. Nomenclatura de entidades

### Padroes de nomes no Home Assistant

| Tipo | Formato | Exemplo |
|------|---------|---------|
| Sensor de porta | `binary_sensor.porta_{local}` | `binary_sensor.porta_entrada` |
| Sensor de janela | `binary_sensor.janela_{local}` | `binary_sensor.janela_sala` |
| Sensor PIR | `binary_sensor.pir_{local}` | `binary_sensor.pir_corredor` |
| Camera | `camera.cam_{local}` | `camera.cam_entrada` |
| Sirene | `switch.sirene_{local}` | `switch.sirene_interna` |
| Alarme | `alarm_control_panel.alarmo` | `alarm_control_panel.alarmo` |

### Padroes de topicos MQTT

| Tipo | Formato | Exemplo |
|------|---------|---------|
| Sensor Zigbee | `zigbee2mqtt/sensor_{tipo}_{local}` | `zigbee2mqtt/sensor_porta_entrada` |
| Camera Frigate | `frigate/{local}` | `frigate/entrada` |

---

## 8. Catalogo de Ativos (`/api/assets`)

**Base URL**: `http://<HOST>:8000`
**Autenticacao leitura**: `X-API-Key: <DASHBOARD_API_KEY>` (operador)
**Autenticacao escrita**: `X-API-Key` + `X-Admin-Key: <DASHBOARD_ADMIN_KEY>` (admin)

### Tipos de ativo

| `asset_type` | Descricao |
|-------------|-----------|
| `sensor` | Sensor Zigbee (porta, janela, PIR) |
| `camera` | Camera IP / Frigate |
| `ugv` | Drone terrestre (UGV) |
| `uav` | Drone aereo (UAV) |

### Status possiveis

| `status` | Descricao |
|----------|-----------|
| `active` | Ativo e operacional |
| `inactive` | Desativado (soft delete) |
| `offline` | Sem comunicacao |
| `maintenance` | Em manutencao |

### Endpoints

| Metodo | Endpoint | Auth | Descricao |
|--------|----------|------|-----------|
| `GET` | `/api/assets` | Operador | Lista ativos com paginacao e filtros |
| `GET` | `/api/assets/{asset_id}` | Operador | Detalhes de um ativo |
| `POST` | `/api/assets` | Admin | Cadastrar novo ativo |
| `PUT` | `/api/assets/{asset_id}` | Admin | Atualizar ativo |
| `DELETE` | `/api/assets/{asset_id}` | Admin | Soft-delete (marca `is_active=False`) |
| `POST` | `/api/assets/{asset_id}/restore` | Admin | Reativar ativo desativado |

### Filtros para `GET /api/assets`

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `asset_type` | string | Filtrar por tipo (`sensor`, `camera`, `ugv`, `uav`) |
| `status` | string | Filtrar por status |
| `is_active` | bool | `true` retorna apenas ativos; `false` apenas inativos |
| `search` | string | Busca parcial em `name`, `entity_id`, `location` |
| `page` | int | Pagina (padrao: 1) |
| `page_size` | int | Itens por pagina (padrao: 50, max: 200) |

**Exemplo — listar sensores ativos:**

```bash
curl -H "X-API-Key: ${DASHBOARD_API_KEY}" \
  "http://localhost:8000/api/assets?asset_type=sensor&is_active=true"
```

```json
{
  "items": [
    {
      "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "asset_type": "sensor",
      "name": "Sensor Porta Entrada",
      "entity_id": "binary_sensor.porta_entrada",
      "location": "entrada",
      "description": null,
      "status": "active",
      "is_active": true,
      "config_json": null,
      "created_at": "2026-02-23T10:00:00+00:00",
      "updated_at": "2026-02-23T10:00:00+00:00"
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 50,
  "pages": 1
}
```

**Exemplo — cadastrar ativo (requer admin key):**

```bash
curl -X POST http://localhost:8000/api/assets \
  -H "X-API-Key: ${DASHBOARD_API_KEY}" \
  -H "X-Admin-Key: ${DASHBOARD_ADMIN_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "asset_type": "sensor",
    "name": "Sensor Janela Sala",
    "entity_id": "binary_sensor.janela_sala",
    "location": "sala",
    "description": "Sensor magnetico de janela"
  }'
```

**Resposta (201 Created):**

```json
{
  "id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
  "asset_type": "sensor",
  "name": "Sensor Janela Sala",
  "entity_id": "binary_sensor.janela_sala",
  "location": "sala",
  "description": "Sensor magnetico de janela",
  "status": "active",
  "is_active": true,
  "config_json": null,
  "created_at": "2026-02-23T10:05:00+00:00",
  "updated_at": "2026-02-23T10:05:00+00:00"
}
```

> **Nota de seguranca**: respostas nunca incluem `credential_ref` nem dados sensíveis de `asset_credentials`.
> Quando `DASHBOARD_ADMIN_KEY` nao esta configurado, operacoes de escrita retornam **503**.

---

## 9. Trilha de Auditoria (`/api/audit`)

**Autenticacao**: `X-API-Key` (operador) — somente leitura

| Metodo | Endpoint | Descricao |
|--------|----------|-----------|
| `GET` | `/api/audit` | Lista registros de auditoria com filtros |
| `GET` | `/api/audit/export` | Exportar trilha (JSON ou CSV) |

### Filtros para `GET /api/audit`

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| `asset_id` | UUID | Filtrar por ativo |
| `action` | string | Filtrar por acao (`create`, `update`, `delete`, `restore`) |
| `actor` | string | Filtrar por autor da operacao |
| `since` | ISO datetime | Registros a partir de data |
| `until` | ISO datetime | Registros ate data |
| `page` | int | Pagina (padrao: 1) |
| `page_size` | int | Itens por pagina (padrao: 50, max: 200) |

**Exemplo — listar auditoria de um ativo:**

```bash
curl -H "X-API-Key: ${DASHBOARD_API_KEY}" \
  "http://localhost:8000/api/audit?asset_id=a1b2c3d4-e5f6-7890-abcd-ef1234567890"
```

```json
{
  "items": [
    {
      "id": 1,
      "asset_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "action": "create",
      "before_json": null,
      "after_json": "{\"name\": \"Sensor Porta Entrada\", \"status\": \"active\"}",
      "actor": "admin",
      "actor_ip": "192.168.10.5",
      "created_at": "2026-02-23T10:00:00+00:00"
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 50,
  "pages": 1
}
```

**Exportar trilha de auditoria:**

```bash
# JSON
curl -H "X-API-Key: ${DASHBOARD_API_KEY}" \
  "http://localhost:8000/api/audit/export?format=json" \
  -o audit_export.json

# CSV
curl -H "X-API-Key: ${DASHBOARD_API_KEY}" \
  "http://localhost:8000/api/audit/export?format=csv" \
  -o audit_export.csv
```

Resposta inclui header `Content-Disposition: attachment; filename="audit_YYYYMMDD_HHMMSS.{format}"`.

---

## Referencias

- [Home Assistant REST API](https://developers.home-assistant.io/docs/api/rest)
- [Home Assistant WebSocket API](https://developers.home-assistant.io/docs/api/websocket)
- [Frigate HTTP API](https://docs.frigate.video/integrations/api)
- [Zigbee2MQTT MQTT Topics](https://www.zigbee2mqtt.io/guide/usage/mqtt_topics_and_messages.html)
- [Mosquitto Configuration](https://mosquitto.org/man/mosquitto-conf-5.html)
- [ADR 011 — Catálogo Dinâmico de Ativos](adr/011-adoption-assets-catalog.md)
- [Runbook de Rollout do Catálogo](ASSETS_CATALOG_ROLLOUT_RUNBOOK.md)
