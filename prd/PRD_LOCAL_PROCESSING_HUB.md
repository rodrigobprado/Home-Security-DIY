# PRD – Hub de Processamento Local

> Sistema de Home Security – Open Source / Open Hardware
>
> Versão: 1.0 | Data: 2026-02-18 | Responsável: Agente_Documentador

---

## 1. Visão geral

- **Nome do produto/funcionalidade**: Hub de Processamento Local (Hardware, SO e Plataformas)
- **Responsável**: Agente_Arquiteto_Tecnico (especificação), Agente_Documentador (documentação)
- **Data**: 2026-02-18
- **PRDs relacionados**: PRD_SENSORS_AND_ALARMS_PLATFORM, PRD_VIDEO_SURVEILLANCE_AND_NVR, PRD_NETWORK_SECURITY, PRD_BACKUP_AND_RESILIENCE

---

## 2. Problema e oportunidade

### 2.1 Problema

Soluções de segurança residencial dependentes de nuvem apresentam riscos:
- **Latência**: Processamento remoto adiciona delay na detecção e notificação
- **Privacidade**: Dados sensíveis (vídeo, acesso) enviados para servidores de terceiros
- **Disponibilidade**: Queda de internet inutiliza o sistema
- **Custo recorrente**: Assinaturas mensais para armazenamento e processamento
- **Descontinuação**: Fabricante pode encerrar serviço, tornando hardware inútil

### 2.2 Oportunidade

Implementar um hub de processamento 100% local que:
- **Processe tudo localmente**: IA, automações, gravações, sem dependência de nuvem
- **Garanta privacidade**: Nenhum dado sai da rede doméstica
- **Ofereça baixa latência**: Processamento em tempo real para detecção e resposta
- **Sem custos recorrentes**: Hardware próprio, software open source
- **Seja escalável**: Suportar desde apartamento (3 sensores) até rural (20+ sensores, 6 câmeras)

---

## 3. Público-alvo

| Perfil | Necessidades específicas |
|--------|--------------------------|
| **Proprietário rural** | Hardware robusto para 4-6 câmeras + 15-20 sensores |
| **Proprietário urbano** | Hardware médio para 3-5 câmeras + 10-15 sensores |
| **Morador de apartamento** | Hardware compacto para 0-1 câmera + 3-5 sensores |
| **Usuário técnico** | Flexibilidade para customizar, acesso SSH, Docker |
| **Usuário iniciante** | Instalação simplificada, HA OS com add-ons |

---

## 4. Requisitos funcionais

### 4.1 Hardware do servidor central

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-001 | CPU com suporte a aceleração de vídeo | Intel Quick Sync (para Frigate) | Alta |
| RF-002 | CPU com iGPU para IA | Intel UHD (OpenVINO) | Alta |
| RF-003 | RAM mínima | 8GB DDR4 | Alta |
| RF-004 | RAM recomendada | 16GB DDR4 | Média |
| RF-005 | Armazenamento do sistema | SSD NVMe 256GB mínimo | Alta |
| RF-006 | Armazenamento de gravações | HDD/SSD 1-4TB separado | Alta |
| RF-007 | Portas USB para Zigbee dongle | Mínimo 2 portas USB (1 para Zigbee, 1 reserva) | Alta |
| RF-008 | Rede Gigabit Ethernet | Mínimo 1 porta, 2 preferível | Alta |
| RF-009 | Consumo de energia | < 25W em idle (economia) | Média |
| RF-010 | Formato compacto | Mini PC ou NUC, discreto | Média |
| RF-011 | Operação silenciosa | < 30dB em operação normal | Média |
| RF-012 | BIOS: Wake on AC | Reiniciar automaticamente após queda de energia | Alta |

### 4.2 Sistema operacional

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-013 | Opção 1: Home Assistant OS (HAOS) | Instalação direta, add-ons integrados | Alta |
| RF-014 | Opção 2: Proxmox + VMs | HA em VM, flexibilidade máxima | Média |
| RF-015 | Opção 3: Debian/Ubuntu + Docker | HA Container, controle total | Média |
| RF-016 | Suporte a Docker/containers | Para executar Frigate, Z2M, Mosquitto | Alta |
| RF-017 | Atualizações de segurança | Patches regulares do SO | Alta |
| RF-018 | SSH para acesso administrativo | Configurável, desabilitado por padrão | Média |

