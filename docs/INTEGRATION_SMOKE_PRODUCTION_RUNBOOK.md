# Runbook de Smoke de Integracao em Ambiente Real

Issue: #141  
Ultima atualizacao: 2026-02-22

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
