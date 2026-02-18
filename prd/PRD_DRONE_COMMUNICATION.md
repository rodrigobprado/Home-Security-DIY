# PRD -- Comunicacao de Drones

> Sistema de Home Security -- Open Source / Open Hardware
>
> Modulo Reativo Avancado -- Rede de Comunicacao
>
> Versao: 1.0 | Data: 2026-02-18 | Responsavel: Agente_Arquiteto_Drones

---

## 1. Visao geral

- **Nome do produto/funcionalidade**: Rede de Comunicacao Redundante para Drones Autonomos
- **Responsavel**: Agente_Arquiteto_Drones
- **Data**: 2026-02-18
- **PRDs relacionados**: PRD_AUTONOMOUS_DRONES, PRD_DRONE_FLEET_MANAGEMENT, PRD_DRONE_DEFENSE_MODULE, PRD_NETWORK_SECURITY

---

## 2. Problema e oportunidade

### 2.1 Problema

Drones autonomos de seguranca dependem criticamente de comunicacao confiavel para:

- **Streaming de video** em tempo real para monitoramento e decisao
- **Telemetria** continua (posicao, bateria, status) para controle operacional
- **Comandos** bidirecionais para controle manual e autorizacoes de defesa
- **Coordenacao de frota** para operacao multi-drone eficiente

As solucoes existentes apresentam fragilidades:

- **Wi-Fi padrao** tem alcance limitado (50-100m) e e instavel em areas externas
- **Canal unico** de comunicacao cria ponto unico de falha
- **Perda de sinal** pode resultar em drones desorientados ou perdidos
- **Latencia alta** compromete streaming de video e autorizacoes de defesa
- **Frequencias nao homologadas** podem gerar multas da ANATEL

### 2.2 Oportunidade

Projetar uma rede de comunicacao que:

- **Combina multiplos canais**: Wi-Fi longo alcance (principal) + LoRa/Meshtastic (redundancia)
- **Failover automatico**: transicao transparente entre canais sem perda de controle
- **Suporta streaming**: video em tempo real com latencia aceitavel
- **Cobre grandes areas**: alcance de 200m+ (Wi-Fi) e 2km+ (LoRa)
- **Respeita regulamentacao**: frequencias e potencias homologadas pela ANATEL (REGRA-DRONE-08/09/10)
- **Integra nativamente**: com Home Assistant, Frigate e dashboard de monitoramento

---

## 3. Publico-alvo

| Perfil | Descricao | Necessidades especificas |
|--------|-----------|--------------------------|
| **Proprietario rural** | Grandes areas (>1 hectare) | Alcance longo, cobertura de perimetro extenso |
| **Proprietario urbano** | Casas com quintal | Cobertura confiavel sem interferencia urbana |
| **Operador de drones** | Pessoa monitorando o sistema | Baixa latencia para video e comandos |
| **Integrador DIY** | Construtor do sistema | Modulos acessiveis, documentacao de configuracao |

---

## 4. Requisitos funcionais

### 4.1 Canal principal -- Wi-Fi longo alcance

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-001 | Wi-Fi 5GHz como canal principal para streaming de video e comandos rapidos | Alta |
| RF-002 | Wi-Fi 2.4GHz como canal secundario para telemetria e comandos (maior alcance) | Alta |
| RF-003 | Access Point externo com antena direcional/setorial para cobertura ampla | Alta |
| RF-004 | Alcance minimo de 200m em linha de visada (Wi-Fi 5GHz) | Alta |
| RF-005 | Alcance minimo de 500m em linha de visada (Wi-Fi 2.4GHz) | Alta |
| RF-006 | Suporte a roaming entre multiplos APs para propriedades grandes | Media |
| RF-007 | Rede Wi-Fi dedicada para drones (VLAN isolada) | Alta |
| RF-008 | Criptografia WPA3-Personal ou WPA3-Enterprise | Alta |

