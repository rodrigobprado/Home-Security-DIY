# Runbook de Smoke de Integracao em Ambiente Real

Issue: #141  
Ultima atualizacao: 2026-02-23

## Objetivo
Padronizar execucao do smoke test no ambiente ativo com evidencias operacionais.

## Escopo do smoke
- Home Assistant, Dashboard e Frigate acessiveis.
- API de backend respondendo `health` e `sensors`.
- Testes manuais complementares: deteccao, alarme, notificacoes, VPN e restauracao.

## Procedimento
1. Definir `DASHBOARD_API_KEY` no ambiente alvo.
2. Executar `bash scripts/integration_smoke_check.sh`.
3. Preencher `tasks/templates/integration_smoke_execution_template.md`.
4. Anexar relatorio `tasks/INTEGRATION_SMOKE_<data>.md`.

## Criterio de aprovacao
- Endpoints criticos sem `FAIL`.
- Todos os testes manuais complementares com evidencia anexada.
- Incidentes registrados com plano de acao e prazo.

## Frequencia
- Executar apos cada release.
- Executar apos mudancas relevantes em HA, Dashboard, Frigate ou rede.

## Ultima execucao registrada (ambiente K3s de validacao)

Data: 2026-02-22

Estado dos workloads (`kubectl -n home-security get pods`):
- dashboard-api: `1/1 Running`
- dashboard-frontend: `1/1 Running`
- homeassistant: `1/1 Running`
- mosquitto: `1/1 Running`
- postgres: `1/1 Running`
- frigate: `1/1 Running`
- zigbee2mqtt: `1/1 Running`

Validacao HTTP via ingress TLS:
- `https://homeassistant-home-security.toca.lan` -> `302`
- `https://dashboard-home-security.toca.lan` -> `200`
- `https://frigate-home-security.toca.lan` -> `200`
- `https://zigbee2mqtt-home-security.toca.lan` -> `200`

Observacao operacional:
- No ambiente de validacao sem hardware fisico (cameras/USB Zigbee),
  `frigate` e `zigbee2mqtt` podem operar em modo stub para manter
  disponibilidade de pods/ingress e viabilizar os testes de plataforma.
- Mesmo em modo stub, os manifests mantem persistencia dos dados criticos
  de plataforma via PVCs:
  `mosquitto-data`, `homeassistant-config`, `zigbee2mqtt-data`,
  `frigate-config`, `frigate-media` e `postgres-data`.
