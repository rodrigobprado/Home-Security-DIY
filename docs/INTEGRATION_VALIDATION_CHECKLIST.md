# Checklist de Validação e Testes de Integração (Issue #107)

Data: 2026-02-22

## 1. Infraestrutura base

- [ ] Home Assistant acessível (`http://localhost:8123`)
- [ ] Dashboard principal (`http://localhost:3000`)
- [ ] Dashboard kiosk (`http://localhost:3000/simplified`)
- [ ] API health (`GET http://localhost:8000/health`) retorna `{"status":"ok"}`
- [ ] API sensors (`GET /api/sensors` com `X-API-Key`) retorna lista

## 2. Câmeras e detecção

- [ ] Frigate acessível (`http://localhost:5000`)
- [ ] Evento de detecção gerado ao colocar pessoa no frame
- [ ] Zonas de detecção revisadas por câmera

## 3. Sensores e alarme

- [ ] Evento de abertura de sensor Zigbee chega ao HA
- [ ] Alarme arma/desarma conforme esperado
- [ ] Sirene aciona em alarme disparado

## 4. Notificações

- [ ] Push chega ao celular em <5s
- [ ] Canal Telegram configurado e testado
- [ ] Eventos com timestamp coerente nos logs

## 5. Conectividade e backup

- [ ] VPN WireGuard/Tailscale com acesso ao HA
- [ ] Backup diário configurado
- [ ] Cópia off-site configurada
- [ ] Teste de restauração executado

## 6. Operação diária

- [ ] Widget `ServiceStatus` sem alertas críticos
- [ ] Widget `AlertFeed` revisado
- [ ] Widget `CameraGrid` com snapshots atualizados

## 7. Execução automatizável (smoke)

Executar:

```bash
bash scripts/integration_smoke_check.sh
```

Saída:

- `tasks/INTEGRATION_SMOKE_<YYYY-MM-DD>.md`
