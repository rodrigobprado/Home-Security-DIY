# PRD – Segurança de Perímetro Rural

> Sistema de Home Security – Open Source / Open Hardware
>
> Versão: 1.0 | Data: 2026-02-12 | Responsável: Agente_Documentador

---

## 1. Visão geral

- **Nome do produto/funcionalidade**: Sistema de Segurança para Propriedade Rural
- **Responsável**: Agente_Arquiteto_Seguranca_Fisica (requisitos), Agente_Documentador (documentação)
- **Data**: 2026-02-12
- **PRDs relacionados**: PRD_SENSORS_AND_ALARMS_PLATFORM, PRD_VIDEO_SURVEILLANCE_AND_NVR, PRD_RURAL_ACCESS_CONTROL

---

## 2. Problema e oportunidade

### 2.1 Problema

Propriedades rurais enfrentam desafios únicos de segurança:
- **Perímetros extensos** (500m a 5.000m+) difíceis de monitorar
- **Isolamento geográfico** com vizinhança distante e baixa vigilância natural
- **Tempo de resposta longo** de autoridades (30 minutos ou mais)
- **Infraestrutura limitada** com possível instabilidade de energia e internet
- **Múltiplos pontos de entrada** incluindo áreas não construídas

### 2.2 Oportunidade

Implementar um sistema de defesa em profundidade com:
- **4 zonas de proteção** (perímetro → área externa → envelope → interior)
- **Monitoramento inteligente** de pontos críticos
- **Alertas precoces** que maximizem tempo de reação
- **Autonomia energética** parcial para pontos remotos

---

## 3. Público-alvo

| Perfil | Características | Necessidades |
|--------|-----------------|--------------|
| **Fazendeiro** | Propriedade produtiva, funcionários | Proteção de equipamentos, controle de acesso |
| **Sitiante** | Propriedade de lazer, ocupação intermitente | Monitoramento remoto, alertas de invasão |
| **Chacareiro** | Propriedade menor, uso frequente | Custo-benefício, simplicidade |

---

## 4. Características do cenário

| Aspecto | Descrição |
|---------|-----------|
| **Perímetro típico** | 500m a 5.000m+ de extensão |
| **Área** | 1 hectare a centenas de hectares |
| **Vizinhança** | Distante, baixa vigilância natural |
| **Acesso** | Uma ou poucas entradas principais, estradas vicinais |
| **Infraestrutura** | Pode ter limitação de energia e internet |
| **Riscos principais** | Invasão por áreas não monitoradas, roubo de equipamentos/animais |

---

## 5. Requisitos funcionais

### 5.1 Zona 1: Perímetro

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-001 | Cerca perimetral física | Alambrado ou tela ≥1,70m, mourões próximos | Alta |
| RF-002 | Cerca elétrica | Sobre cerca física, altura total ≥2,20m | Alta |
| RF-003 | Sinalização de cerca elétrica | Placas a cada 10m, portões, mudanças de direção | Alta |
| RF-004 | Sensor de violação de cerca | Integração com central da cerca elétrica | Média |
| RF-005 | Iluminação perimetral | Solar em pontos críticos (entrada, cantos) | Média |
| RF-006 | Sensor de abertura em portão principal | Magnético ou fim de curso | Alta |
| RF-007 | Câmera no portão de entrada | PoE, 4MP+, visão noturna IR 30m+ | Alta |

### 5.2 Zona 2: Área externa (entorno da sede)

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-008 | Cerca secundária | Delimitar área da sede | Média |
| RF-009 | Iluminação com sensor | Refletores LED PIR em acessos | Alta |
| RF-010 | Câmera na área de máquinas/depósito | PoE, 4MP+, visão noturna | Alta |
| RF-011 | Sensores de movimento externos | PIR duplo ou IVA (2-4 unidades) | Média |
| RF-012 | Paisagismo defensivo | Plantas espinhosas junto a janelas | Baixa |
| RF-013 | Portas de garagem/depósito | Fechadura reforçada ou cadeado | Alta |

### 5.3 Zona 3: Envelope (sede/casa)

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-014 | Porta principal reforçada | Madeira maciça ou metálica, fechadura 3+ pontos | Alta |
| RF-015 | Portas secundárias | Reforçadas com tranca adicional | Alta |
| RF-016 | Janelas térreo | Grades ou telas de segurança | Alta |
| RF-017 | Vidros em áreas críticas | Laminado de segurança | Média |
| RF-018 | Sensores de abertura | Em todas as portas externas (Zigbee) | Alta |
| RF-019 | Sensores de abertura janelas | Janelas acessíveis (Zigbee) | Média |
| RF-020 | Câmera frontal da sede | Visão geral da área social | Alta |
| RF-021 | Câmeras laterais da sede | Cobertura de janelas e acessos | Média |

