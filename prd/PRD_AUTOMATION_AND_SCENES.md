# PRD – Automações de Segurança e Cenas

> Sistema de Home Security – Open Source / Open Hardware
>
> Versão: 1.0 | Data: 2026-02-18 | Responsável: Agente_Documentador

---

## 1. Visão geral

- **Nome do produto/funcionalidade**: Sistema de Automações de Segurança e Cenas
- **Responsável**: Agente_Arquiteto_Tecnico (especificação), Agente_Documentador (documentação)
- **Data**: 2026-02-18
- **PRDs relacionados**: PRD_SENSORS_AND_ALARMS_PLATFORM, PRD_NOTIFICATIONS_AND_ALERTS, PRD_MONITORING_DASHBOARD, PRD_HOUSE_ENVELOPE

---

## 2. Problema e oportunidade

### 2.1 Problema

Sistemas de segurança residencial frequentemente operam de forma isolada:
- **Ações manuais**: Morador precisa lembrar de armar alarme, trancar portas, apagar luzes
- **Resposta passiva**: Sistema apenas detecta e notifica, sem ações reativas automáticas
- **Casa visivelmente vazia**: Ausência prolongada é perceptível por padrões de iluminação
- **Falta de contexto**: Sistema não considera horário, presença ou rotina do morador
- **Desconexão entre subsistemas**: Alarme, câmeras, luzes e fechaduras operam independentemente

### 2.2 Oportunidade

Criar automações inteligentes que:
- **Reajam automaticamente** a eventos de segurança (iluminação reativa, gravação forçada)
- **Simulem presença** durante ausência prolongada
- **Integrem subsistemas** em cenas coerentes ("saindo de casa", "boa noite")
- **Adaptem-se ao contexto** (horário, presença, modo do alarme)
- **Reduzam falhas humanas** automatizando tarefas críticas de segurança

---

## 3. Público-alvo

| Perfil | Necessidades específicas |
|--------|--------------------------|
| **Família ocupada** | Automação de rotinas, reduzir esquecimentos |
| **Viajante frequente** | Simulação de presença convincente |
| **Idoso** | Automações simples, sem necessidade de intervenção |
| **Usuário técnico** | Customização avançada, scripts complexos |
| **Casal trabalhador** | Segurança automática durante dia de trabalho |

---

## 4. Requisitos funcionais

### 4.1 Cenas de segurança pré-definidas

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-001 | Cena "Saindo de casa" | Armar alarme total, trancar portas, desligar luzes internas, verificar janelas | Alta |
| RF-002 | Cena "Chegando em casa" | Desarmar alarme, destrancar porta, acender luzes de entrada | Alta |
| RF-003 | Cena "Boa noite" | Armar alarme parcial (perímetro + portas), trancar todas as portas, apagar luzes externas não-segurança | Alta |
| RF-004 | Cena "Bom dia" | Desarmar alarme, acender luzes de rotina matinal | Média |
| RF-005 | Cena "Pânico" | Acionar todas as sirenes, acender todas as luzes, notificar todos os contatos | Alta |
| RF-006 | Cena "Férias" | Ativar simulação de presença, armar total, notificações para contatos de emergência | Média |
| RF-007 | Cena "Visita" | Desarmar parcialmente, manter perímetro armado | Média |

### 4.2 Iluminação reativa a eventos de segurança

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-008 | Acender luzes externas ao detectar movimento (noite) | PIR externo → refletores LED | Alta |
| RF-009 | Acender todas as luzes ao disparar alarme | Interno e externo, máximo brilho | Alta |
| RF-010 | Flash em lâmpadas ao disparar alarme | Piscar vermelho se RGB disponível | Média |
| RF-011 | Acender luz da entrada ao abrir portão | Transição gradual, timeout 5 min | Média |
| RF-012 | Manter luzes externas de segurança à noite | Automação sunset/sunrise | Alta |
| RF-013 | Apagar luzes automaticamente após timeout | Configurável por zona (5-30 min) | Média |

