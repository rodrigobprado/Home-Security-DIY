# Arquitetura do Sistema

> Sistema de Home Security – Open Source / Open Hardware
>
> Versao: 1.0 | Data: 2026-02-18

---

## 1. Visao geral

Sistema de seguranca residencial 100% local (on-premise), sem dependencia de nuvem, projetado para tres cenarios: propriedade rural, casa urbana e apartamento. Utiliza abordagem defense-in-depth com tres camadas de seguranca (passiva, ativa, reativa).

### Principios arquiteturais

- **Privacy by design**: Processamento e armazenamento 100% local
- **Modularidade**: Componentes independentes comunicando via MQTT
- **Resiliencia**: Modos de operacao degradada, failover de comunicacao
- **Interoperabilidade**: Protocolos abertos (Zigbee, MQTT, RTSP, ONVIF)

---

## 2. Diagrama de componentes

```mermaid
graph TD
    subgraph Servidor ["Servidor Central (Mini PC Intel N100)"]
        HA[Home Assistant + Alarmo]
        Frigate[Frigate NVR + OpenVINO]
        Z2M[Zigbee2MQTT]
        MQTT[Mosquitto MQTT Broker]

        Z2M -->|MQTT publish| MQTT
        MQTT -->|MQTT subscribe| HA
        Frigate -->|MQTT eventos| MQTT
        HA -->|REST API| Frigate
    end

    subgraph Sensores ["Sensores Zigbee 3.0"]
        SA[Sensor Abertura]
        SP[Sensor PIR]
        SM[Sensor mmWave]
        SI[Sirene]
        BT[Botao Panico]
    end

    subgraph Cameras ["Cameras IP (VLAN Isolada)"]
        C1[Cam Entrada]
        C2[Cam Fundos]
        C3[Cam Lateral]
        C4[Cam Garagem]
        SW[Switch PoE]
    end

    subgraph Usuarios ["Usuarios"]
        APP[App HA Companion]
        WEB[Dashboard Web]
        VPN[WireGuard VPN]
    end

    subgraph Notificacoes ["Canais de Alerta"]
        PUSH[Push Notification]
        TG[Telegram]
        EMAIL[E-mail]
    end

    %% Conexoes
    Dongle[USB Zigbee Dongle] -->|Zigbee Mesh| SA
    Dongle -->|Zigbee Mesh| SP
    Dongle -->|Zigbee Mesh| SM
    Dongle -->|Zigbee Mesh| SI
    Dongle -->|Zigbee Mesh| BT
    Dongle -->|USB| Z2M

    C1 -->|PoE| SW
    C2 -->|PoE| SW
    C3 -->|PoE| SW
    C4 -->|PoE| SW
    SW -->|RTSP| Frigate

    VPN -->|Acesso remoto| HA
    APP -->|API| HA
    WEB -->|HTTP| HA

    HA -->|Disparo| PUSH
    HA -->|Disparo| TG
    HA -->|Disparo| EMAIL
```

---

## 3. Fluxo de dados

```mermaid
flowchart LR
    subgraph Entrada ["Fontes de Dados"]
        CAM[Cameras PoE]
        SEN[Sensores Zigbee]
    end

    subgraph Processamento ["Processamento Local"]
        FRI[Frigate - Deteccao IA]
        Z2M2[Zigbee2MQTT]
        MQ[Mosquitto MQTT]
        HA2[Home Assistant]
    end

    subgraph Saida ["Acoes"]
        SIR[Sirenes]
        LUZ[Iluminacao Reativa]
        NOT[Notificacoes]
        GRV[Gravacao em Disco]
    end

    CAM -->|RTSP stream| FRI
    FRI -->|eventos deteccao| MQ
    FRI -->|video clips| GRV

    SEN -->|Zigbee 3.0| Z2M2
    Z2M2 -->|estados sensores| MQ

    MQ -->|subscribe| HA2

    HA2 -->|automacao| SIR
    HA2 -->|automacao| LUZ
    HA2 -->|alerta| NOT
```

---

## 4. Fluxo de evento de alarme

```mermaid
sequenceDiagram
    participant S as Sensor Zigbee
    participant Z as Zigbee2MQTT
    participant M as Mosquitto MQTT
    participant H as Home Assistant
    participant A as Alarmo
    participant F as Frigate

    S->>Z: Evento (abertura/movimento)
    Z->>M: MQTT publish (zigbee2mqtt/sensor/...)
    M->>H: MQTT subscribe
    H->>A: Verificar modo de armamento

    alt Sistema armado
        A->>A: Aplicar delay de entrada (se configurado)
        A->>H: Confirmar alarme
        H->>M: MQTT publish (alarme ativo)
        par Acoes simultaneas
            H->>H: Acionar sirene(s)
            H->>H: Enviar notificacoes (push/Telegram)
            H->>F: Solicitar snapshot/gravacao
            F->>F: Gravar clip do evento
        end
    else Sistema desarmado
        A->>H: Registrar evento (log)
    end
```

---

## 5. Arquitetura de rede

