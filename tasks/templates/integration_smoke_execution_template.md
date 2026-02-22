# Template de Execucao - Integration Smoke (Ambiente Real)

Issue relacionada: #141  
Data: YYYY-MM-DD  
Responsavel: <nome>  
Ambiente: <staging/producao>

## Execucao automatizada
| Item | Evidencia | Status |
|---|---|---|
| `scripts/integration_smoke_check.sh` executado | log/arquivo | PASS/FAIL |
| Home Assistant | HTTP 200 | PASS/FAIL |
| Dashboard + Kiosk | HTTP 200 | PASS/FAIL |
| API health/sensors | HTTP 200 | PASS/FAIL |
| Frigate | HTTP 200 | PASS/FAIL |

## Testes manuais complementares
| Item | Evidencia | Status |
|---|---|---|
| Deteccao Frigate com pessoa no frame | video/log | PASS/FAIL |
| Disparo de alarme/sirene | log/video | PASS/FAIL |
| Notificacao push/Telegram | print/log | PASS/FAIL |
| Acesso VPN remoto | print/log | PASS/FAIL |
| Restore de backup | registro/teste | PASS/FAIL |
