# Resiliência e Modos Degradados

Este documento descreve como o sistema Home Security DIY se comporta quando componentes falham ou são sabotados, e as medidas obrigatórias para garantir operação contínua.

---

## 1. Cenários de Ataque Físico ao Sistema

| # | Cenário | Probabilidade | Impacto | Sofisticação |
|---|---------|---------------|---------|--------------|
| A1 | Corte de energia na rua (disjuntor externo) | Alta | Crítico | Baixa |
| A2 | Corte de cabo de internet/fibra na caixa externa | Alta | Alto | Baixa |
| A3 | Destruição/roubo do servidor (Mini PC) | Média | Crítico | Média |
| A4 | Destruição de câmeras acessíveis (pedra, spray, cabo) | Alta | Alto | Baixa |
| A5 | Sabotagem do quadro elétrico | Média | Crítico | Baixa |
| A6 | Jamming de sinal Zigbee/Wi-Fi | Baixa | Alto | Alta |
| A7 | Corte de energia + internet simultâneos (ataque coordenado) | Média | Crítico | Média |
| A8 | Destruição do switch PoE | Baixa | Alto | Média |

> **A7** é o indicador mais forte de ataque deliberado. Deve ser tratado com prioridade máxima.

### Matriz de resposta por combinação de falhas

| Energia | Internet | Classificação | Ação automática |
|---------|----------|---------------|-----------------|
| OK | Offline | Falha simples | Notificar, ativar 4G, monitorar |
| Offline | OK | Falha simples | Notificar, monitorar autonomia do nobreak |
| **Offline** | **Offline** | **Ataque coordenado** | **Alerta máximo via 4G, sirenes, luzes, gravar tudo** |
| OK | OK | Normal | Operação padrão |

---

## 2. Mitigações Obrigatórias

### 2.1 4G/LTE como canal de notificação redundante

> O 4G **não é opcional**. É obrigatório em todos os cenários (rural, urbano e apartamento).

| Aspecto | Especificação |
|---------|---------------|
| Função | Canal de notificação quando internet fixa cai |
| Hardware | Roteador com slot SIM ou dongle USB 4G no Mini PC |
| Custo estimado | R$ 30–50/mês (dados) + R$ 100–300 (modem) |
| Uso | Apenas notificações críticas (push, SMS, Telegram) — **não** streaming de vídeo |
| Configuração | Failover automático: internet fixa primária, 4G secundária |

### 2.2 Nobreak dimensionado (UPS)

**Carga estimada do sistema:**

| Equipamento | Consumo típico | Essencial? |
|-------------|----------------|------------|
| Mini PC N100 | 10–25 W | Sim |
| Switch PoE 8 portas (com câmeras) | 40–60 W | Sim |
| Roteador/modem | 8–12 W | Sim |
| Modem 4G (se separado) | 5–8 W | Sim |
| **Total estimado** | **~65–95 W** | — |

**Dimensionamento:**

| Nobreak | Autonomia estimada (80 W) | Preço estimado |
|---------|--------------------------|----------------|
| 600 VA / 300 W | ~45 min | R$ 300–400 |
| 1000 VA / 500 W | ~1h15 | R$ 400–600 |
| **1500 VA / 900 W** | **~2 h** | **R$ 500–800** |
| 2200 VA / 1200 W | ~3 h | R$ 800–1.200 |

> **Recomendação**: **1500 VA** como mínimo. Proporciona ~2 horas de autonomia, tempo suficiente para o morador ser notificado via 4G e tomar providências.

**Requisitos do nobreak:**
- Saída senoidal pura ou senoidal simulada de qualidade (evitar onda quadrada)
- Auto-ligamento quando energia retorna
- Porta USB/serial para monitoramento via NUT no Home Assistant

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
          title: "CRÍTICO - Bateria UPS abaixo de 20%"
          message: "Sistema será desligado em 5 minutos para proteger o hardware."
      - delay: "00:05:00"
      - service: hassio.host_shutdown
