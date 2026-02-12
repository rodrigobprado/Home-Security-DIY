# PRD – Videovigilância e NVR

> Sistema de Home Security – Open Source / Open Hardware
>
> Versão: 1.0 | Data: 2026-02-12 | Responsável: Agente_Documentador

---

## 1. Visão geral

- **Nome do produto/funcionalidade**: Sistema de Videovigilância e NVR (Network Video Recorder)
- **Responsável**: Agente_Arquiteto_Tecnico (especificação), Agente_Documentador (documentação)
- **Data**: 2026-02-12
- **PRDs relacionados**: PRD_SENSORS_AND_ALARMS_PLATFORM, PRD_MONITORING_DASHBOARD, PRD_NETWORK_SECURITY

---

## 2. Problema e oportunidade

### 2.1 Problema

Sistemas de videovigilância comerciais apresentam limitações críticas:
- **Dependência de nuvem**: Gravações enviadas para servidores externos, comprometendo privacidade
- **Custos de armazenamento**: Planos de nuvem com armazenamento limitado ou caro
- **Detecção limitada**: Câmeras básicas apenas detectam movimento, sem distinguir pessoas de animais
- **Integração fechada**: Incompatibilidade entre marcas de câmeras e gravadores
- **Latência**: Streaming via nuvem adiciona delay significativo

### 2.2 Oportunidade

Criar um sistema de videovigilância baseado em:
- **NVR open source** (Frigate) com detecção de objetos por IA
- **Armazenamento 100% local** em HDD/SSD próprio
- **Câmeras compatíveis** via protocolos abertos (RTSP/ONVIF)
- **Integração com Home Assistant** para automações
- **Processamento local** com aceleração de hardware (OpenVINO)

---

## 3. Público-alvo

| Perfil | Necessidades específicas |
|--------|--------------------------|
| **Proprietário rural** | Câmeras de longo alcance, visão noturna avançada, cobertura de perímetro |
| **Proprietário urbano** | Cobertura de entrada, garagem e quintal, boa resolução para identificação |
| **Morador de apartamento** | Olho mágico digital, gravação discreta, baixo consumo de espaço |
| **Usuário preocupado com privacidade** | Nenhum dado enviado para nuvem, controle total |

---

## 4. Requisitos funcionais

### 4.1 Câmeras e captura

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-001 | Suportar câmeras IP via protocolo RTSP | Alta |
| RF-002 | Suportar câmeras com protocolo ONVIF | Alta |
| RF-003 | Resolução mínima: 1080p (Full HD) | Alta |
| RF-004 | Resolução recomendada: 2K/4K (4MP+) | Média |
| RF-005 | Codec H.264 obrigatório | Alta |
| RF-006 | Codec H.265 recomendado (economia de espaço) | Média |
| RF-007 | Visão noturna infravermelha (IR) em câmeras externas | Alta |
| RF-008 | Alimentação PoE (802.3af/at) preferencial | Alta |
| RF-009 | Suportar câmeras Wi-Fi quando necessário | Média |
| RF-010 | Suportar múltiplos streams (main + substream) | Alta |

### 4.2 Gravação

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-011 | Gravação contínua 24/7 (opcional) | Baixa |
| RF-012 | Gravação por detecção de movimento | Alta |
| RF-013 | Gravação por detecção de objetos (pessoas, veículos) | Alta |
| RF-014 | Gravação pré-evento (buffer de 5-10 segundos) | Alta |
| RF-015 | Gravação pós-evento configurável (10-60 segundos) | Alta |
| RF-016 | Armazenamento em HDD/SSD local | Alta |
| RF-017 | Formato de gravação: MP4 ou fragmentado | Alta |
| RF-018 | Snapshots (fotos) de eventos detectados | Alta |

