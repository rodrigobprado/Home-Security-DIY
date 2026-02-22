# Execucao das Tarefas de Compliance e Checklists

Data: 2026-02-22
Escopo: Issues `#102` a `#108`

## Objetivo
Consolidar a execucao das tarefas de compliance/checklist em duas frentes:
1. O que pode ser validado por codigo/repositorio (automatizado).
2. O que exige validacao juridica, fisica ou operacional em ambiente real.

## Entregas tecnicas realizadas
1. Retencao padrao de alertas do backend ajustada para 30 dias (baseline LGPD/CFTV).
Arquivo: `src/dashboard/backend/app/config.py`
2. Zigbee2MQTT travado com `permit_join: false` por padrao.
Arquivo: `src/zigbee2mqtt/configuration.yaml`
3. Auditoria semiautomatica criada para as issues `#102` a `#108`.
Arquivo: `scripts/compliance_checklist_audit.sh`
4. Relatorio de status gerado com pass/fail e pendencias manuais.
Arquivo: `tasks/COMPLIANCE_CHECKLIST_AUDIT_2026-02-22.md`

## Status por issue
### #102 - LGPD (cameras, dados e retencao)
- Automatizado: politica de retencao validada em Frigate e backend.
- Automatizado: log operacional de acesso as cameras implementado na API do dashboard.
- Evidencias centralizadas em `docs/LGPD_CAMERA_DATA_RETENTION_CHECKLIST.md`.
- Manual pendente: verificacao fisica de angulo de cameras e placas no local instalado.

### #103 - ANAC/SISANT/DECEA/ANATEL
- Automatizado: base regulatoria e regras documentadas.
- Automatizado: guard-rails de altitude/geofence/RTH adicionados no bridge UAV.
- Evidencias centralizadas em `docs/DRONE_REGULATORY_COMPLIANCE_BR.md`.
- Manual pendente: peso real do UAV, cadastros oficiais e checagem de espaco aereo local.

### #104 - Modulo de defesa nao letal
- Automatizado: restricoes de HITL e bloqueio de disparo automatico documentados.
- Automatizado: pre-requisitos tecnicos de seguranca implementados no controlador de defesa (2FA, aviso pre-disparo, zonas de exclusao, trilha imutavel).
- Evidencias centralizadas em `docs/LEGALIDADE_MODULO_DEFESA_SP_RJ_MG.md`.
- Manual pendente: parecer juridico por UF (SP/RJ/MG) e aprovacao legal formal para uso real.

### #105 - Seguranca fisica e hardening
- Automatizado: checklist consolidado e auditoria tecnica local adicionados.
- Evidencias: `docs/SEGURANCA_FISICA_HARDENING_CHECKLIST.md` e `scripts/physical_hardening_audit.sh`.
- Manual pendente: validacao de campo (perimetro, nobreak, DPS e aterramento).

### #106 - Rede, VLANs e credenciais
- Automatizado: autenticacao MQTT, ACL e `permit_join: false`.
- Manual pendente: isolamento real de VLANs, TLS MQTT em producao e hardening de SSH/TOTP.

### #107 - Testes de integracao
- Automatizado: estrategia de testes e checklist documentados.
- Manual pendente: execucao em ambiente ativo (HA, Dashboard, Frigate, API, sensores, VPN).

### #108 - Matter/Thread
- Automatizado: documento de avaliacao presente.
- Manual pendente: validacao de mercado BR, preco, maturidade de suporte e decisao final.

## Como executar a auditoria
```bash
bash scripts/compliance_checklist_audit.sh
```

Saida:
- `tasks/COMPLIANCE_CHECKLIST_AUDIT_<YYYY-MM-DD>.md`

## Criterio de conclusao para fechar cada issue
1. Todos os itens automatizados em PASS.
2. Itens manuais com evidencia objetiva anexada na issue:
- foto/diagrama para itens fisicos;
- output de comando/config para itens tecnicos;
- link de norma/parecer para itens juridicos;
- logs de teste para itens operacionais.
3. Comentario final na issue com evidencias + data da validacao.
