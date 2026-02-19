# FAQ

## Geral

### Preciso de cloud para o sistema funcionar?
Não. Todo o processamento — vídeo, IA, automações, banco de dados e dashboard — é local. Nenhum dado é enviado para servidores externos.

### Posso começar sem Kubernetes?
Sim. Comece com Docker Compose (`cd src && docker compose up -d`) e migre para K3s quando precisar de maior resiliência ou escala.

### Quais protocolos o sistema usa?
MQTT (mensageria), Zigbee (sensores sem fio), RTSP/ONVIF (câmeras), WebSocket (dashboard em tempo real) e PostgreSQL (persistência).

### Quais são os requisitos mínimos de hardware?
- CPU: Intel N100 ou equivalente (iGPU para aceleração IA no Frigate)
- RAM: 8 GB (16 GB recomendado)
- Armazenamento: SSD para sistema + HDD dedicado para gravações Frigate

---

## Dashboard

### Como acesso o dashboard?
- Modo completo: `http://localhost:3000` (dev) ou `http://dashboard.home.local` (prod)
- Modo kiosk (TV): `http://localhost:3000/simplified`

### O dashboard perde conexão às vezes. O que fazer?
O hook `useWebSocket` reconecta automaticamente com backoff exponencial. Se o problema persistir, verifique se o `dashboard-api` está saudável: `curl http://localhost:8000/health`.

### Como adicionar dispositivos ao mapa operacional?
As posições são carregadas de `GET /api/map/devices` (tabela `dashboard.device_positions` no PostgreSQL). Insira ou edite diretamente no banco, ou aguarde uma futura interface de configuração.

---

## PostgreSQL

### Por que usar PostgreSQL em vez de SQLite?
O Home Assistant usa SQLite por padrão, mas para ambientes com múltiplos acessos simultâneos (dashboard, métricas, backups) e retenção de histórico longo, o PostgreSQL oferece melhor performance, concorrência e confiabilidade.

### Como acesso o banco de dados diretamente?
```bash
# Docker
docker exec -it home-security-postgres psql -U postgres homedb

# Ver alertas do dashboard
\c homedb
SET search_path = dashboard;
SELECT * FROM alert ORDER BY timestamp DESC LIMIT 20;
```

---

## Drones

### O módulo de drones é obrigatório?
Não. É uma camada avançada e totalmente opcional. O sistema funciona completamente sem UGV/UAV.

### Quais regulamentações se aplicam ao UAV?
No Brasil: ANAC (registro de drones) e DECEA (autorização de voo). Consulte `docs/LEGAL_AND_ETHICS.md`.

---

## Contribuição

### Como contribuir?
Abra issues ou Pull Requests no repositório. Siga as diretrizes em `CONTRIBUTING.md`.

### Como reportar uma vulnerabilidade de segurança?
Consulte `SECURITY.md` no repositório para o processo de disclosure responsável.
