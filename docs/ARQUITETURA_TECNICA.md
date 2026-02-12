# Arquitetura Técnica – Sistema de Home Security

> Documento produzido pelo Agente_Arquiteto_Tecnico
>
> Tarefas: T-004 a T-006, T-011 a T-017, T-026, T-027
>
> Data: 2026-02-12

---

## 1. Requisitos de Segurança Ativa por Cenário

### 1.1 Cenário Rural (T-004)

| Componente | Especificação | Quantidade sugerida | Protocolo recomendado |
|------------|---------------|---------------------|----------------------|
| **Câmeras externas** | PoE, 1080p+, visão noturna IR 30m+, RTSP/ONVIF | 4-6 | Ethernet (PoE) |
| **Sensor de abertura portão** | Magnético ou fim de curso | 1-2 | Zigbee ou 433MHz |
| **Sensor de movimento externo** | PIR duplo ou IVA (barreira) | 2-4 | Zigbee ou cabeado |
| **Sensor de vibração cerca** | Para cerca elétrica | 1 (central cerca) | Cabeado/433MHz |
| **Sirene externa** | 110dB+, resistente intempéries | 1-2 | Cabeada ou Zigbee |
| **Sirene interna** | 90dB+ | 1 | Zigbee |
| **Iluminação com sensor** | Refletor LED com PIR | 4-6 | Zigbee ou local |

**Desafios específicos do cenário rural:**
- Distâncias grandes exigem repetidores Zigbee ou sensores cabeados
- Possível necessidade de alimentação solar em pontos remotos
- Animais podem causar falsos positivos - usar sensores PIR pet-immune ou dupla tecnologia

### 1.2 Cenário Casa Urbana (T-005)

| Componente | Especificação | Quantidade sugerida | Protocolo recomendado |
|------------|---------------|---------------------|----------------------|
| **Câmera entrada** | PoE ou Wi-Fi, 1080p+, visão noturna | 1-2 | PoE preferencial |
| **Câmera quintal/fundos** | PoE, 1080p+, visão noturna, ângulo amplo | 1-2 | PoE |
| **Câmera lateral** | PoE ou Wi-Fi, visão noturna | 0-1 | PoE ou Wi-Fi |
| **Sensor abertura porta principal** | Magnético | 1 | Zigbee |
| **Sensor abertura porta serviço** | Magnético | 1 | Zigbee |
| **Sensor abertura janelas térreo** | Magnético | 4-8 | Zigbee |
| **Sensor movimento sala** | PIR | 1 | Zigbee |
| **Sensor movimento corredor** | PIR | 1 | Zigbee |
| **Sensor quebra de vidro** | Acústico | 1-2 | Zigbee |
| **Sirene interna** | 90dB+ | 1 | Zigbee |
| **Sirene externa** | 110dB+ | 1 | Cabeada |
| **Teclado/painel** | Para armar/desarmar | 1 | Zigbee ou Wi-Fi |

**Total estimado: 3-5 câmeras, 8-15 sensores**

### 1.3 Cenário Apartamento (T-006)

| Componente | Especificação | Quantidade sugerida | Protocolo recomendado |
|------------|---------------|---------------------|----------------------|
| **Olho mágico digital** | Câmera com visão noturna, gravação local | 0-1 | Wi-Fi |
| **Sensor abertura porta** | Magnético | 1 | Zigbee |
| **Sensor movimento entrada** | PIR | 1 | Zigbee |
| **Sensor movimento sala** | PIR (opcional) | 0-1 | Zigbee |
| **Fechadura inteligente** | Multiponto, biometria/senha/app | 1 | Zigbee ou Wi-Fi |
| **Sirene interna** | 85-90dB (considerar vizinhos) | 1 | Zigbee |
| **Botão de pânico** | Discreto | 1 | Zigbee |

**Total estimado: 0-1 câmera, 3-5 sensores**

---

## 2. Avaliação de Plataformas Open Source

### 2.1 Plataformas de Automação (T-013)

#### Home Assistant (RECOMENDADO)

| Aspecto | Avaliação |
|---------|-----------|
| **Comunidade** | ⭐⭐⭐⭐⭐ Maior comunidade, muita documentação |
| **Integrações** | ⭐⭐⭐⭐⭐ 2000+ integrações oficiais |
| **Atualizações** | ⭐⭐⭐⭐⭐ Releases mensais |
| **Interface** | ⭐⭐⭐⭐ Lovelace customizável |
| **Curva aprendizado** | ⭐⭐⭐⭐ Moderada, YAML opcional |
| **Segurança nativa** | ⭐⭐⭐⭐ Alarmo add-on excelente |