### 4.3 Detecção inteligente (IA)

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-019 | Detecção de pessoas | Alta |
| RF-020 | Detecção de veículos (carros, motos) | Alta |
| RF-021 | Detecção de animais (para evitar falsos positivos) | Média |
| RF-022 | Zonas de detecção configuráveis por câmera | Alta |
| RF-023 | Máscaras de privacidade (áreas ignoradas) | Média |
| RF-024 | Linhas de cruzamento (tripwire) | Baixa |
| RF-025 | Detecção de objetos abandonados | Baixa |
| RF-026 | Reconhecimento de placas de veículos (ALPR) | Baixa |

### 4.4 Streaming e visualização

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-027 | Streaming ao vivo de todas as câmeras | Alta |
| RF-028 | Streaming via WebRTC (baixa latência) | Alta |
| RF-029 | Streaming via HLS (compatibilidade) | Média |
| RF-030 | Visualização em grid (múltiplas câmeras) | Alta |
| RF-031 | Visualização individual com PTZ virtual | Média |
| RF-032 | Timeline visual de eventos | Alta |
| RF-033 | Busca por tipo de objeto detectado | Alta |
| RF-034 | Playback com velocidade variável (0.5x a 4x) | Média |

### 4.5 Integração com sistema de alarme

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-035 | Publicar eventos de detecção via MQTT | Alta |
| RF-036 | Integração nativa com Home Assistant | Alta |
| RF-037 | Disparo de gravação por evento de alarme externo | Alta |
| RF-038 | Snapshot enviado nas notificações de alarme | Alta |
| RF-039 | Trigger para automações (iluminação, sirene) | Alta |

### 4.6 Retenção e gerenciamento

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-040 | Rotação automática de gravações (FIFO) | Alta |
| RF-041 | Período de retenção configurável por câmera | Alta |
| RF-042 | Retenção diferenciada para eventos vs. contínuo | Alta |
| RF-043 | Marcação de eventos para preservação | Alta |
| RF-044 | Exportação de clips para download | Alta |
| RF-045 | Monitoramento de espaço em disco | Alta |
| RF-046 | Alerta quando disco > 90% de ocupação | Alta |

### 4.7 Acesso remoto

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-047 | Acesso via VPN (WireGuard/Tailscale) | Alta |
| RF-048 | Interface web responsiva | Alta |
| RF-049 | App mobile Home Assistant Companion | Alta |
| RF-050 | Nunca expor diretamente à internet (port forwarding) | Alta |

---

## 5. Requisitos não funcionais

### 5.1 Performance

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-001 | Latência de streaming | < 500ms via WebRTC local |
| RNF-002 | Taxa de detecção de IA | > 10 FPS por câmera (com aceleração) |
| RNF-003 | Tempo para iniciar playback | < 3 segundos |
| RNF-004 | Capacidade de câmeras simultâneas | Mínimo 8 câmeras 1080p ou 4 câmeras 4K |

### 5.2 Armazenamento

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-005 | Capacidade mínima | 1TB para eventos (30 dias) |
| RNF-006 | Capacidade recomendada | 2-4TB (cenários rural/urbano) |
| RNF-007 | Tipo de disco | HDD 7200rpm ou SSD (preferível) |
| RNF-008 | Formato de sistema de arquivos | ext4 ou ZFS |

### 5.3 Segurança e privacidade

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-009 | Isolamento de câmeras | VLAN separada sem acesso à internet |
| RNF-010 | Acesso ao NVR | Autenticação obrigatória, 2FA recomendado |
| RNF-011 | Logs de acesso | Registro de todos os acessos às gravações |
| RNF-012 | Criptografia de disco | Recomendada para dados sensíveis |
| RNF-013 | Processamento de IA | 100% local, sem envio para nuvem |

### 5.4 Conformidade com normas