### 4.3 Plataforma de automação (Home Assistant)

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-019 | Home Assistant Core | Versão estável mais recente | Alta |
| RF-020 | Alarmo (add-on de alarme) | Sistema de alarme completo | Alta |
| RF-021 | HACS (Community Store) | Cards e integrações da comunidade | Alta |
| RF-022 | Banco de dados | MariaDB para histórico (melhor que SQLite) | Alta |
| RF-023 | InfluxDB (opcional) | Para métricas de longo prazo | Baixa |
| RF-024 | Grafana (opcional) | Dashboards avançados de métricas | Baixa |

### 4.4 NVR e detecção de IA (Frigate)

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-025 | Frigate NVR | Detecção de objetos em tempo real | Alta |
| RF-026 | Aceleração via Intel OpenVINO | Usar iGPU do N100 para IA | Alta |
| RF-027 | Modelos de detecção | YOLO ou SSD MobileNet | Alta |
| RF-028 | Suporte a 4-8 câmeras simultâneas (1080p) | Com aceleração | Alta |
| RF-029 | Dual stream | Substream para detecção, mainstream para gravação | Alta |
| RF-030 | Zonas de detecção por câmera | Configuráveis na interface | Alta |

### 4.5 Bridge Zigbee (Zigbee2MQTT)

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-031 | Zigbee2MQTT como bridge primária | Ou ZHA como alternativa | Alta |
| RF-032 | Coordenador Zigbee USB | Sonoff ZBDongle-P (CC2652P) ou SLZB-06 | Alta |
| RF-033 | Suporte a 50+ dispositivos Zigbee | Mesh com roteadores | Alta |
| RF-034 | Interface web para gestão | Dashboard do Z2M | Média |
| RF-035 | OTA updates de firmware | Atualização de sensores via Z2M | Média |

### 4.6 MQTT Broker (Mosquitto)

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-036 | Mosquitto como broker MQTT | Comunicação entre Frigate, Z2M e HA | Alta |
| RF-037 | Autenticação de clientes | Usuário/senha para cada serviço | Alta |
| RF-038 | ACLs de tópicos | Restringir acesso por serviço | Média |
| RF-039 | TLS (opcional) | Criptografia MQTT para comunicação interna | Baixa |

### 4.7 Instalação e configuração

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-040 | Guia de instalação passo a passo | Documentação no projeto | Alta |
| RF-041 | Scripts de configuração inicial | Automatizar setup básico | Média |
| RF-042 | Checklist pós-instalação | Verificar todos os serviços | Alta |
| RF-043 | Configuração de backup automático | Desde o primeiro dia | Alta |

---

## 5. Requisitos não funcionais

### 5.1 Performance

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-001 | Tempo de boot do sistema | < 120 segundos até HA acessível |
| RNF-002 | Uso de CPU em idle | < 15% |
| RNF-003 | Uso de RAM com HA + Frigate + Z2M | < 70% de 8GB |
| RNF-004 | FPS de detecção Frigate (OpenVINO) | > 10 FPS por câmera |
| RNF-005 | Latência de automação | < 200ms do trigger à ação |

### 5.2 Confiabilidade

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-006 | Uptime alvo | > 99.5% (máx ~43h downtime/ano) |
| RNF-007 | Restart automático de serviços | Docker restart: always |
| RNF-008 | Watchdog | Reiniciar HA se não responder por 5 min |
| RNF-009 | SSD com SMART monitoring | Alertar degradação do disco |
| RNF-010 | Temperatura operacional | 0-40°C, ventilação adequada |

### 5.3 Segurança

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-011 | Acesso ao HA com autenticação forte | Senha + 2FA recomendado |
| RNF-012 | SSH desabilitado por padrão | Habilitar apenas quando necessário |
| RNF-013 | Firewall local | Apenas portas necessárias abertas |
| RNF-014 | Atualizações de segurança | Aplicar patches mensalmente |

### 5.4 Escalabilidade

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-015 | Suporte a expansão de RAM | Até 32GB |
| RNF-016 | Suporte a disco adicional | Via USB 3.0 ou segundo M.2 |
| RNF-017 | Suporte a mais câmeras | Até 8 simultâneas com OpenVINO |

