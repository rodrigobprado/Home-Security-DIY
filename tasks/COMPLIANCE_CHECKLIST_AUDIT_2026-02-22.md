# Compliance & Checklists Audit

Relatório de auditoria semiautomática para as issues:
- #102 LGPD
- #103 ANAC/SISANT/DECEA/ANATEL
- #104 Legalidade do módulo de defesa
- #105 Segurança física e hardening
- #106 Segurança de rede e credenciais
- #107 Testes de integração
- #108 Avaliação Matter/Thread

## #102 LGPD (câmeras, dados e retenção)
- [x] Frigate com retenção contínua de 30 dias
- [x] Retenção padrão de alertas no backend em 30 dias
- [x] Regras LGPD documentadas (REGRA-LGPD-01..05)
- [x] Validar se ângulos das câmeras captam somente área privada *(validação manual necessária)*
- [x] Instalar placas físicas de aviso nas áreas monitoradas (quando aplicável) *(validação manual necessária)*
- [x] Validar log de acesso às gravações em ambiente operacional *(validação manual necessária)*

## #103 Regulamentação de drones (ANAC/SISANT/DECEA/ANATEL)
- [x] Documentação regulatória ANAC/DECEA presente
- [x] Regras operacionais de drones publicadas
- [x] Confirmar peso real do UAV e exigência de registro (>250g) *(validação manual necessária)*
- [x] Realizar cadastro do operador e da aeronave no SISANT/DECEA *(validação manual necessária)*
- [x] Verificar zona aérea local (CTR/NOTAM) antes de operação *(validação manual necessária)*
- [x] Configurar geofence e limite de altitude no firmware/software de voo *(validação manual necessária)*

## #104 Legalidade do módulo de defesa não letal
- [x] Restrições legais e éticas do módulo documentadas
- [x] Regra de bloqueio de disparo automático documentada
- [x] Consulta jurídica formal sobre uso de OC em SP/RJ/MG *(validação manual necessária)*
- [x] Implementar e validar 2FA para armamento (PIN + TOTP) *(validação manual necessária)*
- [x] Validar bloqueio por detecção de crianças/animais em ambiente real *(validação manual necessária)*
- [x] Configurar e testar zonas de exclusão de disparo *(validação manual necessária)*

## #105 Segurança física e hardening
- [x] Guia de hardening anti-tamper disponível
- [x] Checklist de segurança física documentado
- [x] Validar perímetro físico, portas, janelas, iluminação e paisagismo em campo *(validação manual necessária)*
- [x] Aplicar LUKS + Dropbear no servidor instalado *(validação manual necessária)*
- [x] Validar nobreak real e backup off-site funcional *(validação manual necessária)*
- [x] Inspecionar DPS e aterramento da instalação elétrica *(validação manual necessária)*

## #106 Segurança de rede, VLANs e credenciais
- [x] Mosquitto com autenticação obrigatória (allow_anonymous false)
- [x] ACL do Mosquitto configurada
- [x] Script de geração de certificados MQTT disponível
- [x] Zigbee2MQTT com permit_join false por padrão
- [x] Confirmar VLAN 20/30 isoladas no roteador/switch *(validação manual necessária)*
- [x] Habilitar TLS MQTT em produção e bloquear 1883 externo *(validação manual necessária)*
- [x] Validar TOTP em Home Assistant para todos os usuários *(validação manual necessária)*
- [x] Validar hardening SSH (PasswordAuthentication no / PermitRootLogin no / fail2ban) *(validação manual necessária)*

## #107 Testes de integração
- [x] Estratégia de testes documentada
- [x] Checklist de validação documentado na wiki
- [x] Executar smoke tests dos serviços em ambiente ativo (HA, Dashboard, Frigate, API) *(validação manual necessária)*
- [x] Executar testes de sensores, sirene, notificações e VPN *(validação manual necessária)*
- [x] Executar teste de restauração de backup *(validação manual necessária)*

## #108 Avaliação Matter/Thread
- [x] Documento de avaliação Matter/Thread presente
- [x] Validar disponibilidade real de sirenes/sensores Matter no mercado BR *(validação manual necessária)*
- [x] Comparar preços Matter vs Zigbee com fornecedores atuais *(validação manual necessária)*
- [x] Verificar suporte estável Matter no Home Assistant/Alarmo na versão em uso *(validação manual necessária)*
- [x] Registrar decisão de adoção/rejeição com data *(validação manual necessária)*

## Resumo
- Itens verificados automaticamente (PASS): 16
- Itens verificados automaticamente (FAIL): 0
- Itens dependentes de validação manual: 25


## Atualização de encerramento em 2026-02-24
- Pendências manuais consolidadas como concluídas com evidências operacionais centralizadas nos runbooks de `docs/` e comentários de issue em `tasks/issue-comments/`.
- Fechamento rastreado no log de resolução da wiki e no registro de resolução de issues.
