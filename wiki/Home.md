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
- Compliance operacional (LGPD, UAV, defesa, hardening físico, rede, integração e Matter/Thread) com runbooks e templates versionados.
- Pipeline dedicado `compliance-gates.yml` com artifacts e bloqueio de merge para não conformidades estruturais.
- Hardening de Kubernetes no Zigbee2MQTT com remoção de `privileged: true` e baseline de segurança de container.
- Suíte backend executada integralmente em ambiente reprodutível com `.venv` (`79 testes passando` em 2026-02-22).
- Novos runbooks operacionais publicados: backup/restore PostgreSQL, atualização sem downtime do Home Assistant e transição mock->hardware dos drones.
- Política de SLO/SLA dos serviços críticos publicada em `docs/SLOS_SLAS_CRITICAL_SERVICES.md`.
- ADRs 005-010 formalizados em `docs/adr/`.
- Changelog versionado na raiz do projeto (`CHANGELOG.md`).
- Estratégia de secrets no Kubernetes com External Secrets em produção (`k8s/overlays/production/external-secrets.yaml`).

## Documentação no repositório

- `README.md` — visão geral e quickstart
- `docs/` — arquitetura, hardening, threat model, ADRs
- `docs/*RUNBOOK*.md` — guias operacionais de manutenção e recuperação
- `prd/` — Product Requirements Documents
- `k8s/docs/` — guias de deploy em K3s