| ID | Requisito | Norma/Regra |
|----|-----------|-------------|
| RNF-014 | Retenção padrão | REGRA-CFTV-01: 30 dias |
| RNF-015 | Rotação automática | REGRA-CFTV-02: FIFO |
| RNF-016 | Preservação de incidentes | REGRA-CFTV-03: Flag para não sobrescrever |
| RNF-017 | Resolução mínima | REGRA-CFTV-05: 1080p para identificação |
| RNF-018 | Visão noturna | REGRA-CFTV-06: Obrigatória em externas |
| RNF-019 | Cobertura | REGRA-CFTV-07: Todos os pontos de entrada |
| RNF-020 | Acesso remoto | REGRA-CFTV-11: Apenas via VPN |
| RNF-021 | Isolamento de rede | REGRA-CFTV-12: VLAN separada |
| RNF-022 | LGPD | REGRA-LGPD-01 a 05: Quando aplicável |

---

## 6. Arquitetura técnica

### 6.1 Stack recomendado

| Componente | Tecnologia | Função |
|------------|------------|--------|
| **NVR** | Frigate | Gravação, detecção IA, streaming |
| **Aceleração IA** | Intel OpenVINO (iGPU N100) | Detecção de objetos |
| **Integração** | Home Assistant | Automações, dashboard, notificações |
| **MQTT Broker** | Mosquitto | Comunicação de eventos |
| **Armazenamento** | HDD/SSD local | Gravações |

### 6.2 Diagrama de arquitetura

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           VLAN CÂMERAS (192.168.30.0/24)                │
│                                                                         │
│   ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐          │
│   │ CAM 1  │  │ CAM 2  │  │ CAM 3  │  │ CAM 4  │  │ CAM N  │          │
│   │ Entrada│  │ Fundos │  │Lateral │  │Garagem │  │  ...   │          │
│   └───┬────┘  └───┬────┘  └───┬────┘  └───┬────┘  └───┬────┘          │
│       │           │           │           │           │                 │
│       └───────────┴───────────┴───────────┴───────────┘                 │
│                               │                                         │
│                      ┌────────┴────────┐                                │
│                      │   SWITCH PoE    │                                │
│                      │   (8+ portas)   │                                │
│                      └────────┬────────┘                                │
│                               │                                         │
└───────────────────────────────┼─────────────────────────────────────────┘
                                │ RTSP (554)
                                │
┌───────────────────────────────┼─────────────────────────────────────────┐
│                    VLAN GESTÃO (192.168.10.0/24)                        │
│                               │                                         │
│                      ┌────────▼────────┐                                │
│                      │   MINI PC N100  │                                │
│                      │                 │                                │
│  ┌────────────┐      │  ┌───────────┐  │      ┌────────────────┐       │
│  │ Intel iGPU │◄─────┤  │  FRIGATE  │  │─────►│  HDD/SSD       │       │
│  │ (OpenVINO) │      │  │   NVR     │  │      │  Gravações     │       │
│  └────────────┘      │  └─────┬─────┘  │      │  (1-4TB)       │       │
│                      │        │        │      └────────────────┘       │
│                      │        │ MQTT   │                                │
│                      │        ▼        │                                │
│                      │  ┌───────────┐  │                                │
│                      │  │ MOSQUITTO │  │                                │
│                      │  └─────┬─────┘  │                                │
│                      │        │        │                                │
│                      │        ▼        │                                │
│                      │  ┌───────────┐  │                                │
│                      │  │   HOME    │  │                                │
│                      │  │ ASSISTANT │  │                                │
│                      │  │ + ALARMO  │  │                                │
│                      │  └───────────┘  │                                │
│                      │                 │                                │
│                      └─────────────────┘                                │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 6.3 Fluxo de processamento de vídeo

```
Câmera IP (RTSP)
       │
       ▼
┌──────────────────┐
│ Frigate - Decode │◄── Substream para detecção (720p)
│                  │◄── Mainstream para gravação (1080p/4K)
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ OpenVINO (iGPU)  │◄── Modelo YOLO/SSD para detecção
│ Detecção de IA   │
└────────┬─────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
Detecção   Sem detecção
    │         │
    │         └─► Buffer descartado (economia de espaço)
    │
    ▼
┌──────────────────┐
│ Gravação evento  │
│ + Snapshot       │
│ + Publicação MQTT│
└──────────────────┘
```