### 4.3 Simulação de presença

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-014 | Ligar/desligar luzes em padrão variado | Horários semi-aleatórios, imitando rotina | Alta |
| RF-015 | Simular uso de TV | Lâmpada com variação de cor/brilho | Média |
| RF-016 | Variar padrão diariamente | Não repetir exatamente o mesmo horário | Alta |
| RF-017 | Ativar/desativar automaticamente | Baseado em geolocalização ou modo férias | Média |
| RF-018 | Incluir múltiplos cômodos | Sala, quarto, cozinha em sequência realista | Alta |
| RF-019 | Horário de "dormir" simulado | Apagar luzes gradualmente após 22h-23h | Média |

### 4.4 Automações de resposta a alarme

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-020 | Ao disparar alarme → iniciar gravação em todas as câmeras | Forçar recording no Frigate | Alta |
| RF-021 | Ao disparar alarme → acionar sirenes | Interna e externa | Alta |
| RF-022 | Ao disparar alarme → enviar notificações multi-canal | Conforme PRD_NOTIFICATIONS_AND_ALERTS | Alta |
| RF-023 | Ao detectar pessoa externa (noite) → acender refletores | Via Frigate + Zigbee | Alta |
| RF-024 | Ao detectar violação de cerca → acender perímetro completo | Integração com central de cerca | Média |
| RF-025 | Ao pressionar botão de pânico → cena Pânico completa | Sirenes + luzes + notificações | Alta |

### 4.5 Automações de rotina com segurança

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-026 | Auto-armar por geolocalização | Armar quando todos saírem | Alta |
| RF-027 | Auto-desarmar por geolocalização | Desarmar ao se aproximar (200m) | Média |
| RF-028 | Auto-armar por horário | Armar parcial às 23h se não armado | Média |
| RF-029 | Verificar portas/janelas antes de armar | Alertar se alguma está aberta | Alta |
| RF-030 | Travamento automático de portas à noite | Travar todas as fechaduras inteligentes às 22h | Média |
| RF-031 | Alerta de porta aberta prolongada | Porta externa aberta > 10 minutos | Média |
| RF-032 | Auto-armar após período de inatividade | 30 minutos sem movimento interno | Baixa |

### 4.6 Automações ambientais de segurança

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-033 | Ao detectar fumaça → desligar HVAC e acender luzes de emergência | Integração com sensores ambientais | Alta |
| RF-034 | Ao detectar vazamento de gás → desligar válvula (se automatizada) | Integração com sensor de gás | Alta |
| RF-035 | Ao detectar inundação → fechar registro (se automatizado) | Integração com sensor de água | Média |
| RF-036 | Notificação de condições adversas | Fumaça, gás, água com prioridade P2 | Alta |

### 4.7 Triggers e condições

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-037 | Trigger por evento de sensor | Abertura, movimento, vibração | Alta |
| RF-038 | Trigger por mudança de estado do alarme | Armado, desarmado, disparado | Alta |
| RF-039 | Trigger por detecção de IA (Frigate) | Pessoa, veículo, animal | Alta |
| RF-040 | Trigger por horário (sol/lua) | Sunset, sunrise, horário fixo | Alta |
| RF-041 | Trigger por geolocalização | Entrada/saída de zona geográfica | Média |
| RF-042 | Condição: período do dia | Noite/dia, horário específico | Alta |
| RF-043 | Condição: presença de moradores | Ninguém em casa / alguém em casa | Alta |
| RF-044 | Condição: modo do alarme | Armado total/parcial/desarmado | Alta |

---

## 5. Requisitos não funcionais

### 5.1 Performance

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-001 | Tempo de execução de cena | < 2 segundos para todos os dispositivos |
| RNF-002 | Tempo de resposta de iluminação reativa | < 1 segundo após detecção |
| RNF-003 | Tempo de resposta ao alarme | < 500ms para acionar sirene e luzes |

