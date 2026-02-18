# PRD – Sensores Ambientais

> Sistema de Home Security – Open Source / Open Hardware
>
> Versão: 1.0 | Data: 2026-02-18 | Responsável: Agente_Documentador

---

## 1. Visão geral

- **Nome do produto/funcionalidade**: Sistema de Sensores Ambientais (Fumaça, Gás, Inundação e Qualidade do Ar)
- **Responsável**: Agente_Arquiteto_Tecnico (especificação), Agente_Documentador (documentação)
- **Data**: 2026-02-18
- **PRDs relacionados**: PRD_SENSORS_AND_ALARMS_PLATFORM, PRD_NOTIFICATIONS_AND_ALERTS, PRD_AUTOMATION_AND_SCENES, PRD_MONITORING_DASHBOARD

---

## 2. Problema e oportunidade

### 2.1 Problema

Riscos ambientais domésticos são frequentemente negligenciados em sistemas de segurança:
- **Incêndios residenciais**: Mais de 50% das mortes em incêndios ocorrem à noite, quando moradores dormem
- **Vazamento de gás (GLP)**: Risco de explosão e intoxicação, especialmente em cozinhas
- **Inundações internas**: Vazamentos de encanamento causam danos estruturais e materiais
- **Qualidade do ar**: Concentração de CO (monóxido de carbono) pode ser letal em ambientes fechados
- **Detecção tardia**: Sem sensores, problemas só são percebidos quando já são graves

### 2.2 Oportunidade

Implementar um sistema de sensoriamento ambiental com:
- **Detecção precoce** de fumaça, calor, gás, água e CO
- **Integração com alarme principal** (Alarmo) para resposta coordenada
- **Notificações com prioridade P2** (alta) para riscos ambientais
- **Automações de segurança** (cortar gás, desligar HVAC, acender luzes de emergência)
- **Monitoramento 24/7** independente do estado do alarme (armado/desarmado)

---

## 3. Público-alvo

| Perfil | Necessidades específicas |
|--------|--------------------------|
| **Família com crianças/idosos** | Detecção precoce de fumaça e gás, alertas sonoros altos |
| **Proprietário rural** | Proteção contra incêndio em instalações isoladas |
| **Morador de apartamento** | Detector de gás na cozinha, alerta de vazamento de água |
| **Proprietário de casa** | Cobertura completa: fumaça + gás + inundação |
| **Ausente frequente** | Notificação remota de eventos ambientais |

---

## 4. Requisitos funcionais

### 4.1 Detecção de fumaça e incêndio

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-001 | Sensor de fumaça fotoelétrico | Detecta fumaça visível, menos falsos positivos | Alta |
| RF-002 | Sensor de calor (temperatura) | Alerta a 57°C ou variação rápida > 8°C/min | Média |
| RF-003 | Alarme sonoro local (85dB+) | Integrado ao sensor, funciona mesmo offline | Alta |
| RF-004 | Notificação via Home Assistant | Push + Telegram com prioridade P2 | Alta |
| RF-005 | Automação: desligar HVAC | Evitar propagação de fumaça pelo sistema de ar | Alta |
| RF-006 | Automação: acender todas as luzes | Facilitar evacuação | Alta |
| RF-007 | Posicionamento: mínimo 1 por pavimento | Cozinha, corredor, quartos | Alta |
| RF-008 | Monitoramento 24h | Ativo independente do estado do alarme | Alta |

### 4.2 Detecção de vazamento de gás (GLP/GN)

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-009 | Sensor de gás combustível (GLP/metano) | Detecção a partir de 10% do LEL (Lower Explosive Limit) | Alta |
| RF-010 | Alarme sonoro local integrado | 85dB+ no sensor | Alta |
| RF-011 | Notificação imediata via Home Assistant | Push + Telegram + SMS (prioridade P1) | Alta |
| RF-012 | Automação: fechar válvula de gás (se automatizada) | Válvula solenoide 12V | Média |
| RF-013 | Automação: NÃO acionar dispositivos elétricos com faísca | Não ligar/desligar relés na zona | Alta |
| RF-014 | Automação: abrir ventilação (se automatizada) | Exaustor ou janela automatizada | Baixa |
| RF-015 | Posicionamento: próximo ao fogão e botijão | Altura adequada ao tipo de gás | Alta |