**Vantagens:**
- Maior número de integrações
- Comunidade muito ativa
- Add-on Alarmo para sistema de alarme completo
- Integração nativa com Frigate
- Suporte a Matter/Thread
- App mobile oficial

**Desvantagens:**
- Atualizações frequentes podem quebrar configurações
- Requer hardware mais robusto para muitas integrações

#### openHAB

| Aspecto | Avaliação |
|---------|-----------|
| **Comunidade** | ⭐⭐⭐ Menor que HA, mas ativa |
| **Integrações** | ⭐⭐⭐⭐ 400+ bindings |
| **Atualizações** | ⭐⭐⭐ Menos frequentes, mais estáveis |
| **Interface** | ⭐⭐⭐ Funcional, menos moderna |
| **Curva aprendizado** | ⭐⭐⭐ Maior, mais técnica |
| **Segurança nativa** | ⭐⭐⭐ Requer configuração manual |

**Vantagens:**
- Mais estável (menos breaking changes)
- Múltiplas linguagens de scripting
- Melhor para usuários técnicos avançados

**Desvantagens:**
- Menos integrações
- Documentação mais escassa
- Interface menos polida

#### Decisão: **Home Assistant**

Recomendado como plataforma principal devido à maior comunidade, mais integrações (especialmente com Frigate), add-on Alarmo para alarme, e app mobile funcional.

### 2.2 NVRs Open Source (T-014)

#### Frigate (RECOMENDADO)

| Aspecto | Avaliação |
|---------|-----------|
| **Detecção de objetos** | ⭐⭐⭐⭐⭐ IA local, pessoas/veículos/animais |
| **Integração HA** | ⭐⭐⭐⭐⭐ Nativa e completa |
| **Consumo recursos** | ⭐⭐⭐⭐ Eficiente com aceleração |
| **Facilidade uso** | ⭐⭐⭐⭐ Configuração YAML |
| **Aceleração IA** | ⭐⭐⭐⭐⭐ Coral, OpenVINO, GPU |

**Vantagens:**
- Detecção de objetos em tempo real
- Integração perfeita com Home Assistant
- Suporte a múltiplos aceleradores de IA
- Gravação apenas quando detecta objetos (economia de espaço)
- Zonas de detecção configuráveis

**Desvantagens:**
- Requer hardware para aceleração (recomendado)
- Configuração inicial mais complexa

#### ZoneMinder

| Aspecto | Avaliação |
|---------|-----------|
| **Maturidade** | ⭐⭐⭐⭐⭐ Projeto mais antigo e estável |
| **Detecção** | ⭐⭐⭐ Movimento básico, IA via plugins |
| **Interface** | ⭐⭐⭐ Web própria, funcional |
| **Integração HA** | ⭐⭐⭐ Via integração, menos completa |
| **Consumo recursos** | ⭐⭐⭐ Pode ser pesado |

**Vantagens:**
- Muito maduro e testado
- Interface web independente
- Boa documentação

**Desvantagens:**
- Detecção de objetos requer configuração adicional
- Interface menos moderna
- Integração com HA menos fluida

#### Shinobi

| Aspecto | Avaliação |
|---------|-----------|
| **Interface** | ⭐⭐⭐⭐ Moderna e responsiva |
| **Recursos** | ⭐⭐⭐⭐ Completo para NVR |
| **Estabilidade** | ⭐⭐⭐ Relatos de bugs |
| **Comunidade** | ⭐⭐⭐ Menor |

**Desvantagens:**
- Menos estável que concorrentes
- Comunidade menor
- Menos integrações

#### Decisão: **Frigate**

Recomendado como NVR principal devido à detecção de objetos nativa, integração perfeita com Home Assistant, e eficiência com aceleradores de IA.

---

## 3. Avaliação de Protocolos de Sensores (T-015)

### Matriz comparativa

