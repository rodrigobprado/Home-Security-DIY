# Alternativas Comerciais Compativeis

> Sistema de Home Security – Open Source / Open Hardware
>
> Versao: 1.0 | Data: 2026-02-18 | Referencia: T-068

---

## 1. Proposito

Documentar alternativas comerciais para cada subsistema quando a abordagem DIY nao e viavel (falta de tempo, conhecimento tecnico ou preferencia por solucao pronta). Todas as alternativas listadas sao compativeis com o ecossistema do projeto.

---

## 2. Criterios de selecao

Para ser listada, a alternativa deve atender pelo menos 3 dos 5 criterios:

- Integracao com Home Assistant (nativa ou via MQTT/API)
- Processamento local (sem dependencia obrigatoria de nuvem)
- Protocolos abertos (RTSP, ONVIF, Zigbee, MQTT)
- Disponibilidade no mercado brasileiro
- Custo acessível para uso residencial

---

## 3. Alternativas por subsistema

### 3.1 Plataforma de automacao

| Alternativa | Tipo | Integracao HA | Preco | Observacao |
|-------------|------|---------------|-------|------------|
| **Home Assistant Green** | Hardware dedicado | Nativa | R$ 500-700 | Plug-and-play, pre-instalado |
| **Home Assistant Yellow** | Hardware dedicado + Zigbee | Nativa | R$ 800-1200 | Inclui chip Zigbee |
| **ODROID-N2+** | SBC pre-configuravel | Nativa | R$ 600-800 | Recomendado pela comunidade HA |
| **Hubitat Elevation** | Hub proprietario | Via Maker API | R$ 500-700 | Local-first, sem assinatura |

**Recomendacao**: Home Assistant Green para usuarios sem experiencia tecnica.

### 3.2 NVR / Videovigilancia

| Alternativa | Tipo | RTSP/ONVIF | Preco | Observacao |
|-------------|------|------------|-------|------------|
| **Reolink NVR (RLN8-410)** | NVR dedicado | Sim | R$ 800-1200 | 8ch, PoE integrado, app mobile |
| **Reolink NVR (RLN16-410)** | NVR dedicado | Sim | R$ 1200-1800 | 16ch, PoE integrado |
| **Hikvision DS-7608NI** | NVR profissional | Sim | R$ 1500-2500 | 8ch, IA basica embutida |
| **Synology DVA1622** | NAS + NVR com IA | Sim | R$ 4000-6000 | Deteccao de objetos, alto custo |
| **Blue Iris** (Windows) | Software NVR | Sim | R$ 350 (licenca) | Bom custo-beneficio, requer PC |

**Recomendacao**: Reolink NVR para quem quer simplicidade; Blue Iris para quem ja tem um PC disponivel.

### 3.3 Sensores e alarme

| Alternativa | Tipo | Protocolo | Preco | Observacao |
|-------------|------|-----------|-------|------------|
| **Kit Aqara Starter** | Kit sensores Zigbee | Zigbee | R$ 400-600 | Hub + 2 sensores + botao |
| **Kit Sonoff Zigbee** | Kit sensores Zigbee | Zigbee | R$ 300-500 | Dongle + sensores |
| **Ajax Systems** | Alarme profissional | Proprietario | R$ 2000-5000 | Alta qualidade, app excelente, nuvem |
| **Intelbras ANM 3004** | Central de alarme | 433MHz / cabeado | R$ 300-500 | Tradicional, sem smart home |
| **Ring Alarm** | Kit alarme | Wi-Fi/Z-Wave | R$ 1500-2500 | Importacao, requer assinatura |

**Recomendacao**: Kit Aqara/Sonoff Zigbee (compativel com o projeto) ou Ajax Systems (se orcamento permitir e aceitar nuvem).

### 3.4 Cameras IP

| Alternativa | Tipo | RTSP | Preco unitario | Observacao |
|-------------|------|------|----------------|------------|
| **Reolink RLC-520A** | Dome PoE 5MP | Sim | R$ 300-400 | Melhor custo-beneficio |
| **Reolink RLC-810A** | Bullet PoE 4K | Sim | R$ 400-600 | Otima para externas |
| **Hikvision DS-2CD1043** | Bullet PoE 4MP | Sim | R$ 350-500 | Profissional |
| **Tapo C320WS** | Wi-Fi outdoor | Sim (hack) | R$ 200-300 | Barata, RTSP via firmware |
| **Intelbras VIP 1230** | Dome PoE 2MP | Sim | R$ 250-400 | Marca nacional, suporte local |

**Recomendacao**: Reolink para melhor compatibilidade com Frigate; Intelbras para suporte local.

### 3.5 Rede e seguranca

| Alternativa | Tipo | VLANs | Preco | Observacao |
|-------------|------|-------|-------|------------|
| **Ubiquiti Dream Machine** | Router + firewall | Sim | R$ 2000-3000 | Interface excelente, VLANs faceis |
| **Ubiquiti EdgeRouter X** | Router | Sim | R$ 400-600 | Barato, CLI |
| **MikroTik hAP ax3** | Router | Sim | R$ 500-800 | Muito configuravel |
| **pfSense (Mini PC)** | Firewall software | Sim | R$ 800-1200 (HW) | Maximo controle |
| **TP-Link Omada** | Sistema gerenciado | Sim | R$ 600-1500 | Alternativa economica a Ubiquiti |

