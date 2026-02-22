# Comunicação Redundante de Drones (T-036)

Data: 2026-02-22
Referência: Issue #91

## Objetivo
Implementar failover automático Wi-Fi -> LoRa para telemetria e comandos críticos de emergência.

## Arquitetura de canal

1. Canal primário: MQTT sobre Wi-Fi.
2. Canal secundário: LoRa/Meshtastic para comandos de contingência.

## Estados de link

- `wifi`: link primário saudável.
- `lora`: failover ativo por timeout ou RSSI baixo.

Critérios de failover:
- `wifi_rssi < -78 dBm` (configurável)
- Sem tráfego MQTT por `30s` (configurável)

## Tópicos novos

### UGV
- `ugv/link/metrics` (entrada, ex.: `{ "wifi_rssi": -82 }`)
- `ugv/link/state` (saída)
- `ugv/lora/command` (entrada de emergência)

### UAV
- `uav/link/metrics` (entrada)
- `uav/link/state` (saída)
- `uav/lora/command` (entrada de emergência)

## Comandos de emergência via LoRa

- `STOP` / `stop`
- `RTH` / `rth`
- `ALARM` / `alarm`

## Latência esperada (documentada)

| Canal | Uso | Latência típica |
|---|---|---|
| Wi-Fi + MQTT | Comando normal e telemetria contínua | 20-80 ms |
| LoRa | Comando de emergência e telemetria reduzida | 300-1500 ms |

## Teste de failover (30s sem Wi-Fi)

1. Iniciar stack de drones.
2. Publicar RSSI baixo ou bloquear tráfego MQTT por 30s.
3. Verificar transição para `mode=lora` em `*/link/state`.
4. Enviar comando de emergência em `*/lora/command`.
5. Restaurar link Wi-Fi.
6. Verificar retorno automático para `mode=wifi`.

## Meshtastic

Meshtastic pode substituir o transporte LoRa raw para rede multi-nó, mantendo o mesmo contrato lógico de comandos de contingência (`*/lora/command`) através de bridge no gateway.