| Protocolo | Alcance | Consumo | Mesh | Criptografia | Custo | Disponibilidade BR |
|-----------|---------|---------|------|--------------|-------|-------------------|
| **Zigbee** | 10-30m | Muito baixo | Sim | AES-128 | Baixo | Alta |
| **Z-Wave** | 30-100m | Muito baixo | Sim | AES-128 + S2 | Médio | Média |
| **Wi-Fi** | 30-50m | Alto | Não | WPA3 | Baixo | Alta |
| **433MHz** | 50-100m | Baixo | Não | Nenhuma | Muito baixo | Alta |
| **Thread/Matter** | 10-30m | Muito baixo | Sim | AES-128 | Médio | Baixa (crescendo) |

### Recomendações por uso

| Tipo de sensor | Protocolo recomendado | Justificativa |
|----------------|----------------------|---------------|
| **Abertura porta/janela** | Zigbee | Baixo consumo, longa bateria, custo baixo |
| **Movimento interno** | Zigbee | Resposta rápida, mesh |
| **Movimento externo** | Zigbee ou cabeado | Cabeado para maior confiabilidade |
| **Fechadura inteligente** | Zigbee ou Z-Wave | Z-Wave mais confiável, Zigbee mais barato |
| **Câmeras** | PoE Ethernet | Alimentação + dados, sem interferência |
| **Sirene** | Zigbee ou cabeada | Cabeada para externa (mais confiável) |

### Decisão: **Zigbee como protocolo principal**

**Justificativa:**
- Maior disponibilidade de sensores no Brasil (Aqara, Sonoff, Tuya)
- Custo-benefício excelente
- Baixo consumo (bateria dura 1-2 anos)
- Mesh network aumenta alcance
- Criptografia AES-128 adequada
- Excelente integração com Home Assistant (ZHA ou Zigbee2MQTT)

**Coordenador recomendado:**
- **Sonoff Zigbee 3.0 USB Dongle Plus** (CC2652P) - ~R$100-150
- Alternativa: **SLZB-06** (PoE, mais robusto) - ~R$200-300

### Sensores Zigbee recomendados

| Tipo | Modelo sugerido | Preço estimado |
|------|-----------------|----------------|
| Abertura porta/janela | Aqara MCCGQ11LM ou Sonoff SNZB-04 | R$50-80 |
| Movimento PIR | Aqara RTCGQ11LM ou Sonoff SNZB-03 | R$60-100 |
| Presença (mmWave) | Aqara FP2 ou Sonoff SNZB-06P | R$150-300 |
| Sirene interna | Heiman HS2WD-E ou Tuya TS0224 | R$100-150 |
| Temperatura/umidade | Aqara WSDCGQ11LM | R$60-100 |

---

## 4. Hardware de Processamento (T-016)

### Comparativo

| Hardware | CPU | RAM | Armazenamento | Preço estimado | Uso recomendado |
|----------|-----|-----|---------------|----------------|-----------------|
| **Raspberry Pi 4 4GB** | ARM Cortex-A72 | 4GB | microSD | R$400-500 | Apenas HA, sem Frigate |
| **Raspberry Pi 5 8GB** | ARM Cortex-A76 | 8GB | microSD/NVMe | R$550-700 | HA + Frigate leve (2-3 câmeras) |
| **Mini PC Intel N100** | Intel N100 | 8-16GB | SSD 256GB+ | R$800-1200 | HA + Frigate (4-8 câmeras) |
| **Mini PC Intel N305** | Intel N305 | 16GB | SSD 512GB+ | R$1500-2000 | HA + Frigate + addons pesados |

### Decisão: **Mini PC Intel N100** (RECOMENDADO)

**Justificativa:**
- Performance 2-3x superior ao Raspberry Pi 5
- Intel Quick Sync para transcodificação de vídeo (Frigate)
- Mais portas USB e conectividade
- SSD incluído (mais confiável que microSD)
- Custo similar ao RPi 5 com acessórios
- Suporte a OpenVINO para detecção de objetos

**Configuração mínima recomendada:**
- CPU: Intel N100 ou superior
- RAM: 8GB (16GB preferível)
- Armazenamento: SSD 256GB (sistema) + HDD/SSD 1TB+ (gravações)
- Rede: Gigabit Ethernet

### Aceleração de IA para Frigate

| Opção | Performance | Consumo | Preço | Recomendação |
|-------|-------------|---------|-------|--------------|
| **CPU (N100)** | 5-10 FPS | Alto | Incluso | Básico (2-3 câmeras) |
| **Intel iGPU (OpenVINO)** | 20-40 FPS | Médio | Incluso | Bom (4-6 câmeras) |
| **Google Coral USB** | 100+ FPS | Baixo | R$300-500 | Excelente eficiência |
| **Coral M.2** | 100+ FPS | Muito baixo | R$400-600 | Melhor para M.2 disponível |

