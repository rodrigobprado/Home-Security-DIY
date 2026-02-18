# PRD – Sistema de Notificações e Alertas

> Sistema de Home Security – Open Source / Open Hardware
>
> Versão: 1.0 | Data: 2026-02-18 | Responsável: Agente_Documentador

---

## 1. Visão geral

- **Nome do produto/funcionalidade**: Sistema de Notificações e Alertas Multi-canal
- **Responsável**: Agente_Arquiteto_Tecnico (especificação), Agente_Documentador (documentação)
- **Data**: 2026-02-18
- **PRDs relacionados**: PRD_SENSORS_AND_ALARMS_PLATFORM, PRD_MONITORING_DASHBOARD, PRD_VIDEO_SURVEILLANCE_AND_NVR, PRD_BACKUP_AND_RESILIENCE

---

## 2. Problema e oportunidade

### 2.1 Problema

Sistemas de segurança residencial frequentemente falham na notificação:
- **Canal único**: Dependência de apenas push notification ou SMS
- **Sem priorização**: Alarme crítico e sensor de bateria fraca têm o mesmo peso
- **Fadiga de alertas**: Excesso de notificações irrelevantes levam o morador a ignorar todas
- **Sem confirmação**: Impossível saber se a notificação foi recebida e vista
- **Dependência de internet**: Push notifications falham sem internet

### 2.2 Oportunidade

Criar um sistema de notificações que ofereça:
- **Múltiplos canais** (push, Telegram, SMS, e-mail, chamada de voz)
- **Priorização inteligente** baseada em severidade e contexto
- **Escalação automática** se o alerta não for confirmado
- **Redundância** para garantir entrega mesmo com falha de um canal
- **Silenciamento configurável** para evitar fadiga de alertas

---

## 3. Público-alvo

| Perfil | Necessidades específicas |
|--------|--------------------------|
| **Morador principal** | Todas as notificações, com priorização |
| **Co-morador/cônjuge** | Alertas críticos e de segurança |
| **Familiar externo** | Alertas de emergência apenas (pânico, invasão) |
| **Vizinho de confiança** | Alerta de emergência quando moradores ausentes |
| **Empresa de segurança** | Integração via API ou webhook (opcional) |

---

## 4. Requisitos funcionais

### 4.1 Canais de notificação

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-001 | Notificação push via Home Assistant Companion | iOS e Android nativo | Alta |
| RF-002 | Notificação via Telegram (bot) | Texto + imagem + botões de ação | Alta |
| RF-003 | Notificação via e-mail | SMTP configurável | Média |
| RF-004 | Notificação via SMS | Via gateway Twilio, Vonage ou modem USB | Média |
| RF-005 | Chamada de voz automática | Via Twilio ou VoIP local | Baixa |
| RF-006 | Notificação via sirene local | Zigbee, sonora e visual | Alta |
| RF-007 | Notificação via iluminação | Flash em lâmpadas Zigbee | Média |
| RF-008 | Webhook para integração externa | HTTP POST configurável | Baixa |

### 4.2 Níveis de prioridade

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-009 | Nível CRÍTICO (P1) | Alarme disparado, invasão, pânico | Alta |
| RF-010 | Nível ALTO (P2) | Sensor ambiental (fumaça, gás), tamper | Alta |
| RF-011 | Nível MÉDIO (P3) | Porta/janela aberta com alarme armado, acesso não reconhecido | Alta |
| RF-012 | Nível BAIXO (P4) | Bateria fraca, sensor offline, porta esquecida aberta | Média |
| RF-013 | Nível INFO (P5) | Alarme armado/desarmado, acesso autorizado | Baixa |

### 4.3 Regras de roteamento por prioridade

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-014 | P1 (CRÍTICO): Todos os canais simultaneamente | Push + Telegram + SMS + sirene + luzes | Alta |
| RF-015 | P2 (ALTO): Push + Telegram + sirene | Notificação imediata em múltiplos canais | Alta |
| RF-016 | P3 (MÉDIO): Push + Telegram | Notificação padrão | Alta |
| RF-017 | P4 (BAIXO): Push apenas | Uma vez ao dia ou agrupado | Média |
| RF-018 | P5 (INFO): Log apenas (push opcional) | Registrado, sem notificação ativa | Média |

### 4.4 Escalação automática

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-019 | Reenvio se não confirmado em 60 segundos (P1) | Escalar para próximo canal/destinatário | Alta |
| RF-020 | Reenvio se não confirmado em 5 minutos (P2) | Escalar para SMS/chamada | Média |
| RF-021 | Cadeia de escalação configurável | Morador 1 → Morador 2 → Familiar → Vizinho | Alta |
| RF-022 | Confirmação de recebimento via Telegram | Botão "OK" / "Falso alarme" / "Ligar 190" | Alta |
| RF-023 | Confirmação de recebimento via push | Actionable notification no app | Alta |

