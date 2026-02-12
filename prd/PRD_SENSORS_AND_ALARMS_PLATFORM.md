# PRD – Plataforma de Sensores e Alarmes

> Sistema de Home Security – Open Source / Open Hardware
>
> Versão: 1.0 | Data: 2026-02-12 | Responsável: Agente_Documentador

---

## 1. Visão geral

- **Nome do produto/funcionalidade**: Plataforma de Sensores e Alarmes
- **Responsável**: Agente_Arquiteto_Tecnico (especificação), Agente_Documentador (documentação)
- **Data**: 2026-02-12
- **PRDs relacionados**: PRD_MONITORING_DASHBOARD, PRD_NETWORK_SECURITY, PRD_LOCAL_PROCESSING_HUB

---

## 2. Problema e oportunidade

### 2.1 Problema

Residências brasileiras estão expostas a invasões e furtos. Soluções comerciais de alarme apresentam:
- **Dependência de nuvem**: Dados enviados para servidores de terceiros, comprometendo privacidade
- **Custos recorrentes**: Mensalidades de monitoramento que encarecem a solução
- **Vendor lock-in**: Sensores proprietários incompatíveis entre fabricantes
- **Limitação de personalização**: Automações e integrações restritas

### 2.2 Oportunidade

Criar uma plataforma de sensores e alarmes baseada em:
- **Protocolos abertos** (Zigbee 3.0) com sensores de múltiplos fabricantes
- **Processamento local** sem dependência de nuvem
- **Código aberto** (Home Assistant + Alarmo) permitindo customização
- **Custo acessível** com hardware disponível no mercado brasileiro

---

## 3. Público-alvo

| Perfil | Descrição | Necessidades específicas |
|--------|-----------|--------------------------|
| **Proprietário rural** | Fazendas, chácaras, sítios | Cobertura de perímetros extensos, autonomia energética |
| **Proprietário urbano** | Casas com quintal | Proteção de múltiplas zonas (perímetro, envelope, interior) |
| **Morador de apartamento** | Apartamentos em condomínios | Proteção de porta principal, integração simples |
| **Usuário técnico** | Profissional de TI ou entusiasta | Customização avançada, automações complexas |
| **Usuário comum** | Sem conhecimento técnico | Interface simples, instalação guiada |

---

## 4. Requisitos funcionais

### 4.1 Tipos de sensores suportados

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-001 | Suportar sensores de abertura (porta/janela) magnéticos | Alta |
| RF-002 | Suportar sensores de movimento PIR (infravermelho passivo) | Alta |
| RF-003 | Suportar sensores de presença mmWave (ondas milimétricas) | Média |
| RF-004 | Suportar sensores de vibração/impacto | Média |
| RF-005 | Suportar sensores de quebra de vidro (acústico) | Média |
| RF-006 | Suportar sensores de fumaça e calor | Alta |
| RF-007 | Suportar sensores de vazamento de gás | Média |
| RF-008 | Suportar sensores de vazamento de água | Baixa |
| RF-009 | Suportar botões de pânico físicos | Alta |
| RF-010 | Suportar sensores de cerca elétrica (integração com central) | Média |

### 4.2 Protocolos de comunicação

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-011 | Protocolo primário: Zigbee 3.0 via Zigbee2MQTT ou ZHA | Alta |
| RF-012 | Protocolo secundário: Z-Wave (para fechaduras) | Baixa |
| RF-013 | Suportar sensores Wi-Fi (quando necessário) | Média |
| RF-014 | Suportar integração via 433MHz (cercas elétricas legadas) | Baixa |
| RF-015 | Coordenador Zigbee: Sonoff ZBDongle-P (CC2652P) ou SLZB-06 | Alta |

### 4.3 Sistema de alarme (Alarmo)

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-016 | Definir zonas de alarme configuráveis (mínimo 4 zonas) | Alta |
| RF-017 | Modos de armamento: desarmado, armado total, armado parcial (noite), armado perímetro | Alta |
| RF-018 | Tempo de entrada configurável (0-120 segundos) | Alta |
| RF-019 | Tempo de saída configurável (0-120 segundos) | Alta |
| RF-020 | Código de acesso numérico (mínimo 4 dígitos) | Alta |
| RF-021 | Código de coação (desarma silenciosamente e notifica) | Média |
| RF-022 | Bypass de sensores individuais | Média |
| RF-023 | Auto-armar por horário ou geolocalização | Média |

