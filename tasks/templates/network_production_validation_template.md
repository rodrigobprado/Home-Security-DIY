# Template de Validacao de Rede em Producao

Issue relacionada: #140  
Data: YYYY-MM-DD  
Responsavel: <nome>

## Segmentacao e acesso
| Controle | Evidencia | Status |
|---|---|---|
| VLAN 20 isolada | regra/output | PASS/FAIL |
| VLAN 30 isolada | regra/output | PASS/FAIL |
| UPnP desabilitado | config/print | PASS/FAIL |
| Sem port forwarding indevido | config/print | PASS/FAIL |

## MQTT e credenciais
| Controle | Evidencia | Status |
|---|---|---|
| MQTT TLS ativo (8883) | config/teste | PASS/FAIL |
| 1883 nao exposta externamente | scan/teste | PASS/FAIL |
| TOTP ativo no HA (admins) | print/config | PASS/FAIL |
| SSH hardening + fail2ban | config/output | PASS/FAIL |
