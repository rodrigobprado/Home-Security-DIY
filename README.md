# Home Security DIY

**Sistema de segurança residencial open source e open hardware com processamento 100% local.**

[![Licença: GPL v3](https://img.shields.io/badge/Licen%C3%A7a-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Status: Em Desenvolvimento](https://img.shields.io/badge/Status-Em_Desenvolvimento-yellow.svg)](#status-do-projeto)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue?logo=docker)](src/docker-compose.yml)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-K3s-blue?logo=kubernetes)](k8s/)

---

## Sobre o projeto

O **Home Security DIY** é um sistema de segurança residencial completo, documentado e replicável, projetado para ser instalado pelo próprio usuário. Todo o software é baseado em plataformas abertas e todo o processamento ocorre localmente — sem dependência de nuvem, sem assinaturas mensais, sem telemetria.

O projeto adota uma abordagem de **defesa em profundidade** com três camadas de segurança e cobre três cenários residenciais distintos (Rural, Urbano, Apartamento).

### Destaques

- 🔒 **Privacidade por design** — processamento local, armazenamento local, sem cloud obrigatório.
- 🏠 **100% local** — toda IA e automação executam no servidor doméstico.
- 💰 **Sem assinatura** — zero custos mensais de monitoramento.
- 🧱 **Modular** — comece simples e expanda conforme necessidade.
- 🔌 **Interoperável** — protocolos abertos (MQTT, Zigbee, RTSP, ONVIF).
- 🚀 **Pronto para uso** — stacks Docker (dev) e Kubernetes/K3s (prod) inclusos.

---

## Stack Tecnológico

| Componente | Tecnologia | Função |
|------------|------------|--------|
| **Automação** | [Home Assistant](https://www.home-assistant.io/) | Cérebro do sistema, dashboard e regras. |
| **NVR + IA** | [Frigate](https://docs.frigate.video/) | Gravação vídeo e detecção de objetos (pessoas, carros) via OpenVINO. |
| **Sensores** | Zigbee 3.0 via [Zigbee2MQTT](https://www.zigbee2mqtt.io/) | Sensores de porta, presença e fumaça sem fio. |
| **Mensageria** | Mosquitto (MQTT) | Comunicação em tempo real entre os serviços. |
| **Infraestrutura**| Docker / K3s | Orquestração de containers. |

---

## Como começar

### Desenvolvimento (Rápido)

Para testar o sistema em seu computador ou servidor de desenvolvimento:

1. Clone o repositório:
   ```bash
   git clone https://github.com/rodrigobprado/Home-Security-DIY.git
   cd Home-Security-DIY/src
   ```

2. Configure o ambiente:
   ```bash
   cp .env.example .env
   # Edite as senhas e URLs das câmeras no arquivo .env
   ```

3. Inicie o stack:
   ```bash
   docker compose up -d
   ```

4. Acesse:
   - Home Assistant: `http://localhost:8123`
   - Frigate NVR: `http://localhost:5000`

> 📘 **Guia completo**: Veja [src/docs/QUICK_START.md](src/docs/QUICK_START.md)

### Produção (Recomendado)

Para instalação definitiva em um Mini PC ou servidor dedicado usando **Kubernetes (K3s)**:

1. Instale o K3s no servidor.
2. Utilize o script de deploy:
   ```bash
   ./scripts/deploy.sh production
   ```

> 📘 **Guia de Produção**: Veja [k8s/docs/K3S_SETUP.md](k8s/docs/K3S_SETUP.md)

---

## Estrutura do repositório

```
Home-Security-DIY/
├── src/                       # Stack Docker Compose (Desenvolvimento)
│   ├── docker-compose.yml
│   └── configs...
├── k8s/                       # Stack Kubernetes/K3s (Produção)
│   ├── base/                  # Manifests base
│   └── overlays/              # Configs específicas (staging/prod)
├── docs/                      # Documentação de arquitetura
│   ├── ARQUITETURA_TECNICA.md
│   └── ...
├── prd/                       # Requisitos de Produto (PRDs)
├── scripts/                   # Scripts de automação e deploy
└── tasks/                     # Gestão de tarefas do projeto
```

---

## Módulo avançado: Drones Autônomos

O projeto inclui uma camada reativa avançada com **frota modular de drones autônomos** (terrestres e aéreos) para patrulha de perímetro.

**Documentação do Módulo Drones:**
- 📄 [Arquitetura UGV (Terrestre)](docs/ARQUITETURA_HARDWARE_UGV.md)
- 📄 [Arquitetura UAV (Aéreo)](docs/ARQUITETURA_HARDWARE_UAV.md)
- 🛠️ [Guia de Montagem UGV](docs/GUIA_MONTAGEM_UGV.md)
- 🛡️ [Módulo de Defesa e Segurança](prd/PRD_DRONE_DEFENSE_MODULE.md)

---

## Status do projeto

| Área | Status | Progresso |
|------|--------|-----------|
| **Base System** | ✅ Configuração Pronta | Stack Docker e K3s funcionais. |
| **Documentação**| ✅ Completa | PRDs, Arquitetura e Guias de Montagem. |
| **Drones (UGV)**| 🟠 Protótipo | Hardware/Firmware definidos, Simulação OK. |
| **Drones (UAV)**| 🔴 Planejamento | Arquitetura definida. |

---

## Contribuição

Contribuições são bem-vindas! Por favor, leia o [CONTRIBUTING.md](CONTRIBUTING.md) (em breve) para detalhes sobre nosso código de conduta e processo de envio de pull requests.

---

## Licença e Aviso Legal

Este projeto é licenciado sob a [GPL v3](LICENSE).

**Aviso Legal**: O usuário é o único responsável por verificar e cumprir a legislação local sobre videovigilância, segurança privada, uso de drones e proteção de dados. Os autores não se responsabilizam pelo uso indevido deste software.

> ⚠️ **Atenção sobre Drones (Brasil)**: A operação de drones autônomos aéreos sem contato visual direto (BVLOS) requer autorização especial da ANAC/DECEA. O software fornecido neste repositório para UAVs é destinado apenas para **voo assistido (VLOS)** ou pesquisa em ambiente confinado. Consulte [LEGAL_AND_ETHICS.md](docs/LEGAL_AND_ETHICS.md) para detalhes.
