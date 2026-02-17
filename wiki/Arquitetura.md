# Arquitetura

## Componentes principais

- **Home Assistant**: automação, dashboards e regras.
- **Frigate**: gravação de vídeo + detecção de objetos.
- **Zigbee2MQTT**: integração de sensores Zigbee.
- **Mosquitto**: barramento MQTT para eventos.

## Topologia lógica

1. Sensores e câmeras publicam eventos/streams.
2. Frigate processa vídeo localmente e envia eventos.
3. Home Assistant consome eventos MQTT e executa automações.
4. Dashboards consolidam estado e alertas em tempo real.

## Ambientes

- **Dev**: `src/docker-compose.yml`
- **Prod**: `k8s/base` + `k8s/overlays/*`

## Leituras recomendadas

- `docs/ARCHITECTURE.md`
- `docs/ARQUITETURA_TECNICA.md`
- ADRs em `docs/adr/`
