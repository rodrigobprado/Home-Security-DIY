# Instalação Rápida

## Pré-requisitos

- Linux 64-bit (testado em Debian 12 / Ubuntu 22.04)
- Docker Engine ≥ 24 + Docker Compose v2
- 8 GB RAM mínimo, 16 GB recomendado
- Câmeras RTSP/ONVIF e coordenador Zigbee USB (ex.: Sonoff ZBDongle-P)

## Desenvolvimento (Docker Compose)

```bash
# 1. Clone o repositório
git clone https://github.com/rodrigobprado/Home-Security-DIY.git
cd Home-Security-DIY/src

# 2. Configure as variáveis de ambiente
cp .env.example .env
nano .env   # edite senhas, IPs das câmeras e HA_TOKEN

# 3. Suba o stack completo
docker compose up -d

# 4. Aguarde os serviços ficarem saudáveis (~60s)
docker compose ps
```

### Variáveis obrigatórias no `.env`

| Variável | Descrição |
|---|---|
| `POSTGRES_PASSWORD` | Senha do admin PostgreSQL |
| `POSTGRES_HA_PASSWORD` | Senha do usuário `ha_user` |
| `POSTGRES_DASHBOARD_PASSWORD` | Senha do usuário `dashboard_user` |
| `MQTT_USER` / `MQTT_PASSWORD` | Credenciais MQTT |
| `HA_HOST` | IP do host onde o Home Assistant roda |
| `HA_TOKEN` | Long-lived access token do Home Assistant |
| `DASHBOARD_API_KEY` | Chave de API do dashboard (`openssl rand -hex 32`) |
| `FRIGATE_CAM_*_URL` | URLs RTSP das câmeras (com credenciais reais de cada câmera) |
| `DEFENSE_PIN_UGV` | PIN de defesa do UGV (obrigatório se UGV em uso) |
| `DEFENSE_PIN_UAV` | PIN de defesa do UAV (obrigatório se UAV em uso) |
| `COMMAND_HMAC_SECRET_UGV` | Secret HMAC para comandos MQTT do UGV (`openssl rand -hex 32`) |
| `COMMAND_HMAC_SECRET_UAV` | Secret HMAC para comandos MQTT do UAV (`openssl rand -hex 32`) |

> **Atenção de segurança:** Substitua **todos** os valores `CHANGE_ME_*` antes de subir o stack. O sistema recusa inicializar com valores padrão ou em branco.

```bash
# Gerar secrets seguros rapidamente
echo "DASHBOARD_API_KEY=$(openssl rand -hex 32)"
echo "COMMAND_HMAC_SECRET_UGV=$(openssl rand -hex 32)"
echo "COMMAND_HMAC_SECRET_UAV=$(openssl rand -hex 32)"
```

### URLs de acesso

| Serviço | URL |
|---|---|
| Home Assistant | `http://localhost:8123` |
| Frigate NVR | `http://localhost:5000` |
| Zigbee2MQTT | `http://localhost:8080` |
| Dashboard (completo) | `http://localhost:3000` |
| Dashboard (kiosk) | `http://localhost:3000/simplified` |
| Dashboard API | `http://localhost:8000` |
| Dashboard Healthcheck | `http://localhost:8000/health` |

> **Dica:** Para gerar o `HA_TOKEN`, acesse Home Assistant → Perfil → Tokens de acesso de longa duração.

## Produção (K3s)

```bash
# Deploy completo
./scripts/deploy.sh production

# Validar manifests antes do deploy
kubectl kustomize k8s/overlays/production
```

### Entradas DNS (produção)

Adicione ao DNS local ou `/etc/hosts`:

```
192.168.10.X  security.home.local
192.168.10.X  frigate.home.local
192.168.10.X  zigbee.home.local
192.168.10.X  dashboard.home.local
```

## Verificação pós-instalação

```bash
# Docker Compose
docker compose ps                          # todos healthy

# Health (sem autenticação)
curl http://localhost:8000/health          # {"status":"ok"}

# API protegida (exige DASHBOARD_API_KEY)
API_KEY=$(grep DASHBOARD_API_KEY src/.env | cut -d= -f2)
curl -H "X-API-Key: $API_KEY" http://localhost:8000/api/sensors     # lista de entidades HA

# Verificar security headers do nginx
curl -I http://localhost:3000 | grep -E "X-Frame|Content-Security|Strict-Transport"

# K3s
kubectl get pods -n home-security          # todos Running
kubectl logs -n home-security deployment/dashboard-api
```

## Solução de Problemas Comuns

| Sintoma | Causa provável | Solução |
|---------|----------------|---------|
| Container não sobe | Variável de ambiente faltando | Comparar `.env` com `.env.example` |
| Frigate sem stream | URL RTSP incorreta | Verificar `FRIGATE_CAM_*_URL` no `.env` |
| Zigbee offline | Dongle USB não detectado | Verificar `/dev/ttyUSB*` + permissões |
| Dashboard sem dados | `HA_TOKEN` inválido ou expirado | Gerar novo token no perfil do HA |
| Dashboard API retorna 403 | `DASHBOARD_API_KEY` ausente ou errado | Verificar `DASHBOARD_API_KEY` no `.env` e usar header `X-API-Key` |
| MQTT sem conexão | Credenciais incorretas | Verificar `MQTT_USER`/`MQTT_PASSWORD` |
| UGV/UAV rejeitam comandos | `COMMAND_HMAC_SECRET_*` não configurado | Verificar variáveis no `.env` e `docker-compose.ugv.yml` |
| K8s pods em `Pending` | Recurso insuficiente | `kubectl describe pod <nome>` |

```bash
# Verificar logs de um serviço específico
docker compose logs -f dashboard-api

# Reiniciar um serviço
docker compose restart homeassistant

# Ver todos os containers e status
docker compose ps
```

## Guias Detalhados

- Docker: `src/docs/QUICK_START.md`
- K3s: `k8s/docs/K3S_SETUP.md`

## Contribuindo com o Projeto

### Estrutura do repositório

```
Home-Security-DIY/
├── src/            # Docker Compose stack (desenvolvimento)
├── k8s/            # Kubernetes/K3s stack (produção)
├── docs/           # Documentação técnica e ADRs
├── prd/            # Product Requirements Documents
├── scripts/        # Scripts de automação e validação
└── .github/        # CI/CD com GitHub Actions
```

### Fluxo de contribuição

```bash
# 1. Fork e clone
git clone https://github.com/rodrigobprado/Home-Security-DIY.git

# 2. Criar branch
git checkout -b feat/descricao-curta

# 3. Fazer alterações

# 4. Validar
./scripts/validate-configs.sh

# 5. Commit (Conventional Commits)
git commit -m "feat: adiciona suporte a sensor X"

# 6. Abrir Pull Request
```

### Nomenclatura de dispositivos

| Tipo | Formato | Exemplo |
|------|---------|---------|
| Sensor de porta | `sensor_porta_{local}` | `sensor_porta_entrada` |
| Câmera | `cam_{local}` | `cam_entrada` |
| Sirene | `sirene_{tipo}` | `sirene_interna` |
