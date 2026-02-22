# Runbook de Evidencias Operacionais LGPD (Cameras)

Issue: #136  
Ultima atualizacao: 2026-02-22

## Objetivo
Padronizar a coleta de evidencias de campo para conformidade LGPD em uso de cameras.

## Checklist de campo
- Validar que cada camera monitora apenas area privada necessaria.
- Validar ausencia de enquadramento indevido de via publica/janela de terceiros.
- Registrar foto do angulo final de cada camera instalada.
- Confirmar presenca de aviso de monitoramento em locais de acesso.
- Registrar evidencia de consulta de logs de acesso a gravacoes no dashboard.

## Evidencia minima por item
- Foto com data/hora visivel ou metadata preservada.
- Identificador da camera e local (ex.: `camera.portao_frente`).
- Responsavel pela validacao.
- Resultado (`PASS`/`FAIL`) com observacao objetiva.

## Procedimento recomendado
1. Abrir checklist template em `tasks/templates/lgpd_field_evidence_template.md`.
2. Preencher item por item para cada camera.
3. Anexar fotos e capturas de tela no registro da issue.
4. Consolidar conclusao final e data de revisao.

## Frequencia
- Revisao inicial na implantacao.
- Revalidacao semestral ou apos alteracao fisica de posicionamento.