```mermaid
graph TB
    subgraph Internet
        WG[WireGuard VPN]
    end

    subgraph Router ["Router / Firewall"]
        FW[Firewall + VLANs]
    end

    subgraph VLAN1 ["VLAN 1 - Principal (192.168.1.0/24)"]
        PC[Notebooks]
        CEL[Celulares]
    end

    subgraph VLAN10 ["VLAN 10 - Gestao (192.168.10.0/24)"]
        SRV[Servidor HA / NVR]
    end

    subgraph VLAN20 ["VLAN 20 - IoT (192.168.20.0/24)"]
        IOT[Sensores Wi-Fi]
    end

    subgraph VLAN30 ["VLAN 30 - Cameras (192.168.30.0/24)"]
        CAMS[Cameras IP]
    end

    WG --> FW
    FW --> VLAN1
    FW --> VLAN10
    FW --> VLAN20
    FW --> VLAN30

    VLAN1 -.->|TCP 8123| VLAN10
    VLAN10 -->|TCP 1883, 8123| VLAN20
    VLAN10 -->|TCP 554, 80| VLAN30
    VLAN20 -.-x|BLOQUEADO| Internet
    VLAN30 -.-x|BLOQUEADO| Internet
```

### Regras de acesso entre VLANs

| Origem | Destino | Permitido | Portas |
|--------|---------|-----------|--------|
| VLAN 1 (Principal) | VLAN 10 (Gestao) | Sim | TCP 8123 (dashboard HA) |
| VLAN 10 (Gestao) | VLAN 20 (IoT) | Sim | TCP 1883 (MQTT), 8123 |
| VLAN 10 (Gestao) | VLAN 30 (Cameras) | Sim | TCP 554 (RTSP), 80, 443 |
| VLAN 20 (IoT) | Internet | **Nao** | - |
| VLAN 30 (Cameras) | Internet | **Nao** | - |
| VLAN 10 (Gestao) | Internet | Limitado | TCP 443 (updates), NTP |

---

## 6. Stack tecnologico

| Componente | Tecnologia | Funcao |
|------------|-----------|--------|
| **Automacao** | Home Assistant + Alarmo | Central de automacao e alarme |
| **NVR + IA** | Frigate (OpenVINO) | Gravacao + deteccao de objetos |
| **Sensores** | Zigbee 3.0 via Zigbee2MQTT | Sensores wireless |
| **Messaging** | Mosquitto (MQTT) | Comunicacao entre servicos |
| **Infra dev** | Docker Compose | Orquestracao em desenvolvimento |
| **Infra prod** | K3s (Kubernetes) | Orquestracao em producao |
| **Hardware** | Mini PC Intel N100 | Hub de processamento |
| **Cameras** | Reolink / Hikvision (PoE) | Videovigilancia |
| **Acesso remoto** | WireGuard VPN | Acesso seguro externo |
| **Coordenador** | Sonoff ZBDongle-P (CC2652P) | Bridge Zigbee-USB |

---

## 7. Ambientes de deploy

| Ambiente | Tecnologia | Diretorio | Uso |
|----------|-----------|-----------|-----|
| **Desenvolvimento** | Docker Compose | `src/docker-compose.yml` | Testes locais |
| **Staging** | K3s + Kustomize | `k8s/overlays/staging/` | Validacao pre-producao |
| **Producao** | K3s + Kustomize | `k8s/overlays/production/` | Deploy real com Ingress |

---

## 8. Decisoes de arquitetura

Decisoes formalizadas em Architecture Decision Records (ADRs):

| ADR | Decisao | Documento |
|-----|---------|-----------|
| ADR-001 | Home Assistant como plataforma principal | `docs/adr/001-adoption-home-assistant.md` |
| ADR-002 | Frigate como NVR com IA | `docs/adr/002-adoption-frigate.md` |
| ADR-003 | Zigbee 3.0 como protocolo de sensores | `docs/adr/003-adoption-zigbee.md` |
| ADR-004 | K3s como infraestrutura de produção | `docs/adr/004-adoption-kubernetes.md` |
| ADR-005 | Mini PC N100 como hardware principal | `docs/adr/005-adoption-mini-pc-n100.md` |
| ADR-006 | Câmeras PoE como padrão | `docs/adr/006-adoption-poe-cameras.md` |
| ADR-007 | Acesso remoto VPN-only | `docs/adr/007-adoption-vpn-only-remote-access.md` |
| ADR-008 | PostgreSQL com isolamento por schema | `docs/adr/008-adoption-postgres-schema-isolation.md` |
| ADR-009 | Compose para dev + K3s para produção | `docs/adr/009-adoption-compose-and-k3s.md` |
| ADR-010 | External Secrets em produção | `docs/adr/010-adoption-external-secrets.md` |

---

## 9. Modulos do sistema

| Modulo | Descricao | PRD |
|--------|-----------|-----|
| Plataforma de sensores e alarmes | Sensores Zigbee + Alarmo | PRD_SENSORS_AND_ALARMS_PLATFORM |
| Videovigilancia e NVR | Cameras + Frigate + deteccao IA | PRD_VIDEO_SURVEILLANCE_AND_NVR |
| Dashboard de monitoramento | Interface web + mobile | PRD_MONITORING_DASHBOARD |
| Seguranca de rede | VLANs + firewall + VPN | PRD_NETWORK_SECURITY |
| Drones autonomos | UGV/UAV com IA embarcada | PRD_AUTONOMOUS_DRONES |

---

## Referencias

- `docs/ARQUITETURA_TECNICA.md` — Detalhamento tecnico completo
- `docs/ARQUITETURA_SEGURANCA_FISICA.md` — Camadas de seguranca fisica
- `docs/ARQUITETURA_DRONES_AUTONOMOS.md` — Arquitetura de drones
- `docs/THREAT_MODEL.md` — Modelo de ameacas (STRIDE)
- `rules/RULES_COMPLIANCE_AND_STANDARDS.md` — Normas e compliance