### 4.4 Atuadores (saídas)

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-024 | Acionar sirene interna (Zigbee, 90dB+) | Alta |
| RF-025 | Acionar sirene externa (cabeada ou Zigbee, 110dB+) | Alta |
| RF-026 | Acionar iluminação reativa via Zigbee | Média |
| RF-027 | Acionar fechaduras eletrônicas | Baixa |
| RF-028 | Integrar com automação de portões | Baixa |

### 4.5 Notificações

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-029 | Notificação push via app Home Assistant | Alta |
| RF-030 | Notificação via Telegram | Alta |
| RF-031 | Notificação via e-mail | Média |
| RF-032 | Notificação via SMS (via gateway ou serviço) | Baixa |
| RF-033 | Notificação via chamada de voz (via serviço externo) | Baixa |
| RF-034 | Múltiplos destinatários configuráveis | Alta |
| RF-035 | Silenciamento por horário/zona | Média |

### 4.6 Integração com outros sistemas

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-036 | Integração nativa com Frigate (eventos de detecção) | Alta |
| RF-037 | Disparo de gravação em câmeras ao detectar alarme | Alta |
| RF-038 | Integração com dashboard de monitoramento | Alta |
| RF-039 | API REST para integrações externas | Média |
| RF-040 | Integração com assistentes de voz (opcional) | Baixa |

---

## 5. Requisitos não funcionais

### 5.1 Performance

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-001 | Tempo de detecção | < 500ms do evento ao registro no sistema |
| RNF-002 | Tempo de notificação | < 5 segundos do alarme à notificação push |
| RNF-003 | Tempo de resposta da sirene | < 1 segundo após confirmação de alarme |
| RNF-004 | Disponibilidade | 99.5% uptime (máximo ~43h downtime/ano) |

### 5.2 Segurança

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-005 | Criptografia de comunicação Zigbee | AES-128 (nativo do protocolo) |
| RNF-006 | Autenticação no painel/app | Senha forte + 2FA recomendado |
| RNF-007 | Proteção anti-tamper | Sensores devem notificar tentativa de remoção |
| RNF-008 | Logs de eventos | Todos os eventos registrados com timestamp |
| RNF-009 | Isolamento de rede | Sensores Wi-Fi em VLAN separada, sem internet |

### 5.3 Confiabilidade

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-010 | Autonomia de bateria | Sensores Zigbee: mínimo 12 meses |
| RNF-011 | Monitoramento de bateria | Alerta quando bateria < 20% |
| RNF-012 | Continuidade em queda de energia | Nobreak com 30 minutos de autonomia |
| RNF-013 | Redundância de notificação | Mínimo 2 canais distintos configurados |
| RNF-014 | Mesh Zigbee | Mínimo 2 dispositivos roteadores para resiliência |

### 5.4 Usabilidade

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-015 | Interface de configuração | Web responsiva (Home Assistant) |
| RNF-016 | App mobile | Home Assistant Companion (iOS/Android) |
| RNF-017 | Armamento/desarmamento | Teclado físico, app, NFC tag, código |
| RNF-018 | Feedback visual | LED ou display no teclado/painel |
| RNF-019 | Feedback sonoro | Bips de confirmação configuráveis |

### 5.5 Conformidade com normas

| ID | Requisito | Norma/Regra |
|----|-----------|-------------|
| RNF-020 | Senhas padrão | REGRA-IOT-01: Nunca manter senhas de fábrica |
| RNF-021 | Serviços desnecessários | REGRA-IOT-02: Desabilitar Telnet, FTP, UPnP |
| RNF-022 | Acesso à internet | REGRA-IOT-03: Bloquear acesso externo |
| RNF-023 | Atualizações | REGRA-IOT-05: Verificar firmware mensalmente |
| RNF-024 | Inventário | REGRA-IOT-06: Documentar todos os dispositivos |

---

## 6. Arquitetura técnica

### 6.1 Diagrama de componentes

```
┌─────────────────────────────────────────────────────────────────────┐
│                         SERVIDOR CENTRAL                            │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐     │
│  │  HOME ASSISTANT │  │   ZIGBEE2MQTT   │  │    MOSQUITTO    │     │
│  │     + ALARMO    │◄─┤  (ou ZHA)       │◄─┤   (MQTT Broker) │     │
│  └────────┬────────┘  └────────┬────────┘  └─────────────────┘     │
│           │                    │                                    │
│           │                    │                                    │
│  ┌────────▼────────┐  ┌────────▼────────┐                          │
│  │   AUTOMAÇÕES    │  │   COORDENADOR   │                          │
│  │   & ALERTAS     │  │     ZIGBEE      │                          │
│  └─────────────────┘  │  (USB Dongle)   │                          │
│                       └────────┬────────┘                          │
└────────────────────────────────┼────────────────────────────────────┘
                                 │
                    ┌────────────┼────────────┐
                    │            │            │
              ┌─────▼────┐ ┌─────▼────┐ ┌─────▼────┐
              │ SENSORES │ │ SENSORES │ │ ATUADORES│
              │ ABERTURA │ │   PIR    │ │ (Sirene) │
              └──────────┘ └──────────┘ └──────────┘
```

