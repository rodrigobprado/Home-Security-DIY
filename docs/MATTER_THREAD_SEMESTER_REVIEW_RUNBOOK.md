# Runbook de Revisao Semestral Matter/Thread

Issue: #142  
Ultima atualizacao: 2026-02-22

## Objetivo
Padronizar a reavaliacao semestral da estrategia Matter/Thread com decisao registrada.

## Checklist da revisao
- Verificar disponibilidade local de sirenes Matter para seguranca residencial.
- Verificar disponibilidade local de sensores criticos (fumaca, gas, abertura).
- Comparar custo total Matter vs Zigbee para o mesmo escopo.
- Validar maturidade de suporte no Home Assistant e Alarmo.
- Revisar riscos de migracao e impacto operacional.

## Decisao padrao
- `adotar`: criterios atendidos e plano de migracao aprovado.
- `postergar`: criterios nao atendidos, manter stack atual.

## Procedimento
1. Preencher `tasks/templates/matter_thread_review_template.md`.
2. Atualizar `docs/MATTER_THREAD_EVALUATION.md` com resultado.
3. Registrar decisao com data, responsavel e proxima revisao.

## Frequencia
- Revisao fixa semestral.
- Revisao extraordinaria quando houver mudanca relevante de mercado/plataforma.