### 4.2 Canal redundante -- LoRa/Meshtastic

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-009 | LoRa 915MHz como canal de redundancia para telemetria e comandos criticos | Alta |
| RF-010 | Protocolo Meshtastic para rede mesh auto-organizada | Alta |
| RF-011 | Alcance minimo de 2km em linha de visada | Alta |
| RF-012 | Capacidade de transmitir: posicao GPS, nivel de bateria, status operacional | Alta |
| RF-013 | Comandos criticos via LoRa: RTH (Return To Home), emergencia, desarmamento | Alta |
| RF-014 | Multiplos nos Meshtastic para cobertura mesh do perimetro | Media |
| RF-015 | Gateway LoRa na estacao base com integracao MQTT | Alta |

### 4.3 Failover automatico

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-016 | Deteccao automatica de perda de Wi-Fi 5GHz (timeout 3 segundos) | Alta |
| RF-017 | Failover para Wi-Fi 2.4GHz com reducao de qualidade de video | Alta |
| RF-018 | Deteccao de perda de Wi-Fi 2.4GHz (timeout 5 segundos) | Alta |
| RF-019 | Failover para LoRa/Meshtastic em modo degradado (apenas telemetria e comandos) | Alta |
| RF-020 | Em perda total de comunicacao: ativar modo autonomo (RTH) conforme REGRA-DRONE-18 | Alta |
| RF-021 | Reconexao automatica ao canal de maior prioridade quando disponivel | Alta |
| RF-022 | Registro de todos os eventos de failover em log | Alta |
| RF-023 | Notificacao ao operador quando failover e ativado | Alta |

### 4.4 Streaming de video

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-024 | Streaming RTSP/H.264 da camera principal | Alta |
| RF-025 | Resolucao adaptativa: 1080p (Wi-Fi 5GHz), 720p (Wi-Fi 2.4GHz) | Alta |
| RF-026 | Latencia de video < 500ms em Wi-Fi 5GHz | Alta |
| RF-027 | Compatibilidade com Frigate para analise de video | Alta |
| RF-028 | Suporte a WebRTC para visualizacao no dashboard | Media |
| RF-029 | Gravacao local no drone quando streaming nao disponivel | Alta |
| RF-030 | Sincronizacao de video gravado localmente quando comunicacao restaurada | Media |

### 4.5 Telemetria e comandos

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-031 | Telemetria continua via MQTT: posicao GPS, bateria, velocidade, heading | Alta |
| RF-032 | Frequencia de telemetria: 1Hz (Wi-Fi), 0.1Hz (LoRa) | Alta |
| RF-033 | Comandos bidirecionais: navegacao, defesa, status, configuracao | Alta |
| RF-034 | Latencia de comando < 200ms em Wi-Fi, < 2s em LoRa | Alta |
| RF-035 | Heartbeat entre drone e estacao base (timeout configuravel) | Alta |
| RF-036 | QoS diferenciado: comandos criticos com prioridade maxima | Alta |

### 4.6 Conformidade ANATEL

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-037 | Frequencias permitidas: 2.4GHz, 5.8GHz (Wi-Fi), 915MHz (LoRa) -- REGRA-DRONE-09 | Alta |
| RF-038 | Potencia maxima de transmissao conforme limites ANATEL (<=1W EIRP) -- REGRA-DRONE-10 | Alta |
| RF-039 | Utilizar apenas modulos de radio homologados pela ANATEL -- REGRA-DRONE-08 | Alta |
| RF-040 | Documentar certificacao de cada modulo de radio utilizado | Alta |

### 4.7 Seguranca de comunicacao

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-041 | Criptografia end-to-end para todos os canais (REGRA-DRONE-08) | Alta |
| RF-042 | TLS 1.3 para comunicacao Wi-Fi | Alta |
| RF-043 | AES-256 para payload LoRa | Alta |
| RF-044 | Autenticacao mutua (mTLS) entre drone e estacao base | Alta |
| RF-045 | Certificados digitais unicos por drone | Alta |
| RF-046 | Protecao contra replay attack (nonce + timestamp) | Alta |
| RF-047 | Deteccao de jamming (queda subita de RSSI em todos os canais) | Media |