**Nota:** Google Coral está sendo descontinuado. Para novas instalações, preferir OpenVINO (Intel) que já está incluso no N100.

---

## 5. Câmeras IP Compatíveis (T-017)

### Requisitos mínimos

- **Resolução**: 1080p (Full HD) mínimo, 2K/4K preferível
- **Protocolos**: RTSP obrigatório, ONVIF recomendado
- **Visão noturna**: IR 20m+ para externas
- **Alimentação**: PoE (802.3af) preferível
- **Codec**: H.264 obrigatório, H.265 preferível

### Marcas compatíveis com Frigate

| Marca | Compatibilidade | Faixa de preço | Observações |
|-------|-----------------|----------------|-------------|
| **Reolink** | ⭐⭐⭐⭐⭐ | R$200-600 | Excelente custo-benefício, RTSP nativo |
| **Hikvision** | ⭐⭐⭐⭐⭐ | R$300-1000 | Profissional, ONVIF completo |
| **Dahua** | ⭐⭐⭐⭐ | R$300-800 | Profissional, variações de firmware |
| **Annke** | ⭐⭐⭐⭐ | R$200-500 | Bom custo-benefício |
| **Amcrest** | ⭐⭐⭐⭐ | R$250-600 | RTSP confiável |
| **TP-Link (Tapo)** | ⭐⭐⭐ | R$150-300 | RTSP via hack em alguns modelos |

### Modelos sugeridos por cenário

| Cenário | Tipo | Modelo sugerido | Preço estimado |
|---------|------|-----------------|----------------|
| **Rural - entrada** | Bullet PoE 4MP | Reolink RLC-810A | R$400-500 |
| **Rural - perímetro** | Bullet PoE 5MP IR longo | Hikvision DS-2CD2055 | R$500-700 |
| **Urbana - entrada** | Dome/Bullet PoE 4MP | Reolink RLC-520A | R$300-400 |
| **Urbana - quintal** | Bullet PoE 4MP wide | Annke C500 | R$250-350 |
| **Apartamento** | Olho mágico digital | Aqara G4 Video Doorbell | R$500-700 |

### Infraestrutura de rede para câmeras

- **Switch PoE**: 8 portas mínimo, 802.3af/at, ~100W total
- **Sugestão**: TP-Link TL-SG1008P (~R$400) ou Ubiquiti USW-Lite-8-PoE (~R$800)
- **Cabeamento**: Cat5e ou Cat6, máximo 100m por cabo

---

## 6. Arquitetura Lógica de Integração (T-011)

