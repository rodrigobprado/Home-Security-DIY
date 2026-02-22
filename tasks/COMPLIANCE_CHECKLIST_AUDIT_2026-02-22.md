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
- [ ] Validar se ângulos das câmeras captam somente área privada *(validação manual necessária)*
- [ ] Instalar placas físicas de aviso nas áreas monitoradas (quando aplicável) *(validação manual necessária)*
- [ ] Validar log de acesso às gravações em ambiente operacional *(validação manual necessária)*

## #103 Regulamentação de drones (ANAC/SISANT/DECEA/ANATEL)
- [x] Documentação regulatória ANAC/DECEA presente
- [x] Regras operacionais de drones publicadas
- [ ] Confirmar peso real do UAV e exigência de registro (>250g) *(validação manual necessária)*
- [ ] Realizar cadastro do operador e da aeronave no SISANT/DECEA *(validação manual necessária)*
- [ ] Verificar zona aérea local (CTR/NOTAM) antes de operação *(validação manual necessária)*
- [ ] Configurar geofence e limite de altitude no firmware/software de voo *(validação manual necessária)*

## #104 Legalidade do módulo de defesa não letal
- [x] Restrições legais e éticas do módulo documentadas
- [x] Regra de bloqueio de disparo automático documentada
- [ ] Consulta jurídica formal sobre uso de OC em SP/RJ/MG *(validação manual necessária)*
- [ ] Implementar e validar 2FA para armamento (PIN + TOTP) *(validação manual necessária)*
- [ ] Validar bloqueio por detecção de crianças/animais em ambiente real *(validação manual necessária)*
- [ ] Configurar e testar zonas de exclusão de disparo *(validação manual necessária)*

## #105 Segurança física e hardening
- [x] Guia de hardening anti-tamper disponível
- [x] Checklist de segurança física documentado
- [ ] Validar perímetro físico, portas, janelas, iluminação e paisagismo em campo *(validação manual necessária)*
- [ ] Aplicar LUKS + Dropbear no servidor instalado *(validação manual necessária)*
- [ ] Validar nobreak real e backup off-site funcional *(validação manual necessária)*
- [ ] Inspecionar DPS e aterramento da instalação elétrica *(validação manual necessária)*

## #106 Segurança de rede, VLANs e credenciais
- [x] Mosquitto com autenticação obrigatória (allow_anonymous false)
- [x] ACL do Mosquitto configurada
- [x] Script de geração de certificados MQTT disponível
- [x] Zigbee2MQTT com permit_join false por padrão
- [ ] Confirmar VLAN 20/30 isoladas no roteador/switch *(validação manual necessária)*
- [ ] Habilitar TLS MQTT em produção e bloquear 1883 externo *(validação manual necessária)*
- [ ] Validar TOTP em Home Assistant para todos os usuários *(validação manual necessária)*
- [ ] Validar hardening SSH (PasswordAuthentication no / PermitRootLogin no / fail2ban) *(validação manual necessária)*

## #107 Testes de integração
- [x] Estratégia de testes documentada
- [x] Checklist de validação documentado na wiki
- [ ] Executar smoke tests dos serviços em ambiente ativo (HA, Dashboard, Frigate, API) *(validação manual necessária)*
- [ ] Executar testes de sensores, sirene, notificações e VPN *(validação manual necessária)*
- [ ] Executar teste de restauração de backup *(validação manual necessária)*

## #108 Avaliação Matter/Thread
- [x] Documento de avaliação Matter/Thread presente
- [ ] Validar disponibilidade real de sirenes/sensores Matter no mercado BR *(validação manual necessária)*
- [ ] Comparar preços Matter vs Zigbee com fornecedores atuais *(validação manual necessária)*
- [ ] Verificar suporte estável Matter no Home Assistant/Alarmo na versão em uso *(validação manual necessária)*
- [ ] Registrar decisão de adoção/rejeição com data *(validação manual necessária)*

## Resumo
- Itens verificados automaticamente (PASS): 16
- Itens verificados automaticamente (FAIL): 0
- Itens dependentes de validação manual: 25