---

## 5. Requisitos nao funcionais

### 5.1 Performance

| ID | Requisito | Especificacao |
|----|-----------|---------------|
| RNF-001 | Latencia de video (Wi-Fi 5GHz) | < 500ms |
| RNF-002 | Latencia de video (Wi-Fi 2.4GHz) | < 1000ms |
| RNF-003 | Latencia de comando (Wi-Fi) | < 200ms |
| RNF-004 | Latencia de comando (LoRa) | < 2 segundos |
| RNF-005 | Throughput de video (5GHz) | >= 5 Mbps |
| RNF-006 | Throughput de video (2.4GHz) | >= 2 Mbps |
| RNF-007 | Throughput de telemetria (LoRa) | >= 1 Kbps |
| RNF-008 | Tempo de failover entre canais | < 5 segundos |

### 5.2 Alcance e cobertura

| ID | Requisito | Especificacao |
|----|-----------|---------------|
| RNF-009 | Alcance Wi-Fi 5GHz (com AP externo) | > 200m LOS |
| RNF-010 | Alcance Wi-Fi 2.4GHz (com AP externo) | > 500m LOS |
| RNF-011 | Alcance LoRa 915MHz | > 2km LOS |
| RNF-012 | Alcance Meshtastic (mesh com 3 nos) | > 5km cobertura total |
| RNF-013 | Operacao em ambiente com obstaculos (vegetacao, muros) | Degradacao < 50% do alcance |

### 5.3 Confiabilidade

| ID | Requisito | Especificacao |
|----|-----------|---------------|
| RNF-014 | Disponibilidade do link de comunicacao | > 99.5% |
| RNF-015 | Taxa de perda de pacotes aceitavel | < 1% (Wi-Fi), < 5% (LoRa) |
| RNF-016 | Redundancia minima de canais | 2 canais independentes |
| RNF-017 | Recuperacao de falha de AP | < 30 segundos (reconexao) |
| RNF-018 | Protecao IP do AP externo | IP65 ou superior |

### 5.4 Conformidade

| ID | Requisito | Referencia |
|----|-----------|------------|
| RNF-019 | Modulos homologados ANATEL | REGRA-DRONE-08 |
| RNF-020 | Frequencias dentro das faixas permitidas | REGRA-DRONE-09 |
| RNF-021 | Potencia dentro dos limites legais | REGRA-DRONE-10 |
| RNF-022 | Criptografia end-to-end | REGRA-DRONE-08 |

---

## 6. Arquitetura tecnica

### 6.1 Diagrama de rede

```
+-----------------------------------------------------------------------+
|                         ESTACAO BASE                                  |
|  +--------------------+  +------------------+  +-------------------+  |
|  |   HOME ASSISTANT   |  |    MOSQUITTO     |  |     FRIGATE       |  |
|  |   + Dashboard      |<-|   MQTT Broker    |->|   NVR + IA        |  |
|  +--------------------+  +--------+---------+  +-------------------+  |
|                                   |                                   |
|         +-----------------+-------+-------+-----------------+         |
|         |                 |               |                 |         |
|  +------+------+  +------+------+  +------+------+  +------+------+  |
|  | AP Wi-Fi    |  | AP Wi-Fi    |  | Gateway     |  | Nos          | |
|  | 5GHz        |  | 2.4GHz      |  | LoRa        |  | Meshtastic   | |
|  | (Ubiquiti/  |  | (Ubiquiti/  |  | (RAK7268)   |  | (x3)         | |
|  |  Mikrotik)  |  |  Mikrotik)  |  |             |  | (T-Beam/     | |
|  +------+------+  +------+------+  +------+------+  |  XIAO)       | |
|         |                |                |          +------+------+  |
+---------+----------------+----------------+-----------------+---------+
          |                |                |                 |
          |        AREA DE COBERTURA        |                 |
          |                |                |                 |
   +------+------+  +-----+------+  +------+------+  +------+------+
   |   DRONE 1   |  |  DRONE 2   |  |  DRONE 3   |  |  DRONE N   |
   |              |  |            |  |            |  |            |
   | [ESP32-S3]  |  | [ESP32-S3] |  | [ESP32-S3] |  | [ESP32-S3] |
   | Wi-Fi 5GHz  |  | Wi-Fi 5GHz |  | Wi-Fi 5GHz |  | Wi-Fi 5GHz |
   | Wi-Fi 2.4GHz|  | Wi-Fi 2.4G |  | Wi-Fi 2.4G |  | Wi-Fi 2.4G |
   | LoRa (RFM95)|  | LoRa       |  | LoRa       |  | LoRa       |
   +-------------+  +------------+  +------------+  +------------+
```

