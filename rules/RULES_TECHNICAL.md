# Regras Técnicas – Sistema de Home Security

> Comentário: Diretrizes técnicas, boas práticas e padrões esperados para o projeto de segurança residencial.

## Versionamento

- Utilizar Git para controle de versão.
- Commits devem ser pequenos, com mensagens claras e descritivas.
- Todas as configurações de plataformas (Home Assistant, Frigate, etc.) devem ser versionadas como código.
- Manter histórico de mudanças em configurações de sensores e automações.

## Qualidade de código

- Seguir boas práticas de engenharia de software adequadas à stack escolhida (por exemplo, PEP 8 para Python).
- Priorizar testes automatizados sempre que possível.
- Configurações YAML devem seguir indentação consistente (2 espaços).
- Automações devem ter nomes descritivos e comentários explicando a lógica.

## Segurança

- Nunca incluir segredos, chaves de API ou credenciais diretamente em arquivos `.md` ou de configuração versionados.
- Utilizar gestão de secrets adequada (ex.: secrets.yaml no Home Assistant, variáveis de ambiente).
- Documentar mecanismos de segurança em `ARCHITECTURE.md` e `API_DOCS.md` quando aplicável.

## Logging e observabilidade

- Decisões importantes de arquitetura devem ser registradas em `MEMORY_EVOLUTION_LOG.md`.
- Problemas recorrentes ou incidentes devem ser adicionados em `TECH_DEBT.md` ou `IMPROVEMENTS.md`.
- Configurar logging adequado em todas as plataformas para troubleshooting.

---

## Stack e diretrizes técnicas deste projeto

### Plataformas de automação suportadas

O projeto deve priorizar plataformas open source maduras e com comunidade ativa:

| Plataforma | Uso recomendado | Considerações |
|------------|-----------------|---------------|
| **Home Assistant** | Central de automação principal | Ampla compatibilidade, grande comunidade, atualizações frequentes, interface Lovelace customizável. Recomendado como primeira opção. |
| **openHAB** | Alternativa para automação | Mais flexível em configurações avançadas, curva de aprendizado maior, boa para usuários técnicos. |
| **Node-RED** | Automações complexas e integrações | Complemento ao Home Assistant para lógicas visuais complexas, integrações customizadas. |

> **Decisão (2026-02)**: Plataforma principal selecionada: **Home Assistant** (versão 2024.12+).
> Justificativa: maior comunidade, integração nativa com Frigate, Zigbee2MQTT e MQTT; já em produção neste projeto.

### Tecnologias open source para videovigilância

| Tecnologia | Uso recomendado | Considerações |
|------------|-----------------|---------------|
| **Frigate** | NVR com detecção de objetos (pessoas, veículos) | Usa aceleração de hardware (Coral TPU, GPU), integração nativa com Home Assistant, detecção em tempo real. Recomendado como primeira opção. |
| **ZoneMinder** | NVR tradicional com detecção de movimento | Mais maduro, interface web própria, curva de aprendizado moderada. |
| **Shinobi** | NVR alternativo | Interface moderna, código aberto, boa documentação. |
| **Viseron** | NVR com ML integrado | Foco em detecção inteligente, menos maduro que Frigate. |

> **Decisão (2026-02)**: NVR primário selecionado: **Frigate 0.14.1**.
> Justificativa: detecção de objetos em tempo real com aceleração Intel OpenVINO (iGPU via `/dev/dri`), integração nativa com Home Assistant via MQTT, já em produção neste projeto.

### Protocolos de comunicação para sensores