### 5.4 Zona 4: Interior

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-022 | Sensor de movimento interno | PIR (1-2 em áreas de passagem) | Média |
| RF-023 | Cofre | Para documentos, valores, armas (se aplicável) | Média |
| RF-024 | Área segura | Cômodo reforçado para refúgio (opcional) | Baixa |

### 5.5 Sistema de alarme

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-025 | Sirene externa | 110dB+, resistente a intempéries (1-2 unidades) | Alta |
| RF-026 | Sirene interna | 90dB+ (1 unidade) | Alta |
| RF-027 | Botão de pânico | Discreto, em área de fácil acesso | Alta |
| RF-028 | Iluminação reativa | Acender luzes ao detectar alarme | Média |
| RF-029 | Notificação multi-canal | Push + Telegram/SMS | Alta |

### 5.6 Continuidade operacional

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-030 | Nobreak para central | Autonomia mínima 30 minutos | Alta |
| RF-031 | Alimentação solar em pontos remotos | Câmeras/sensores de perímetro | Média |
| RF-032 | Backup de internet | 4G como failover (opcional) | Baixa |

---

## 6. Requisitos não funcionais

### 6.1 Performance

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-001 | Detecção de invasão | < 5 segundos |
| RNF-002 | Notificação após alarme | < 30 segundos |
| RNF-003 | Cobertura de câmeras | 100% dos pontos de entrada |

### 6.2 Confiabilidade

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-004 | Autonomia em queda de energia | 30 minutos (central), 8h (sensores bateria) |
| RNF-005 | Alcance Zigbee | Usar repetidores se necessário para perímetro |
| RNF-006 | Resistência a intempéries | IP65+ para equipamentos externos |

### 6.3 Conformidade

| ID | Requisito | Norma/Regra |
|----|-----------|-------------|
| RNF-007 | Cerca elétrica | Lei 13.477/2017, REGRA-CERCA-01 a 06 |
| RNF-008 | Câmeras | REGRA-CFTV-05 a 12 |
| RNF-009 | LGPD | REGRA-LGPD-01 a 05 (se capturar via pública) |

---

## 7. Arquitetura física

### 7.1 Diagrama de posicionamento

```
                    ESTRADA VICINAL
                          │
                    ┌─────┴─────┐
                    │  PORTÃO   │◄── Câmera 1 (entrada)
                    │ PRINCIPAL │    Sensor de abertura
                    └─────┬─────┘
                          │
    ══════════════════════╪══════════════════════ CERCA ELÉTRICA
    ║                     │                     ║
    ║    PASTAGEM/        │      ÁREA DE        ║
    ║    PLANTAÇÃO   ┌────┴────┐  MÁQUINAS      ║
    ║                │ ESTRADA │                ║
    ║                │ INTERNA │                ║
    ║                └────┬────┘                ║
    ║                     │                     ║
    ║              ┌──────┴──────┐              ║
    ║              │   GARAGEM   │◄── Câmera 3  ║
    ║              │   DEPÓSITO  │    Sensor    ║
    ║              └──────┬──────┘              ║
    ║                     │                     ║
    ║    ┌────────────────┼────────────────┐    ║
    ║    │          ┌─────┴─────┐          │    ║
    ║    │          │   SEDE    │          │    ║
    ║    │◄─Câmera 4│  (CASA)   │Câmera 5─►│    ║
    ║    │  lateral │           │ lateral  │    ║
    ║    │          │  Câmera 2 │          │    ║
    ║    │          │  (frente) │          │    ║
    ║    │          └───────────┘          │    ║
    ║    │      JARDIM / ÁREA SOCIAL       │    ║
    ║    └─────────────────────────────────┘    ║
    ║           CERCA SECUNDÁRIA               ║
    ══════════════════════════════════════════════ CERCA ELÉTRICA

    LEGENDA:
    ═══ Cerca elétrica perimetral
    ─── Cerca secundária (área da sede)
    ◄── Posição de câmera
```

### 7.2 Posicionamento de câmeras

| Câmera | Localização | Função | Especificação |
|--------|-------------|--------|---------------|
| 1 | Portão principal | Captura entrada, placas | Bullet PoE 4MP, IR 30m+ |
| 2 | Frente da sede | Área social, entrada | PoE 4MP, wide angle |
| 3 | Garagem/depósito | Equipamentos | Dome PoE 4MP |
| 4-5 | Laterais | Janelas, acessos | Bullet PoE 4MP |
| 6 (opcional) | Perímetro | Ponto cego | Solar + 4G ou PoE longo alcance |

### 7.3 Posicionamento de sensores

