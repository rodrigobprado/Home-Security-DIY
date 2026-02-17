# Instalação Rápida

## Desenvolvimento (Docker Compose)

```bash
git clone https://github.com/rodrigobprado/Home-Security-DIY.git
cd Home-Security-DIY/src
cp .env.example .env
docker compose up -d
```

Acessos padrão:

- Home Assistant: `http://localhost:8123`
- Frigate: `http://localhost:5000`

Guia detalhado: `src/docs/QUICK_START.md`.

## Produção (K3s)

```bash
./scripts/deploy.sh production
```

Guia detalhado: `k8s/docs/K3S_SETUP.md`.

## Pré-requisitos recomendados

- Host Linux com Docker (dev) ou K3s (prod).
- Rede local estável e segmentação para IoT.
- Câmeras RTSP/ONVIF e broker MQTT ativo.
