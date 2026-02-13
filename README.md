# Home Security DIY

**Sistema de seguranca residencial open source e open hardware com processamento 100% local.**

[![Licenca: GPL v3](https://img.shields.io/badge/Licen%C3%A7a-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Status: Planejamento](https://img.shields.io/badge/Status-Planejamento-yellow.svg)](#status-do-projeto)

---

## Sobre o projeto

O Home Security DIY e um sistema de seguranca residencial completo, documentado e replicavel, projetado para ser instalado pelo proprio usuario. Todo o software e baseado em plataformas abertas e todo o processamento ocorre localmente -- sem dependencia de nuvem, sem assinaturas mensais, sem telemetria.

O projeto adota uma abordagem de **defesa em profundidade** com tres camadas de seguranca e cobre tres cenarios residenciais distintos.

### Camadas de seguranca

| Camada | Descricao | Exemplos |
|--------|-----------|----------|
| **Passiva** | Elementos fisicos que dificultam ou retardam invasoes | Muros, cercas, grades, fechaduras reforçadas, paisagismo defensivo |
| **Ativa** | Sistemas eletronicos que detectam, monitoram e alertam | Sensores Zigbee, cameras IP com IA, alarmes, controle de acesso |
| **Reativa** | Mecanismos de resposta a incidentes | Notificacoes em tempo real, gravacao de evidencias, planos de acao, drones autonomos |

### Cenarios residenciais

| Cenario | Caracteristicas | Investimento estimado |
|---------|-----------------|----------------------|
| **Propriedade rural** | Perimetro extenso, 4-6 cameras PoE, sensores de longo alcance | ~R$ 5.950 |
| **Casa urbana com quintal** | Perimetro medio, 3-5 cameras, 8-15 sensores | ~R$ 4.950 |
| **Apartamento** | Foco em controle de acesso e porta principal | ~R$ 2.450 |

> Valores estimados para 2026, sujeitos a variacao conforme fornecedor e configuracao.

---

## Destaques

- **Privacidade por design** -- processamento local, armazenamento local, sem cloud obrigatorio
- **100% local** -- toda IA e automacao executam no servidor domestico
- **Sem assinatura** -- sem custos mensais de monitoramento ou nuvem
- **Modular** -- comece simples e expanda conforme necessidade
- **Interoperavel** -- protocolos abertos (MQTT, Zigbee, RTSP, ONVIF)
- **Conformidade** -- projetado considerando LGPD, NBR 5410, NBR 5419 e boas praticas de videovigilancia

---

## Stack tecnologico

| Componente | Tecnologia recomendada | Alternativa |
|------------|----------------------|-------------|
| Plataforma de automacao | [Home Assistant](https://www.home-assistant.io/) | openHAB |
| NVR com deteccao por IA | [Frigate](https://docs.frigate.video/) | ZoneMinder |
| Protocolo de sensores | Zigbee 3.0 (via [Zigbee2MQTT](https://www.zigbee2mqtt.io/)) | Z-Wave |
| Hardware servidor | Mini PC Intel N100 (8-16 GB RAM, SSD) | Raspberry Pi 5 |
| Aceleracao de IA | Intel OpenVINO (integrado ao N100) | Google Coral |
| Acesso remoto | WireGuard VPN | Tailscale |
| Broker MQTT | Mosquitto | - |
| Sistema de alarme | Alarmo (add-on HA) | - |

---

## Estrutura do repositorio

```
Home-Security-DIY/
  PROJECT_OVERVIEW.md          # Visao geral do projeto e escopo
  docs/
    ARQUITETURA_TECNICA.md     # Stack, rede, hardware, integracao
    ARQUITETURA_SEGURANCA_FISICA.md  # Camadas passiva/ativa/reativa + diagramas
    ARQUITETURA_DRONES_AUTONOMOS.md  # Modulo avancado de drones
  prd/
    PRD_SENSORS_AND_ALARMS_PLATFORM.md
    PRD_VIDEO_SURVEILLANCE_AND_NVR.md
    PRD_MONITORING_DASHBOARD.md
    PRD_PERIMETER_RURAL.md
    PRD_PERIMETER_URBAN_HOUSE.md
    PRD_APARTMENT_SECURITY.md
    PRD_AUTONOMOUS_DRONES.md
  rules/                       # Regras tecnicas, gerais e de compliance
  standards/                   # Normas pesquisadas e aplicadas (NBR, LGPD, ANAC)
  tasks/                       # Kanban em Markdown (backlog, em progresso, concluidas)
  memory/                      # Memoria compartilhada entre agentes de IA
  agents/                      # Configuracao e memoria local dos agentes
  quality/                     # Melhorias, debito tecnico, itens pendentes
```

---

## Modulo avancado: drones autonomos

O projeto inclui uma camada reativa avancada com **frota modular de drones autonomos** (terrestres, aereos e aquaticos) para patrulha de perimetro, vigilancia e resposta a incidentes. O modulo utiliza ROS2, visao computacional com YOLO/TensorFlow Lite e comunicacao redundante via Wi-Fi + LoRa/Meshtastic.

Para detalhes completos, consulte [`docs/ARQUITETURA_DRONES_AUTONOMOS.md`](docs/ARQUITETURA_DRONES_AUTONOMOS.md) e [`prd/PRD_AUTONOMOUS_DRONES.md`](prd/PRD_AUTONOMOUS_DRONES.md).

---

## Status do projeto

O projeto esta em **fase de planejamento e documentacao**. Ainda nao ha codigo-fonte ou configuracoes implementadas.

| Categoria | Concluidas | Total | Status |
|-----------|-----------|-------|--------|
| Levantamento de requisitos | 7 | 7 | Completo |
| Arquitetura e design | 5 | 5 | Completo |
| Selecao de tecnologias | 5 | 5 | Completo |
| Normas e compliance | 7 | 7 | Completo |
| Documentacao e PRDs | 4 | 4 | Completo |
| Privacidade e seguranca | 2 | 2 | Completo |
| Drones autonomos | 2 | 15 | Em andamento |
| Revisao e melhorias | 2 | 23 | Em andamento |
| **Total** | **34** | **68** | **50%** |

O sistema de seguranca base (sem drones) tem toda a documentacao e arquitetura concluidas. As proximas etapas incluem threat modeling, guias de implementacao e inicio do desenvolvimento do modulo de drones.

---

## Como contribuir

Este projeto esta em fase inicial e ainda nao possui um guia formal de contribuicao. Um `CONTRIBUTING.md` sera criado em breve.

Enquanto isso, se voce tem interesse em contribuir:

1. Leia o [`PROJECT_OVERVIEW.md`](PROJECT_OVERVIEW.md) para entender o escopo
2. Consulte [`tasks/TASKS_BACKLOG.md`](tasks/TASKS_BACKLOG.md) para ver as tarefas pendentes
3. Abra uma issue para discutir ideias ou reportar problemas

---

## Licenca

Este projeto e licenciado sob a [GNU General Public License v3.0](LICENSE).

Voce pode copiar, modificar e distribuir este projeto livremente, desde que mantenha a mesma licenca e disponibilize o codigo-fonte.

---

## Aviso legal

Este projeto e fornecido "como esta", sem garantias de qualquer tipo. O usuario e o unico responsavel por:

- Verificar e cumprir toda a **legislacao local** aplicavel (seguranca privada, videovigilancia, protecao de dados, uso de drones, etc.)
- Garantir que a instalacao atenda as **normas tecnicas** vigentes (NBR 5410, NBR 5419, entre outras)
- Avaliar a **legalidade do modulo de drones** e do sistema de defesa nao letal em sua jurisdicao antes de qualquer implementacao
- Assegurar que cameras e sensores **nao captem areas publicas ou propriedades de terceiros** sem autorizacao

Os autores nao se responsabilizam por danos, perdas ou consequencias legais decorrentes do uso deste projeto.