### 6.2 Fluxo de eventos de alarme

```
1. Sensor detecta evento (abertura, movimento)
           │
           ▼
2. Zigbee2MQTT recebe mensagem Zigbee
           │
           ▼
3. MQTT publica evento no broker
           │
           ▼
4. Home Assistant (Alarmo) processa:
   - Verifica modo de armamento
   - Verifica zona e configuração
   - Aplica delay de entrada (se configurado)
           │
           ▼
5. Se alarme confirmado:
   ├── Aciona sirene(s)
   ├── Envia notificações
   ├── Registra evento
   └── Dispara gravação em câmeras (Frigate)
```

### 6.3 Configuração de zonas recomendada

| Zona | Nome | Sensores típicos | Comportamento |
|------|------|------------------|---------------|
| 1 | Perímetro | Cerca elétrica, sensores externos | Alerta imediato |
| 2 | Entrada principal | Porta principal, PIR entrada | Delay de entrada |
| 3 | Portas e janelas | Sensores de abertura | Alerta imediato |
| 4 | Interior | PIR internos | Apenas armado total |

---

## 7. Sensores recomendados

### 7.1 Sensores Zigbee homologados

| Tipo | Modelo | Preço estimado | Compatibilidade |
|------|--------|----------------|-----------------|
| **Abertura porta/janela** | Aqara MCCGQ11LM | R$ 50-80 | ✓ Z2M, ✓ ZHA |
| **Abertura porta/janela** | Sonoff SNZB-04 | R$ 40-60 | ✓ Z2M, ✓ ZHA |
| **Movimento PIR** | Aqara RTCGQ11LM | R$ 60-100 | ✓ Z2M, ✓ ZHA |
| **Movimento PIR** | Sonoff SNZB-03 | R$ 50-80 | ✓ Z2M, ✓ ZHA |
| **Presença mmWave** | Aqara FP2 | R$ 250-350 | ✓ Z2M, ✓ ZHA |
| **Presença mmWave** | Sonoff SNZB-06P | R$ 150-200 | ✓ Z2M, ✓ ZHA |
| **Sirene interna** | Heiman HS2WD-E | R$ 100-150 | ✓ Z2M, ✓ ZHA |
| **Sirene interna** | Tuya TS0224 | R$ 80-120 | ✓ Z2M |
| **Botão de pânico** | Aqara WXKG11LM | R$ 60-90 | ✓ Z2M, ✓ ZHA |
| **Fumaça** | Heiman HS1SA-E | R$ 100-150 | ✓ Z2M, ✓ ZHA |
| **Vazamento de água** | Aqara SJCGQ11LM | R$ 80-120 | ✓ Z2M, ✓ ZHA |

### 7.2 Coordenadores Zigbee recomendados

| Modelo | Chip | Interface | Preço | Observações |
|--------|------|-----------|-------|-------------|
| **Sonoff ZBDongle-P** | CC2652P | USB | R$ 100-150 | Melhor custo-benefício |
| **SLZB-06** | CC2652P | PoE/USB | R$ 200-300 | Mais robusto, PoE |
| **ConBee II** | - | USB | R$ 250-350 | Boa opção alternativa |

---

## 8. Estimativa de sensores por cenário

### 8.1 Cenário rural

| Componente | Quantidade | Subtotal |
|------------|------------|----------|
| Sensor abertura portão | 1-2 | R$ 80-160 |
| Sensor movimento externo | 2-4 | R$ 200-400 |
| Sensor abertura portas | 2-3 | R$ 100-180 |
| Sensor abertura janelas | 4-6 | R$ 200-360 |
| Sensor movimento interno | 1-2 | R$ 100-200 |
| Sirene externa | 1-2 | R$ 150-300 |
| Sirene interna | 1 | R$ 100 |
| Botão de pânico | 1-2 | R$ 60-120 |
| **Total sensores** | **13-22** | **R$ 990-1.820** |

### 8.2 Cenário casa urbana

