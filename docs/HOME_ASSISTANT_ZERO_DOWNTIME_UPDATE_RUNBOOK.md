# Runbook: Atualização do Home Assistant sem Downtime

## Objetivo
Atualizar Home Assistant minimizando indisponibilidade operacional.

## Estratégia
Blue/Green lógico com validação prévia e rollback rápido.

## Pré-check
1. Confirmar backup recente de configuração.
2. Confirmar banco PostgreSQL saudável.
3. Validar integração MQTT e Frigate.
4. Anunciar janela de mudança.

## Procedimento (Compose)
1. Baixar imagem nova sem trocar container ativo:
```bash
cd src
docker compose pull homeassistant
```
2. Executar validação de configuração em instância de teste:
```bash
docker compose run --rm --no-deps homeassistant python -m homeassistant --script check_config --config /config
```
3. Aplicar troca controlada:
```bash
docker compose up -d --no-deps homeassistant
```
4. Validar saúde pós-troca:
```bash
curl -fsS http://localhost:8123/ >/dev/null
```
5. Validar automações críticas (alarme, MQTT, notificações).

## Rollback
1. Reverter para imagem anterior conhecida.
2. Subir container com tag anterior.
3. Restaurar snapshot caso necessário.

## SLO de mudança
- Downtime máximo aceitável: 2 minutos.
- Tempo máximo de rollback: 5 minutos.

## Evidência obrigatória
- Versão anterior/nova
- Horários início/fim
- Resultado dos smoke tests
- Ação de rollback (se aplicável)