### 6.2 Matriz de redundancia e failover

```
PRIORIDADE 1: Wi-Fi 5GHz (baixa latencia, alto throughput)
     |
     +-- Dados: Video HD + Telemetria + Comandos
     +-- Falha detectada (timeout 3s)
     |
     v
PRIORIDADE 2: Wi-Fi 2.4GHz (maior alcance)
     |
     +-- Dados: Video SD + Telemetria + Comandos
     +-- Falha detectada (timeout 5s)
     |
     v
PRIORIDADE 3: LoRa/Meshtastic (ultra-longo alcance)
     |
     +-- Dados: Apenas telemetria + comandos criticos
     +-- Modo degradado: sem video, comandos basicos
     |
     v
FALLBACK: Modo autonomo total
     |
     +-- RTH (Return To Home) automatico (REGRA-DRONE-18)
     +-- Gravacao local de video
     +-- Tentativa de reconexao periodica
```

### 6.3 Protocolo de comunicacao por camada

| Camada | Wi-Fi 5GHz | Wi-Fi 2.4GHz | LoRa |
|--------|------------|--------------|------|
| **Transporte** | TCP/UDP | TCP/UDP | LoRa PHY |
| **Sessao** | TLS 1.3 | TLS 1.3 | AES-256 |
| **Aplicacao** | MQTT + RTSP/WebRTC | MQTT | Meshtastic Protocol |
| **Dados** | Video + Telemetria + Comandos | Telemetria + Comandos | Telemetria critica |

### 6.4 Topicos MQTT

| Topico | Direcao | QoS | Descricao |
|--------|---------|-----|-----------|
| `drone/{id}/telemetry` | Drone -> Base | 0 | Posicao, bateria, velocidade, heading |
| `drone/{id}/status` | Drone -> Base | 1 | Status operacional completo |
| `drone/{id}/command` | Base -> Drone | 2 | Comandos de navegacao e operacao |
| `drone/{id}/emergency` | Bidirecional | 2 | Comandos de emergencia (RTH, stop) |
| `drone/{id}/defense/*` | Bidirecional | 2 | Comandos do modulo de defesa |
| `drone/{id}/video/snapshot` | Drone -> Base | 0 | Snapshots periodicos |
| `drone/{id}/link/quality` | Drone -> Base | 0 | RSSI, SNR, canal ativo |
| `fleet/coordination` | Base -> Todos | 1 | Comandos de coordenacao de frota |

### 6.5 Integracao ROS2

| No ROS2 | Funcao |
|---------|--------|
| `/comm_manager` | Gerencia canais de comunicacao e failover |
| `/mqtt_bridge` | Ponte entre ROS2 e MQTT broker |
| `/video_streamer` | Streaming adaptativo de video (RTSP/WebRTC) |
| `/lora_driver` | Driver para modulo LoRa (SPI) |
| `/link_monitor` | Monitora qualidade de todos os links |

---

## 7. Hardware e componentes recomendados

### 7.1 Estacao base -- Access Points