### 4.3 Detecção de vazamento de água / inundação

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-016 | Sensor de presença de água no chão | Contato elétrico com água | Média |
| RF-017 | Posicionamento: sob pias, máquina de lavar, aquecedor | Pontos de maior risco | Média |
| RF-018 | Notificação via Home Assistant | Push + Telegram com prioridade P3 | Média |
| RF-019 | Automação: fechar registro (se válvula automatizada) | Válvula solenoide de água | Baixa |
| RF-020 | Alerta se sensor detectar água por mais de 5 minutos | Persistência de alerta | Média |

### 4.4 Detecção de monóxido de carbono (CO)

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-021 | Sensor de CO (monóxido de carbono) | Alerta a partir de 50 ppm | Média |
| RF-022 | Alarme sonoro local | 85dB+ | Média |
| RF-023 | Notificação com prioridade P1 | Risco de vida | Média |
| RF-024 | Posicionamento: próximo a aquecedores a gás | Banheiro com aquecedor, cozinha | Média |

### 4.5 Monitoramento de temperatura e umidade

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-025 | Sensor de temperatura e umidade | Registro contínuo, histórico | Baixa |
| RF-026 | Alerta de temperatura extrema | > 40°C ou < 5°C | Baixa |
| RF-027 | Alerta de umidade extrema | > 80% ou < 20% | Baixa |
| RF-028 | Histórico de dados | Gráficos no dashboard via InfluxDB/Grafana | Baixa |

### 4.6 Integração com sistema de segurança

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-029 | Sensores ambientais ativos 24/7 | Independente do modo do alarme (armado/desarmado) | Alta |
| RF-030 | Integração com Alarmo como zona especial | Zona "ambiental" com disparo imediato sempre | Alta |
| RF-031 | Dashboard com status de todos os sensores ambientais | Temperatura, umidade, fumaça, gás, água | Alta |
| RF-032 | Integração com câmeras | Gravar ao detectar evento ambiental | Média |

---

## 5. Requisitos não funcionais

### 5.1 Performance

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-001 | Tempo de detecção de fumaça | < 30 segundos após início da combustão |
| RNF-002 | Tempo de detecção de gás | < 60 segundos após vazamento |
| RNF-003 | Tempo de notificação | < 5 segundos após detecção |
| RNF-004 | Alarme sonoro local | Imediato (< 1 segundo) |

### 5.2 Confiabilidade

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-005 | Bateria de sensores Zigbee | Mínimo 24 meses |
| RNF-006 | Auto-teste periódico | Sensor verifica funcionamento semanalmente |
| RNF-007 | Alerta de bateria fraca | Notificação quando < 20% |
| RNF-008 | Alerta de sensor offline | Notificação se sensor não reporta por 24h |
| RNF-009 | Funcionamento sem internet | Alarme sonoro local mantido |

### 5.3 Segurança

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-010 | Sensores certificados | Preferir modelos com certificação (CE, UL) |
| RNF-011 | Sensor de gás: não gerar faísca | Sensor deve ser seguro para ambientes com gás |
| RNF-012 | Proteção anti-tamper | Alertar se sensor for removido |

### 5.4 Posicionamento

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-013 | Sensor de fumaça | Teto, centro do cômodo, longe de ventilação |
| RNF-014 | Sensor de gás GLP | 30cm do chão (GLP é mais pesado que o ar) |
| RNF-015 | Sensor de gás natural | 30cm do teto (gás natural é mais leve) |
| RNF-016 | Sensor de CO | Altura de 1,5m (nível de respiração) |
| RNF-017 | Sensor de água | Diretamente no chão, ponto mais baixo |

---

## 6. Arquitetura técnica

### 6.1 Diagrama de componentes