### 5.2 Confiabilidade

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-004 | Automações devem ser 100% locais | Sem dependência de nuvem ou internet |
| RNF-005 | Fallback se dispositivo não responder | Prosseguir com demais dispositivos da cena |
| RNF-006 | Retry automático | 3 tentativas para dispositivos que falharam |
| RNF-007 | Log de todas as automações executadas | Timestamp + resultado |

### 5.3 Usabilidade

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-008 | Ativar cenas em < 2 toques no app | Botões na tela principal |
| RNF-009 | NFC tags para ativar cenas | Tag na porta = "Saindo de casa" |
| RNF-010 | Configuração via UI | Sem necessidade de YAML para cenas básicas |
| RNF-011 | Templates prontos | Cenas pré-configuradas adaptáveis |

### 5.4 Segurança

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-012 | Cenas que desarmam alarme exigem autenticação | Código, biometria ou geolocalização |
| RNF-013 | Simulação de presença não revelável | Padrão variado, sem repetição previsível |

---

## 6. Arquitetura técnica

### 6.1 Diagrama de automações

```
┌─────────────────────────────────────────────────────────────────────┐
│                    HOME ASSISTANT - ENGINE DE AUTOMAÇÃO               │
│                                                                     │
│  TRIGGERS                    CONDIÇÕES                 AÇÕES        │
│  ┌──────────────┐           ┌──────────────┐          ┌───────────┐│
│  │ Sensor Zigbee│           │ Horário/Sol  │          │ Alarmo    ││
│  │ (abertura,   │──┐       │ (noite/dia)  │──┐      │ (arm/dis) ││
│  │ PIR, vibr.)  │  │       └──────────────┘  │      └───────────┘│
│  └──────────────┘  │       ┌──────────────┐  │      ┌───────────┐│
│  ┌──────────────┐  │       │ Presença     │  │      │ Luzes     ││
│  │ Alarmo       │  ├──────►│ (geoloc.)    │──├─────►│ (Zigbee)  ││
│  │ (arm/disarm/ │  │       └──────────────┘  │      └───────────┘│
│  │  triggered)  │──┤       ┌──────────────┐  │      ┌───────────┐│
│  └──────────────┘  │       │ Estado       │  │      │ Fechaduras││
│  ┌──────────────┐  │       │ Alarme       │──┘      │ (lock)    ││
│  │ Frigate      │  │       └──────────────┘         └───────────┘│
│  │ (pessoa,     │──┤                                ┌───────────┐│
│  │  veículo)    │  │                                │ Sirenes   ││
│  └──────────────┘  │                                │ (Zigbee)  ││
│  ┌──────────────┐  │                                └───────────┘│
│  │ Horário      │──┤                                ┌───────────┐│
│  │ (cron/sun)   │  │                                │ Notific.  ││
│  └──────────────┘  │                                │ (multi)   ││
│  ┌──────────────┐  │                                └───────────┘│
│  │ Geolocation  │──┘                                ┌───────────┐│
│  │ (HA Comp.)   │                                   │ Câmeras   ││
│  └──────────────┘                                   │ (Frigate) ││
│                                                     └───────────┘│
└─────────────────────────────────────────────────────────────────────┘
```

### 6.2 Exemplo: Cena "Saindo de Casa"