---

## 7. Câmeras recomendadas

### 7.1 Requisitos mínimos

| Característica | Obrigatório | Recomendado |
|----------------|-------------|-------------|
| Resolução | 1080p | 4MP (2K) |
| Protocolo | RTSP | RTSP + ONVIF |
| Codec | H.264 | H.264 + H.265 |
| Visão noturna | Sim (externas) | IR 30m+ |
| Alimentação | PoE ou 12V DC | PoE (802.3af) |
| Dual stream | Sim | Sim |

### 7.2 Modelos recomendados por cenário

#### Cenário rural

| Posição | Tipo | Modelo sugerido | Preço estimado |
|---------|------|-----------------|----------------|
| Entrada/portão | Bullet PoE 4MP, IR longo | Reolink RLC-810A | R$ 400-500 |
| Perímetro | Bullet PoE 5MP, IR 50m+ | Hikvision DS-2CD2055 | R$ 500-700 |
| Depósito/garagem | Dome PoE 4MP | Reolink RLC-520A | R$ 300-400 |
| Sede (amplo) | PTZ ou wide angle | Reolink RLC-823A | R$ 600-800 |

**Total estimado (4-6 câmeras): R$ 1.600-2.400**

#### Cenário casa urbana

| Posição | Tipo | Modelo sugerido | Preço estimado |
|---------|------|-----------------|----------------|
| Entrada (rua) | Bullet PoE 4MP | Reolink RLC-510A | R$ 250-350 |
| Garagem | Dome PoE 4MP | Reolink RLC-520A | R$ 300-400 |
| Quintal/fundos | Bullet PoE 4MP, wide | Annke C500 | R$ 250-350 |
| Lateral (opcional) | Mini bullet Wi-Fi | Reolink E1 Outdoor | R$ 250-350 |

**Total estimado (3-5 câmeras): R$ 800-1.450**

#### Cenário apartamento

| Posição | Tipo | Modelo sugerido | Preço estimado |
|---------|------|-----------------|----------------|
| Olho mágico digital | Video doorbell | Aqara G4 Video Doorbell | R$ 500-700 |
| Alternativa | Câmera interna | Aqara G3 | R$ 400-550 |

**Total estimado (0-1 câmera): R$ 0-700**

### 7.3 Switch PoE recomendado

| Modelo | Portas | Potência | Preço estimado |
|--------|--------|----------|----------------|
| TP-Link TL-SG1008P | 8 (4 PoE) | 55W | R$ 350-450 |
| TP-Link TL-SG1016PE | 16 (8 PoE) | 110W | R$ 600-800 |
| Ubiquiti USW-Lite-8-PoE | 8 (4 PoE+) | 52W | R$ 700-900 |

---

## 8. Política de retenção

### 8.1 Períodos de retenção

| Tipo de gravação | Período | Justificativa |
|------------------|---------|---------------|
| **Gravações normais (movimento)** | 30 dias | Padrão de mercado, REGRA-CFTV-01 |
| **Eventos com detecção de pessoa** | 60 dias | Maior relevância |
| **Incidentes marcados** | 1 ano | Evidências para uso legal |
| **Snapshots** | 90 dias | Referência rápida |

### 8.2 Cálculo de armazenamento

| Cenário | Câmeras | Resolução | Horas/dia* | Espaço/dia | Espaço 30 dias |
|---------|---------|-----------|------------|------------|----------------|
| Rural | 5 | 4MP H.265 | 2h | ~15 GB | ~450 GB |
| Urbana | 4 | 4MP H.265 | 3h | ~18 GB | ~540 GB |
| Apartamento | 1 | 1080p H.265 | 1h | ~2 GB | ~60 GB |