---

## 6. Arquitetura técnica

### 6.1 Diagrama de stack de software

```
┌─────────────────────────────────────────────────────────────────────┐
│                    MINI PC INTEL N100                                 │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                  SISTEMA OPERACIONAL                          │  │
│  │         Home Assistant OS  /  Proxmox  /  Debian + Docker    │  │
│  │                                                               │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │  │
│  │  │   HOME      │  │   FRIGATE   │  │ ZIGBEE2MQTT │          │  │
│  │  │  ASSISTANT  │  │    NVR      │  │   (Bridge)  │          │  │
│  │  │  + Alarmo   │  │  + OpenVINO │  │             │          │  │
│  │  │  + HACS     │  │             │  │             │          │  │
│  │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘          │  │
│  │         │                │                │                   │  │
│  │         │         ┌──────▼──────┐         │                   │  │
│  │         └────────►│  MOSQUITTO  │◄────────┘                   │  │
│  │                   │ (MQTT Broker)│                             │  │
│  │                   └─────────────┘                             │  │
│  │                                                               │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │  │
│  │  │  MariaDB    │  │  InfluxDB   │  │  Grafana    │          │  │
│  │  │ (Histórico) │  │ (Métricas)  │  │ (Dashboards)│          │  │
│  │  │             │  │ (opcional)  │  │ (opcional)  │          │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘          │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  HARDWARE:                                                          │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐    │
│  │ CPU     │ │  iGPU   │ │  SSD    │ │  HDD    │ │ USB     │    │
│  │ N100    │ │ UHD     │ │ 256GB   │ │ 2TB     │ │ Zigbee  │    │
│  │ 4 cores │ │OpenVINO │ │(sistema)│ │(gravaç.)│ │ Dongle  │    │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘    │
│                                                                     │
│  ┌─────────┐ ┌─────────┐                                          │
│  │Ethernet │ │ Nobreak │                                          │
│  │ Gigabit │ │ (UPS)   │                                          │
│  └─────────┘ └─────────┘                                          │
└─────────────────────────────────────────────────────────────────────┘
```

### 6.2 Fluxo de dados do sistema

```
CÂMERAS IP (RTSP)                    SENSORES ZIGBEE
       │                                    │
       │ RTSP (1080p/4K)                    │ Zigbee 3.0
       ▼                                    ▼
┌──────────────┐                   ┌──────────────┐
│   FRIGATE    │                   │ ZIGBEE2MQTT  │
│   NVR + IA   │                   │              │
│              │                   │              │
│ Detect:      │                   │ Converte:    │
│ - Pessoas    │                   │ - Abertura   │
│ - Veículos   │                   │ - Movimento  │
│ - Animais    │                   │ - Temp/Umid  │
└──────┬───────┘                   └──────┬───────┘
       │ MQTT (eventos)                   │ MQTT (estados)
       ▼                                  ▼
┌──────────────────────────────────────────────┐
│               MOSQUITTO (MQTT Broker)         │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│           HOME ASSISTANT + ALARMO             │
│                                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │Automações│  │ Dashboard│  │  Alarmo   │   │
│  │& Scripts │  │(Lovelace)│  │ (Alarme)  │   │
│  └──────────┘  └──────────┘  └──────────┘   │
│                                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Notif.  │  │  Cenas   │  │   Logs   │   │
│  │(Push/TG) │  │          │  │(MariaDB) │   │
│  └──────────┘  └──────────┘  └──────────┘   │
└───────────────────────────────────────────────┘
```

### 6.3 Comparativo de opções de SO

| Aspecto | Home Assistant OS | Proxmox + VM | Debian + Docker |
|---------|-------------------|--------------|-----------------|
| **Facilidade** | Muito fácil | Avançado | Intermediário |
| **Add-ons** | Nativos (1-click) | Via Docker/LXC | Via Docker compose |
| **Flexibilidade** | Limitada | Máxima | Alta |
| **Performance** | Boa | Boa (overhead VM) | Melhor (bare metal) |
| **Backup** | Integrado | Snapshot VM | Manual/scripts |
| **Ideal para** | Iniciantes | Power users | Técnicos |
| **Recomendação** | Cenário padrão | Multi-serviço | Customização total |