```
┌─────────────────────────────────────────────────────────────────────┐
│                    SENSORES AMBIENTAIS (Zigbee)                      │
│                                                                     │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐       │
│  │  FUMAÇA   │  │   GÁS     │  │   ÁGUA    │  │   CO      │       │
│  │ Heiman    │  │ Tuya      │  │ Aqara     │  │ Heiman    │       │
│  │ HS1SA-E   │  │ TS0601    │  │ SJCGQ11LM│  │ HS1CA-E   │       │
│  └─────┬─────┘  └─────┬─────┘  └─────┬─────┘  └─────┬─────┘       │
│        │              │              │              │               │
│        └──────────────┴──────────────┴──────────────┘               │
│                              │                                      │
│                    Zigbee 3.0 (AES-128)                             │
│                              │                                      │
│                    ┌─────────▼─────────┐                            │
│                    │   COORDENADOR     │                            │
│                    │   ZIGBEE          │                            │
│                    │  (Sonoff Dongle)  │                            │
│                    └─────────┬─────────┘                            │
│                              │                                      │
└──────────────────────────────┼──────────────────────────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │    ZIGBEE2MQTT      │
                    │    (ou ZHA)         │
                    └──────────┬──────────┘
                               │ MQTT
                    ┌──────────▼──────────┐
                    │    HOME ASSISTANT   │
                    │                     │
                    │  ┌───────────────┐  │
                    │  │ ALARMO        │  │
                    │  │ (Zona 24h)    │  │
                    │  └───────────────┘  │
                    │  ┌───────────────┐  │
                    │  │ AUTOMAÇÕES    │  │
                    │  │ (Resposta)    │  │
                    │  └───────────────┘  │
                    │  ┌───────────────┐  │
                    │  │ NOTIFICAÇÕES  │  │
                    │  │ (Multi-canal) │  │
                    │  └───────────────┘  │
                    └─────────────────────┘
```

### 6.2 Fluxo de detecção de fumaça

```
1. Sensor de fumaça detecta partículas
           │
           ├──► Alarme sonoro local (85dB+) - IMEDIATO
           │
           ▼
2. Evento Zigbee → Zigbee2MQTT → MQTT
           │
           ▼
3. Home Assistant processa:
   ├── Registra evento com timestamp
   ├── Alarmo: zona ambiental → disparo imediato
   │
   ▼
4. Automações de resposta:
   ├── Desligar HVAC (ar-condicionado, ventilação)
   ├── Acender TODAS as luzes (evacuação)
   ├── Iniciar gravação em câmeras
   │
   ▼
5. Notificações (prioridade P2):
   ├── Push (crítico, ignora modo silencioso)
   ├── Telegram com localização do sensor
   ├── SMS para contatos de emergência
   └── Sirene do sistema de alarme
```

### 6.3 Regra de segurança para gás

```
REGRA CRÍTICA - Detecção de Gás:

  AO DETECTAR GÁS:
  ├── NÃO acionar nenhum relé/switch elétrico na zona
  │   (evitar faísca que pode causar explosão)
  │
  ├── NOTIFICAR imediatamente com instruções:
  │   "Vazamento de gás detectado na cozinha.
  │    NÃO acione interruptores.
  │    Abra portas e janelas.
  │    Feche o registro do gás.
  │    Saia do local."
  │
  └── SE válvula automatizada instalada:
      └── Fechar válvula solenoide (ação segura, sem faísca)
```

---

## 7. Produtos/componentes recomendados

### 7.1 Sensores de fumaça

| Modelo | Protocolo | Preço estimado | Compatibilidade | Observações |
|--------|-----------|----------------|-----------------|-------------|
| **Heiman HS1SA-E** | Zigbee | R$ 100-150 | Z2M, ZHA | Fotoelétrico, 85dB, bateria CR123A |
| **Tuya TS0205** | Zigbee | R$ 80-120 | Z2M | Fotoelétrico, econômico |
| **Aqara JY-GZ-01AQ** | Zigbee | R$ 120-180 | Z2M, ZHA | Alta qualidade, HomeKit |