### Diagrama de componentes

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              REDE DOMÉSTICA                                 │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        VLAN PRINCIPAL (Usuários)                     │   │
│  │   ┌──────────┐    ┌──────────┐    ┌──────────┐                      │   │
│  │   │ Notebook │    │ Celular  │    │  Tablet  │                      │   │
│  │   └────┬─────┘    └────┬─────┘    └────┬─────┘                      │   │
│  │        └───────────────┼───────────────┘                            │   │
│  └────────────────────────┼────────────────────────────────────────────┘   │
│                           │                                                 │
│  ┌────────────────────────┼────────────────────────────────────────────┐   │
│  │              VLAN GESTÃO (Servidor Home Security)                   │   │
│  │                        │                                            │   │
│  │            ┌───────────┴───────────┐                                │   │
│  │            │     MINI PC N100      │                                │   │
│  │            │  ┌─────────────────┐  │                                │   │
│  │            │  │ HOME ASSISTANT  │  │                                │   │
│  │            │  │  + Alarmo       │  │                                │   │
│  │            │  │  + Zigbee2MQTT  │  │                                │   │
│  │            │  │  + Frigate      │  │                                │   │
│  │            │  │  + MQTT Broker  │  │                                │   │
│  │            │  └─────────────────┘  │                                │   │
│  │            │         │             │                                │   │
│  │            │    ┌────┴────┐        │                                │   │
│  │            │    │ Zigbee  │        │                                │   │
│  │            │    │ Dongle  │        │                                │   │
│  │            │    └────┬────┘        │                                │   │
│  │            └─────────┼─────────────┘                                │   │
│  └──────────────────────┼──────────────────────────────────────────────┘   │
│                         │                                                   │
│  ┌──────────────────────┼──────────────────────────────────────────────┐   │
│  │              VLAN IoT (Sensores Zigbee - via dongle)                │   │
│  │                      │                                              │   │
│  │    ┌─────────────────┼─────────────────┐                            │   │
│  │    │                 │                 │                            │   │
│  │ ┌──┴──┐  ┌──────┐  ┌─┴───┐  ┌──────┐  ┌┴─────┐                     │   │
│  │ │Porta│  │Janela│  │ PIR │  │Sirene│  │Outros│                     │   │
│  │ └─────┘  └──────┘  └─────┘  └──────┘  └──────┘                     │   │
│  │  SNZB-04  SNZB-04  SNZB-03  HS2WD-E   Zigbee                       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │               VLAN CÂMERAS (Isolada, sem internet)                  │   │
│  │                                                                      │   │
│  │   ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐                   │   │
│  │   │ CAM 1  │  │ CAM 2  │  │ CAM 3  │  │ CAM 4  │                   │   │
│  │   │Entrada │  │ Fundos │  │Lateral │  │Garagem │                   │   │
│  │   └───┬────┘  └───┬────┘  └───┬────┘  └───┬────┘                   │   │
│  │       └───────────┴───────────┴───────────┘                        │   │
│  │                       │                                             │   │
│  │              ┌────────┴────────┐                                    │   │
│  │              │  SWITCH PoE     │                                    │   │
│  │              │  (8 portas)     │                                    │   │
│  │              └─────────────────┘                                    │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Fluxo de dados

```
┌──────────────┐     RTSP      ┌──────────────┐    Detecção    ┌──────────────┐
│   CÂMERAS    │──────────────►│   FRIGATE    │───────────────►│HOME ASSISTANT│
│   (PoE)      │               │   (NVR+IA)   │    Eventos     │   (Alarmo)   │
└──────────────┘               └──────────────┘                └──────┬───────┘
                                      │                               │
                               Gravação local                         │
                                      │                               │
                               ┌──────▼──────┐                        │
                               │  HDD/SSD    │                        │
                               │ (1TB+ NVR)  │                        │
                               └─────────────┘                        │
                                                                      │
┌──────────────┐    Zigbee     ┌──────────────┐     MQTT       ┌──────▼───────┐
│   SENSORES   │──────────────►│ ZIGBEE2MQTT  │───────────────►│HOME ASSISTANT│
│ (Zigbee 3.0) │               │  ou ZHA      │    Estados     │   (Alarmo)   │
└──────────────┘               └──────────────┘                └──────┬───────┘
                                                                      │
                                                               Automações
                                                                      │
                                                    ┌─────────────────┼─────────────────┐
                                                    │                 │                 │
                                             ┌──────▼──────┐   ┌──────▼──────┐   ┌──────▼──────┐
                                             │   SIRENES   │   │ NOTIFICAÇÕES│   │ ILUMINAÇÃO  │
                                             │             │   │ (Push/SMS)  │   │  (Reativa)  │
                                             └─────────────┘   └─────────────┘   └─────────────┘
```

### Componentes de software

| Componente | Função | Comunicação |
|------------|--------|-------------|
| **Home Assistant OS** | Sistema operacional | - |
| **Home Assistant Core** | Automação central | API REST, WebSocket |
| **Alarmo** | Sistema de alarme | Integração HA |
| **Frigate** | NVR + detecção IA | RTSP (entrada), MQTT (eventos) |
| **Zigbee2MQTT** | Bridge Zigbee | MQTT |
| **Mosquitto** | MQTT Broker | MQTT |
| **MariaDB** | Histórico de eventos | SQL |
| **InfluxDB** | Métricas (opcional) | InfluxDB protocol |
| **Grafana** | Dashboards (opcional) | HTTP |

---

## 7. Arquitetura de Rede Segura (T-012)

### Segmentação por VLANs

| VLAN | ID | Subnet | Função | Acesso Internet |
|------|-----|--------|--------|-----------------|
| **Principal** | 1 | 192.168.1.0/24 | Usuários, notebooks, celulares | Sim |
| **Gestão** | 10 | 192.168.10.0/24 | Servidor HA, NVR | Limitado (updates) |
| **IoT** | 20 | 192.168.20.0/24 | Sensores Wi-Fi (se houver) | Não |
| **Câmeras** | 30 | 192.168.30.0/24 | Câmeras IP | Não |

