# SLOs e SLAs dos Serviços Críticos

## Objetivo
Definir metas operacionais mínimas para disponibilidade e recuperação.

## Escopo e vigência
- Vigência inicial: 2026-03-01 até 2026-08-31.
- Revisão obrigatória: semestral ou após 2 incidentes P1 no mesmo serviço.
- Ambiente de medição: produção (K3s), com validação de tendência em homol.

## Serviços críticos
- Home Assistant
- Mosquitto MQTT
- PostgreSQL
- Frigate
- Dashboard API

## SLOs
| Serviço | SLI | Janela | SLO |
|---|---|---|
| Home Assistant | Disponibilidade HTTP (2xx/3xx em `/`) | 30 dias corridos | >= 99.5% |
| Mosquitto | Disponibilidade broker (connect + publish + subscribe) | 30 dias corridos | >= 99.9% |
| PostgreSQL | Disponibilidade de conexão (probe SQL) | 30 dias corridos | >= 99.9% |
| Frigate | Disponibilidade de UI/API (HTTP + stream ativo) | 30 dias corridos | >= 99.0% |
| Dashboard API | Disponibilidade de `/health` e latência p95 de `/api/services/status` | 30 dias corridos | >= 99.5% e p95 <= 350 ms |

## SLAs operacionais internos
- Incidente P1: início de resposta <= 15 min.
- Incidente P1: restauração parcial <= 60 min.
- Incidente P1: restauração total <= 4 h.
- Incidente P2: resposta <= 4 h úteis.
- Comunicação interna de incidente P1: primeira atualização em <= 30 min.

## Error budget
- Home Assistant e Dashboard API (99.5%): ~3h39m de indisponibilidade/mês.
- Mosquitto e PostgreSQL (99.9%): ~43m de indisponibilidade/mês.
- Frigate (99.0%): ~7h18m de indisponibilidade/mês.

## Método de medição (SLI)
- Coleta primária por healthchecks e métricas dos serviços.
- Frequência de coleta: 60s para disponibilidade, 30s para latência em endpoints HTTP.
- Regra de cálculo de disponibilidade: `success / total` por janela móvel de 30 dias.
- Regra de latência: percentil p95 no período, com exclusão de janelas de manutenção aprovada.

## Fontes de evidência
- Dashboard operacional (`ServiceStatus`) para status corrente.
- Logs de aplicação e plataforma (`docker compose logs` / `kubectl logs`) para auditoria.
- Histórico de incidentes e post-mortem em `docs/INCIDENT_RESPONSE.md`.

## Observabilidade mínima
- Healthchecks ativos em Compose/K8s.
- Logs centralizados por serviço.
- Teste de restore PostgreSQL trimestral.
- Alerta automático quando uso do error budget exceder 50% no mês.

## Governança
- Revisão semestral de metas.
- Ajuste de SLO condicionado a capacidade operacional e histórico de incidentes.
- Qualquer flexibilização de SLO exige ADR ou registro formal de exceção com prazo.