### 7.2 Sensores de gás

| Modelo | Protocolo | Preço estimado | Compatibilidade | Observações |
|--------|-----------|----------------|-----------------|-------------|
| **Tuya TS0601 (gas)** | Zigbee | R$ 100-150 | Z2M | GLP/metano, alimentação 220V |
| **Heiman HS1CG-E** | Zigbee | R$ 120-180 | Z2M, ZHA | Gás combustível, 220V |
| **Detector Kidde** | Standalone | R$ 60-100 | - | Sem integração, backup local |

### 7.3 Sensores de água/inundação

| Modelo | Protocolo | Preço estimado | Compatibilidade | Observações |
|--------|-----------|----------------|-----------------|-------------|
| **Aqara SJCGQ11LM** | Zigbee | R$ 80-120 | Z2M, ZHA | Compacto, bateria CR2032 |
| **Sonoff SNZB-05** | Zigbee | R$ 50-80 | Z2M, ZHA | Econômico |
| **Tuya TS0207** | Zigbee | R$ 40-70 | Z2M | Mais acessível |

### 7.4 Sensores de CO (monóxido de carbono)

| Modelo | Protocolo | Preço estimado | Compatibilidade | Observações |
|--------|-----------|----------------|-----------------|-------------|
| **Heiman HS1CA-E** | Zigbee | R$ 120-180 | Z2M, ZHA | Certificação CE |
| **Detector Kidde CO** | Standalone | R$ 80-120 | - | Backup local sem integração |

### 7.5 Sensores de temperatura e umidade

| Modelo | Protocolo | Preço estimado | Compatibilidade | Observações |
|--------|-----------|----------------|-----------------|-------------|
| **Aqara WSDCGQ11LM** | Zigbee | R$ 60-100 | Z2M, ZHA | Temperatura + umidade + pressão |
| **Sonoff SNZB-02D** | Zigbee | R$ 40-60 | Z2M, ZHA | Display LCD, econômico |

### 7.6 Atuadores de segurança (opcionais)

| Componente | Modelo sugerido | Preço estimado | Observações |
|------------|-----------------|----------------|-------------|
| Válvula solenoide gás 12V | Genérica 1/2" | R$ 80-150 | Para corte automático de gás |
| Válvula solenoide água 12V | Genérica 3/4" | R$ 60-120 | Para corte automático de água |
| Relé Zigbee para válvula | Sonoff ZBMINI-L2 | R$ 60-90 | Controle da válvula |

---

## 8. Estimativas por cenário

### 8.1 Cenário casa urbana (cobertura completa)

| Componente | Quantidade | Subtotal |
|------------|------------|----------|
| Sensor fumaça Zigbee (corredor, cozinha, quartos) | 3 | R$ 300-450 |
| Sensor gás combustível (cozinha) | 1 | R$ 100-150 |
| Sensor de água (cozinha, banheiro, lavanderia) | 3 | R$ 150-240 |
| Sensor temperatura/umidade | 2 | R$ 80-120 |
| Válvula solenoide gás (opcional) | 1 | R$ 80-150 |
| Relé Zigbee para válvula | 1 | R$ 60-90 |
| **Total casa urbana** | | **R$ 770-1.200** |

### 8.2 Cenário rural (sede + depósitos)

| Componente | Quantidade | Subtotal |
|------------|------------|----------|
| Sensor fumaça Zigbee (sede) | 3 | R$ 300-450 |
| Sensor fumaça (depósito, standalone) | 1 | R$ 60-100 |
| Sensor gás combustível (cozinha) | 1 | R$ 100-150 |
| Sensor de água (cozinha, banheiro) | 2 | R$ 100-160 |
| Sensor temperatura/umidade | 2 | R$ 80-120 |
| **Total rural** | | **R$ 640-980** |

### 8.3 Cenário apartamento (essencial)

