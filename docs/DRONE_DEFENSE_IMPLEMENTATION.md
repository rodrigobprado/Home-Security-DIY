# Implementacao do Modulo de Defesa Nao Letal (T-037)

Este documento descreve os limites tecnicos e operacionais da implementacao de defesa nao letal no projeto.

## Escopo de software entregue

- Armamento em modo `semi_auto` com 2 fatores: PIN + TOTP.
- Modo automatico de disparo explicitamente rejeitado.
- Janela obrigatoria de aviso pre-disparo (`warning_seconds`, padrao 5s).
- Cooldown entre disparos e limite diario de disparos.
- Bloqueio de disparo por:
  - deteccao de criancas/animais no pipeline de visao (`defense_blocked`)
  - zonas de exclusao configuraveis por ambiente
  - falha de saude operacional (health monitor)
- Auditoria imutavel em arquivo append-only com cadeia de hash SHA-256.

## Especificacao de atuador fisico (referencia para integracao)

Implementacao alvo (nao inclui montagem fisica neste repositorio):

- Atuador principal: `valvula solenoide 12V NC`
- Propelente: cartucho CO2 com valvula dedicada
- Acionamento eletrico: rele de seguranca + driver de potencia
- Trava fisica: chave de corte de energia do atuador

Interface de configuracao:

- `DEFENSE_ACTUATOR_SPEC_UGV` (ex.: `solenoid_12v_nc+co2_valve`)

## Mapeamento de topicos MQTT (UGV)

- Status de defesa: `ugv/defense/status`
- Auditoria de tentativa de disparo: `ugv/defense/audit`
- Comando principal: `ugv/command`
  - `defense_mode`
  - `defense_arm`
  - `defense_disarm`
  - `defense_fire`

## Variaveis de ambiente de seguranca

- `DEFENSE_PIN_UGV`
- `DEFENSE_TOTP_SECRET_UGV`
- `DEFENSE_WARNING_SECONDS_UGV`
- `DEFENSE_COOLDOWN_SECONDS_UGV`
- `DEFENSE_MAX_TRIGGERS_PER_DAY_UGV`
- `DEFENSE_EXCLUSION_ZONES_UGV`
- `DEFENSE_AUDIT_LOG_PATH_UGV`
  - recomendado: caminho persistente fora de `/tmp` (ex.: `/var/lib/home-security/audit/ugv_defense_audit.log`)

## Consulta juridica (registro minimo obrigatorio)

Antes de operacao em ambiente real, registrar formalmente:

1. Jurisdicao aplicavel (municipio/estado/pais).
2. Parecer juridico sobre uso de agente OC/CO2 em propriedade privada.
3. Limites operacionais aprovados (zonas, horarios, responsavel).
4. Responsavel tecnico e responsavel legal pelo sistema.
5. Data de revisao juridica e periodo de validade do parecer.

Template recomendado para registro: `docs/LEGAL_AND_ETHICS.md` + anexo interno do operador.

## Observacoes criticas

- Este projeto nao habilita disparo automatico autonomo.
- O modulo de defesa deve permanecer desativado por padrao.
- O operador e o unico responsavel por conformidade legal e uso proporcional.