| Sensor | Localização | Tipo | Protocolo |
|--------|-------------|------|-----------|
| S1 | Portão principal | Abertura | Zigbee ou 433MHz |
| S2-S5 | Portas externas | Abertura | Zigbee |
| S6-S9 | Janelas térreo | Abertura | Zigbee |
| S10-S11 | Laterais sede | Movimento PIR | Zigbee |
| S12 | Corredor interno | Movimento PIR | Zigbee |
| S13 | Cerca elétrica | Violação | Integração central |

---

## 8. Estimativa de investimento

### 8.1 Componentes e custos

| Componente | Quantidade | Preço unitário | Subtotal |
|------------|------------|----------------|----------|
| **Central de processamento** |
| Mini PC Intel N100 8GB | 1 | R$ 1.000 | R$ 1.000 |
| SSD 256GB (sistema) | 1 | R$ 150 | R$ 150 |
| HDD 2TB (gravações) | 1 | R$ 350 | R$ 350 |
| **Câmeras** |
| Câmera Bullet PoE 4MP (Reolink RLC-810A) | 4-5 | R$ 450 | R$ 1.800-2.250 |
| Switch PoE 8 portas | 1 | R$ 400 | R$ 400 |
| **Sensores** |
| Coordenador Zigbee (Sonoff ZBDongle-P) | 1 | R$ 150 | R$ 150 |
| Sensor abertura (Sonoff SNZB-04) | 6-8 | R$ 50 | R$ 300-400 |
| Sensor PIR (Sonoff SNZB-03) | 3-4 | R$ 70 | R$ 210-280 |
| Sirene externa | 1 | R$ 200 | R$ 200 |
| Sirene interna (Heiman HS2WD-E) | 1 | R$ 120 | R$ 120 |
| Botão de pânico | 1 | R$ 80 | R$ 80 |
| **Infraestrutura** |
| Nobreak 1000VA | 1 | R$ 500 | R$ 500 |
| Cabeamento Cat6 (100m) | 1 | R$ 200 | R$ 200 |
| Conectores, caixas, diversos | - | R$ 200 | R$ 200 |

### 8.2 Total estimado

| Item | Faixa de preço |
|------|----------------|
| **Configuração mínima** (4 câmeras, 9 sensores) | R$ 5.460 |
| **Configuração recomendada** (5 câmeras, 12 sensores) | R$ 6.480 |
| **Instalação profissional** (opcional) | R$ 1.000-2.000 |

> Valores estimados, podem variar conforme fornecedor e região.

---

## 9. Critérios de aceitação

| ID | Critério | Método de verificação |
|----|----------|----------------------|
| CA-001 | Cerca elétrica instalada com sinalização adequada | Inspeção visual |
| CA-002 | Todas as câmeras com visão clara e sem pontos cegos | Teste de cobertura |
| CA-003 | Portão detectado ao abrir em qualquer condição | Teste funcional |
| CA-004 | Alarme dispara em < 5 segundos após violação | Teste com cronômetro |
| CA-005 | Notificação recebida em < 30 segundos | Teste com cronômetro |
| CA-006 | Sistema opera por 30 min sem energia | Teste de interrupção |
| CA-007 | Detecção de pessoas funciona à noite | Teste noturno |
| CA-008 | PIR externo não dispara com animais pequenos | Teste de sensibilidade |

---

## 10. Métricas de sucesso

| Métrica | Alvo | Medição |
|---------|------|---------|
| **Falsos positivos** | < 2/semana | Contagem de alarmes indevidos |
| **Cobertura de detecção** | 100% pontos de entrada | Mapeamento |
| **Tempo de resposta** | < 30s notificação | Monitoramento |
| **Disponibilidade** | > 99% | Uptime |

---

## 11. Riscos e mitigações

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Alcance Zigbee insuficiente | Média | Alto | Repetidores ou sensores cabeados |
| Animais causam falsos positivos | Alta | Médio | PIR pet-immune, ajuste sensibilidade |
| Queda de energia prolongada | Média | Alto | Nobreak + gerador (opcional) |
| Internet instável | Média | Médio | 4G backup, cache local de eventos |
| Vandalismo em câmeras | Baixa | Alto | Posicionamento alto, caixa proteção |

---

## 12. Referências

### Documentos do projeto
- `docs/ARQUITETURA_SEGURANCA_FISICA.md` - Seções 2, 5, 7
- `docs/ARQUITETURA_TECNICA.md` - Seção 1.1
- `rules/RULES_COMPLIANCE_AND_STANDARDS.md` - REGRA-CERCA-*, REGRA-CFTV-*

### Externos
- Lei 13.477/2017 - Cercas elétricas
- NBR 15.401 - Cercas eletrificadas

---

> **Status**: Rascunho v1.0
>
> **Próxima revisão**: Após validação pelo Agente_Arquiteto_Seguranca_Fisica