**Recomendacao**: Ubiquiti Dream Machine para simplicidade; MikroTik ou pfSense para maximo controle.

### 3.6 Switch PoE

| Alternativa | Portas PoE | Potencia | Preco | Observacao |
|-------------|-----------|----------|-------|------------|
| **TP-Link TL-SG1008P** | 4 PoE + 4 | 64W | R$ 350-500 | Basico, nao gerenciavel |
| **TP-Link TL-SG2008P** | 4 PoE + 4 | 62W | R$ 500-700 | Gerenciavel, VLANs |
| **Ubiquiti USW-Lite-8-PoE** | 4 PoE + 4 | 52W | R$ 700-1000 | Integracao UniFi |
| **Intelbras SG 800 Q+** | 4 PoE + 4 | 60W | R$ 300-450 | Nacional, suporte local |

**Recomendacao**: Intelbras para custo-beneficio; Ubiquiti para ecossistema UniFi.

### 3.7 Fechaduras inteligentes

| Alternativa | Acesso | Protocolo | Preco | Observacao |
|-------------|--------|-----------|-------|------------|
| **Aqara U200** | PIN + app + chave | Zigbee + Matter | R$ 800-1200 | Otima integracao HA |
| **Yale Assure Lock 2** | PIN + app + chave | Wi-Fi/Matter | R$ 1500-2500 | Marca premium |
| **Papaiz Smart Lock** | PIN + biometria + chave | Wi-Fi | R$ 600-1000 | Nacional |
| **Samsung SHP-DP609** | Biometria + PIN + app | Wi-Fi | R$ 2000-3000 | Premium, boa biometria |
| **Intelbras FR 320** | Biometria + PIN + chave | Standalone | R$ 500-800 | Nacional, sem smart home |

**Recomendacao**: Aqara U200 para integracao com HA; Papaiz para opcao nacional.

### 3.8 Nobreak / UPS

| Alternativa | Potencia | Autonomia* | Preco | Observacao |
|-------------|----------|------------|-------|------------|
| **APC Back-UPS 600VA** | 600VA / 300W | 15-20 min | R$ 400-600 | Basico |
| **APC Back-UPS 1500VA** | 1500VA / 900W | 30-40 min | R$ 900-1300 | Recomendado |
| **SMS Station II 1400VA** | 1400VA / 840W | 25-35 min | R$ 700-1000 | Nacional |
| **Ts Shara UPS 1800VA** | 1800VA / 1080W | 30-45 min | R$ 800-1200 | Senoidal pura |

*Autonomia estimada com carga do servidor + switch PoE (~150W total)

**Recomendacao**: APC 1500VA para confiabilidade; SMS/Ts Shara como opcoes nacionais.

---

## 4. Kits recomendados por perfil

### Perfil 1: "Quero facil e rapido" (minimo DIY)

| Componente | Produto | Preco |
|------------|---------|-------|
| Hub | Home Assistant Green | R$ 600 |
| NVR | Reolink RLN8-410 (4 cameras incluso) | R$ 2500 |
| Alarme | Kit Aqara Starter | R$ 500 |
| Fechadura | Papaiz Smart Lock | R$ 800 |
| Nobreak | APC 1500VA | R$ 1100 |
| **Total** | | **~R$ 5.500** |

### Perfil 2: "DIY com ajuda" (parcialmente DIY)

| Componente | Produto | Preco |
|------------|---------|-------|
| Servidor | Mini PC N100 + Docker | R$ 1000 |
| Cameras | 4x Reolink RLC-520A | R$ 1400 |
| Sensores | Sonoff Zigbee (dongle + 8 sensores) | R$ 600 |
| Rede | MikroTik hAP ax3 + switch PoE | R$ 1000 |
| Nobreak | SMS 1400VA | R$ 800 |
| **Total** | | **~R$ 4.800** |

### Perfil 3: "100% DIY" (projeto completo)

Seguir a arquitetura principal do projeto. Ver `docs/ARQUITETURA_TECNICA.md` Secao 10 para estimativas detalhadas.

---

## 5. Servicos de monitoramento compativeis

Para quem deseja monitoramento profissional como complemento:

| Servico | Compatibilidade | Preco mensal | Observacao |
|---------|-----------------|--------------|------------|
| **Nabu Casa** | Home Assistant nativo | ~R$ 35/mes | Acesso remoto + Alexa/Google |
| **Pushover** | API REST | R$ 25 (unico) | Notificacoes push confiáveis |
| **Telegram Bot** | API gratuita | Gratuito | Canal de notificacao backup |

> **Nota**: O projeto e desenhado para **nao depender de servicos pagos**. Estes sao opcionais para conveniencia.

---

## Referencias

- `docs/ARQUITETURA_TECNICA.md` — Stack tecnologico recomendado
- `prd/PRD_SENSORS_AND_ALARMS_PLATFORM.md` — Sensores e alarme
- `prd/PRD_VIDEO_SURVEILLANCE_AND_NVR.md` — Videovigilancia
- `prd/PRD_NETWORK_SECURITY.md` — Seguranca de rede
