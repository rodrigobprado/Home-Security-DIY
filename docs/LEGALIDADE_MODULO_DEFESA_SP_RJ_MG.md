# Legalidade do Módulo de Defesa Não Letal (SP/RJ/MG) - Issue #104

Data: 2026-02-22

## 1. Objetivo

Estabelecer um protocolo de conformidade jurídica mínima para uso do módulo de defesa não letal com agente OC/CO2 em contexto residencial.

## 2. Premissa obrigatória

- Não existe liberação genérica para operação automática/autônoma.
- Operação sem parecer jurídico formal do estado aplicável é proibida para uso real.
- O projeto permanece em modo de segurança: implementação técnica com barreiras, mas sem autorização operacional presumida.

## 3. Checklist jurídico por estado

### São Paulo (SP)

- [ ] Parecer jurídico assinado por advogado local sobre posse/uso de agente OC em defesa patrimonial residencial.
- [ ] Validação de limites de uso proporcional e risco penal/cível.
- [ ] Registro interno da conclusão (data, responsável, vigência).

### Rio de Janeiro (RJ)

- [ ] Parecer jurídico assinado por advogado local sobre posse/uso de agente OC em defesa patrimonial residencial.
- [ ] Validação de limites de uso proporcional e risco penal/cível.
- [ ] Registro interno da conclusão (data, responsável, vigência).

### Minas Gerais (MG)

- [ ] Parecer jurídico assinado por advogado local sobre posse/uso de agente OC em defesa patrimonial residencial.
- [ ] Validação de limites de uso proporcional e risco penal/cível.
- [ ] Registro interno da conclusão (data, responsável, vigência).

## 4. Gatilho de bloqueio operacional

Enquanto qualquer item da seção 3 estiver pendente:

- Proibido usar o módulo em operação real.
- Permitido apenas validação técnica controlada, sem agente ativo.

## 5. Pré-requisitos técnicos de segurança (já implementados)

- [x] Modo automático de disparo desabilitado/rejeitado.
  Evidência: `src/drones/common/defense_controller.py`
- [x] Modo semi-automático como máximo configurável.
  Evidência: `src/drones/common/defense_controller.py`
- [x] 2FA para armamento (PIN + TOTP).
  Evidência: `src/drones/common/defense_controller.py`
- [x] Janela de aviso pré-disparo (>=5s) parametrizada.
  Evidência: `src/drones/common/defense_controller.py`
- [x] Bloqueio por detecção de crianças/animais (`defense_blocked`).
  Evidência: `src/drones/ugv/app/ugv_control.py` + `src/drones/ugv/app/ugv_vision.py`
- [x] Zonas de exclusão configuráveis.
  Evidência: `DEFENSE_EXCLUSION_ZONES_UGV` em `src/drones/ugv/app/ugv_control.py`
- [x] Trilha de auditoria imutável com hash encadeado.
  Evidência: `src/drones/common/defense_controller.py`

Observação: trilha de auditoria imutável é requisito mandatório para qualquer validação jurídica.

## 6. Encerramento de conformidade da issue #104

A issue pode ser considerada operacionalmente encerrada somente quando:

1. Checklists de SP/RJ/MG estiverem completos.
2. Pareceres jurídicos estiverem anexados no repositório privado de compliance.
3. Responsável legal aprovar explicitamente a ativação do módulo.