```

### 2.3 Câmeras com edge recording (cartão SD)

| Aspecto | Configuração recomendada |
|---------|--------------------------|
| Capacidade | 64 GB mínimo, **128 GB recomendado** por câmera |
| Tipo de cartão | microSD High Endurance (Samsung PRO Endurance, SanDisk High Endurance) |
| Modo | Gravação contínua em loop/FIFO |
| Resolução no SD | Sub-stream (720p ou 1080p) para maximizar retenção |
| Retenção estimada | 64 GB a 720p contínuo: ~5–7 dias; 128 GB: ~10–14 dias |
| Quando ativar | **Sempre**, independente do Frigate estar funcionando |

> Cartões SD comuns falham rapidamente com gravação contínua. Use apenas cartões classificados para videovigilância.

### 2.4 Servidor em local escondido e fixado

| Prática | Descrição |
|---------|-----------|
| Local não óbvio | Evitar escritório, rack visível ou embaixo da TV |
| Locais sugeridos | Forro/sótão, armário embutido, nicho na parede com porta, compartimento sob escada |
| Fixação | Parafusado na parede ou prateleira |
| Identificação | Sem etiquetas ou LEDs visíveis do exterior |
| Nobreak junto | No mesmo local ou próximo, cabos organizados |
| Acesso à rede | Cabo Ethernet — não usar Wi-Fi para o servidor |

### 2.5 Alarme de ataque coordenado

```yaml
automation:
  - alias: "CRÍTICO - Possível ataque coordenado"
    trigger:
      - platform: state
        entity_id: sensor.ups_status
        to: "OB"
    condition:
      - condition: state
        entity_id: binary_sensor.internet_status
        state: "off"
    action:
      - service: notify.telegram_via_4g
        data:
          title: "ALERTA MÁXIMO - POSSÍVEL ATAQUE"
          message: >
            Energia E internet cortadas simultaneamente.
            Possível ataque coordenado em andamento.
            Horário: {{ now().strftime('%H:%M:%S') }}
      - service: siren.turn_on
        target:
          entity_id: all
      - service: light.turn_on
        target:
          entity_id: group.luzes_externas
        data:
          brightness: 255
```

### 2.6 Proteção do quadro elétrico e switch PoE

| Medida | Descrição |
|--------|-----------|
| Cadeado no quadro | Fechadura ou cadeado no quadro de distribuição |
| Quadro em área interna | Se possível, manter dentro da casa |
| Sensor de abertura no quadro | Zigbee detecta abertura não autorizada |
| Switch PoE junto ao servidor | No local escondido, alimentado pelo nobreak |
| Cabos em conduítes | Ethernet para câmeras em conduítes embutidos (dificulta corte) |

---

## 3. Modos de Operação Degradada

### Tabela resumo

| Componente falho | Severidade | Vídeo? | Sensores? | Alarme? | Notificações? | Tempo máx. tolerável |
|-----------------|------------|--------|-----------|---------|---------------|---------------------|
| Frigate (NVR) | Alta | Parcial (SD) | Sim | Sim | Sim | 5 min |
| Coordenador Zigbee | Alta | Sim | **NÃO** | **NÃO** | Sim | 5 min |
| MQTT Broker | Crítica | Parcial | Parcial | **NÃO** | Parcial | 2 min |
| Home Assistant | Crítica | Sim (Frigate independente) | Parcial | **NÃO** | **NÃO** | 5 min |
| Internet | Baixa* | Sim | Sim | Sim | Via 4G | Indefinido |
| Energia (com UPS) | Crítica | Sim (~2 h) | Sim | Sim | Sim | ~2 h |
| Energia (sem UPS) | Catastrófica | **NÃO** | Parcial (bateria) | **NÃO** | **NÃO** | 0 min |
| HDD/SSD gravações | Média | Parcial (SD) | Sim | Sim | Sim | Horas |
| Câmera individual | Baixa–Média | Parcial (outras câmeras) | Sim | Sim | Sim | Varia |
| Sensor individual | Baixa | Sim | Parcial | Parcial | Sim | Horas |
| Switch PoE | Crítica | **NÃO** | Sim | Parcial | Sim | 0 min |

*Severidade da queda de internet é baixa **se** o 4G estiver implementado.

### Pontos únicos de falha

1. **Nobreak** — se falha, tudo desliga
2. **Mini PC N100** — roda todos os serviços de software
3. **Switch PoE** — alimenta e conecta todas as câmeras
4. **Dongle Zigbee USB** — único ponto de comunicação com sensores
5. **MQTT Broker** — barramento central de mensagens

### Frigate (NVR) offline

**O que para:** Gravação centralizada, detecção por IA, snapshots, eventos MQTT.
**O que continua:** HA, alarme, sensores Zigbee, notificações, **edge recording no SD das câmeras**.
**Recuperação automática:** `restart: unless-stopped` no Docker + watchdog.

```yaml
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
          message: "Câmeras gravando apenas em SD local."
      - service: hassio.addon_restart
        data:
          addon: frigate
```

### Home Assistant offline

**O que para:** Todas as automações, alarme Alarmo, interface, notificações push.
**O que continua:** Frigate grava RTSP diretamente, Zigbee2MQTT opera, Mosquitto MQTT opera, câmeras com SD.
> **Limitação crítica**: quando o HA está offline, sirenes Zigbee **não** são acionadas automaticamente.

### Switch PoE falha

**O que para:** **Todas as câmeras** simultâneas — sem vídeo, sem gravação NVR.
**O que continua:** Sensores Zigbee, automações baseadas em sensores.
> Considerar manter switch de reserva ou injetores PoE individuais para câmeras críticas (entrada, portão).

### Câmera individual offline

```yaml
automation:
  - alias: "Alerta - Câmera offline"
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
          title: "ALERTA - Câmera offline"
          message: "{{ trigger.to_state.name }} está offline há 2 min. Verificar sabotagem."
