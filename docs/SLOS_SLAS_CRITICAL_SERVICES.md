# SLOs e SLAs dos Serviços Críticos

## Objetivo
Definir metas operacionais mínimas para disponibilidade e recuperação.

## Serviços críticos
- Home Assistant
- Mosquitto MQTT
- PostgreSQL
- Frigate
- Dashboard API

## SLOs
| Serviço | SLI | SLO mensal |
|---|---|---|
| Home Assistant | Disponibilidade HTTP | >= 99.5% |
| Mosquitto | Disponibilidade broker | >= 99.9% |
| PostgreSQL | Disponibilidade de conexão | >= 99.9% |
| Frigate | Disponibilidade de UI/API | >= 99.0% |
| Dashboard API | Disponibilidade `/health` | >= 99.5% |

## SLAs operacionais internos
- Incidente P1: início de resposta <= 15 min.
- Incidente P1: restauração parcial <= 60 min.
- Incidente P1: restauração total <= 4 h.
- Incidente P2: resposta <= 4 h úteis.

## Error budget
- Home Assistant (99.5%): ~3h39m de indisponibilidade/mês.
- Serviços 99.9%: ~43m de indisponibilidade/mês.

## Observabilidade mínima
- Healthchecks ativos em Compose/K8s.
- Logs centralizados por serviço.
- Teste de restore PostgreSQL trimestral.

## Governança
- Revisão semestral de metas.
- Ajuste de SLO condicionado a capacidade operacional e histórico de incidentes.