| Protocolo | Vantagens | Desvantagens | Uso recomendado |
|-----------|-----------|--------------|-----------------|
| **Zigbee** | Baixo consumo, mesh network, sem dependência de nuvem | Requer coordenador (ex.: Sonoff Zigbee, ConBee) | Sensores de portas/janelas, movimento, temperatura |
| **Z-Wave** | Interoperabilidade certificada, mesh, baixa interferência | Custo maior, menos dispositivos disponíveis no Brasil | Fechaduras, sensores premium |
| **Wi-Fi** | Sem hub adicional, fácil configuração | Maior consumo de energia, congestão de rede | Câmeras, dispositivos com alimentação fixa |
| **433MHz** | Barato, longo alcance | Sem criptografia nativa, unidirecional | Sensores básicos, controles remotos legados |
| **Thread/Matter** | Futuro padrão unificado, baixo consumo, mesh | Ainda em adoção, poucos dispositivos | Considerar para novos projetos |
| **PoE (Power over Ethernet)** | Alimentação e dados em um cabo | Requer switch PoE | Câmeras IP, dispositivos fixos |

#### Matriz de decisão — protocolo por tipo de dispositivo

| Tipo de Dispositivo | Protocolo Recomendado | Justificativa |
|---|---|---|
| Sensores de abertura / movimento / temperatura | **Zigbee** | Baixo consumo, mesh, sem nuvem, amplo suporte no BR |
| Câmeras IP (indoor/outdoor fixas) | **Wi-Fi 2.4/5GHz ou PoE** | Largura de banda necessária para stream RTSP |
| Câmeras em áreas sem cabeamento | **Wi-Fi 5GHz** | Flexibilidade de instalação |
| Fechaduras eletrônicas premium | **Z-Wave** | Interoperabilidade certificada, menor interferência |
| Sensores legados / controles remotos antigos | **433MHz** | Compatibilidade retroativa (somente leitura) |
| Drones UGV/UAV — canal primário | **Wi-Fi 5GHz + MQTT** | Baixa latência, integração direta com broker |
| Drones UGV/UAV — canal de failover | **LoRa 915MHz** | Longo alcance, resistente a jamming Wi-Fi |
| Sensores de perímetro rural (longas distâncias) | **LoRa / Meshtastic** | Alcance de km sem infraestrutura Wi-Fi |
| Novos dispositivos (avaliação futura) | **Matter / Thread** | Adotar quando ecossistema BR estiver maduro (ver issue #108) |

### Hardware de processamento

O sistema deve rodar em hardware acessível e disponível localmente:

| Hardware | Especificações mínimas | Uso recomendado |
|----------|----------------------|-----------------|
| **Raspberry Pi 4/5** | 4GB RAM, 32GB SD/SSD | Instalações pequenas (até 4 câmeras, <20 sensores) |
| **Mini PC (ex.: Beelink, Minisforum)** | Intel N100 ou superior, 8GB RAM, 256GB SSD | Instalações médias (até 8 câmeras, Frigate com aceleração) |
| **NUC ou equivalente** | Intel i3/i5, 16GB RAM, 512GB SSD | Instalações grandes ou com detecção ML intensiva |
| **Coral USB/M.2 TPU** | Acelerador de ML | Recomendado para Frigate em qualquer hardware |

#### Hardware alvo por cenário residencial

| Cenário | CPU | RAM | Armazenamento | Acelerador ML | Câmeras | Sensores |
|---|---|---|---|---|---|---|
| **Apartamento** | Raspberry Pi 4/5 ou Mini PC N100 | 4–8 GB | 64 GB SSD | Coral USB TPU | até 4 | até 20 |
| **Casa Urbana** | Mini PC Intel N100/N305 (ex.: Beelink) | 8–16 GB | 256 GB SSD | Coral USB TPU + iGPU | até 8 | até 40 |
| **Imóvel Rural / Drones** | NUC Intel i3/i5 ou equivalente | 16–32 GB | 512 GB SSD + HDD NAS | Coral M.2 TPU + iGPU | até 16 | ilimitado |

> **Referência deste projeto**: Mini PC com Intel iGPU — aceleração OpenVINO ativa no Frigate via `/dev/dri`.

### Boas práticas de segurança para ambientes residenciais

#### Segregação de rede

- **VLAN de IoT**: Isolar todos os dispositivos IoT (sensores, automações) em VLAN separada.
- **VLAN de câmeras**: Isolar câmeras em VLAN dedicada, sem acesso à internet.
- **VLAN de gestão**: Separar o hub de processamento (Home Assistant, NVR) com acesso controlado.
- Configurar firewall para permitir apenas comunicação necessária entre VLANs.

#### Acesso remoto seguro

- **Nunca expor diretamente à internet**: Home Assistant, Frigate e NVR não devem ter portas abertas ao público.
- **VPN obrigatória**: Usar WireGuard, OpenVPN ou Tailscale para acesso remoto.
- Alternativa: Home Assistant Cloud (Nabu Casa) para quem aceitar serviço pago.
- Configurar autenticação de dois fatores (2FA) onde disponível.

#### Mínima exposição à internet

- Dispositivos IoT (sensores, câmeras) não devem ter acesso à internet (bloquear no firewall).
- Atualizações de firmware devem ser feitas manualmente ou via servidor local.
- Desabilitar telemetria e comunicação com nuvem do fabricante quando possível.

#### Atualizações e manutenção

- Manter Home Assistant, Frigate e outros softwares atualizados (checar releases mensalmente).
- Atualizar firmware de dispositivos IoT quando correções de segurança forem publicadas.
- Fazer backup regular de configurações (automatizado, diário ou semanal).

### Diretrizes de documentação

#### Inventário de dispositivos

Manter documento `docs/DEVICE_INVENTORY.md` com:

```markdown
| ID | Dispositivo | Tipo | Localização | Protocolo | IP/Endereço | Notas |
|----|-------------|------|-------------|-----------|-------------|-------|
| CAM-01 | Câmera entrada | IP PoE | Portão principal | Ethernet | 192.168.10.101 | Modelo XYZ |
| SEN-01 | Sensor porta | Zigbee | Porta frontal | Zigbee | 0x00158d000... | Reed switch |
```

#### Documentação de automações

Cada automação complexa deve ter comentário ou documentação explicando:
- Gatilho (trigger): o que dispara a automação.
- Condições: quando deve ou não executar.
- Ações: o que faz.
- Motivo: por que foi criada.

#### Diagramas de arquitetura

- Manter diagrama de rede em `docs/ARCHITECTURE.md` usando Mermaid, Draw.io ou similar.
- Incluir diagrama de posicionamento físico de sensores e câmeras por cenário.

### Versionamento de configurações

- **Home Assistant**: Usar integração com Git ou backup automatizado para `config/`.
- **Frigate**: Versionar `config.yml` no repositório.
- **Automações**: Preferir automações em YAML (versionáveis) a automações criadas pela UI.
- **Manter changelog**: Documentar mudanças significativas em `MEMORY_EVOLUTION_LOG.md`.

### Padrões de nomenclatura

| Tipo | Padrão | Exemplo |
|------|--------|---------|
| Sensores | `sensor.<local>_<tipo>` | `sensor.porta_frontal_abertura` |
| Câmeras | `camera.<local>` | `camera.portao_principal` |
| Automações | `automation.<acao>_<contexto>` | `automation.ligar_luz_movimento_entrada` |
| Scripts | `script.<acao>_<contexto>` | `script.armar_alarme_noite` |

#### Drones — UGV (Unmanned Ground Vehicle)

| Tipo | Padrão | Exemplo |
|---|---|---|
| Sensores de telemetria | `sensor.ugv_<campo>` | `sensor.ugv_bateria`, `sensor.ugv_status` |
| Câmera embarcada | `camera.ugv_<posicao>` | `camera.ugv_frente` |
| Controles / switches | `switch.ugv_<modo>` | `switch.ugv_patrulha` |
| Automações | `automation.ugv_<acao>_<contexto>` | `automation.ugv_iniciar_patrulha_alarme` |

#### Drones — UAV (Unmanned Aerial Vehicle)

| Tipo | Padrão | Exemplo |
|---|---|---|
| Sensores de telemetria | `sensor.uav_<campo>` | `sensor.uav_bateria`, `sensor.uav_altitude` |
| Câmera embarcada | `camera.uav_<posicao>` | `camera.uav_embarcada` |
| Controles / switches | `switch.uav_<modo>` | `switch.uav_decolar` |
| Automações | `automation.uav_<acao>_<contexto>` | `automation.uav_inspecionar_zona_alerta` |

