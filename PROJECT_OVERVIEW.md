# Project Overview – Sistema de Home Security Open Source

> Comentário: Este arquivo descreve o projeto em alto nível. Humanos e agentes devem ler este arquivo antes de qualquer outro.

## Contexto

Este projeto é um **Sistema de Segurança Residencial (Home Security)** desenvolvido sob os princípios de **open source** (software) e **open hardware** (especificações abertas de sensores e módulos). O sistema adota uma abordagem de **defesa em profundidade**, organizando a segurança em camadas concêntricas que protegem desde o perímetro externo até os ambientes internos da residência.

O projeto considera **três cenários residenciais distintos**, cada um com características, riscos e necessidades específicas:

1. **Propriedade em área rural** – Grandes extensões de terreno, perímetro extenso, menor densidade de vizinhança, riscos de invasão por áreas não monitoradas.
2. **Casa com quintal grande em área urbana/suburbana** – Perímetro médio, muros ou cercas, portão de veículos, maior presença de vizinhos, riscos de invasão por portões, janelas e muros.
3. **Apartamento** – Sem perímetro externo próprio, foco em controle de acesso (porta principal), segurança interna e integração com sistemas condominiais.

## Camadas de segurança

O sistema implementa três camadas de segurança que DEVEM estar presentes em todos os cenários:

### Segurança passiva
Elementos físicos e arquitetônicos que dificultam ou retardam invasões sem necessidade de energia ou automação:
- Muros, cercas, grades e portões robustos
- Portas e janelas com fechaduras de qualidade, reforços e vidros resistentes
- Iluminação natural e artificial (dissuasória)
- Paisagismo defensivo (plantas espinhosas, visibilidade)
- Cofres e áreas seguras internas

### Segurança ativa
Sistemas eletrônicos e automatizados que detectam, monitoram e alertam:
- Sensores de movimento (PIR, micro-ondas), presença, abertura (portas/janelas), vibração, quebra de vidro
- Sensores ambientais (fumaça, gás, vazamento de água)
- Câmeras IP com gravação local (NVR) e detecção inteligente (pessoas, veículos, objetos)
- Alarmes e sirenes (internos e externos)
- Controle de acesso (fechaduras eletrônicas, leitores biométricos, teclados)
- Automações (iluminação reativa, simulação de presença, travamento automático)

### Segurança reativa
Procedimentos e mecanismos de resposta a incidentes:
- Notificações em tempo real (push, SMS, e-mail, chamada)
- Registro de eventos e evidências (logs, gravações)
- Planos de ação pré-definidos por tipo de incidente
- Integração com serviços de emergência e vizinhança
- Backup de alimentação (nobreak, bateria)
- **Frota de drones autônomos modulares** (terrestre, aéreo, aquático) para patrulha, vigilância e resposta ativa

### Módulo reativo avançado: Drones autônomos

O sistema inclui uma **frota modular de drones autônomos** projetados para vigilância, segurança, inspeção e monitoramento ambiental. Este módulo representa a camada mais avançada de segurança reativa.

#### Categorias de drones

| Tipo | Descrição | Aplicação |
|------|-----------|-----------|
| **Terrestres** | Drones com rodas ou esteiras motorizadas | Patrulha de perímetro, inspeção de áreas de difícil acesso |
| **Aéreos** | Multirrotores ou asa fixa | Vigilância aérea, resposta rápida, mapeamento |
| **Aquáticos** | Drones aquáticos ou anfíbios | Monitoramento de espelhos d'água, áreas alagadas |

#### Sensores e módulos embarcados
- Câmeras visuais e infravermelhas
- Microfones e alto-falantes para comunicação e resposta sonora
- IA embarcada para visão computacional, reconhecimento e decisão autônoma
- GPS/RTK para navegação de precisão
- IMU e sensores ultrassônicos/lidar para detecção de obstáculos

#### Sistema de defesa não letal
- Arma de CO₂ com munição de pimenta e gás de gengibre
- Controlado apenas sob protocolo de segurança autenticado
- Registro completo de cada disparo para auditoria
- Função de dissuasão e afastamento sem danos permanentes

#### Comunicação e rede
- Wi-Fi de longo alcance (rede principal)
- LoRa/Meshtastic (redundância para alertas, telemetria e comandos críticos)
- Integração segura com Home Security System
- Transmissão de imagens e vídeo em tempo real

> **Nota**: O uso do módulo reativo de defesa deve seguir legislações locais, priorizando segurança e não letalidade. Ver `docs/ARQUITETURA_DRONES_AUTONOMOS.md` para especificações completas.

## Princípios técnicos

- **Open source**: Todo o software será baseado em plataformas abertas como Home Assistant, openHAB, ZoneMinder, Frigate, entre outras.
- **Open hardware**: Especificações abertas para sensores, controladores e módulos, permitindo uso de componentes genéricos ou fabricação própria.
- **Hardware acessível**: Arquitetura pensada para rodar em Raspberry Pi, mini PC, NUC ou hardware equivalente.
- **Privacidade por design**: Processamento e armazenamento local, sem dependência de nuvem, conformidade com LGPD/GDPR.
- **Modularidade**: Cada componente (sensores, câmeras, NVR, dashboard) pode ser implantado de forma independente.
- **Interoperabilidade**: Integração via protocolos abertos (MQTT, Zigbee, Z-Wave, Wi-Fi, PoE).