```

---

## 4. Estratégia de Backup do NVR

### 4.1 Edge recording (câmeras com SD) — primeira camada

O edge recording é a camada mais importante porque funciona **independente do servidor**.

| Aspecto | Configuração recomendada |
|---------|--------------------------|
| Cartão | Samsung PRO Endurance ou SanDisk High Endurance |
| Capacidade | 128 GB por câmera |
| Modo | Contínuo em loop (FIFO) |
| Resolução | Sub-stream (720p) para maximizar retenção |
| Ativação | **Sempre ligado**, mesmo com Frigate funcionando normalmente |

### 4.2 Armazenamento por cenário

| Cenário | Sistema | NVR | Backup |
|---------|---------|-----|--------|
| Apartamento | SSD 256 GB (M.2) | Mesmo SSD (partição) | SD câmeras |
| Casa urbana | SSD 256 GB (M.2) | HDD 2 TB (USB/SATA) | SD + HDD USB mensal |
| Rural | SSD 256 GB (M.2) | 2× HDD 2 TB RAID 1 | SD + RAID |

### 4.3 Monitoramento S.M.A.R.T. com alertas

```bash
# Instalar e habilitar
sudo apt install smartmontools
sudo systemctl enable smartd

# Verificar status
sudo smartctl -a /dev/sda
```

```yaml
# Integração com Home Assistant
sensor:
  - platform: command_line
    name: "Disco NVR saúde"
    command: "smartctl -H /dev/sda | grep -i 'result' | awk '{print $NF}'"
    scan_interval: 3600

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
          title: "CRÍTICO - Disco NVR com falha iminente"
          message: "S.M.A.R.T. reportou falha. SUBSTITUIR IMEDIATAMENTE."
```

---

## 5. Hardening Anti-Tamper do Servidor

### 5.1 Criptografia de disco (LUKS)

A medida mais eficaz contra roubo de dados e alteração offline:

1. Ao instalar Linux (Debian/Ubuntu Server), selecione **"Guided - use entire disk and set up encrypted LVM"**
2. Escolha uma passphrase forte

**Unlock remoto via Dropbear SSH** (para servidores headless):

```bash
sudo apt install dropbear-initramfs
# Adicionar chave pública em /etc/dropbear-initramfs/authorized_keys
sudo update-initramfs -u

# No boot, conectar e desbloquear:
ssh -i id_rsa root@IP_DO_SERVER
# digitar: cryptroot-unlock
```

### 5.2 Proteção de BIOS/UEFI

1. **Senha de BIOS**: impede alteração da ordem de boot
2. **Secure Boot**: impede execução de bootloaders não assinados
3. **Desativar boot USB**: remove USB/CD da ordem de boot

### 5.3 Backup off-site automatizado

```bash
# Sincroniza clipes Frigate a cada 10 minutos para bucket S3/B2 criptografado
*/10 * * * * rclone copy /media/frigate/clips remote:bucket-seguranca --transfers 4
```

---

## 6. Regras Derivadas

```
REGRA-RESIL-01: Nobreak dimensionado para mínimo 2 horas de autonomia para todos
os componentes críticos (servidor, switch PoE, roteador).

REGRA-RESIL-02: Todas as câmeras externas devem ter cartão SD com edge recording
ativo, operando independentemente do NVR.

REGRA-RESIL-03: O sistema deve detectar e alertar queda de energia via 4G em até
1 minuto após o evento.

REGRA-RESIL-04: O sistema deve ter monitoramento de saúde de disco (S.M.A.R.T.)
com alertas configurados.

REGRA-RESIL-05: O servidor deve ser fisicamente fixado e escondido em local não
óbvio da residência.

REGRA-RESIL-06: O sistema deve ter plano de recuperação documentado para falha de
cada componente crítico.
```

---

## Referências

- `docs/RESILIENCIA_E_MODOS_DEGRADADOS.md` — fonte principal
- `docs/HARDENING_ANTI_TAMPER.md` — criptografia e proteção física
- [Network UPS Tools (NUT)](https://www.home-assistant.io/integrations/nut/)
- [Frigate NVR — Storage Documentation](https://docs.frigate.video/configuration/record)
- [Smartmontools](https://www.smartmontools.org/)
- [Segurança e Compliance](Seguranca-e-Compliance) — modelo de ameaças e resposta a incidentes