| Componente | Modelo | Preco estimado (R$) | Especificacao |
|------------|--------|---------------------|---------------|
| AP Wi-Fi externo | Ubiquiti LiteAP AC (LAP-120) | R$ 600-900 | 5GHz, 120 graus, IP67 |
| AP Wi-Fi externo | Mikrotik SXTsq 5 ac | R$ 400-600 | 5GHz, direcional, IP66 |
| AP Wi-Fi 2.4GHz | Ubiquiti NanoStation Loco M2 | R$ 300-500 | 2.4GHz, longo alcance |
| AP Wi-Fi (alternativa) | TP-Link CPE510 | R$ 250-400 | 5GHz, 13dBi, outdoor |

### 7.2 Estacao base -- LoRa/Meshtastic

| Componente | Modelo | Preco estimado (R$) | Especificacao |
|------------|--------|---------------------|---------------|
| Gateway LoRa | RAK7268 WisGate Edge Lite 2 | R$ 800-1.200 | 915MHz, 8 canais, PoE |
| Gateway (alternativa) | Dragino LPS8N | R$ 500-800 | 915MHz, indoor |
| No Meshtastic | LILYGO T-Beam v1.2 (x3) | R$ 150-250 (cada) | ESP32 + LoRa + GPS |
| No Meshtastic (alt.) | Seeed XIAO nRF52840 + LoRa | R$ 100-180 (cada) | Compacto, baixo consumo |
| Antena externa LoRa | Fiberglass 915MHz 6dBi | R$ 80-150 | Omnidirecional, outdoor |

### 7.3 Modulo no drone

| Componente | Modelo | Preco estimado (R$) | Especificacao |
|------------|--------|---------------------|---------------|
| Wi-Fi + BLE | ESP32-S3 (dual-band) | R$ 50-80 | 2.4GHz + 5GHz |
| Modulo LoRa | RFM95W 915MHz | R$ 30-50 | SPI, 915MHz, +20dBm |
| Antena Wi-Fi (drone) | PCB ou dipolo 2.4/5GHz | R$ 10-20 | Compacta, leve |
| Antena LoRa (drone) | Wire whip 915MHz | R$ 5-15 | 1/4 onda, leve |
| U.FL pigtails | Cabo adaptador | R$ 10-20 | Para antenas externas |

### 7.4 Estimativa de custo total

| Configuracao | Custo estimado |
|--------------|----------------|
| **Estacao base basica (1 AP + 1 gateway LoRa)** | R$ 900-1.500 |
| **Estacao base completa (2 APs + gateway + 3 nos mesh)** | R$ 2.000-3.500 |
| **Modulo de comunicacao por drone** | R$ 100-180 |
| **Infraestrutura rural (3 APs + gateway + 5 nos mesh)** | R$ 3.500-5.500 |

---

## 8. Criterios de aceitacao

| ID | Criterio | Metodo de verificacao |
|----|----------|----------------------|
| CA-001 | Streaming de video funciona com latencia < 500ms em Wi-Fi 5GHz | Medicao de latencia com ferramenta de benchmark |
| CA-002 | Alcance Wi-Fi 5GHz atinge 200m+ em linha de visada | Teste de campo com medicao de RSSI |
| CA-003 | Alcance Wi-Fi 2.4GHz atinge 500m+ em linha de visada | Teste de campo |
| CA-004 | Alcance LoRa atinge 2km+ em linha de visada | Teste de campo |
| CA-005 | Failover Wi-Fi 5GHz -> 2.4GHz ocorre em menos de 5 segundos | Teste de interrupcao de sinal |
| CA-006 | Failover Wi-Fi -> LoRa ocorre em menos de 8 segundos | Teste de interrupcao de sinal |
| CA-007 | RTH automatico ativa em perda total de comunicacao | Teste de interrupcao total |
| CA-008 | Telemetria via LoRa transmite posicao e bateria corretamente | Teste funcional |
| CA-009 | Comandos criticos (RTH, emergencia) funcionam via LoRa | Teste funcional |
| CA-010 | Criptografia end-to-end ativa em todos os canais | Teste de captura de pacotes |
| CA-011 | Video gravado localmente e sincronizado apos reconexao | Teste de gravacao + reconexao |
| CA-012 | Todos os modulos de radio sao homologados ANATEL | Verificacao de certificados |
| CA-013 | MQTT integra corretamente com Home Assistant | Teste de integracao |