## Objetivos principais

- Criar um sistema de segurança residencial completo, documentado e replicável.
- Fornecer guias de implementação para os três cenários residenciais.
- Disponibilizar templates de configuração para plataformas open source.
- Garantir privacidade e controle total dos dados pelo usuário.
- Permitir evolução incremental: começar simples e expandir conforme necessidade.

## Escopo

O projeto abrange:

- **Documentação de requisitos** (PRDs) para cada cenário e subsistema.
- **Arquitetura física**: layout de sensores, câmeras, pontos de instalação por cenário.
- **Arquitetura lógica**: integração de software, fluxos de dados, automações.
- **Seleção de tecnologias**: análise comparativa de plataformas e dispositivos open source.
- **Guias de instalação e configuração**: passo a passo para cada componente.
- **Normas e compliance**: levantamento de normas físicas e de privacidade aplicáveis.

> TODO (humano): Validar se os três cenários cobrem as necessidades ou se há cenários adicionais a considerar (ex.: condomínio horizontal, sítio/chácara).

## Stakeholders

- **Product Owner**: Responsável pelas decisões de escopo e priorização.
- **Arquiteto de Segurança Física**: Define camadas passivas/ativas/reativas.
- **Arquiteto Técnico**: Define integrações, automações e stack de software.
- **Usuários finais**: Moradores das residências que utilizarão o sistema.
- **Orquestrador de Agentes de IA**: Coordena os agentes que trabalham na documentação e planejamento.

> Comentário: Preencha com nomes reais conforme a equipe for definida.

## Premissas e riscos

### Premissas
- Os agentes terão acesso a todos os arquivos `.md` deste repositório.
- Haverá um orquestrador responsável por coordenar os agentes.
- O sistema será instalado pelo próprio usuário (DIY) ou por profissional contratado.
- Não haverá dependência de serviços em nuvem para funcionamento básico.
- O usuário possui conhecimento básico de redes e configuração de software.

### Riscos
- Falta de preenchimento correto dos templates pode gerar recomendações inadequadas.
- Incompatibilidade entre dispositivos de diferentes fabricantes.
- Mudanças em plataformas open source podem exigir atualizações frequentes.
- Riscos de segurança cibernética em dispositivos IoT mal configurados.
- Dificuldade de usuários leigos em implementar sem suporte técnico.

> TODO (humano): Revisar premissas e riscos com base no contexto real de implantação.

## Critérios de sucesso

- Toda a estrutura de documentação está preenchida e validada para os três cenários.
- Existem guias de configuração funcionais para pelo menos uma plataforma open source (ex.: Home Assistant).
- O sistema pode ser replicado por um usuário técnico seguindo apenas a documentação.
- A privacidade dos dados está garantida por design (sem cloud obrigatório).
- O projeto está publicado como open source com licença permissiva.

## Componentes principais

| Componente | Descrição | Exemplos de tecnologias |
|------------|-----------|-------------------------|
| Sensores de intrusão | Detectam movimento, abertura, vibração, quebra de vidro | PIR, reed switch, sensor de vibração, detector de vidro |
| Sensores ambientais | Detectam fumaça, gás, vazamento de água | Detector de fumaça, sensor de gás, sensor de inundação |
| Câmeras IP | Capturam vídeo para monitoramento e gravação | Câmeras PoE/Wi-Fi compatíveis com RTSP/ONVIF |
| NVR (gravador de vídeo) | Armazena gravações e processa detecção inteligente | ZoneMinder, Frigate, Shinobi |
| Central de automação | Integra sensores, câmeras e automações | Home Assistant, openHAB |
| Alarmes e sirenes | Emitem alertas sonoros em caso de incidente | Sirenes internas/externas, buzzers |
| Controle de acesso | Gerencia fechaduras e autenticação | Fechaduras eletrônicas, leitores RFID/biométricos |
| Dashboard | Interface de monitoramento e controle | Home Assistant Lovelace, Grafana |
| Notificações | Envia alertas para usuários | Push (app), SMS, e-mail, Telegram |
| **Drones terrestres** | Patrulha de perímetro com rodas/esteiras | Raspberry Pi, ESP32-CAM, ROS2 |
| **Drones aéreos** | Vigilância aérea e resposta rápida | Multirrotores, NVIDIA Jetson, PX4/ArduPilot |
| **Drones aquáticos** | Monitoramento aquático e áreas alagadas | Chassis anfíbio, sensores de profundidade |
| **IA embarcada** | Visão computacional e decisão autônoma | TensorFlow Lite, OpenVINO, YOLO |
| **Módulo de defesa** | Sistema não letal de dissuasão | CO₂ + munição de pimenta/gengibre |
| **Comunicação redundante** | Rede de comunicação resiliente | Wi-Fi longo alcance, LoRa, Meshtastic |

> Ver `docs/ARQUITETURA_DRONES_AUTONOMOS.md` para especificações completas do módulo de drones.