*Estimativa com gravação apenas quando há detecção

### 8.3 Configuração Frigate (exemplo)

```yaml
record:
  enabled: True
  retain:
    days: 30
    mode: motion
  events:
    retain:
      default: 60
      mode: active_objects
      objects:
        person: 90  # Pessoas: 90 dias
        car: 60     # Veículos: 60 dias

snapshots:
  enabled: True
  retain:
    default: 90
```

---

## 9. Critérios de aceitação

| ID | Critério | Método de verificação |
|----|----------|----------------------|
| CA-001 | Todas as câmeras aparecem no Frigate com stream ativo | Verificação visual |
| CA-002 | Detecção de pessoas funciona corretamente | Teste caminhando em frente às câmeras |
| CA-003 | Detecção de veículos funciona corretamente | Teste com veículo |
| CA-004 | Gravações são criadas apenas quando há detecção | Verificação de arquivos |
| CA-005 | Snapshots são enviados nas notificações | Teste de notificação |
| CA-006 | Rotação automática libera espaço corretamente | Verificação após 30 dias |
| CA-007 | Streaming ao vivo tem latência < 500ms | Teste com cronômetro |
| CA-008 | Playback de gravações funciona corretamente | Teste de navegação |
| CA-009 | Acesso via VPN funciona externamente | Teste fora da rede local |
| CA-010 | Câmeras não têm acesso à internet | Verificação de firewall |

---

## 10. Métricas de sucesso

| Métrica | Alvo | Medição |
|---------|------|---------|
| **Taxa de detecção de pessoas** | > 95% | Testes com walkthrough |
| **Taxa de falsos positivos** | < 5% | Contagem de detecções incorretas |
| **Latência de streaming** | < 500ms | Medição com cronômetro |
| **Uptime do NVR** | > 99.5% | Monitoramento |
| **FPS de detecção** | > 10 FPS | Monitoramento do Frigate |

---

## 11. Riscos e dependências

### 11.1 Riscos

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Câmera incompatível com Frigate | Baixa | Alto | Verificar compatibilidade antes da compra |
| Performance insuficiente para IA | Média | Alto | Usar aceleração OpenVINO, reduzir FPS |
| Falha de disco com perda de gravações | Baixa | Alto | Backup de configuração, considerar RAID |
| Interferência de rede PoE | Baixa | Médio | Usar cabeamento Cat6, evitar emendas |
| Câmera hackeada | Média | Alto | Isolar em VLAN, bloquear internet |

### 11.2 Dependências

| Dependência | Tipo | PRD relacionado |
|-------------|------|-----------------|
| Hardware central (Mini PC N100) | Infraestrutura | PRD_LOCAL_PROCESSING_HUB |
| Rede segmentada (VLANs) | Infraestrutura | PRD_NETWORK_SECURITY |
| Sistema de alarme | Integração | PRD_SENSORS_AND_ALARMS_PLATFORM |
| Dashboard | Interface | PRD_MONITORING_DASHBOARD |

---

## 12. Referências

### Documentos do projeto
- `docs/ARQUITETURA_TECNICA.md` - Seções 2, 5, 6, 9
- `docs/ARQUITETURA_SEGURANCA_FISICA.md` - Diagramas de posicionamento
- `rules/RULES_COMPLIANCE_AND_STANDARDS.md` - REGRA-CFTV-*, REGRA-LGPD-*

### Externos
- [Frigate NVR - Documentação](https://docs.frigate.video/)
- [Frigate - Câmeras compatíveis](https://docs.frigate.video/frigate/hardware)
- [Intel OpenVINO](https://docs.openvino.ai/)
- [Home Assistant - Frigate Integration](https://docs.frigate.video/integrations/home-assistant)

---

> **Status**: Rascunho v1.0
>
> **Próxima revisão**: Após validação pelo Agente_Arquiteto_Tecnico
