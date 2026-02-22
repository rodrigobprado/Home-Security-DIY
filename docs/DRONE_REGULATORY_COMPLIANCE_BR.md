# Compliance Regulatório de Drones (BR) - ANAC, SISANT/DECEA e ANATEL

Data: 2026-02-22  
Issue: #103

## 1. Escopo

Checklist regulatório para operação de UAV no projeto Home Security DIY, incluindo:

- Registro e classificação ANAC/SISANT
- Restrições de espaço aéreo (DECEA)
- Homologação de rádio (ANATEL)
- Regras operacionais mínimas (VLOS, distância de terceiros, altitude, geofence, RTH)

## 2. Itens com suporte técnico implementado no repositório

- [x] Limite de altitude AGL configurável no bridge UAV  
  Evidência: `MAX_ALTITUDE_M_AGL_UAV` em `src/drones/uav/mavlink_bridge.py`
- [x] Geofence configurável no bridge UAV  
  Evidência: `GEOFENCE_MIN_*` e `GEOFENCE_MAX_*` em `src/drones/uav/mavlink_bridge.py`
- [x] RTH automático por bateria baixa  
  Evidência: `RTH_BATTERY_THRESHOLD_UAV` em `src/drones/uav/mavlink_bridge.py`
- [x] Failover de link publicado para monitoramento  
  Evidência: `uav/link/state` em `src/drones/uav/mavlink_bridge.py`
- [x] Flags de compliance publicadas no status  
  Evidência: campo `compliance` em `uav/status`

## 3. Itens obrigatórios com validação operacional/manual

- [ ] Verificar peso real do UAV e classe aplicável (>250g exige registro)
- [ ] Registrar UAV no sistema ANAC/SISANT e manter documentação
- [ ] Cadastrar operação no DECEA quando aplicável (incluindo CTR)
- [ ] Confirmar homologação ANATEL dos módulos de rádio instalados
- [ ] Comprovar RETA para operação não recreativa quando aplicável
- [ ] Garantir VLOS em toda operação (ou autorização específica BVLOS)
- [ ] Garantir distância mínima de 30m de pessoas não anuentes
- [ ] Confirmar luzes de navegação para operação noturna

## 4. Procedimento mínimo antes de cada voo operacional

1. Confirmar enquadramento legal da operação (VLOS/área/autorização).
2. Validar geofence e limite de altitude carregados no sistema.
3. Confirmar modo de fail-safe/RTH ativo.
4. Confirmar checklist pré-voo do UAV em `docs/GUIA_MONTAGEM_UAV.md`.
5. Registrar evidências (print de configuração + registro de voo).

## 5. Referências internas

- `standards/STANDARDS_TO_RESEARCH.md`
- `rules/RULES_COMPLIANCE_AND_STANDARDS.md`
- `docs/LEGAL_AND_ETHICS.md`
- `docs/GUIA_MONTAGEM_UAV.md`
