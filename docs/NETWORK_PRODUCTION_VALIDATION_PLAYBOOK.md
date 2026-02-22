# Playbook de Validacao de Rede em Producao

Issue: #140  
Ultima atualizacao: 2026-02-22

## Objetivo
Padronizar validacoes de isolamento de rede, superficie de exposicao e identidade.

## Controles obrigatorios
- VLAN 20 e VLAN 30 isoladas e sem acesso indevido a internet.
- MQTT com autenticacao ativa e TLS habilitado em producao.
- Ausencia de exposicao externa da porta 1883.
- Home Assistant com TOTP para contas administrativas.
- SSH endurecido (`PermitRootLogin no`, `PasswordAuthentication no`) e fail2ban.

## Evidencia tecnica recomendada
- Saida de regras/firewall/switch com timestamp.
- Saida de teste de conectividade entre VLANs.
- Evidencia de configuracao TLS MQTT e certificados.
- Evidencia de estado de TOTP/SSH/fail2ban.

## Procedimento
1. Preencher `tasks/templates/network_production_validation_template.md`.
2. Anexar output de comandos e prints da interface de rede.
3. Registrar desvios com prazo e dono.

## Frequencia
- Revisao mensal.
- Revisao extraordinaria apos mudanca de roteador/switch/firewall.