| Componente | Quantidade | Subtotal |
|------------|------------|----------|
| Sensor fumaça Zigbee (cozinha, corredor) | 2 | R$ 200-300 |
| Sensor gás combustível (cozinha) | 1 | R$ 100-150 |
| Sensor de água (cozinha, banheiro) | 2 | R$ 100-160 |
| **Total apartamento** | | **R$ 400-610** |

---

## 9. Critérios de aceitação

| ID | Critério | Método de verificação |
|----|----------|----------------------|
| CA-001 | Sensor de fumaça dispara alarme sonoro local ao detectar fumaça | Teste com spray de teste |
| CA-002 | Notificação recebida em < 5 segundos após detecção | Teste com cronômetro |
| CA-003 | Sensor de gás detecta vazamento e notifica | Teste com isqueiro (gas) a distância segura |
| CA-004 | Sensor de água detecta presença de água no chão | Teste com pano úmido |
| CA-005 | Automação desliga HVAC ao detectar fumaça | Teste funcional |
| CA-006 | Luzes de emergência acendem ao detectar fumaça | Teste funcional |
| CA-007 | Sensores ambientais funcionam com alarme desarmado | Teste em modo desarmado |
| CA-008 | Dashboard exibe status de todos os sensores ambientais | Verificação visual |
| CA-009 | Alerta de bateria fraca funciona | Monitoramento |
| CA-010 | Histórico de temperatura/umidade registrado | Verificação de gráficos |

---

## 10. Métricas de sucesso

| Métrica | Alvo | Medição |
|---------|------|---------|
| **Cobertura de detecção** | Fumaça em 100% dos cômodos críticos | Inventário |
| **Falsos positivos de fumaça** | < 1/mês | Contagem |
| **Tempo de detecção** | < 60 segundos para todos os tipos | Testes periódicos |
| **Disponibilidade dos sensores** | > 99% online | Monitoramento |
| **Bateria dos sensores** | > 24 meses | Registro de trocas |

---

## 11. Riscos e dependências

### 11.1 Riscos

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Falso positivo de fumaça (cozinha) | Média | Médio | Posicionar longe do fogão, usar fotoelétrico |
| Sensor de gás perde calibração | Baixa | Alto | Trocar sensor a cada 3-5 anos |
| Sensor de água não detecta (posição errada) | Média | Médio | Posicionar no ponto mais baixo |
| Bateria acaba sem aviso | Baixa | Alto | Monitoramento de bateria, alerta a 20% |
| Automação de gás aciona faísca | Baixa | Crítico | Nunca acionar relés na zona com gás detectado |

### 11.2 Dependências

| Dependência | Tipo | PRD relacionado |
|-------------|------|-----------------|
| Coordenador Zigbee | Infraestrutura | PRD_LOCAL_PROCESSING_HUB |
| Home Assistant + Alarmo | Plataforma | PRD_SENSORS_AND_ALARMS_PLATFORM |
| Sistema de notificações | Funcional | PRD_NOTIFICATIONS_AND_ALERTS |
| Automações de resposta | Funcional | PRD_AUTOMATION_AND_SCENES |
| Dashboard | Interface | PRD_MONITORING_DASHBOARD |

---

## 12. Referências

### Documentos do projeto
- `docs/ARQUITETURA_TECNICA.md` - Seções 1, 3, 6
- `prd/PRD_SENSORS_AND_ALARMS_PLATFORM.md` - Sensores RF-006, RF-007, RF-008
- `prd/PRD_NOTIFICATIONS_AND_ALERTS.md` - Prioridades P1 e P2
- `rules/RULES_COMPLIANCE_AND_STANDARDS.md`

### Externos
- [Zigbee2MQTT - Sensores de Fumaça](https://www.zigbee2mqtt.io/supported-devices/#e=smoke)
- NBR 17240 - Sistemas de detecção e alarme de incêndio
- NFPA 72 - National Fire Alarm Code (referência internacional)
- [Home Assistant - Sensor Integration](https://www.home-assistant.io/integrations/sensor/)

---

> **Status**: Rascunho v1.0
>
> **Próxima revisão**: Após validação pelo Agente_Arquiteto_Tecnico