---

## 7. Produtos/componentes recomendados

### 7.1 Mini PCs recomendados

| Modelo | CPU | RAM | SSD | Preço estimado | Recomendação |
|--------|-----|-----|-----|----------------|--------------|
| **Beelink Mini S12 Pro** | Intel N100 | 8GB | 256GB | R$ 800-1.100 | Custo-benefício (apartamento) |
| **Beelink EQ12** | Intel N100 | 16GB | 500GB | R$ 1.000-1.400 | Recomendado (casa urbana) |
| **MinisForum UM560** | AMD Ryzen 5 | 16GB | 512GB | R$ 1.500-2.000 | Alto desempenho (rural) |
| **Intel NUC 12** | Intel N100 | 16GB | 512GB | R$ 1.200-1.800 | Marca premium |
| **Beelink SER5** | AMD Ryzen 5 | 16GB | 500GB | R$ 1.300-1.800 | Alternativa AMD |

### 7.2 Armazenamento

| Componente | Modelo sugerido | Preço estimado | Uso |
|------------|-----------------|----------------|-----|
| SSD NVMe 256GB (sistema) | Kingston NV2 | R$ 120-180 | SO + configurações |
| SSD NVMe 512GB (sistema) | WD SN770 | R$ 200-300 | SO + configs + buffer |
| HDD 2TB (gravações) | Seagate BarraCuda | R$ 350-500 | Gravações Frigate |
| HDD 4TB (gravações) | WD Purple (surveillance) | R$ 500-700 | Gravações + redundância |
| SSD SATA 1TB (gravações) | Kingston A400 | R$ 350-500 | Alternativa silenciosa |

### 7.3 Coordenador Zigbee

| Modelo | Chip | Interface | Preço estimado | Observações |
|--------|------|-----------|----------------|-------------|
| **Sonoff ZBDongle-P** | CC2652P | USB | R$ 100-150 | Melhor custo-benefício |
| **Sonoff ZBDongle-E** | EFR32MG21 | USB | R$ 100-150 | Thread/Matter futuro |
| **SLZB-06** | CC2652P | PoE/USB/Ethernet | R$ 200-300 | Mais robusto, PoE |
| **ConBee II** | - | USB | R$ 250-350 | Alternativa para ZHA |

### 7.4 Acessórios

| Componente | Modelo sugerido | Preço estimado | Observações |
|------------|-----------------|----------------|-------------|
| Extensão USB para Zigbee | Cabo USB 1m com base | R$ 20-40 | Afastar dongle de interferência |
| Suporte VESA para Mini PC | Genérico | R$ 30-50 | Montar atrás de monitor/TV |
| Dissipador extra (se necessário) | Pad térmico | R$ 15-30 | Para operação contínua |

---

## 8. Estimativas por cenário

### 8.1 Cenário rural (alto desempenho)

| Componente | Preço estimado |
|------------|----------------|
| Mini PC Intel N100 16GB (Beelink EQ12) | R$ 1.200 |
| SSD NVMe 512GB (sistema) | R$ 250 |
| HDD 4TB WD Purple (gravações) | R$ 600 |
| Coordenador Zigbee (SLZB-06 PoE) | R$ 250 |
| Extensão USB | R$ 30 |
| **Total servidor rural** | **R$ 2.330** |

### 8.2 Cenário casa urbana (recomendado)

| Componente | Preço estimado |
|------------|----------------|
| Mini PC Intel N100 16GB (Beelink EQ12) | R$ 1.200 |
| SSD NVMe 256GB (sistema) | R$ 150 |
| HDD 2TB (gravações) | R$ 400 |
| Coordenador Zigbee (Sonoff ZBDongle-P) | R$ 120 |
| Extensão USB | R$ 30 |
| **Total servidor urbano** | **R$ 1.900** |

### 8.3 Cenário apartamento (compacto)

| Componente | Preço estimado |
|------------|----------------|
| Mini PC Intel N100 8GB (Beelink Mini S12 Pro) | R$ 900 |
| SSD NVMe 256GB (sistema + gravações) | R$ 150 |
| Coordenador Zigbee (Sonoff ZBDongle-P) | R$ 120 |
| Extensão USB | R$ 30 |
| **Total servidor apartamento** | **R$ 1.200** |