### 4.5 Conteúdo das notificações

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-024 | Texto descritivo do evento | "Alarme disparado - Sensor porta principal" | Alta |
| RF-025 | Snapshot da câmera (quando aplicável) | Imagem do Frigate no momento do evento | Alta |
| RF-026 | Timestamp do evento | Data/hora precisa | Alta |
| RF-027 | Zona do alarme afetada | "Zona: Entrada principal" | Alta |
| RF-028 | Botões de ação rápida | "Desarmar", "Ver câmera", "Ligar polícia" | Alta |
| RF-029 | Link direto para dashboard | Abrir app na tela relevante | Média |
| RF-030 | Clip de vídeo (quando disponível) | GIF ou MP4 curto do Frigate | Média |

### 4.6 Silenciamento e agendamento

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-031 | Silenciar por período | "Silenciar 1h / 4h / até manhã" | Média |
| RF-032 | Silenciar por zona | "Silenciar sensor quintal" | Média |
| RF-033 | Silenciar por tipo | "Silenciar bateria fraca" | Média |
| RF-034 | Horário de não perturbar | Configurável por usuário | Média |
| RF-035 | Exceção: P1 nunca silenciável | Alertas críticos ignoram silenciamento | Alta |
| RF-036 | Modo férias | Notificações extras para familiares/vizinhos | Baixa |

### 4.7 Configuração e gestão

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-037 | Múltiplos destinatários configuráveis | Mínimo 5 destinatários | Alta |
| RF-038 | Preferências por destinatário | Quais canais e quais prioridades | Alta |
| RF-039 | Teste de notificação | Botão para testar cada canal | Alta |
| RF-040 | Histórico de notificações enviadas | Log com status de entrega | Média |
| RF-041 | Estatísticas de notificações | Quantidade por tipo/período | Baixa |

---

## 5. Requisitos não funcionais

### 5.1 Performance

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-001 | Tempo do evento à notificação push | < 5 segundos |
| RNF-002 | Tempo do evento à notificação Telegram | < 5 segundos |
| RNF-003 | Tempo do evento ao SMS | < 30 segundos |
| RNF-004 | Tempo de acionamento da sirene | < 1 segundo |

### 5.2 Confiabilidade

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-005 | Taxa de entrega push | > 99% em condições normais |
| RNF-006 | Redundância mínima | 2 canais distintos configurados |
| RNF-007 | Funcionamento sem internet | Sirene + iluminação local mantidos |
| RNF-008 | Fila de mensagens | Enfileirar notificações se canal indisponível |

### 5.3 Segurança

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-009 | Bot Telegram privado | Apenas chat IDs autorizados |
| RNF-010 | SMTP com TLS | Criptografia obrigatória para e-mail |
| RNF-011 | Proteção contra spam | Rate limiting de notificações (máx 10/min) |
| RNF-012 | Ações autenticadas | Desarme via notificação requer confirmação |

### 5.4 Usabilidade

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-013 | Configuração guiada | Wizard para setup inicial de canais |
| RNF-014 | Templates editáveis | Texto das notificações customizável |
| RNF-015 | Idioma | Português brasileiro |

---

## 6. Arquitetura técnica

### 6.1 Diagrama de componentes

```
┌─────────────────────────────────────────────────────────────────────┐
│                    HOME ASSISTANT (Servidor Central)                  │
│                                                                     │
│  ┌─────────────┐    ┌─────────────────────┐    ┌───────────────┐   │
│  │   ALARMO    │    │ ENGINE DE NOTIFICAÇÃO│    │   FRIGATE     │   │
│  │  (eventos)  │───►│                     │◄───│  (snapshots)  │   │
│  └─────────────┘    │  ┌───────────────┐  │    └───────────────┘   │
│                     │  │ Classificação │  │                         │
│  ┌─────────────┐    │  │ de Prioridade │  │                         │
│  │  SENSORES   │───►│  └───────┬───────┘  │                         │
│  │  (MQTT)     │    │          │          │                         │
│  └─────────────┘    │  ┌───────▼───────┐  │                         │
│                     │  │  Roteamento   │  │                         │
│                     │  │  por Canal    │  │                         │
│                     │  └───────┬───────┘  │                         │
│                     │          │          │                         │
│                     └──────────┼──────────┘                         │
│                                │                                    │
└────────────────────────────────┼────────────────────────────────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
       ┌──────▼──────┐   ┌──────▼──────┐   ┌──────▼──────┐
       │    PUSH     │   │  TELEGRAM   │   │    SMS      │
       │ (HA Comp.)  │   │   (Bot)     │   │ (Twilio/    │
       │             │   │             │   │  Modem USB) │
       └─────────────┘   └─────────────┘   └─────────────┘
              │                  │                  │
       ┌──────▼──────┐   ┌──────▼──────┐   ┌──────▼──────┐
       │   E-MAIL    │   │  SIRENE     │   │   WEBHOOK   │
       │   (SMTP)    │   │  (Zigbee)   │   │  (HTTP POST)│
       └─────────────┘   └─────────────┘   └─────────────┘
```

