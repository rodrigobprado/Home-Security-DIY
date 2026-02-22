# Runbook Operacional de Hardening Fisico Recorrente

Issue: #139  
Ultima atualizacao: 2026-02-22

## Objetivo
Definir rotina de inspeção física e critérios objetivos de aprovação/reprovação.

## Cadencia recomendada
- Inspeção mensal: perímetro, portas, janelas, iluminação e nobreak.
- Inspeção trimestral: aterramento, DPS e revisão completa da sala técnica.
- Inspeção extraordinária: após incidente físico ou intervenção elétrica.

## Itens críticos
- Integridade de fechamentos físicos e acesso restrito.
- Ausência de pontos cegos de iluminação/câmeras.
- Integridade elétrica (DPS/aterramento) com evidência técnica.
- Continuidade de backup off-site e recuperação de energia.

## Critérios de aprovação
- Item crítico com `FAIL` bloqueia aprovação da inspeção.
- Item não crítico com `FAIL` exige plano corretivo com prazo.
- Relatório só pode ser fechado com responsável e data.

## Procedimento
1. Executar checklist em `tasks/templates/physical_hardening_field_audit_template.md`.
2. Anexar evidências fotográficas e registros técnicos.
3. Registrar conclusão e plano de ação corretiva.