```yaml
# Cena: Saindo de Casa
script:
  saindo_de_casa:
    alias: "Saindo de Casa"
    sequence:
      # Verificar se portas/janelas estão fechadas
      - condition: state
        entity_id: group.todas_aberturas
        state: "off"

      # Se alguma aberta, notificar e abortar
      - if:
          - condition: state
            entity_id: group.todas_aberturas
            state: "on"
        then:
          - service: notify.mobile_app_celular
            data:
              title: "Atenção"
              message: "Há portas/janelas abertas. Feche antes de sair."
          - stop: "Aberturas abertas"

      # Trancar fechaduras inteligentes
      - service: lock.lock
        target:
          entity_id: lock.porta_principal

      # Desligar luzes internas
      - service: light.turn_off
        target:
          entity_id: group.luzes_internas

      # Armar alarme total (com delay de saída)
      - service: alarm_control_panel.alarm_arm_away
        target:
          entity_id: alarm_control_panel.alarmo
        data:
          code: !secret alarmo_code

      # Feedback
      - service: notify.mobile_app_celular
        data:
          title: "Casa segura"
          message: "Alarme armado, portas trancadas."
```

### 6.3 Exemplo: Simulação de presença

```yaml
# Automação: Simulação de presença
automation:
  - alias: "Simulação de Presença"
    trigger:
      - platform: time
        at: "18:30:00"
    condition:
      - condition: state
        entity_id: alarm_control_panel.alarmo
        state: "armed_away"
    action:
      - repeat:
          until:
            - condition: time
              after: "23:00:00"
          sequence:
            # Sala: ligar por 20-40 min
            - service: light.turn_on
              target:
                entity_id: light.sala
              data:
                brightness_pct: "{{ range(60, 100) | random }}"
            - delay:
                minutes: "{{ range(20, 40) | random }}"
            - service: light.turn_off
              target:
                entity_id: light.sala

            # Cozinha: ligar por 10-20 min
            - delay:
                minutes: "{{ range(5, 15) | random }}"
            - service: light.turn_on
              target:
                entity_id: light.cozinha
            - delay:
                minutes: "{{ range(10, 20) | random }}"
            - service: light.turn_off
              target:
                entity_id: light.cozinha

      # "Dormir" - apagar tudo gradualmente
      - service: light.turn_off
        target:
          entity_id: group.luzes_internas
```

---

## 7. Produtos/componentes recomendados

### 7.1 Iluminação Zigbee para automações

| Componente | Modelo sugerido | Preço estimado | Observações |
|------------|-----------------|----------------|-------------|
| Lâmpada E27 branca | Sonoff B02-BL-A60 | R$ 30-50 | Dimmerizável, Zigbee |
| Lâmpada E27 RGB | Sonoff B05-BL-A60 | R$ 40-70 | RGB para alertas visuais |
| Refletor LED externo | Lâmpada Zigbee + holofote | R$ 60-120 | Para iluminação reativa |
| Smart plug Zigbee | Sonoff S26R2 | R$ 50-80 | Para abajures, TV simulação |
| Tomada Zigbee embutida | Tuya TS011F | R$ 40-70 | Para automação de tomadas |
| Fita LED Zigbee | Gledopto GL-C-008P | R$ 80-150 | Para iluminação perimetral |

### 7.2 NFC Tags e triggers físicos

| Componente | Modelo sugerido | Preço estimado | Observações |
|------------|-----------------|----------------|-------------|
| NFC Tag NTAG215 (10 unidades) | Genérico | R$ 30-50 | Para cenas por aproximação |
| Botão Zigbee | Aqara WXKG11LM | R$ 60-90 | 1 clique, 2 cliques, long press |
| Cubo Zigbee | Aqara MFKZQ01LM | R$ 80-120 | Múltiplas ações (shake, flip) |

### 7.3 Estimativa de investimento em automação

| Cenário | Lâmpadas | Plugs | NFC/Botões | Total |
|---------|----------|-------|------------|-------|
| Apartamento | 3-4 (R$ 120-200) | 1 (R$ 50) | 2 NFC (R$ 10) | **R$ 180-260** |
| Casa urbana | 6-10 (R$ 240-500) | 2-3 (R$ 100-240) | 3 NFC + 1 botão (R$ 80) | **R$ 420-820** |
| Rural | 4-8 (R$ 160-400) | 2 (R$ 100) | 2 NFC + 1 botão (R$ 80) | **R$ 340-580** |