### Regras de firewall

```
# VLAN Câmeras (30) → Bloqueio total de saída
VLAN30 → Internet: DENY ALL
VLAN30 → VLAN1: DENY ALL
VLAN30 → VLAN10: ALLOW TCP 554 (RTSP), 80, 443 (ONVIF)
VLAN30 → VLAN20: DENY ALL

# VLAN IoT (20) → Acesso apenas ao servidor HA
VLAN20 → Internet: DENY ALL
VLAN20 → VLAN1: DENY ALL
VLAN20 → VLAN10: ALLOW TCP 1883 (MQTT), 8123 (HA)
VLAN20 → VLAN30: DENY ALL

# VLAN Gestão (10) → Acesso controlado
VLAN10 → Internet: ALLOW TCP 443 (updates), NTP
VLAN10 → VLAN1: ALLOW (para dashboard)
VLAN10 → VLAN20: ALLOW (gerenciar IoT)
VLAN10 → VLAN30: ALLOW (gerenciar câmeras)

# VLAN Principal (1) → Acesso ao dashboard
VLAN1 → VLAN10: ALLOW TCP 8123 (HA dashboard)
VLAN1 → VLAN20: DENY
VLAN1 → VLAN30: DENY
```

### Acesso remoto seguro

| Método | Segurança | Complexidade | Recomendação |
|--------|-----------|--------------|--------------|
| **WireGuard VPN** | ⭐⭐⭐⭐⭐ | Média | Recomendado |
| **Tailscale** | ⭐⭐⭐⭐⭐ | Baixa | Alternativa fácil |
| **Nabu Casa** | ⭐⭐⭐⭐ | Muito baixa | Opção paga ($6.5/mês) |
| **Cloudflare Tunnel** | ⭐⭐⭐⭐ | Média | Alternativa gratuita |
| **Port forwarding** | ⭐⭐ | Baixa | NÃO recomendado |

**Decisão: WireGuard VPN** (gratuito, seguro, integrado ao HA)

### Checklist de segurança de rede

- [ ] VLANs configuradas e isoladas
- [ ] Câmeras sem acesso à internet
- [ ] Sensores IoT Wi-Fi sem acesso à internet
- [ ] Firewall com regras restritivas
- [ ] VPN configurada para acesso remoto
- [ ] Senhas de todos os dispositivos alteradas
- [ ] Firmware de câmeras atualizado
- [ ] Wi-Fi com WPA3 (ou WPA2-AES mínimo)
- [ ] SSID da rede IoT oculto (opcional)

---

## 8. Requisitos de Privacidade por Design (T-026)

### Princípios implementados

| Princípio | Implementação |
|-----------|---------------|
| **Processamento local** | Toda IA e automação executam no servidor local |
| **Armazenamento local** | Gravações em HDD/SSD local, sem nuvem |
| **Minimização de dados** | Gravar apenas quando detecta movimento/pessoa |
| **Controle de acesso** | Autenticação obrigatória, 2FA recomendado |
| **Criptografia** | HTTPS para dashboard, VPN para acesso remoto |
| **Sem telemetria** | Desabilitar envio de dados a fabricantes |
| **Retenção limitada** | Rotação automática de gravações |

### Regras derivadas

```
REGRA-PRIV-01: Nenhum serviço de nuvem obrigatório para funcionamento básico.

REGRA-PRIV-02: Câmeras não devem ter acesso à internet (bloquear no firewall).

REGRA-PRIV-03: Desabilitar telemetria e "phone home" em todos os dispositivos.

REGRA-PRIV-04: Gravações armazenadas apenas localmente, com criptografia de disco recomendada.

REGRA-PRIV-05: Acesso remoto apenas via VPN, nunca port forwarding direto.

REGRA-PRIV-06: Autenticação obrigatória com senha forte; 2FA recomendado.

REGRA-PRIV-07: Log de todos os acessos ao sistema mantido por 90 dias.
```

---

## 9. Política de Retenção de Gravações (T-027)

### Períodos de retenção

