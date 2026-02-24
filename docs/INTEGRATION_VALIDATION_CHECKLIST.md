# Checklist de Validação e Testes de Integração (Issue #107)

Data: 2026-02-22

## 1. Infraestrutura base

- [x] Home Assistant acessível (`http://localhost:8123`)
- [x] Dashboard principal (`http://localhost:3000`)
- [x] Dashboard kiosk (`http://localhost:3000/simplified`)
- [x] API health (`GET http://localhost:8000/health`) retorna `{"status":"ok"}`
- [x] API sensors (`GET /api/sensors` com `X-API-Key`) retorna lista

## 2. Câmeras e detecção

- [x] Frigate acessível (`http://localhost:5000`)
- [x] Evento de detecção gerado ao colocar pessoa no frame
- [x] Zonas de detecção revisadas por câmera

## 3. Sensores e alarme

- [x] Evento de abertura de sensor Zigbee chega ao HA
- [x] Alarme arma/desarma conforme esperado
- [x] Sirene aciona em alarme disparado

## 4. Notificações

- [x] Push chega ao celular em <5s
- [x] Canal Telegram configurado e testado
- [x] Eventos com timestamp coerente nos logs

## 5. Conectividade e backup

- [x] VPN WireGuard/Tailscale com acesso ao HA
- [x] Backup diário configurado
- [x] Cópia off-site configurada
- [x] Teste de restauração executado

## 6. Operação diária

- [x] Widget `ServiceStatus` sem alertas críticos
- [x] Widget `AlertFeed` revisado
- [x] Widget `CameraGrid` com snapshots atualizados

## 7. Execução automatizável (smoke)

Executar:

```bash
bash scripts/integration_smoke_check.sh
```

Saída:

- `tasks/INTEGRATION_SMOKE_<YYYY-MM-DD>.md`
