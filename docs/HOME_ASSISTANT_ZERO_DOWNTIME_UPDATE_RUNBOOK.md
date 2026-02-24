# Runbook: Atualização do Home Assistant sem Downtime

## Objetivo
Atualizar Home Assistant minimizando indisponibilidade operacional.

## Estratégia
Blue/Green lógico com validação prévia e rollback rápido.

## Escopo
- Ambiente Docker Compose (desenvolvimento/homologação).
- Ambiente K3s (produção).
- Fluxo com canário curto, smoke tests e rollback imediato.

## Pré-check
1. Confirmar backup recente de configuração.
2. Confirmar banco PostgreSQL saudável.
3. Validar integração MQTT e Frigate.
4. Anunciar janela de mudança.
5. Registrar versão atual (`docker inspect` ou `kubectl get deploy`).

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

## Procedimento (K3s / Produção)
1. Atualizar tag da imagem no deployment:
```bash
kubectl -n home-security set image deploy/homeassistant homeassistant=ghcr.io/home-assistant/home-assistant:<nova-tag>
```
2. Acompanhar rollout:
```bash
kubectl -n home-security rollout status deploy/homeassistant --timeout=180s
```
3. Verificar readiness e eventos:
```bash
kubectl -n home-security get pods -l app=homeassistant -o wide
kubectl -n home-security describe deploy/homeassistant
```
4. Executar smoke tests pós-rollout:
```bash
curl -fsS https://homeassistant-home-security.toca.lan/ >/dev/null
curl -fsS http://localhost:8000/api/services/status >/dev/null
```

## Rollback
1. Reverter para imagem anterior conhecida.
2. Subir container com tag anterior.
3. Restaurar snapshot caso necessário.

### Rollback Compose
```bash
cd src
docker compose up -d --no-deps homeassistant
```

### Rollback K3s
```bash
kubectl -n home-security rollout undo deploy/homeassistant
kubectl -n home-security rollout status deploy/homeassistant --timeout=180s
```

## SLO de mudança
- Downtime máximo aceitável: 2 minutos.
- Tempo máximo de rollback: 5 minutos.

## Critérios de sucesso
- Serviço com `healthcheck` estável por 10 minutos após mudança.
- `ServiceStatus` no dashboard sem degradação para Home Assistant.
- Fluxos críticos funcionando: arme/desarme, eventos MQTT e webhook de alerta.

## Evidência obrigatória
- Versão anterior/nova
- Horários início/fim
- Resultado dos smoke tests
- Ação de rollback (se aplicável)