| Tipo de gravação | Período | Justificativa |
|------------------|---------|---------------|
| **Gravações normais** | 30 dias | Padrão de mercado, equilíbrio espaço/utilidade |
| **Eventos com detecção** | 60 dias | Maior relevância, menor volume |
| **Incidentes marcados** | 1 ano | Evidências para possível uso legal |
| **Logs de acesso** | 90 dias | Auditoria de segurança |
| **Snapshots de eventos** | 90 dias | Referência rápida |

### Cálculo de armazenamento

| Cenário | Câmeras | Resolução | Horas/dia gravação* | Espaço/dia | Espaço 30 dias |
|---------|---------|-----------|---------------------|------------|----------------|
| Rural | 5 | 4MP H.265 | 2h | ~15 GB | ~450 GB |
| Urbana | 4 | 4MP H.265 | 3h | ~18 GB | ~540 GB |
| Apartamento | 1 | 1080p H.265 | 1h | ~2 GB | ~60 GB |

*Estimativa com gravação apenas quando há detecção de pessoa/veículo

**Recomendação de armazenamento:**
- **Rural/Urbana**: HDD 2TB mínimo (4TB recomendado)
- **Apartamento**: SSD 500GB suficiente

### Automação de rotação

```yaml
# Configuração Frigate - exemplo de retenção
record:
  enabled: True
  retain:
    days: 30
    mode: motion  # Apenas quando há movimento
  events:
    retain:
      default: 60  # Eventos detectados: 60 dias
```

---

## 10. Resumo de Recomendações

### Stack tecnológico recomendado

| Componente | Escolha | Alternativa |
|------------|---------|-------------|
| **Plataforma automação** | Home Assistant | openHAB |
| **NVR / Detecção IA** | Frigate | ZoneMinder |
| **Protocolo sensores** | Zigbee 3.0 | Z-Wave |
| **Coordenador Zigbee** | Sonoff ZBDongle-P | SLZB-06 |
| **Hardware servidor** | Mini PC Intel N100 | Raspberry Pi 5 |
| **Aceleração IA** | Intel OpenVINO | Google Coral |
| **Acesso remoto** | WireGuard VPN | Tailscale |

### Estimativa de investimento por cenário

| Componente | Rural | Urbana | Apartamento |
|------------|-------|--------|-------------|
| Servidor (Mini PC N100) | R$ 1.000 | R$ 1.000 | R$ 800 |
| Armazenamento (HDD/SSD) | R$ 400 | R$ 400 | R$ 200 |
| Coordenador Zigbee | R$ 150 | R$ 150 | R$ 150 |
| Câmeras (PoE) | R$ 2.000 | R$ 1.500 | R$ 500 |
| Switch PoE | R$ 400 | R$ 400 | - |
| Sensores Zigbee | R$ 800 | R$ 600 | R$ 300 |
| Sirene | R$ 200 | R$ 200 | R$ 100 |
| Nobreak | R$ 500 | R$ 400 | R$ 300 |
| Infraestrutura rede | R$ 500 | R$ 300 | R$ 100 |
| **TOTAL ESTIMADO** | **R$ 5.950** | **R$ 4.950** | **R$ 2.450** |

> Nota: Valores estimados, podem variar conforme fornecedor e configuração específica.

---

## Referências

### Plataformas
- [Home Assistant](https://www.home-assistant.io/)
- [Frigate NVR](https://docs.frigate.video/)
- [Zigbee2MQTT](https://www.zigbee2mqtt.io/)

### Comparativos
- [Home Assistant vs openHAB - WunderTech](https://www.wundertech.net/openhab-vs-home-assistant/)
- [Raspberry Pi 5 vs Intel N100 - CNX Software](https://www.cnx-software.com/2024/04/29/raspberry-pi-5-intel-n100-mini-pc-comparison-features-benchmarks-price/)
- [Zigbee vs Z-Wave vs WiFi - Key Security](https://www.keysecurity.com.tw/guia-de-comparacao-zigbee-vs-z-wave.html?lang=PT)

### Segurança
- [OWASP IoT Top 10](https://owasp.org/www-project-internet-of-things/)
- [Segurança em IoT - Kaspersky](https://www.kaspersky.com.br/resource-center/threats/secure-iot-devices-on-your-home-network)

---

> **Próximos passos**: Este documento deve ser usado como base para os PRDs técnicos (PRD_SENSORS_AND_ALARMS_PLATFORM, PRD_VIDEO_SURVEILLANCE_AND_NVR, PRD_NETWORK_SECURITY).

