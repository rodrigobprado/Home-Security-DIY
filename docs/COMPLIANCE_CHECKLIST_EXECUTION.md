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
- Automatizado: checklist e auditoria técnica dedicada adicionados.
- Evidencias: `docs/NETWORK_SECURITY_VLAN_CREDENTIALS_CHECKLIST.md` e `scripts/network_security_audit.sh`.
- Manual pendente: isolamento real de VLANs, TLS MQTT em producao e hardening de SSH/TOTP.

### #107 - Testes de integracao
- Automatizado: checklist consolidado e script de smoke test adicionados.
- Evidencias: `docs/INTEGRATION_VALIDATION_CHECKLIST.md` e `scripts/integration_smoke_check.sh`.
- Manual pendente: execucao em ambiente ativo (HA, Dashboard, Frigate, API, sensores, VPN).

### #108 - Matter/Thread
- Automatizado: decisao operacional registrada com checklist objetivo.
- Evidencias: `docs/MATTER_THREAD_EVALUATION.md` e `docs/MATTER_THREAD_DECISION_2026-02-22.md`.
- Resultado atual: manter Zigbee e reavaliar em 6 meses.

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

## Gate de compliance no CI (T-046)
- Workflow: `.github/workflows/compliance-gates.yml`
- Gatilhos: `pull_request` e `push` para `main` (alem de `workflow_dispatch`)
- O que executa:
- `scripts/physical_hardening_audit.sh`
- `scripts/network_security_audit.sh`
- `scripts/integration_smoke_check.sh`
- testes de contrato:
- `tests/backend/test_lgpd_compliance_contract.py`
- `tests/backend/test_drone_regulatory_compliance_contract.py`
- `tests/backend/test_defense_legality_compliance_contract.py`
- `tests/backend/test_physical_hardening_compliance_contract.py`
- `tests/backend/test_network_security_compliance_contract.py`
- `tests/backend/test_integration_checklist_contract.py`
- `tests/backend/test_matter_thread_decision_contract.py`

### Politica de bloqueio
- O workflow falha se os relatorios estruturais (`PHYSICAL_HARDENING_AUDIT` e `NETWORK_SECURITY_AUDIT`) contiverem item `FAIL`.
- O relatorio `INTEGRATION_SMOKE` e executado no CI como evidencia operacional; falhas ali devem ser tratadas no plano de integracao do ambiente.
- Itens `WARN` nao bloqueiam merge, mas exigem tratativa operacional/documental.

### Evidencias no CI
- Artifact publicado: `compliance-gate-report`
- Conteudo: relatorios `*.md`, logs de execucao e `compliance-gate-summary.txt`

## Backlog operacional aberto em 2026-02-22
- #136: evidencias operacionais LGPD em `docs/LGPD_OPERATIONAL_EVIDENCE_RUNBOOK.md`
- #137: evidencias regulatorias UAV em `docs/UAV_REGULATORY_EVIDENCE_RUNBOOK.md`
- #138: evidencias juridicas do modulo de defesa em `docs/DEFENSE_LEGAL_EVIDENCE_RUNBOOK.md`
- #139: runbook de hardening fisico recorrente em `docs/PHYSICAL_HARDENING_OPERATIONS_RUNBOOK.md`
- #140: validacao de rede em producao em `docs/NETWORK_PRODUCTION_VALIDATION_PLAYBOOK.md`
- #141: smoke de integracao em ambiente real em `docs/INTEGRATION_SMOKE_PRODUCTION_RUNBOOK.md`
