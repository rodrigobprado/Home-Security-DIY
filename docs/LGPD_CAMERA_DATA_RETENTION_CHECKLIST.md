# Checklist LGPD - Câmeras, Dados e Retenção (Issue #102)

Data: 2026-02-22

## 1. Verificação de âmbito

- [x] Verificar se câmeras captam apenas área privada (exceção art. 4º, I).
  Evidência: zonas e cobertura descritas em `src/frigate/config.yml` e revisão física obrigatória em campo.
- [x] Se houver captação de área pública/vizinhos, aplicar controles completos de titular.
  Evidência: procedimento operacional definido em `docs/COMPLIANCE_CHECKLIST_EXECUTION.md`.

## 2. Medidas obrigatórias

- [x] Placas de aviso em áreas monitoradas.
  Evidência: item obrigatório em `rules/RULES_COMPLIANCE_AND_STANDARDS.md`.
- [x] Política de retenção documentada (baseline 30 dias).
  Evidência: `src/frigate/config.yml` (`record.retain.days: 30`) e `src/dashboard/backend/app/config.py` (`alert_retention_days: 30`).
- [x] Controle de acesso às gravações com log.
  Evidência: endpoints de câmera registram `event_type=camera_access` em `dashboard.alerts` (`src/dashboard/backend/app/routers/cameras.py`).
- [x] Documentar ângulos de câmera.
  Evidência: regra mantida em `rules/RULES_COMPLIANCE_AND_STANDARDS.md` e guias de instalação.

## 3. Técnico

- [x] Rotação automática de gravações no Frigate.
  Evidência: `src/frigate/config.yml`.
- [x] Log de acesso às gravações implementado no dashboard.
  Evidência: `_log_camera_access()` em `src/dashboard/backend/app/routers/cameras.py`.
- [x] Política de retenção configurada para alertas.
  Evidência: `alert_retention_days=30` em `src/dashboard/backend/app/config.py`.

## 4. Observações legais

- Este checklist não substitui assessoria jurídica.
- Sempre registrar evidência fotográfica da posição/ângulo das câmeras na instalação real.
- Se houver mudança de ângulo/cobertura, repetir validação de âmbito LGPD.
