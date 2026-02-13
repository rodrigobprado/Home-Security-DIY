# Resiliencia e Modos Degradados -- Sistema de Home Security

> Documento produzido durante a revisao do projeto em 2026-02-12
>
> Escopo: Protecao contra tamper/destruicao, modos de operacao degradada e estrategia de backup do NVR
>
> Referencia principal: `docs/ARQUITETURA_TECNICA.md`

---

## Indice

1. [Protecao contra tamper e destruicao](#1-protecao-contra-tamper-e-destruicao)
2. [Modos de operacao degradada](#2-modos-de-operacao-degradada)
3. [Estrategia de backup do NVR](#3-estrategia-de-backup-do-nvr)
4. [Regras derivadas (REGRA-RESIL)](#4-regras-derivadas)
5. [Referencias](#5-referencias)

---

## 1. Protecao contra tamper e destruicao

### 1.1 Modelo de ameaca

O sistema de seguranca residencial DIY e, por definicao, um alvo de interesse para invasores que desejam neutraliza-lo antes ou durante uma invasao. Diferente de sistemas monitorados por empresas de seguranca, nao ha central de monitoramento 24h verificando sinais de vida do sistema. Isso torna a **resiliencia contra sabotagem** um requisito critico, nao opcional.

### 1.2 Cenarios de ataque fisico ao sistema

| # | Cenario de ataque | Probabilidade | Impacto | Sofisticacao do atacante |
|---|-------------------|---------------|---------|--------------------------|
| A1 | **Corte de energia na rua** (disjuntor externo ou poste) | Alta | Critico | Baixa |
| A2 | **Corte de cabo de internet/fibra** na caixa externa | Alta | Alto | Baixa |
| A3 | **Destruicao/roubo do servidor central** (Mini PC) | Media | Critico | Media |
| A4 | **Destruicao de cameras acessiveis** (pedra, spray, corte de cabo) | Alta | Alto | Baixa |
| A5 | **Sabotagem do quadro eletrico** (desligar disjuntores) | Media | Critico | Baixa |
| A6 | **Jamming de sinal Zigbee/Wi-Fi** | Baixa | Alto | Alta |
| A7 | **Corte de energia + internet simultaneos** (ataque coordenado) | Media | Critico | Media |
| A8 | **Destruicao do switch PoE** | Baixa | Alto | Media |

#### Detalhamento dos cenarios

**A1 -- Corte de energia na rua**

O cenario mais comum e mais simples. O atacante desliga o disjuntor geral no poste ou na caixa de entrada antes do quadro eletrico da residencia. Consequencias:
- Sem nobreak: todo o sistema desliga imediatamente
- Cameras PoE desligam (switch sem energia)
- Servidor desliga, gravacoes param
- Sensores Zigbee (bateria) continuam operando, porem sem coordenador para processar eventos

**A2 -- Corte de cabo de internet/fibra**

A caixa da operadora de fibra optica (ONU/ONT) geralmente fica em local acessivel externamente. O corte elimina:
- Notificacoes push (app Home Assistant Companion)
- SMS e chamadas via VoIP
- Acesso remoto via VPN/Tailscale
- Atualizacoes de status em tempo real

O sistema local continua operando (automacoes, gravacao, sirene), mas o morador **nao e notificado** se estiver fora de casa.

**A3 -- Destruicao/roubo do servidor central**

Se o invasor localiza e destroi ou rouba o Mini PC N100:
- Home Assistant para completamente
- Frigate para (sem NVR)
- Zigbee2MQTT para (sem bridge)
- MQTT Mosquitto para (sem broker)
- Todas as automacoes cessam
- Gravacoes no disco do servidor sao perdidas

Este e o cenario de **ponto unico de falha mais critico** da arquitetura.

**A4 -- Destruicao de cameras acessiveis**

Cameras externas sao alvos faceis:
- Spray de tinta na lente
- Corte do cabo de rede (PoE)
- Destruicao fisica (pedra, martelo)

Impacto: perda de monitoramento visual daquela zona. Se a camera nao tiver edge recording (cartao SD), as imagens anteriores ao corte sao preservadas apenas no NVR.

**A5 -- Sabotagem do quadro eletrico**

Quadros eletricos residenciais frequentemente ficam em areas externas ou semi-acessiveis. O invasor pode desligar disjuntores seletivamente.

**A6 -- Jamming de sinal Zigbee/Wi-Fi**

Ataque mais sofisticado, usando dispositivos de interferencia eletromagnetica. Efeito:
- Sensores Zigbee nao conseguem comunicar com o coordenador
- Cameras Wi-Fi (se houver) perdem conexao
- Dificil de detectar sem hardware especializado

**A7 -- Ataque coordenado (energia + internet)**

A combinacao de A1 + A2 e o **indicador mais forte de ataque deliberado**, e nao de falha acidental. Deve ser tratado com a prioridade maxima pelo sistema.

**A8 -- Destruicao do switch PoE**

Se o switch PoE esta em local acessivel, sua destruicao desliga todas as cameras simultaneamente, mesmo com o servidor e nobreak intactos.

---

### 1.3 Mitigacoes obrigatorias

#### 1.3.1 Conectividade 4G/LTE como REQUISITO

> **IMPORTANTE**: O 4G/LTE nao e opcional. E um requisito para todos os cenarios (rural, urbano e apartamento).

| Aspecto | Especificacao |
|---------|---------------|
| **Funcao** | Canal de notificacao redundante quando internet fixa cai |
| **Hardware** | Roteador/modem 4G ou dongle USB 4G no Mini PC |
| **Operadora** | Chip pre-pago ou plano de dados minimo (1-2GB/mes suficiente) |
| **Custo estimado** | R$30-50/mes (plano dados) + R$100-300 (modem 4G) |
| **Configuracao** | Failover automatico: internet fixa primaria, 4G secundaria |
| **Uso** | Apenas notificacoes criticas (push, SMS, Telegram) -- NAO streaming de video |

**Implementacao tecnica:**

```yaml
# Exemplo: roteador com failover ou script de monitoramento
# O Home Assistant deve ter automacao que detecta queda de internet
# e roteia notificacoes via 4G

# automacao HA para detectar queda de internet
automation:
  - alias: "Alerta - Internet principal offline"
    trigger:
      - platform: state
        entity_id: binary_sensor.internet_status
        to: "off"
        for: "00:01:00"
    action:
      - service: notify.telegram_via_4g
        data:
          message: "ALERTA: Internet fixa OFFLINE. Sistema operando via 4G."
```

**Opcoes de hardware 4G:**

| Opcao | Preco estimado | Vantagem | Desvantagem |
|-------|----------------|----------|-------------|
| Roteador com slot SIM (ex: TP-Link TL-MR6400) | R$300-500 | Failover automatico | Mais um equipamento |
| Dongle USB 4G no Mini PC | R$100-200 | Compacto, integrado | Configuracao manual no Linux |
| Smartphone antigo como hotspot | R$0 (reuso) | Custo zero hardware | Menos confiavel, bateria degrada |

#### 1.3.2 Nobreak dimensionado

**Calculo de carga:**

| Equipamento | Consumo tipico | Essencial? |
|-------------|----------------|------------|
| Mini PC N100 | 10-15W (idle), 25W (pico) | Sim |
| Switch PoE 8 portas (com cameras) | 40-60W | Sim |
| Roteador/modem internet | 8-12W | Sim |
| Modem 4G (se separado) | 5-8W | Sim |
| Coordenador Zigbee USB | 1-2W (via Mini PC) | Sim (incluso no Mini PC) |
| **Total estimado** | **~65-95W** | - |

**Dimensionamento do nobreak:**

| Nobreak | Capacidade real* | Autonomia estimada (80W) | Preco estimado |
|---------|-----------------|--------------------------|----------------|
| 600VA / 300W | 300W | ~45 min | R$300-400 |
| 1000VA / 500W | 500W | ~1h15 | R$400-600 |
| **1500VA / 900W** | **900W** | **~2h** | **R$500-800** |
| 2200VA / 1200W | 1200W | ~3h | R$800-1200 |

*Capacidade real (watts) geralmente e 50-60% da capacidade em VA.

> **Recomendacao**: Nobreak **1500VA** como minimo. Proporciona aproximadamente 2 horas de autonomia, tempo suficiente para que o morador seja notificado (via 4G) e tome providencias.

**Requisitos do nobreak:**

- Saida senoidal pura (ou senoidal simulada de qualidade) -- evitar modelos onda quadrada
- Funcao de auto-ligamento quando energia retorna
- Porta USB ou serial para monitoramento via NUT (Network UPS Tools) no Home Assistant
- Alarme sonoro quando em bateria (pode ser desabilitado via software se indesejado)

```yaml
# Monitoramento do nobreak via NUT no Home Assistant
sensor:
  - platform: nut
    host: localhost
    resources:
      - ups.status
      - battery.charge
      - battery.runtime
      - input.voltage

automation:
  - alias: "Alerta - Queda de energia (nobreak em bateria)"
    trigger:
      - platform: state
        entity_id: sensor.ups_status
        to: "OB"  # On Battery
    action:
      - service: notify.notify
        data:
          title: "ALERTA CRITICO"
          message: "Queda de energia detectada. Sistema operando em bateria. Autonomia: {{ states('sensor.ups_battery_runtime') }} segundos."
```

#### 1.3.3 Cameras com edge recording (cartao SD)

| Aspecto | Especificacao |
|---------|---------------|
| **Funcao** | Fallback de gravacao quando o NVR (Frigate) esta indisponivel |
| **Requisito** | Cameras com slot para cartao microSD |
| **Capacidade** | Cartao 32-128GB por camera |
| **Modo** | Gravacao continua ou por deteccao de movimento (loop/FIFO) |
| **Retencao no SD** | 2-7 dias (depende da resolucao e capacidade do cartao) |

**Cameras recomendadas com slot SD:**

| Modelo | Slot SD | Gravacao local | Protocolo |
|--------|---------|----------------|-----------|
| Reolink RLC-810A | Sim (microSD ate 256GB) | Continua ou movimento | RTSP/ONVIF |
| Reolink RLC-520A | Sim (microSD ate 256GB) | Continua ou movimento | RTSP/ONVIF |
| Hikvision DS-2CD2x55 | Sim (microSD ate 256GB) | Continua ou evento | RTSP/ONVIF |
| Annke C500 | Sim (microSD ate 256GB) | Movimento | RTSP/ONVIF |

> **IMPORTANTE**: O edge recording no cartao SD deve estar **sempre ativo**, mesmo quando o Frigate esta funcionando normalmente. E a ultima linha de defesa caso o servidor seja destruido ou roubado.

#### 1.3.4 Servidor em local escondido e fixado

**Principio**: O servidor (Mini PC N100) NAO deve estar em local obvio. O invasor nao deve conseguir localiza-lo facilmente.

| Pratica | Descricao |
|---------|-----------|
| **Local nao obvio** | Evitar escritorio, rack de rede visivel, embaixo da TV |
| **Locais sugeridos** | Forro/soto, armario embutido, nicho na parede com porta, compartimento sob escada |
| **Fixacao** | Parafusado na parede ou prateleira (evitar roubo rapido) |
| **Ventilacao** | Garantir circulacao de ar (Mini PC N100 esquenta pouco, ~15W) |
| **Acesso a rede** | Cabo Ethernet ate o switch -- nao usar Wi-Fi para o servidor |
| **Identificacao** | Sem etiquetas ou luzes de LED visiveis do exterior |
| **Nobreak junto** | Nobreak no mesmo local ou proximo, com cabos organizados |

**Diagrama sugerido -- local do servidor:**

```
    ┌─────────────────────────────────────────┐
    │              ARMARIO EMBUTIDO            │
    │         (porta com chave simples)        │
    │                                          │
    │  ┌──────────┐  ┌──────────┐              │
    │  │ Mini PC  │  │ Nobreak  │              │
    │  │  N100    │  │ 1500VA   │              │
    │  │(parafuso)│  │          │              │
    │  └────┬─────┘  └────┬─────┘              │
    │       │              │                    │
    │  ┌────┴──────────────┴────┐              │
    │  │    Regua com DPS       │              │
    │  └────────────┬───────────┘              │
    │               │                          │
    │  ┌────────────┴───────────┐              │
    │  │  Switch PoE 8 portas   │              │
    │  │  (alimentado pelo UPS) │              │
    │  └────────────┬───────────┘              │
    │               │                          │
    │     Cabos Ethernet para cameras          │
    │     (passam por conduites na parede)     │
    └─────────────────────────────────────────┘
```

#### 1.3.5 Alarme de ataque coordenado

A deteccao simultanea de **queda de energia + queda de internet** e o sinal mais forte de um ataque deliberado. O sistema deve tratar esse cenario com prioridade maxima.

**Logica de deteccao:**

```yaml
automation:
  - alias: "CRITICO - Possivel ataque coordenado"
    description: >
      Detecta queda simultanea de energia e internet,
      indicador forte de ataque deliberado.
    trigger:
      - platform: state
        entity_id: sensor.ups_status
        to: "OB"
    condition:
      - condition: state
        entity_id: binary_sensor.internet_status
        state: "off"
    action:
      # Notificacao via 4G (unico canal disponivel)
      - service: notify.telegram_via_4g
        data:
          title: "ALERTA MAXIMO - POSSIVEL ATAQUE"
          message: >
            Energia E internet cortadas simultaneamente.
            Possivel ataque coordenado em andamento.
            Horario: {{ now().strftime('%H:%M:%S') }}
            Autonomia bateria: {{ states('sensor.ups_battery_runtime') }}s
      # Ativar todas as sirenes
      - service: siren.turn_on
        target:
          entity_id: all
      # Acender todas as luzes externas
      - service: light.turn_on
        target:
          entity_id: group.luzes_externas
        data:
          brightness: 255
      # Iniciar gravacao em resolucao maxima em todas as cameras
      - service: frigate.increase_detect_resolution
        data:
          camera_name: all
```

**Matriz de resposta por combinacao de falhas:**

| Energia | Internet | Classificacao | Acao automatica |
|---------|----------|---------------|-----------------|
| OK | Offline | Falha simples | Notificar, ativar 4G, monitorar |
| Offline | OK | Falha simples | Notificar, monitorar autonomia nobreak |
| **Offline** | **Offline** | **Ataque coordenado** | **Alerta maximo via 4G, sirenes, luzes, gravar tudo** |
| OK | OK | Normal | Operacao padrao |

#### 1.3.6 Protecao do quadro eletrico

| Medida | Descricao |
|--------|-----------|
| **Cadeado no quadro** | Quadro de distribuicao com fechadura ou cadeado |
| **Quadro em area interna** | Se possivel, manter o quadro dentro da casa |
| **Sensor de abertura** | Sensor Zigbee no quadro (detecta abertura nao autorizada) |
| **Disjuntor do sistema de seguranca** | Em circuito separado, nao identificado no quadro |

#### 1.3.7 Switch PoE protegido

| Medida | Descricao |
|--------|-----------|
| **Junto ao servidor** | Switch PoE no mesmo local escondido que o Mini PC |
| **Alimentado pelo nobreak** | Conectado na saida do UPS |
| **Cabos em conduites** | Cabos Ethernet para cameras em conduites embutidos (dificulta corte) |

---

### 1.4 Protecao contra jamming (A6)

O jamming de sinais sem fio (Zigbee 2.4GHz, Wi-Fi) e um ataque de baixa probabilidade mas alto impacto.

**Mitigacoes:**

| Medida | Descricao | Eficacia |
|--------|-----------|----------|
| **Sensores cabeados em pontos criticos** | Porta principal e pontos de entrada mais provaveis cabeados, nao Zigbee | Alta |
| **Deteccao de jamming** | Monitorar RSSI dos sensores Zigbee; queda subita em todos indica jamming | Media |
| **Redundancia de protocolo** | Sensores Zigbee + cabeados na mesma zona | Alta |
| **Cameras PoE** (ja implementado) | Cameras nao sao afetadas por jamming wireless | Alta |

```yaml
# Deteccao de possivel jamming Zigbee
automation:
  - alias: "Alerta - Possivel jamming Zigbee"
    trigger:
      - platform: numeric_state
        entity_id: sensor.zigbee_coordinator_lqi
        below: 20
        for: "00:02:00"
    action:
      - service: notify.notify
        data:
          title: "ALERTA - Possivel jamming"
          message: "Qualidade do sinal Zigbee degradou severamente. Possivel interferencia."
```

---

## 2. Modos de operacao degradada

### 2.1 Principio

Nenhum sistema e 100% confiavel. A arquitetura deve ser projetada para que, quando um componente falha, o sistema **degrade graciosamente** em vez de falhar completamente. Cada componente deve ter:

1. **Deteccao automatica** da falha
2. **Modo degradado** definido (o que ainda funciona)
3. **Notificacao** ao proprietario
4. **Procedimento de recuperacao** documentado

### 2.2 Tabela de modos degradados por componente

#### 2.2.1 Frigate (NVR) crash

| Aspecto | Detalhe |
|---------|---------|
| **Componente** | Frigate NVR (container Docker / add-on HA) |
| **Funcao** | Gravacao de video, deteccao de objetos por IA, eventos MQTT |
| **O que PARA de funcionar** | Gravacao centralizada, deteccao de pessoas/veiculos/animais, eventos de camera no HA, timeline de eventos, snapshots |
| **O que CONTINUA funcionando** | Home Assistant (automacoes, alarme), Zigbee2MQTT (sensores), MQTT broker, sirenes, notificacoes, cameras continuam transmitindo RTSP (sem gravar no servidor), **edge recording no cartao SD das cameras** |
| **Deteccao** | Monitoramento do container Docker via HA (integration `docker` ou `systemmonitor`); sensor `binary_sensor.frigate_running`; ausencia de eventos MQTT no topico `frigate/events` |
| **Recuperacao automatica** | Docker restart policy: `restart: unless-stopped`; watchdog script que reinicia container se nao responder em 60s; HA automation que notifica se Frigate offline por mais de 2 minutos |
| **Recuperacao manual** | SSH no servidor, `docker restart frigate`; verificar logs `docker logs frigate`; verificar espaco em disco (causa comum); verificar se stream RTSP das cameras esta acessivel |
| **Tempo toleravel offline** | 5 minutos (com edge recording ativo) |

```yaml
# Monitoramento do Frigate
automation:
  - alias: "Watchdog - Frigate offline"
    trigger:
      - platform: state
        entity_id: binary_sensor.frigate_running
        to: "off"
        for: "00:02:00"
    action:
      - service: notify.notify
        data:
          title: "FALHA - Frigate NVR offline"
          message: "Frigate esta offline ha 2 minutos. Cameras gravando apenas em SD local."
      - service: hassio.addon_restart
        data:
          addon: frigate
```

---

#### 2.2.2 Coordenador Zigbee (falha)

| Aspecto | Detalhe |
|---------|---------|
| **Componente** | Dongle Zigbee USB (Sonoff ZBDongle-P / CC2652P) + Zigbee2MQTT |
| **Funcao** | Bridge entre sensores Zigbee e MQTT/HA |
| **O que PARA de funcionar** | Todos os sensores Zigbee (abertura, PIR, temperatura, sirene Zigbee), sistema de alarme Alarmo (sem input de sensores), automacoes baseadas em sensores |
| **O que CONTINUA funcionando** | Frigate (cameras PoE independentes), gravacao de video, deteccao de objetos, Home Assistant (interface, automacoes baseadas em cameras), notificacoes, acesso remoto |
| **Deteccao** | Zigbee2MQTT publica status no topico `zigbee2mqtt/bridge/state`; monitorar se topico para de atualizar; HA sensor `sensor.zigbee2mqtt_bridge_state` |
| **Recuperacao automatica** | Docker restart do container Zigbee2MQTT; script que reseta porta USB (`usbreset`); se dongle USB soltar, `udev` rule para rebind |
| **Recuperacao manual** | Verificar conexao USB (`lsusb`); reiniciar Zigbee2MQTT; em caso de hardware queimado, substituir dongle (manter spare); re-pair de sensores se necessario (raro) |
| **Tempo toleravel offline** | 5 minutos (cameras ainda detectam, porem sem sensores de abertura/movimento) |

> **RECOMENDACAO**: Manter um coordenador Zigbee **sobressalente** (custo ~R$100-150). A falha do dongle USB e rara mas catastrofica para sensores.

---

#### 2.2.3 MQTT Broker (Mosquitto) crash

| Aspecto | Detalhe |
|---------|---------|
| **Componente** | Mosquitto MQTT Broker |
| **Funcao** | Barramento de mensagens entre Frigate, Zigbee2MQTT e Home Assistant |
| **O que PARA de funcionar** | Comunicacao Frigate para HA (eventos de deteccao), comunicacao Zigbee2MQTT para HA (estados de sensores), qualquer integracao MQTT |
| **O que CONTINUA funcionando** | Cameras gravam via RTSP diretamente (Frigate tem o stream, mas nao publica eventos), sensores Zigbee detectam mas nao comunicam ao HA, interface do HA (com dados desatualizados), notificacoes manuais |
| **Deteccao** | HA integration MQTT mostra `unavailable`; monitorar porta 1883 (`tcp_check`); Zigbee2MQTT e Frigate logam erro de conexao MQTT |
| **Recuperacao automatica** | Docker restart policy; systemd watchdog; HA automation baseada em `binary_sensor.mqtt_connected` |
| **Recuperacao manual** | `docker restart mosquitto`; verificar arquivo de configuracao `mosquitto.conf`; verificar permissoes; verificar disco (persistent storage) |
| **Tempo toleravel offline** | 2 minutos (e o barramento central de comunicacao) |

```yaml
automation:
  - alias: "Watchdog - MQTT broker offline"
    trigger:
      - platform: state
        entity_id: binary_sensor.mqtt_connected
        to: "off"
        for: "00:01:00"
    action:
      - service: notify.notify
        data:
          title: "FALHA CRITICA - MQTT Broker offline"
          message: "Mosquitto esta offline. Sensores e cameras nao comunicam com HA."
```

---

#### 2.2.4 Home Assistant crash

| Aspecto | Detalhe |
|---------|---------|
| **Componente** | Home Assistant Core |
| **Funcao** | Orquestracao central: automacoes, alarme (Alarmo), interface, notificacoes |
| **O que PARA de funcionar** | Todas as automacoes, sistema de alarme Alarmo, interface web/app, notificacoes push, integracao com Frigate (dashboard), scripts e cenas |
| **O que CONTINUA funcionando** | Frigate grava video independentemente (RTSP direto das cameras), Zigbee2MQTT continua operando (sensores publicam no MQTT), Mosquitto MQTT continua rodando, cameras com edge recording (SD) |
| **Deteccao** | Monitoramento externo (ping/HTTP check na porta 8123 via cron ou script separado); UptimeKuma ou similar rodando em container separado; app HA Companion mostra "desconectado" |
| **Recuperacao automatica** | Docker restart policy; HAOS watchdog integrado; script cron externo que reinicia o container/servico se nao responder |
| **Recuperacao manual** | SSH: `ha core restart` (HAOS) ou `docker restart homeassistant`; verificar logs: `ha core logs`; causa comum: addon com bug, integracao com erro, disco cheio |
| **Tempo toleravel offline** | 5 minutos (Frigate e sensores continuam operando de forma independente) |

> **NOTA**: Quando o HA esta offline, as sirenes Zigbee NAO serao acionadas automaticamente (pois as automacoes estao no HA). Esta e uma limitacao arquitetural significativa. Mitigacao: considerar automacoes locais no Zigbee2MQTT ou regras MQTT standalone.

---

#### 2.2.5 Queda de internet

| Aspecto | Detalhe |
|---------|---------|
| **Componente** | Conexao de internet fixa (fibra optica) |
| **Funcao** | Acesso remoto, notificacoes push, atualizacoes, NTP |
| **O que PARA de funcionar** | Notificacoes push via internet, acesso remoto (VPN/Tailscale/Nabu Casa), atualizacoes de firmware e software, servicos de DNS externo |
| **O que CONTINUA funcionando** | **Todo o sistema local**: HA, Frigate, Zigbee2MQTT, MQTT, automacoes, sirenes, gravacao, deteccao de objetos. Notificacoes via **4G** (se implementado). Rede local intacta. |
| **Deteccao** | HA sensor `binary_sensor.internet_status` (ping para 8.8.8.8 ou DNS check); monitora latencia e perda de pacotes; Frigate nao depende de internet |
| **Recuperacao automatica** | Failover para 4G (apenas notificacoes); internet fixa geralmente retorna sozinha; roteador com auto-reconnect |
| **Recuperacao manual** | Verificar ONU/ONT da operadora; reiniciar roteador; contatar operadora; verificar cabos fisicos |
| **Tempo toleravel offline** | Indefinido para operacao local; critico apenas se morador esta fora de casa e precisa ser notificado (4G resolve) |

---

#### 2.2.6 Queda de energia

| Aspecto | Detalhe |
|---------|---------|
| **Componente** | Energia eletrica da concessionaria |
| **Funcao** | Alimentacao de todo o sistema |
| **O que PARA de funcionar (sem nobreak)** | TUDO |
| **O que CONTINUA funcionando (com nobreak 1500VA)** | Mini PC (~2h), switch PoE + cameras (~2h), roteador (~2h), sensores Zigbee (bateria propria, meses). **Edge recording no SD continua enquanto camera tiver energia via PoE.** |
| **Deteccao** | Sensor UPS via NUT: `sensor.ups_status` muda para "OB" (On Battery); automacao imediata de alerta |
| **Recuperacao automatica** | Energia retorna: nobreak volta para modo AC, todos os equipamentos ja ligados; Mini PC configurado para auto-power-on no BIOS |
| **Recuperacao manual** | Se nobreak esgotou: ligar equipamentos manualmente; verificar se HA iniciou corretamente; verificar se Frigate reconectou nas cameras; verificar estado dos sensores Zigbee |
| **Tempo toleravel offline** | Ate esgotar nobreak (~2h com 1500VA). Apos isso, sistema completamente offline ate retorno da energia. |

**Automacao de shutdown gracioso:**

```yaml
automation:
  - alias: "UPS - Shutdown gracioso com bateria baixa"
    trigger:
      - platform: numeric_state
        entity_id: sensor.ups_battery_charge
        below: 20
    condition:
      - condition: state
        entity_id: sensor.ups_status
        state: "OB"
    action:
      - service: notify.notify
        data:
          title: "CRITICO - Bateria UPS abaixo de 20%"
          message: "Sistema sera desligado em 5 minutos para proteger o hardware."
      - delay: "00:05:00"
      - service: hassio.host_shutdown
```

---

#### 2.2.7 Falha de HDD/SSD (gravacoes)

| Aspecto | Detalhe |
|---------|---------|
| **Componente** | HDD ou SSD de gravacoes (disco secundario do NVR) |
| **Funcao** | Armazenamento de gravacoes do Frigate |
| **O que PARA de funcionar** | Gravacoes novas do Frigate (disco cheio ou falha de I/O), historico de eventos, exportacao de evidencias |
| **O que CONTINUA funcionando** | Sistema operacional (no SSD principal), HA, automacoes, deteccao em tempo real (Frigate processa mas nao grava), sensores, sirenes, notificacoes, **edge recording no SD das cameras** |
| **Deteccao** | S.M.A.R.T. monitoring com alertas (ver secao 3.3); monitorar espaco livre em disco; Frigate loga erro de gravacao; HA sensor `sensor.disk_use_percent` |
| **Recuperacao automatica** | Frigate com rotacao FIFO: apaga gravacoes antigas para liberar espaco; se disco falhou: nao ha recuperacao automatica |
| **Recuperacao manual** | Substituir disco; restaurar configuracao do Frigate; gravacoes antigas perdidas (a menos que haja backup); camera SD pode preencher lacuna |
| **Tempo toleravel offline** | Horas a dias (cameras SD fazem fallback), porem sem deteccao IA nas gravacoes |

---

#### 2.2.8 Camera individual offline

| Aspecto | Detalhe |
|---------|---------|
| **Componente** | Camera IP individual (PoE) |
| **Funcao** | Monitoramento visual de uma zona especifica |
| **O que PARA de funcionar** | Visao daquela zona especifica; deteccao de objetos naquela area; gravacao daquele angulo |
| **O que CONTINUA funcionando** | Todas as demais cameras, todos os sensores, automacoes, alarme, Frigate (demais cameras), sistema completo exceto a zona cega |
| **Deteccao** | Frigate reporta camera offline via MQTT; HA sensor `binary_sensor.camera_X_connected`; ping check no IP da camera; alerta se offline por mais de 2 minutos |
| **Recuperacao automatica** | Frigate tenta reconectar automaticamente ao stream RTSP; porta PoE pode ser reiniciada via switch gerenciavel (power cycle) |
| **Recuperacao manual** | Verificar cabo de rede; reiniciar porta PoE no switch; acessar camera via IP (ONVIF/web); verificar se camera nao foi destruida fisicamente |
| **Tempo toleravel offline** | Depende da zona: camera de entrada = 0 minutos (critica); camera lateral = horas (menos critica) |

```yaml
automation:
  - alias: "Alerta - Camera offline"
    trigger:
      - platform: state
        entity_id:
          - binary_sensor.camera_entrada
          - binary_sensor.camera_fundos
          - binary_sensor.camera_lateral
          - binary_sensor.camera_garagem
        to: "unavailable"
        for: "00:02:00"
    action:
      - service: notify.notify
        data:
          title: "ALERTA - Camera offline"
          message: "Camera {{ trigger.to_state.name }} esta offline ha 2 minutos. Verificar possivel sabotagem."
```

---

#### 2.2.9 Sensor individual offline

| Aspecto | Detalhe |
|---------|---------|
| **Componente** | Sensor Zigbee individual (abertura, PIR, etc.) |
| **Funcao** | Deteccao em uma zona especifica |
| **O que PARA de funcionar** | Deteccao naquela zona especifica; se sensor de zona de entrada, Alarmo pode nao disparar |
| **O que CONTINUA funcionando** | Todos os demais sensores, cameras (IA faz deteccao visual), automacoes baseadas em outros sensores, sistema de alarme (com cobertura parcial) |
| **Deteccao** | Zigbee2MQTT reporta `availability: false`; HA mostra entidade como `unavailable`; monitoramento de bateria (causa #1 de offline) |
| **Recuperacao automatica** | Sensor pode reconectar automaticamente ao mesh Zigbee; se bateria acabou, nao ha recuperacao sem troca |
| **Recuperacao manual** | Trocar bateria (CR2032 ou CR2450); re-pair se necessario; verificar alcance do mesh Zigbee (pode precisar de repetidor) |
| **Tempo toleravel offline** | Horas (cameras cobrem parcialmente), porem alarme fica com cobertura reduzida |

> **RECOMENDACAO**: Configurar alerta de bateria baixa (< 20%) para todos os sensores Zigbee, com antecedencia de semanas antes da falha.

---

#### 2.2.10 Switch PoE falha

| Aspecto | Detalhe |
|---------|---------|
| **Componente** | Switch PoE (8 portas) |
| **Funcao** | Alimentacao e conectividade de rede para todas as cameras |
| **O que PARA de funcionar** | **TODAS as cameras simultaneamente** (sem video, sem deteccao IA, sem gravacao NVR); se switch tambem conecta o servidor a rede, toda a rede interna pode cair |
| **O que CONTINUA funcionando** | Sensores Zigbee (comunicacao wireless via dongle USB), sirenes Zigbee, Home Assistant (se conectado ao roteador por outra via), automacoes baseadas em sensores, **mas SEM video** |
| **Deteccao** | Todas as cameras ficam offline simultaneamente (Frigate loga); ping no IP do switch falha; HA detecta multiplas cameras `unavailable` ao mesmo tempo |
| **Recuperacao automatica** | Se falha temporaria: switch reinicia sozinho. Nao ha bypass automatico. |
| **Recuperacao manual** | Reiniciar switch (power cycle); verificar se nobreak alimenta o switch; verificar se switch nao queimou; **manter switch PoE sobressalente** ou switch simples + injetores PoE individuais como workaround |
| **Tempo toleravel offline** | 0 minutos (perda total de video e um cenario critico) |

> **RECOMENDACAO**: O switch PoE e um ponto unico de falha para todo o subsistema de video. Considerar manter um switch de reserva ou, no minimo, injetores PoE individuais para cameras criticas (entrada, portao).

---

### 2.3 Tabela resumo de modos degradados

| Componente falho | Severidade | Video funciona? | Sensores funcionam? | Alarme funciona? | Notificacoes funcionam? | Tempo max. toleravel |
|-----------------|------------|-----------------|---------------------|-------------------|-------------------------|---------------------|
| Frigate (NVR) | Alta | Parcial (SD) | Sim | Sim | Sim | 5 min |
| Coordenador Zigbee | Alta | Sim | **NAO** | **NAO** | Sim | 5 min |
| MQTT Broker | Critica | Parcial (grava, nao notifica) | Parcial (detecta, nao comunica) | **NAO** | Parcial | 2 min |
| Home Assistant | Critica | Sim (Frigate independente) | Parcial (Zigbee2MQTT opera) | **NAO** | **NAO** | 5 min |
| Internet | Baixa* | Sim | Sim | Sim | Via 4G | Indefinido |
| Energia (com UPS) | Critica | Sim (~2h) | Sim | Sim | Sim | ~2h |
| Energia (sem UPS) | Catastrofica | **NAO** | Parcial (bateria) | **NAO** | **NAO** | 0 min |
| HDD/SSD gravacoes | Media | Parcial (SD) | Sim | Sim | Sim | Horas |
| Camera individual | Baixa-Media | Parcial (outras cameras) | Sim | Sim | Sim | Varia |
| Sensor individual | Baixa | Sim | Parcial (outros sensores) | Parcial | Sim | Horas |
| Switch PoE | Critica | **NAO** | Sim | Parcial | Sim | 0 min |

*Severidade da queda de internet e baixa SE o 4G estiver implementado. Sem 4G, a severidade e alta quando o morador esta fora de casa.

### 2.4 Diagrama de dependencias entre componentes

```
                    ┌────────────┐
                    │  ENERGIA   │
                    │ (concession│
                    │   aria)    │
                    └─────┬──────┘
                          │
                    ┌─────▼──────┐
                    │  NOBREAK   │
                    │  (1500VA)  │
                    └─────┬──────┘
                          │
          ┌───────────────┼───────────────┐
          │               │               │
    ┌─────▼──────┐  ┌─────▼──────┐  ┌─────▼──────┐
    │  MINI PC   │  │ SWITCH PoE │  │  ROTEADOR  │
    │   N100     │  │  8 portas  │  │  + 4G      │
    └─────┬──────┘  └─────┬──────┘  └─────┬──────┘
          │               │               │
    ┌─────┼───────┐       │          ┌────┴─────┐
    │     │       │       │          │ INTERNET │
    │     │       │  ┌────▼─────┐   │  (fibra  │
    │     │       │  │ CAMERAS  │   │   + 4G)  │
    │     │       │  │ (PoE)    │   └──────────┘
    │     │       │  └──────────┘
    │     │       │
┌───▼──┐ │  ┌────▼──────┐
│MOSQU-│ │  │ZIGBEE2MQTT│
│ITTO  │ │  │ + Dongle  │
│(MQTT)│ │  └────┬──────┘
└───┬──┘ │       │
    │    │  ┌────▼──────┐
    │    │  │ SENSORES  │
    │    │  │ (Zigbee)  │
    │    │  └───────────┘
    │    │
┌───▼────▼──┐
│   HOME    │
│ ASSISTANT │
│ + Alarmo  │
└─────┬─────┘
      │
┌─────▼──────┐
│  FRIGATE   │
│  (NVR+IA)  │
└─────┬──────┘
      │
┌─────▼──────┐
│  HDD/SSD   │
│ (gravacoes)│
└────────────┘
```

**Pontos unicos de falha identificados:**

1. **Nobreak** -- se o nobreak falha, tudo desliga
2. **Mini PC N100** -- roda todos os servicos de software
3. **Switch PoE** -- alimenta e conecta todas as cameras
4. **Dongle Zigbee USB** -- unico ponto de comunicacao com sensores
5. **MQTT Broker** -- barramento central de mensagens

---

## 3. Estrategia de backup do NVR

### 3.1 Edge recording (cameras com cartao SD)

O edge recording e a **primeira e mais importante camada de backup** porque funciona de forma completamente independente do servidor.

| Aspecto | Configuracao recomendada |
|---------|--------------------------|
| **Capacidade do cartao** | 64GB minimo, 128GB recomendado por camera |
| **Tipo de cartao** | microSD de alta durabilidade (High Endurance) -- ex: Samsung PRO Endurance, SanDisk High Endurance |
| **Modo de gravacao** | Continua (loop/FIFO) -- quando cheio, sobrescreve mais antigo |
| **Resolucao no SD** | Sub-stream (720p ou 1080p) para maximizar retencao |
| **Retencao estimada** | 64GB a 720p continuo: ~5-7 dias; 128GB a 720p continuo: ~10-14 dias |
| **Ativacao** | **Sempre ligado**, independente do estado do Frigate |

**Cartoes recomendados:**

| Modelo | Capacidade | Durabilidade | Preco estimado |
|--------|------------|-------------|----------------|
| Samsung PRO Endurance | 128GB | 140.160 horas | R$80-120 |
| SanDisk High Endurance | 128GB | 20.000 horas | R$70-100 |
| Kingston High Endurance | 128GB | - | R$60-90 |

> **ATENCAO**: Cartoes SD comuns (nao High Endurance) falham rapidamente com gravacao continua. Usar apenas cartoes classificados para videovigilancia.

### 3.2 Opcoes de RAID para o Mini PC

O Mini PC N100 geralmente tem 1 slot M.2 NVMe (sistema) e possibilidade de conectar HDD/SSD via USB 3.0 ou SATA (se houver).

| Configuracao | Descricao | Protecao | Custo adicional | Recomendacao |
|-------------|-----------|----------|-----------------|--------------|
| **Disco unico** | 1x SSD 1-2TB | Nenhuma | R$0 | Minimo aceitavel (com SD nas cameras) |
| **Disco unico + backup USB** | 1x SSD + 1x HDD USB externo | Backup periodico | R$200-400 | Boa relacao custo-beneficio |
| **RAID 1 via software (mdadm)** | 2x HDD/SSD espelhados | Tolerancia a falha de 1 disco | R$300-600 | Ideal se Mini PC tem 2 conexoes SATA/USB |
| **RAID 1 via case externo** | Case USB com 2 HDDs em RAID 1 | Tolerancia a falha de 1 disco | R$400-800 | Alternativa se Mini PC so tem USB |

**Configuracao recomendada por cenario:**

| Cenario | Armazenamento sistema | Armazenamento NVR | Backup |
|---------|----------------------|-------------------|--------|
| **Apartamento** | SSD 256GB (M.2) | Mesmo SSD (particao) | SD cameras |
| **Casa urbana** | SSD 256GB (M.2) | HDD 2TB (USB/SATA) | SD cameras + HDD USB mensal |
| **Rural** | SSD 256GB (M.2) | 2x HDD 2TB RAID 1 | SD cameras + RAID |

### 3.3 Monitoramento S.M.A.R.T. com alertas

S.M.A.R.T. (Self-Monitoring, Analysis and Reporting Technology) permite prever falhas de disco antes que ocorram.

**Implementacao:**

```bash
# Instalar smartmontools
sudo apt install smartmontools

# Verificar status S.M.A.R.T. do disco
sudo smartctl -a /dev/sda

# Habilitar verificacao periodica
sudo systemctl enable smartd
```

**Configuracao do smartd (/etc/smartd.conf):**

```
# Verificar todos os discos a cada 12 horas
# Alertar via script quando detectar problema
/dev/sda -a -o on -S on -s (S/../.././02|L/../../6/03) -m root -M exec /usr/local/bin/smartd_alert.sh
/dev/sdb -a -o on -S on -s (S/../.././02|L/../../6/03) -m root -M exec /usr/local/bin/smartd_alert.sh
```

**Integracao com Home Assistant:**

```yaml
# Monitorar saude do disco via sensor de linha de comando
sensor:
  - platform: command_line
    name: "Disco NVR saude"
    command: "smartctl -H /dev/sda | grep -i 'result' | awk '{print $NF}'"
    scan_interval: 3600  # Verificar a cada hora

  - platform: command_line
    name: "Disco NVR temperatura"
    command: "smartctl -A /dev/sda | grep Temperature_Celsius | awk '{print $10}'"
    unit_of_measurement: "C"
    scan_interval: 300

automation:
  - alias: "Alerta - Disco NVR com problemas"
    trigger:
      - platform: state
        entity_id: sensor.disco_nvr_saude
        to: "FAILED"
    action:
      - service: notify.notify
        data:
          title: "CRITICO - Disco NVR com falha iminente"
          message: "S.M.A.R.T. reportou falha no disco de gravacoes. SUBSTITUIR IMEDIATAMENTE."

  - alias: "Alerta - Disco NVR temperatura alta"
    trigger:
      - platform: numeric_state
        entity_id: sensor.disco_nvr_temperatura
        above: 55
    action:
      - service: notify.notify
        data:
          title: "ALERTA - Disco NVR superaquecendo"
          message: "Temperatura do disco de gravacoes: {{ states('sensor.disco_nvr_temperatura') }}C. Verificar ventilacao."
```

**Atributos S.M.A.R.T. criticos para monitorar:**

| Atributo | ID | O que indica | Limiar de alerta |
|----------|----|-------------|-----------------|
| Reallocated Sector Count | 5 | Setores defeituosos remapeados | > 0 (qualquer valor) |
| Current Pending Sector | 197 | Setores aguardando remapeamento | > 0 |
| Offline Uncorrectable | 198 | Setores irrecuperaveis | > 0 |
| Temperature Celsius | 194 | Temperatura do disco | > 55C |
| Power-On Hours | 9 | Horas de uso | > 35.000h (HDD) |
| Spin Retry Count | 10 | Tentativas de spin-up | > 0 |

### 3.4 Rotina de backup para gravacoes de incidentes

As gravacoes normais sao rotacionadas automaticamente pelo Frigate (FIFO, 30 dias). Porem, gravacoes de **incidentes** (alarmes, deteccoes de intrusos) devem ser preservadas.

**Estrategia em 3 niveis:**

| Nivel | Tipo | Destino | Frequencia | Retencao |
|-------|------|---------|-----------|----------|
| **1** | Edge recording (SD) | Cartao SD na camera | Continua | 5-14 dias (loop) |
| **2** | Gravacao Frigate | HDD/SSD local | Continua | 30 dias (normal), 60 dias (eventos) |
| **3** | Backup de incidentes | HDD USB externo ou NAS | Diario (apenas incidentes) | 1 ano |

**Script de backup de incidentes:**

```bash
#!/bin/bash
# backup_incidentes.sh
# Copia gravacoes marcadas como incidentes para disco de backup

FRIGATE_MEDIA="/media/frigate/recordings"
BACKUP_DEST="/mnt/backup_usb/incidentes"
DATE=$(date +%Y-%m-%d)
LOG="/var/log/backup_incidentes.log"

echo "[$(date)] Iniciando backup de incidentes..." >> $LOG

# Copiar eventos marcados como retidos (retain: true) nas ultimas 24h
# Frigate armazena eventos em /media/frigate/clips/
rsync -av --progress \
  "$FRIGATE_MEDIA/../clips/" \
  "$BACKUP_DEST/$DATE/" \
  >> $LOG 2>&1

# Verificar espaco no disco de backup
USAGE=$(df -h "$BACKUP_DEST" | tail -1 | awk '{print $5}' | tr -d '%')
if [ "$USAGE" -gt 90 ]; then
    echo "[$(date)] ALERTA: Disco de backup com ${USAGE}% de uso!" >> $LOG
    # Aqui poderia chamar uma API para notificar via HA
fi

echo "[$(date)] Backup concluido." >> $LOG
```

**Crontab:**

```cron
# Backup diario de incidentes as 3h da manha
0 3 * * * /usr/local/bin/backup_incidentes.sh
```

### 3.5 Recomendacoes de local fisico para o servidor

Complementando a secao 1.3.4, as recomendacoes detalhadas para cada cenario:

**Cenario rural:**

| Local sugerido | Vantagens | Cuidados |
|----------------|-----------|----------|
| Comodo interno sem janela (dispensa, closet) | Nao visivel, protegido | Ventilacao, umidade |
| Forro da casa (se acessivel e ventilado) | Muito discreto | Calor excessivo no verao, acesso dificil |
| Armario embutido com chave | Discreto, protegido | Ventilacao adequada |

**Cenario casa urbana:**

| Local sugerido | Vantagens | Cuidados |
|----------------|-----------|----------|
| Armario embutido no corredor | Discreto, acessivel | Furar para ventilacao/cabos |
| Sob escada (se houver) | Espaco subutilizado | Umidade, ventilacao |
| Soto/porao | Muito escondido | Umidade alta, pode inundar |
| Quarto de servico/lavanderia | Pouco frequentado por visitantes | Umidade de roupas |

**Cenario apartamento:**

| Local sugerido | Vantagens | Cuidados |
|----------------|-----------|----------|
| Armario de rede/telecom (se houver) | Projetado para isso | Verificar ventilacao |
| Atras de movel fixo | Muito discreto | Acesso para manutencao |
| Dentro de armario com porta | Protegido, discreto | Circulacao de ar |

**Regras gerais para todos os cenarios:**

1. **Nunca** colocar o servidor proximo a janelas ou areas acessiveis do exterior
2. **Nunca** deixar LEDs indicadores visiveis de fora da casa
3. **Sempre** fixar fisicamente (parafusos, braket VESA)
4. **Sempre** garantir ventilacao minima (Mini PC N100 gera ~15W de calor)
5. **Sempre** manter junto ao nobreak (cabos curtos = menos pontos de falha)
6. **Evitar** locais com risco de inundacao (banheiros, areas externas)
7. **Evitar** locais com temperatura acima de 40C no verao

---

## 4. Regras derivadas

As regras abaixo complementam as regras existentes em `rules/RULES_COMPLIANCE_AND_STANDARDS.md` e devem ser referenciadas nos PRDs e documentos tecnicos.

```
REGRA-RESIL-01: O sistema DEVE possuir conectividade 4G/LTE como canal
redundante de notificacao. Nao e opcional.

REGRA-RESIL-02: O sistema DEVE possuir nobreak (UPS) com autonomia minima
de 1 hora para servidor, switch PoE e roteador. Recomendado: 2 horas
(1500VA).

REGRA-RESIL-03: Todas as cameras externas DEVEM ter cartao microSD High
Endurance com edge recording ativo permanentemente, independente do estado
do NVR.

REGRA-RESIL-04: O servidor central (Mini PC) DEVE ser instalado em local
nao obvio, fixado fisicamente na parede ou movel, sem LEDs visiveis do
exterior.

REGRA-RESIL-05: A deteccao simultanea de queda de energia e queda de
internet DEVE disparar alarme de nivel maximo via 4G, sirenes e
iluminacao, tratando como possivel ataque coordenado.

REGRA-RESIL-06: O switch PoE DEVE ser alimentado pelo nobreak e instalado
junto ao servidor, com cabos em conduites embutidos.

REGRA-RESIL-07: DEVE ser mantido estoque de componentes criticos
sobressalentes: 1 coordenador Zigbee USB, 2 cartoes SD High Endurance,
1 fonte PoE de emergencia (injetor individual).

REGRA-RESIL-08: Os discos de armazenamento (HDD/SSD) DEVEM ser
monitorados via S.M.A.R.T. com alertas automaticos para atributos
criticos (Reallocated Sectors, Pending Sectors, temperatura).
```

---

## 5. Referencias

### Documentos internos do projeto

- `docs/ARQUITETURA_TECNICA.md` -- Arquitetura tecnica completa (HA, Frigate, Zigbee, Mini PC N100, VLANs)
- `docs/ARQUITETURA_SEGURANCA_FISICA.md` -- Seguranca fisica, zonas de protecao, posicionamento de cameras
- `rules/RULES_COMPLIANCE_AND_STANDARDS.md` -- Regras de compliance (REGRA-CFTV, REGRA-IOT, REGRA-NOBREAK, etc.)
- `prd/PRD_VIDEO_SURVEILLANCE_AND_NVR.md` -- PRD do sistema de videovigilancia
- `prd/PRD_SENSORS_AND_ALARMS_PLATFORM.md` -- PRD da plataforma de sensores e alarmes

### Referencias externas

- [Frigate NVR - Recording Configuration](https://docs.frigate.video/configuration/record/)
- [Home Assistant - UPS Integration (NUT)](https://www.home-assistant.io/integrations/nut/)
- [Zigbee2MQTT - Availability](https://www.zigbee2mqtt.io/guide/configuration/devices-groups.html#common-device-options)
- [smartmontools - S.M.A.R.T. Monitoring](https://www.smartmontools.org/)
- [Samsung PRO Endurance - Especificacoes](https://semiconductor.samsung.com/consumer-storage/memory-cards/)
- [Network UPS Tools (NUT)](https://networkupstools.org/)
- [Home Assistant - System Monitor](https://www.home-assistant.io/integrations/systemmonitor/)
- [Linux mdadm RAID](https://raid.wiki.kernel.org/index.php/Linux_Raid)

---

> **Data de criacao**: 2026-02-12 (revisao do projeto)
>
> **Regras derivadas**: REGRA-RESIL-01 a REGRA-RESIL-08
>
> **Proximos passos**: Integrar as regras REGRA-RESIL-* ao documento `rules/RULES_COMPLIANCE_AND_STANDARDS.md` e referenciar nos PRDs relevantes (PRD_VIDEO_SURVEILLANCE_AND_NVR, PRD_SENSORS_AND_ALARMS_PLATFORM).