### 6.2 Fluxo de processamento de notificação

```
1. Evento gerado (Alarmo, sensor, Frigate)
           │
           ▼
2. Classificação de prioridade
   ├── P1: Alarme disparado, pânico, invasão
   ├── P2: Fumaça, gás, tamper
   ├── P3: Abertura com alarme armado
   ├── P4: Bateria fraca, offline
   └── P5: Status, acesso autorizado
           │
           ▼
3. Verificar silenciamento
   ├── Silenciado (e não é P1) → Log apenas
   └── Ativo → Continua
           │
           ▼
4. Construir conteúdo
   ├── Texto descritivo
   ├── Snapshot (se câmera disponível)
   ├── Botões de ação
   └── Links relevantes
           │
           ▼
5. Roteamento por prioridade
   ├── Selecionar canais conforme nível
   └── Selecionar destinatários
           │
           ▼
6. Envio paralelo em todos os canais
           │
           ▼
7. Monitorar confirmação
   ├── Confirmado → Registrar
   └── Não confirmado → Escalar
```

### 6.3 Exemplo de automação YAML

```yaml
# Automação de notificação P1 - Alarme disparado
automation:
  - alias: "Notificação P1 - Alarme Disparado"
    trigger:
      - platform: state
        entity_id: alarm_control_panel.alarmo
        to: "triggered"
    action:
      # Canal 1: Push notification com snapshot
      - service: notify.mobile_app_celular_morador
        data:
          title: "🚨 ALARME DISPARADO"
          message: >
            Alarme disparado - {{ trigger.to_state.attributes.open_sensors }}
            Zona: {{ trigger.to_state.attributes.changed_by }}
          data:
            image: /api/frigate/notifications/latest.jpg
            actions:
              - action: DESARMAR
                title: "Desarmar"
              - action: VER_CAMERA
                title: "Ver câmera"
            push:
              sound:
                name: alarm.caf
                critical: 1
                volume: 1.0

      # Canal 2: Telegram com snapshot
      - service: telegram_bot.send_photo
        data:
          target: !secret telegram_chat_id
          caption: >
            🚨 *ALARME DISPARADO*
            Sensor: {{ trigger.to_state.attributes.open_sensors }}
            Hora: {{ now().strftime('%H:%M:%S') }}
          url: /api/frigate/notifications/latest.jpg
          inline_keyboard:
            - "Desarmar:/desarmar, Ver câmera:/camera"

      # Canal 3: SMS (via Twilio)
      - service: notify.twilio_sms
        data:
          message: >
            ALARME DISPARADO - {{ trigger.to_state.attributes.open_sensors }}
            {{ now().strftime('%H:%M') }}
          target:
            - !secret telefone_morador_1
            - !secret telefone_morador_2
```

---

## 7. Produtos/componentes recomendados

### 7.1 Canais de notificação - serviços

| Canal | Serviço recomendado | Custo | Observações |
|-------|---------------------|-------|-------------|
| Push notification | Home Assistant Companion | Gratuito | iOS e Android |
| Telegram | Bot API Telegram | Gratuito | Ilimitado, suporta mídia |
| E-mail | Gmail/Outlook SMTP | Gratuito | Limite de envios por dia |
| SMS | Twilio | ~R$ 0,15/SMS | Créditos pré-pagos |
| SMS (alternativa) | Modem USB 4G (Huawei) | R$ 150-300 (hardware) | Sem custo recorrente para SMS local |
| Chamada de voz | Twilio | ~R$ 0,50/chamada | Para emergências P1 |

### 7.2 Hardware para notificação local

| Componente | Modelo sugerido | Preço estimado | Observações |
|------------|-----------------|----------------|-------------|
| Sirene interna Zigbee | Heiman HS2WD-E | R$ 100-150 | 95dB, Z2M/ZHA |
| Sirene interna Zigbee | Tuya TS0224 | R$ 80-120 | 90dB, Z2M |
| Sirene externa | Genérica 12V 110dB | R$ 100-200 | Via relé Zigbee |
| Lâmpada Zigbee (flash) | Sonoff B05-BL-A60 | R$ 40-70 | RGB para alerta visual |
| Modem USB 4G | Huawei E3372 | R$ 150-250 | Para SMS sem Twilio |

### 7.3 Custos recorrentes estimados