---

## 8. Critérios de aceitação

| ID | Critério | Método de verificação |
|----|----------|----------------------|
| CA-001 | Cena "Saindo de casa" arma alarme, tranca portas, apaga luzes | Teste funcional completo |
| CA-002 | Cena "Chegando em casa" desarma alarme e acende luzes | Teste funcional |
| CA-003 | Iluminação reativa acende em < 1 segundo após detecção | Teste com cronômetro |
| CA-004 | Simulação de presença opera em padrão variado | Observação por 3 dias |
| CA-005 | Automação de alarme por geolocalização funciona | Teste saindo/chegando de casa |
| CA-006 | Automação de resposta ao alarme aciona sirenes + luzes | Teste de disparo |
| CA-007 | NFC tag ativa cena corretamente | Teste por aproximação |
| CA-008 | Automações funcionam sem internet | Teste desconectando internet |
| CA-009 | Verificação de portas/janelas antes de armar funciona | Teste com porta aberta |
| CA-010 | Log de automações executadas acessível no HA | Verificação de registros |

---

## 9. Métricas de sucesso

| Métrica | Alvo | Medição |
|---------|------|---------|
| **Taxa de execução bem-sucedida** | > 99% das automações | Logs do HA |
| **Tempo de resposta das cenas** | < 2 segundos | Monitoramento |
| **Adoção pelos moradores** | 100% usando cenas diariamente | Logs de uso |
| **Redução de esquecimentos** | 0 vezes alarme não armado ao sair | Logs |
| **Falsos alarmes por automação** | 0 | Contagem |

---

## 10. Riscos e dependências

### 10.1 Riscos

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Geolocalização imprecisa dispara cena errada | Média | Médio | Zona de buffer de 200m, confirmação |
| Lâmpada Zigbee não responde (offline) | Baixa | Baixo | Retry automático, continuar cena |
| Simulação de presença detectada como artificial | Baixa | Médio | Variar padrão diariamente |
| Automação conflitante com ação manual | Média | Baixo | Priorizar ação manual sobre automação |
| Morador não configura cenas corretamente | Média | Médio | Templates prontos, wizard de configuração |

### 10.2 Dependências

| Dependência | Tipo | PRD relacionado |
|-------------|------|-----------------|
| Sistema de alarme (Alarmo) | Funcional | PRD_SENSORS_AND_ALARMS_PLATFORM |
| Notificações multi-canal | Funcional | PRD_NOTIFICATIONS_AND_ALERTS |
| Frigate (detecção de IA) | Funcional | PRD_VIDEO_SURVEILLANCE_AND_NVR |
| Fechaduras inteligentes | Opcional | PRD_HOUSE_ENVELOPE, PRD_APARTMENT_SMART_LOCK |
| Sensores ambientais | Opcional | PRD_ENVIRONMENTAL_SENSORS |
| Home Assistant Core | Plataforma | PRD_LOCAL_PROCESSING_HUB |

---

## 11. Referências

### Documentos do projeto
- `docs/ARQUITETURA_TECNICA.md` - Seções 6, 8
- `prd/PRD_SENSORS_AND_ALARMS_PLATFORM.md` - Integração com Alarmo
- `prd/PRD_NOTIFICATIONS_AND_ALERTS.md` - Sistema de notificações
- `rules/RULES_COMPLIANCE_AND_STANDARDS.md`

### Externos
- [Home Assistant - Automations](https://www.home-assistant.io/docs/automation/)
- [Home Assistant - Scripts](https://www.home-assistant.io/integrations/script/)
- [Home Assistant - Scenes](https://www.home-assistant.io/integrations/scene/)
- [Alarmo - Automações](https://github.com/nielsfaber/alarmo)

---

> **Status**: Rascunho v1.0
>
> **Próxima revisão**: Após validação pelo Agente_Arquiteto_Tecnico
