# Home Security DIY Wiki

Bem-vindo à wiki do **Home Security DIY** — sistema de segurança residencial open source com processamento 100% local, sem dependência de cloud.

## Visão geral

O projeto combina automação, vídeo inteligente, sensores e drones para segurança em camadas:

| Serviço | Função |
|---|---|
| **Home Assistant** | Automações, alarme (Alarmo) e integrações |
| **Frigate** | NVR com detecção de objetos por IA (OpenVINO) |
| **Zigbee2MQTT** | Bridge Zigbee → MQTT para sensores sem fio |
| **Mosquitto** | Broker MQTT — barramento de eventos |
| **PostgreSQL 16** | Banco de dados central (schemas isolados por serviço) |
| **Dashboard** | Interface operacional React (modo completo + kiosk) |
| **Docker / K3s** | Execução em dev (Compose) e prod (K3s) |

## Comece por aqui

1. [Instalação Rápida](Instalacao-Rapida)
2. [Arquitetura](Arquitetura)
3. [Operação e Manutenção](Operacao-e-Manutencao)
4. [Drones Autônomos](Drones-Autonomos)
5. [Segurança e Compliance](Seguranca-e-Compliance)
6. [FAQ](FAQ)

## Escopo do projeto

- Cenários residenciais: **Rural, Urbano e Apartamento**
- Defesa em profundidade: camadas passiva, ativa e reativa
- Privacidade por design: sem cloud obrigatório
- Infraestrutura como código: Docker Compose (dev) + Kustomize/K3s (prod)

## Status das implementações

| Issue | Descrição | Status |
|---|---|---|
| #1 | Persistência dos dados (PostgreSQL) | ✅ Concluído |
| #2 | Dashboard operacional (FastAPI + React) | ✅ Concluído |

## Atualizações recentes (Fev/2026)

- Autenticação obrigatória por `X-API-Key`/Bearer na Dashboard API (REST e WebSocket).
- CI com validação Kubernetes via `kubeconform` (sem dependência de cluster).
- Workflow Snyk com execução condicional quando `SNYK_TOKEN` não está configurado.
- Testes backend do dashboard adicionados ao pipeline (`backend-quality`).
- Observabilidade WebSocket: endpoint `GET /api/services/ws-metrics`.
- Política de retenção de alertas com script de limpeza (`scripts/cleanup_alerts.py`).
- Validação automática de links Markdown no CI (`docs-links`).

## Documentação no repositório

- `README.md` — visão geral e quickstart
- `docs/` — arquitetura, hardening, threat model, ADRs
- `prd/` — Product Requirements Documents
- `k8s/docs/` — guias de deploy em K3s