| Serviço | Uso estimado/mês | Custo mensal |
|---------|------------------|--------------|
| Telegram Bot | Ilimitado | R$ 0 |
| Push (HA Companion) | Ilimitado | R$ 0 |
| SMS via Twilio (emergências) | 5-10 SMS | R$ 1-2 |
| E-mail SMTP | 20-50 e-mails | R$ 0 |
| **Total recorrente estimado** | | **R$ 0-2/mês** |

---

## 8. Estimativa de implementação por cenário

### 8.1 Cenário rural

| Componente | Custo |
|------------|-------|
| Sirene externa 110dB | R$ 150 |
| Sirene interna Zigbee | R$ 120 |
| Modem USB 4G (SMS local) | R$ 200 |
| Chip operadora | R$ 15/mês |
| Configuração Telegram + Push | R$ 0 |
| **Total setup** | **R$ 470** |

### 8.2 Cenário casa urbana

| Componente | Custo |
|------------|-------|
| Sirene externa 110dB | R$ 150 |
| Sirene interna Zigbee | R$ 120 |
| Lâmpada flash Zigbee | R$ 50 |
| Configuração Telegram + Push | R$ 0 |
| Crédito Twilio (SMS) | R$ 20/ano |
| **Total setup** | **R$ 320** |

### 8.3 Cenário apartamento

| Componente | Custo |
|------------|-------|
| Sirene interna Zigbee (volume moderado) | R$ 100 |
| Configuração Telegram + Push | R$ 0 |
| **Total setup** | **R$ 100** |

---

## 9. Critérios de aceitação

| ID | Critério | Método de verificação |
|----|----------|----------------------|
| CA-001 | Push notification chega em < 5 segundos | Teste com cronômetro |
| CA-002 | Telegram recebe mensagem com snapshot | Teste gerando alarme |
| CA-003 | SMS entregue em < 30 segundos | Teste com cronômetro |
| CA-004 | Sirene aciona em < 1 segundo | Teste com cronômetro |
| CA-005 | Escalação funciona se não houver confirmação | Teste de timeout |
| CA-006 | Botão de ação "Desarmar" via push funciona | Teste funcional |
| CA-007 | Silenciamento respeita exceção P1 | Teste com silenciamento ativo |
| CA-008 | Histórico de notificações acessível no dashboard | Verificação visual |
| CA-009 | Rate limiting impede mais de 10 notificações/min | Teste de stress |
| CA-010 | Notificação P1 funciona sem internet (sirene local) | Teste de desconexão |

---

## 10. Métricas de sucesso

| Métrica | Alvo | Medição |
|---------|------|---------|
| **Taxa de entrega push** | > 99% | Monitoramento de status |
| **Tempo médio de notificação** | < 5 segundos (push/Telegram) | Logs de timestamp |
| **Taxa de confirmação de alertas P1** | > 95% em 60 segundos | Monitoramento |
| **Falsos positivos reportados** | < 1/semana | Feedback |
| **Satisfação com notificações** | > 4/5 (sem fadiga) | Pesquisa |

---

## 11. Riscos e dependências

### 11.1 Riscos

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Internet cai e push/Telegram falham | Média | Alto | SMS via modem local + sirene local |
| Fadiga de alertas (muitas notificações) | Alta | Médio | Priorização e silenciamento inteligente |
| Telegram Bot API indisponível | Baixa | Médio | Push como canal alternativo |
| Morador ignora notificação crítica | Média | Alto | Escalação + chamada de voz |
| Custo de SMS cresce com muitos alertas | Baixa | Baixo | SMS apenas para P1, limitar volume |

### 11.2 Dependências

| Dependência | Tipo | PRD relacionado |
|-------------|------|-----------------|
| Home Assistant Core | Plataforma | PRD_LOCAL_PROCESSING_HUB |
| Alarmo (gerador de eventos) | Funcional | PRD_SENSORS_AND_ALARMS_PLATFORM |
| Frigate (snapshots/clips) | Funcional | PRD_VIDEO_SURVEILLANCE_AND_NVR |
| Internet (para push/Telegram) | Infraestrutura | PRD_BACKUP_AND_RESILIENCE |
| Failover 4G (para SMS sem internet) | Infraestrutura | PRD_BACKUP_AND_RESILIENCE |

---

## 12. Referências

### Documentos do projeto
- `docs/ARQUITETURA_TECNICA.md` - Seções 6, 8
- `prd/PRD_SENSORS_AND_ALARMS_PLATFORM.md` - Seção 4.5 (notificações)
- `rules/RULES_COMPLIANCE_AND_STANDARDS.md`

### Externos
- [Home Assistant - Notifications](https://www.home-assistant.io/integrations/#notifications)
- [Home Assistant - Actionable Notifications](https://companion.home-assistant.io/docs/notifications/actionable-notifications)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Twilio SMS API](https://www.twilio.com/docs/sms)

---

> **Status**: Rascunho v1.0
>
> **Próxima revisão**: Após validação pelo Agente_Arquiteto_Tecnico
