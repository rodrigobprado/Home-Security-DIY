# UGV ROS2 Navigation Stack (T-034)

Data: 2026-02-22
Referencias: Issue #89, T-034

## Escopo implementado

- Ambiente Docker para UGV com ROS2 Humble + Nav2 + SLAM Toolbox + Gazebo.
- Comando `patrol` funcional no `ugv_control.py`.
- Integracao MQTT para waypoints e rotas configuraveis.
- Recuperacao automatica de camera aprimorada em `ugv_vision.py`.

## Arquivos principais

- `src/drones/ugv/Dockerfile`
- `src/drones/ugv/docker-compose.ugv.yml`
- `src/drones/ugv/app/ugv_control.py`
- `src/drones/ugv/app/ugv_vision.py`
- `src/drones/ugv/ros2/params/nav2_params.yaml`
- `src/drones/ugv/ros2/params/slam_toolbox.yaml`
- `src/drones/ugv/ros2/maps/residential_map.yaml`
- `src/drones/ugv/ros2/routes/patrol_routes.json`
- `src/drones/ugv/scripts/start_nav_stack.sh`
- `src/drones/ugv/scripts/run_gazebo_smoke_test.sh`

## Topicos MQTT usados

- Comandos gerais: `ugv/command`
- Cadastro/atualizacao de rotas: `ugv/patrol/waypoints/set`
- Estado de rotas: `ugv/patrol/waypoints/state`
- Waypoints publicados para observabilidade: `ugv/patrol/waypoints`
- Estado geral: `ugv/status`

## Formato de rota configuravel

Arquivo base: `src/drones/ugv/ros2/routes/patrol_routes.json`

Exemplo:

```json
{
  "perimeter_day": [
    {"x": 0.0, "y": 0.0, "yaw": 0.0},
    {"x": 2.0, "y": 0.0, "yaw": 0.0}
  ]
}
```

## Comando patrol

Payload por MQTT em `ugv/command`:

```json
{
  "cmd": "patrol",
  "route": "perimeter_day",
  "source_id": "dashboard",
  "timestamp": 1730000000,
  "signature": "<hmac_sha256>"
}
```

Comportamento:

1. Valida HMAC/source/timestamp.
2. Carrega a rota solicitada (ou fallback para rota padrao).
3. Publica waypoints em `ugv/patrol/waypoints`.
4. Tenta enviar rota para ROS2 em `/ugv/patrol/goal` (`std_msgs/String`).
5. Publica status `started` (ROS2 ok) ou `started_mqtt_only` (fallback).

## Simulacao/Gazebo

Smoke test de dependencias:

```bash
docker compose -f src/drones/ugv/docker-compose.ugv.yml --profile test run --rm ugv-gazebo-smoke
```

Stack ROS2 (SLAM + Nav2):

```bash
docker compose -f src/drones/ugv/docker-compose.ugv.yml up -d ugv-ros2-nav ugv-brain
```

## Observacoes

- O mapa `residential_map.yaml` e um placeholder inicial para bringup; deve ser substituido
  pelo mapa real da residencia apos fase de mapeamento.
- A execucao de navegacao fisica depende da calibracao de odometria/TF e do firmware (T-033).
