# Arquitetura

## Diagrama lógico

```
┌─────────────────────────────────────────────────────────────────┐
│                        HOST LINUX (N100)                        │
│                                                                 │
│  ┌──────────────┐   RTSP   ┌──────────────┐                    │
│  │   Câmeras    │─────────▶│    Frigate   │ ← OpenVINO (iGPU)  │
│  │  (4x ONVIF)  │          │  NVR + IA    │                    │
│  └──────────────┘          └──────┬───────┘                    │
│                                   │ MQTT events                │
│  ┌──────────────┐   Zigbee  ┌─────▼───────┐                    │
│  │   Sensores   │──────────▶│  Mosquitto  │ ← MQTT broker      │
│  │  (porta/PIR) │           └─────┬───────┘                    │
│  └──────────────┘                 │                            │
│                             ┌─────▼───────┐                    │
│                             │   Home      │ ← Alarmo           │
│                             │  Assistant  │   automações       │
│                             └─────┬───────┘                    │
│                                   │ WebSocket API              │
│                             ┌─────▼───────┐   ┌────────────┐  │
│                             │  Dashboard  │──▶│ PostgreSQL │  │
│                             │    API      │   │   16       │  │
│                             │  (FastAPI)  │   └────────────┘  │
│                             └─────┬───────┘                    │
│                                   │ WebSocket / REST           │
│                             ┌─────▼───────┐                    │
│                             │  Dashboard  │ ← React + Nginx    │
│                             │  Frontend   │   porta 3000       │
│                             └─────────────┘                    │
└─────────────────────────────────────────────────────────────────┘
```

## Componentes

### Camada de percepção
- **Câmeras IP**: 4 câmeras ONVIF/RTSP (entrada, fundos, lateral, garagem)
- **Sensores Zigbee**: abertura de portas/janelas, PIR (movimento), sirene
- **Frigate NVR**: gravação contínua + detecção de objetos com OpenVINO (iGPU Intel N100)

### Camada de processamento
- **Home Assistant**: central de automação, integra todos os serviços via MQTT e REST; gerencia o alarme via Alarmo
- **Zigbee2MQTT**: bridge entre coordenador Zigbee USB e o broker MQTT
- **Mosquitto**: broker MQTT para comunicação entre todos os serviços

### Camada de persistência
- **PostgreSQL 16** com schemas isolados por serviço:
  - `homeassistant` → usuário `ha_user` (recorder do Home Assistant)
  - `dashboard` → usuário `dashboard_user` (alertas, posições de dispositivos)
  - `metrics` → usuário `metrics_user` (métricas de sensores e câmeras)

### Camada de apresentação
- **Dashboard API** (FastAPI/Python 3.12):
  - Autenticação obrigatória via `X-API-Key` ou `Authorization: Bearer <API_KEY>`
  - WebSocket `/ws`: fan-out em tempo real de eventos do Home Assistant
  - `GET /api/sensors`: estados de entidades
  - `GET /api/cameras/{name}/snapshot`: proxy de snapshots Frigate
  - `GET /api/alerts`: histórico paginado do PostgreSQL
  - `GET /api/services/status`: saúde dos serviços
  - `GET /api/services/ws-metrics`: métricas operacionais de fan-out/drops WS
  - `GET /api/map/devices`: posições dos dispositivos no mapa
- **Dashboard Frontend** (React 18 + Vite + Tailwind CSS):
  - Modo completo (`/`): grid 3 colunas com todos os widgets
  - Modo kiosk (`/simplified`): barra de alarme + mapa + câmeras

## Ambientes

| Ambiente | Stack | Comando |
|---|---|---|
| Desenvolvimento | Docker Compose | `docker compose up -d` |
| Produção | K3s + Kustomize | `./scripts/deploy.sh production` |

### Docker Compose (dev) — `src/docker-compose.yml`

Serviços definidos:
- `postgres` — PostgreSQL 16 (porta `127.0.0.1:5432`)
- `mosquitto` — MQTT broker (porta 1883)
- `zigbee2mqtt` — bridge Zigbee (porta 8080)
- `frigate` — NVR + IA (portas 5000, 8554, 8555)
- `homeassistant` — automação (network_mode: host, porta 8123)
- `dashboard-api` — API FastAPI (porta 8000)
- `dashboard-frontend` — SPA React/Nginx (porta 3000)

### K3s / Kustomize (prod) — `k8s/`

```
k8s/
  base/
    namespace.yaml
    postgres/postgres.yaml          ← StatefulSet + PVC 20Gi
    mosquitto/mosquitto.yaml
    zigbee2mqtt/zigbee2mqtt.yaml
    frigate/frigate.yaml
    homeassistant/homeassistant.yaml
    dashboard/dashboard.yaml        ← API + Frontend Deployments
  overlays/
    staging/
    production/
      ingress.yaml                  ← security/frigate/zigbee/dashboard.home.local
```

## Rede

- Todos os contêineres (exceto HA) na rede bridge `home-security-net`
- Home Assistant usa `network_mode: host` para acesso ao PostgreSQL local e dispositivos USB
- PostgreSQL bind somente em loopback (`127.0.0.1:5432`) no host

## Leituras recomendadas

- `docs/ARCHITECTURE.md`
- `docs/ARQUITETURA_TECNICA.md`
- ADRs em `docs/adr/`