---

## 9. Metricas de sucesso

| Metrica | Alvo | Medicao |
|---------|------|---------|
| **Disponibilidade do link** | > 99.5% de tempo com comunicacao ativa | Monitoramento continuo de heartbeat |
| **Latencia media de video** | < 500ms (5GHz), < 1000ms (2.4GHz) | Medicao periodica |
| **Taxa de perda de pacotes** | < 1% (Wi-Fi), < 5% (LoRa) | Analise de logs MQTT |
| **Tempo medio de failover** | < 5 segundos entre canais | Analise de logs de failover |
| **Cobertura de area** | 100% da propriedade com pelo menos 1 canal ativo | Mapeamento de cobertura |
| **Uptime da estacao base** | > 99.9% | Monitoramento de infraestrutura |

---

## 10. Riscos e dependencias

### 10.1 Riscos

| Risco | Probabilidade | Impacto | Mitigacao |
|-------|---------------|---------|-----------|
| Interferencia Wi-Fi em area urbana densa | Alta | Medio | Usar 5GHz (menos congestionado) + canais DFS |
| Alcance Wi-Fi insuficiente em propriedade rural | Media | Alto | Multiplos APs com roaming + LoRa como backup |
| Jamming intencional de comunicacao | Baixa | Critico | Deteccao de jamming + RTH automatico + gravacao local |
| Falha do gateway LoRa | Baixa | Alto | Nos Meshtastic como redundancia (mesh descentralizado) |
| Latencia excessiva para autorizacao de defesa | Media | Alto | QoS prioritario para comandos de defesa |
| Incompatibilidade entre modulos e firmware | Media | Medio | Testes de integracao rigorosos + versoes de firmware pinadas |
| Umidade/temperatura danifica equipamento externo | Media | Medio | Equipamentos IP65+, caixas hermeticas |

### 10.2 Dependencias

| Dependencia | Tipo | PRD relacionado |
|-------------|------|-----------------|
| Rede local segmentada (VLANs) | Infraestrutura | PRD_NETWORK_SECURITY |
| Plataforma de drones autonomos | Base | PRD_AUTONOMOUS_DRONES |
| Dashboard de monitoramento | Interface | PRD_MONITORING_DASHBOARD |
| Gerenciamento de frota | Coordenacao | PRD_DRONE_FLEET_MANAGEMENT |
| MQTT Broker (Mosquitto) | Middleware | PRD_LOCAL_PROCESSING_HUB |

---

## 11. Referencias

### Documentos do projeto

- `docs/ARQUITETURA_DRONES_AUTONOMOS.md` -- Secao 5 (Arquitetura de Comunicacao)
- `rules/RULES_COMPLIANCE_AND_STANDARDS.md` -- REGRA-DRONE-08, 09, 10, 18
- `standards/STANDARDS_TO_RESEARCH.md` -- Secao 8.3 (ANATEL)

### Regulamentacao

- [ANATEL - Certificacao e Homologacao](https://www.gov.br/anatel/pt-br/regulado/certificacao-de-produtos)
- [Faixas de frequencia ISM Brasil - ANATEL](https://sistemas.anatel.gov.br/sch/)
- [DECEA - Requisitos de comunicacao](https://www.decea.mil.br/)

### Externos

- [Meshtastic Documentation](https://meshtastic.org/docs/)
- [LoRa Alliance](https://lora-alliance.org/)
- [Ubiquiti airMAX Documentation](https://help.ui.com/hc/en-us/categories/airmax)
- [Mikrotik RouterOS Documentation](https://help.mikrotik.com/)
- [ESP32-S3 Wi-Fi Documentation](https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/)
- [RFM95W Datasheet](https://www.hoperf.com/modules/lora/RFM95.html)

---

> **Status**: Rascunho v1.0
>
> **Proxima revisao**: Apos testes de alcance e cobertura em campo