---

## 9. Critérios de aceitação

| ID | Critério | Método de verificação |
|----|----------|----------------------|
| CA-001 | Home Assistant acessível via browser em < 120s após boot | Teste de reinicialização |
| CA-002 | Frigate detecta pessoas em tempo real (> 10 FPS) | Verificação no dashboard Frigate |
| CA-003 | Zigbee2MQTT conectado e todos os sensores visíveis | Verificação na interface Z2M |
| CA-004 | MQTT Broker funcionando com todos os clientes | Teste de publicação/recebimento |
| CA-005 | Alarmo configurado com zonas e modos | Teste de armar/desarmar |
| CA-006 | Backup automático diário executando | Verificação de logs |
| CA-007 | Uso de CPU < 50% em operação normal | Monitoramento por 24h |
| CA-008 | Uso de RAM < 70% em operação normal | Monitoramento por 24h |
| CA-009 | Temperatura do servidor < 70°C sob carga | Monitoramento |
| CA-010 | Sistema reinicia automaticamente após queda de energia | Teste de power cycle |
| CA-011 | Coordenador Zigbee estável com mesh ativo | Verificação de topologia |
| CA-012 | Dashboard acessível via app mobile (HA Companion) | Teste em smartphone |

---

## 10. Métricas de sucesso

| Métrica | Alvo | Medição |
|---------|------|---------|
| **Uptime do servidor** | > 99.5% | Monitoramento contínuo |
| **Tempo de boot** | < 120 segundos | Teste periódico |
| **Uso médio de CPU** | < 40% | System Monitor |
| **Uso médio de RAM** | < 60% | System Monitor |
| **FPS de detecção Frigate** | > 10 FPS | Dashboard Frigate |
| **Temperatura operacional** | < 65°C | System Monitor |

---

## 11. Riscos e dependências

### 11.1 Riscos

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| SSD falha e perde configuração | Baixa | Alto | Backup diário automatizado |
| Mini PC não suporta todas as câmeras | Baixa | Alto | Usar substream, limitar a 6 câmeras em N100 |
| Coordenador Zigbee falha | Baixa | Alto | Manter backup de coordinator + reserva |
| Atualização do HA quebra integração | Média | Médio | Fazer backup antes de atualizar |
| Overheating em local sem ventilação | Média | Médio | Posicionar em local ventilado |
| Extensão USB causa problemas Zigbee | Baixa | Médio | Usar cabo blindado de qualidade |

### 11.2 Dependências

| Dependência | Tipo | PRD relacionado |
|-------------|------|-----------------|
| Rede segmentada (VLANs) | Infraestrutura | PRD_NETWORK_SECURITY |
| Nobreak/UPS | Resiliência | PRD_BACKUP_AND_RESILIENCE |
| Câmeras compatíveis (RTSP) | Dispositivos | PRD_VIDEO_SURVEILLANCE_AND_NVR |
| Sensores Zigbee compatíveis | Dispositivos | PRD_SENSORS_AND_ALARMS_PLATFORM |
| Backup e restauração | Operacional | PRD_BACKUP_AND_RESILIENCE |

---

## 12. Referências

### Documentos do projeto
- `docs/ARQUITETURA_TECNICA.md` - Seções 2, 4, 6
- `prd/PRD_VIDEO_SURVEILLANCE_AND_NVR.md` - Requisitos de Frigate
- `prd/PRD_SENSORS_AND_ALARMS_PLATFORM.md` - Requisitos de Zigbee
- `rules/RULES_COMPLIANCE_AND_STANDARDS.md`

### Externos
- [Home Assistant Installation](https://www.home-assistant.io/installation/)
- [Frigate - Hardware Requirements](https://docs.frigate.video/frigate/hardware)
- [Zigbee2MQTT - Getting Started](https://www.zigbee2mqtt.io/guide/getting-started/)
- [Intel OpenVINO Toolkit](https://docs.openvino.ai/)
- [Proxmox VE](https://www.proxmox.com/en/proxmox-virtual-environment/overview)

---

> **Status**: Rascunho v1.0
>
> **Próxima revisão**: Após validação pelo Agente_Arquiteto_Tecnico