| Componente | Quantidade | Subtotal |
|------------|------------|----------|
| Sensor abertura portas | 2-3 | R$ 100-180 |
| Sensor abertura janelas | 4-8 | R$ 200-480 |
| Sensor movimento interno | 2-3 | R$ 150-300 |
| Sensor quebra de vidro | 1-2 | R$ 80-160 |
| Sirene externa | 1 | R$ 150 |
| Sirene interna | 1 | R$ 100 |
| Teclado/painel | 1 | R$ 100-150 |
| **Total sensores** | **12-19** | **R$ 880-1.520** |

### 8.3 Cenário apartamento

| Componente | Quantidade | Subtotal |
|------------|------------|----------|
| Sensor abertura porta | 1 | R$ 50-80 |
| Sensor movimento entrada | 1 | R$ 60-100 |
| Sensor movimento sala | 0-1 | R$ 0-100 |
| Sirene interna | 1 | R$ 100 |
| Botão de pânico | 1 | R$ 60-90 |
| **Total sensores** | **4-5** | **R$ 270-470** |

---

## 9. Critérios de aceitação

| ID | Critério | Método de verificação |
|----|----------|----------------------|
| CA-001 | Todos os sensores instalados aparecem no Home Assistant | Verificação visual no dashboard |
| CA-002 | Alarmo arma e desarma corretamente em todos os modos | Teste funcional de cada modo |
| CA-003 | Sirene dispara em menos de 1 segundo após confirmação | Teste com cronômetro |
| CA-004 | Notificação push chega em menos de 5 segundos | Teste com cronômetro |
| CA-005 | Delay de entrada/saída funciona conforme configurado | Teste funcional |
| CA-006 | Código de coação notifica sem acionar sirene | Teste funcional |
| CA-007 | Bypass de sensor funciona corretamente | Teste de bypass individual |
| CA-008 | Sistema continua operando em queda de energia (nobreak) | Teste de interrupção |
| CA-009 | Logs registram todos os eventos com timestamp | Verificação de logs |
| CA-010 | Mesh Zigbee estável com pelo menos 2 roteadores | Verificação de topologia |

---

## 10. Métricas de sucesso

| Métrica | Alvo | Medição |
|---------|------|---------|
| **Taxa de falsos positivos** | < 1/semana após ajuste inicial | Contagem de alarmes indevidos |
| **Taxa de detecção** | 100% de eventos reais detectados | Testes periódicos |
| **Tempo de resposta** | < 5 segundos para notificação | Monitoramento de logs |
| **Uptime do sistema** | > 99.5% | Monitoramento de disponibilidade |
| **Duração de bateria** | > 12 meses | Registro de trocas |

---

## 11. Riscos e dependências

### 11.1 Riscos

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Interferência Zigbee (Wi-Fi 2.4GHz) | Média | Médio | Usar canal Zigbee afastado de canais Wi-Fi |
| Sensor com firmware incompatível | Baixa | Alto | Verificar compatibilidade em zigbee2mqtt.io antes de comprar |
| Falha do coordenador Zigbee | Baixa | Alto | Manter backup de configuração, considerar coordenador reserva |
| Falsos positivos de PIR (animais) | Média | Baixo | Usar PIR pet-immune ou ajustar sensibilidade |
| Queda de internet impede notificação | Média | Alto | Configurar múltiplos canais (push + SMS local) |

### 11.2 Dependências

| Dependência | Tipo | PRD relacionado |
|-------------|------|-----------------|
| Hardware central (Mini PC N100) | Infraestrutura | PRD_LOCAL_PROCESSING_HUB |
| Rede segmentada (VLANs) | Infraestrutura | PRD_NETWORK_SECURITY |
| Dashboard de monitoramento | Interface | PRD_MONITORING_DASHBOARD |
| NVR para gravação de eventos | Integração | PRD_VIDEO_SURVEILLANCE_AND_NVR |

---

## 12. Referências

### Documentos do projeto
- `docs/ARQUITETURA_TECNICA.md` - Seções 1, 3, 6
- `rules/RULES_COMPLIANCE_AND_STANDARDS.md` - REGRA-IOT-*

### Externos
- [Zigbee2MQTT - Dispositivos suportados](https://www.zigbee2mqtt.io/supported-devices/)
- [Home Assistant - Alarmo](https://github.com/nielsfaber/alarmo)
- [OWASP IoT Top 10](https://owasp.org/www-project-internet-of-things/)

---

> **Status**: Rascunho v1.0
>
> **Próxima revisão**: Após validação pelo Agente_Arquiteto_Tecnico
