# Cenários Residenciais

Este guia detalha como adaptar o sistema Home Security DIY aos três cenários de habitação mais comuns: **Propriedade Rural**, **Casa Urbana com Quintal** e **Apartamento**. Cada cenário tem características, riscos e recomendações distintas.

---

## Tabela Comparativa

| Aspecto | Rural | Casa Urbana | Apartamento |
|---------|-------|-------------|-------------|
| **Perímetro** | Cerca + cerca elétrica | Muro + cerca elétrica | Responsabilidade do condomínio |
| **Câmeras sugeridas** | 4–6 | 3–5 | 0–1 (olho mágico digital) |
| **Sensores sugeridos** | 4–8 | 6–10 (8–15 com mais zonas) | 2–4 |
| **Iluminação** | Solar/sensor | Constante + sensor de presença | Responsabilidade do condomínio |
| **Tempo de resposta (polícia)** | Longo (30 min+) | Médio (10–20 min) | Curto (5–15 min) |
| **Investimento relativo** | Alto | Médio | Baixo |
| **Complexidade de implantação** | Alta | Média | Baixa |

---

## Cenário 1 — Propriedade Rural

### Características

| Aspecto | Descrição |
|---------|-----------|
| Perímetro típico | 500 m a 5.000 m+ |
| Área | 1 ha a centenas de ha |
| Vizinhança | Distante, baixa vigilância natural |
| Acesso | Uma ou poucas entradas, estradas vicinais |
| Infraestrutura | Pode ter limitação de energia e internet |
| Riscos principais | Invasão por áreas não monitoradas, roubo de equipamentos/animais, tempo de resposta longo |

### Defesa em profundidade — Zonas de proteção

```
┌─────────────────────────────────────────────────────────────────────┐
│                         ZONA 1: PERÍMETRO                          │
│  Cerca elétrica + alambrado, portão principal, iluminação solar     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │                    ZONA 2: ÁREA EXTERNA                       │ │
│  │    Cerca secundária, garagem, depósito, refletores LED        │ │
│  │  ┌─────────────────────────────────────────────────────────┐  │ │
│  │  │                 ZONA 3: ENVELOPE (SEDE)                 │  │ │
│  │  │     Portas reforçadas, janelas gradeadas, batentes      │  │ │
│  │  │  ┌───────────────────────────────────────────────────┐  │  │ │
│  │  │  │              ZONA 4: INTERIOR                     │  │  │ │
│  │  │  │    Cofre, área segura, objetos fora da vista      │  │  │ │
│  │  │  └───────────────────────────────────────────────────┘  │  │ │
│  │  └─────────────────────────────────────────────────────────┘  │ │
│  └───────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

### Diagrama de posicionamento de câmeras e sensores

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
    ║    │◄─Câm. 4  │  (CASA)   │  Câm. 5─►│   ║
    ║    │  lateral │           │  lateral  │   ║
    ║    │          │  Câm. 2   │           │   ║
    ║    │          │  (frente) │           │   ║
    ║    │          └───────────┘           │   ║
    ║    │      JARDIM / ÁREA SOCIAL        │   ║
    ║    └──────────────────────────────────┘   ║
    ║           CERCA SECUNDÁRIA               ║
    ══════════════════════════════════════════════

    LEGENDA:
    ═══ Cerca elétrica perimetral
    ─── Cerca secundária da sede
    ◄── Posição de câmera + sensor
```

**Câmeras:**
- **Câm. 1** — Portão principal: captura entrada de veículos/pessoas e placas
- **Câm. 2** — Frente da sede: visão geral da área social e entrada principal
- **Câm. 3** — Garagem/depósito: monitoramento de equipamentos
- **Câm. 4/5** — Laterais da sede: cobertura de janelas e acessos secundários

**Sensores:**
- Abertura no portão principal
- PIR (ou câmera com IVA) nas laterais da sede
- Vibração na cerca elétrica (opcional)

### Componentes por prioridade

| Elemento | Zona | Prioridade |
|----------|------|------------|
| Cerca perimetral (1,70 m+) | Perímetro | Alta |
| Cerca elétrica (2,20 m total) | Perímetro | Alta |
| Portão metálico com tranca | Perímetro | Alta |
| Iluminação solar em pontos críticos | Perímetro | Média |
| Refletores LED com sensor de movimento | Área externa | Alta |
| Portas com fechadura de 3+ pontos | Envelope | Alta |
| Janelas térreo com grades | Envelope | Alta |
| Câmera na entrada + sensor de abertura | Todos | Alta |

---

## Cenário 2 — Casa Urbana com Quintal

### Características

| Aspecto | Descrição |
|---------|-----------|
| Perímetro típico | 50–200 m |
| Área | 200–1.000 m² |
| Vizinhança | Próxima, vigilância natural moderada |
| Acesso | Portão de pedestres, portão de veículos, muros laterais |
| Infraestrutura | Energia e internet estáveis |
| Riscos principais | Invasão por muro/portão, janelas térreo, tempo de resposta médio |

### Diagrama de posicionamento

```
                         RUA
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                    │         │
            ┌───────┴───┐ ┌───┴───────┐
            │  PORTÃO   │ │  PORTÃO   │
            │ PEDESTRE  │ │ VEÍCULOS  │
            └───────┬───┘ └───┬───────┘
                    │         │
    ┌───────────────┴─────────┴───────────────┐
    │ Câmera 1 ─►  ┌───────────┐              │
    │ (entrada)    │  JARDIM   │   ◄─ Luz     │
    │              │  FRONTAL  │   constante  │
    ├──────────────┴───────────┴──────────────┤
    │  ┌──────────────────────────────────┐   │
    │  │         GARAGEM            Câm.2─►   │
    │  └────────────┬─────────────────────┘   │
    │  ┌────────────┴─────────────────────┐   │
    │  │                                  │   │
    │  │           C A S A                │   │ MURO
    │  │  ┌──────┐           ┌──────┐     │◄──┤ LATERAL
    │  │  │ Sala │  Corredor │ Coz. │     │   │ Câm. 3
    │  │  └──────┘           └──────┘     │   │
    │  └────────────┬─────────────────────┘   │
    │  ┌────────────┴─────────────────────┐   │
    │  │  QUINTAL / SERVIÇO / CHURRASCO   │◄──┤
    │  │                            Câm. 4│   │ + Luz sensor
    │  └──────────────────────────────────┘   │
    └─────────────────────────────────────────┘
                    MURO FUNDOS
```

**Câmeras:**
- **Câm. 1** — Entrada: visão da rua, calçada e portões
- **Câm. 2** — Garagem: monitoramento de veículos e acesso
- **Câm. 3** — Lateral: corredor lateral e janelas
- **Câm. 4** — Fundos/quintal: área de serviço

**Sensores:**
- Abertura: portões, porta principal, porta de serviço, porta do quintal
- Movimento: quintal (cobertura ampla)
- Quebra de vidro: janelas térreo (opcional com grades)

### Componentes por prioridade

| Elemento | Zona | Prioridade |
|----------|------|------------|
| Muro frontal 2,0–2,5 m | Perímetro | Alta |
| Cerca elétrica sobre o muro (total 2,50 m+) | Perímetro | Alta |
| Portões metálicos com fechadura de segurança | Perímetro | Alta |
| Iluminação frontal constante (LED) | Área externa | Alta |
| Iluminação lateral/fundo com sensor | Área externa | Alta |
| Evitar vegetação que crie esconderijos | Área externa | Alta |
| Porta principal madeira maciça ou blindada | Envelope | Alta |
| Janelas térreo com grades | Envelope | Alta |
| Câmera na entrada + sensor de abertura | Todos | Alta |

---

## Cenário 3 — Apartamento

### Características

| Aspecto | Descrição |
|---------|-----------|
| Perímetro | Responsabilidade do condomínio |
| Área | 40–200 m² |
| Vizinhança | Muito próxima; portaria como primeira barreira |
| Acesso | Porta principal única |
| Infraestrutura | Energia e internet estáveis |
| Riscos principais | Invasão pela porta, engenharia social na portaria |

### Diagrama de posicionamento

```
    ┌─────────────────────────────────────────────────────┐
    │                    CORREDOR DO PRÉDIO               │
    │                                                     │
    │    ┌──────────────────────────────────────────┐     │
    │    │              APARTAMENTO                 │     │
    │    │                                          │     │
    │    │  ┌────────┐  ┌────────┐  ┌────────┐     │     │
    │    │  │QUARTO 1│  │QUARTO 2│  │ BANHO  │     │     │
    │    │  └────────┘  └────────┘  └────────┘     │     │
    │    │                                          │     │
    │    │  ┌─────────────────────────┐ ┌──────┐   │     │
    │    │  │      SALA / LIVING      │ │ Coz. │   │     │
    │    │  └─────────────────────────┘ └──────┘   │     │
    │    │                                          │     │
    │    │  ════════════════════════════════════   │     │
    │    │              VARANDA                     │     │
    │    │  (verificar acesso de andares próximos) │     │
    │    │  ════════════════════════════════════   │     │
    │    │                                          │     │
    │    └──────────────────────────────────────────┘     │
    │                      ▲                              │
    │            ┌──────────┴──────────┐                  │
    │            │  PORTA BLINDADA     │◄── Sensor abertura│
    │            │  + Olho mágico opt. │    Câm. opcional  │
    │            └─────────────────────┘                  │
    │                                                     │
    └─────────────────────────────────────────────────────┘
```

**Componentes recomendados:**

| Componente | Especificação | Prioridade |
|------------|---------------|------------|
| Porta blindada | Fechadura multiponto (3+ pontos), cilindro europeu com protetor | Alta |
| Batente | Metálico com parafusos longos | Alta |
| Dobradiças | Internas ou com pino anti-remoção | Alta |
| Olho mágico digital | Com câmera, visão noturna, SD | Média |
| Sensor de abertura | Na porta principal | Alta |
| Sensor de movimento | Sala/corredor interno, ativado quando ausente | Opcional |
| Câmera interna | Não recomendada por privacidade | — |

> **Nota sobre perímetro**: Segurança perimetral é responsabilidade do condomínio. Avalie se há portaria 24 h, câmeras em áreas comuns e controle de acesso antes de decidir pelo imóvel.

---

## Segurança Reativa — Todos os Cenários

### Detecção

| Requisito | Implementação |
|-----------|---------------|
| Detecção < 5 s | Sensores em todos os pontos de entrada |
| Redundância | PIR + abertura, ou PIR + câmera |
| Anti-mascaramento | Sensores com recurso anti-tamper |

### Alerta

| Requisito | Implementação |
|-----------|---------------|
| Sirene local | Interna (90 dB+) + externa (110 dB+) |
| Notificação < 30 s | Push notification, SMS, Telegram via 4G |
| Múltiplos canais | App + SMS + e-mail |
| Contatos de emergência | Mínimo 2–3 contatos cadastrados |

### Procedimento em caso de invasão confirmada

```
1. NÃO CONFRONTAR o invasor
2. Ir para local seguro (cômodo com tranca, se disponível)
3. Ligar para polícia (190): informar endereço, situação, nº de invasores
4. Notificar contatos de emergência
5. Permanecer em silêncio e aguardar autoridades
6. Preservar gravações após o incidente
7. Registrar boletim de ocorrência
```

### Tipos de alerta e ações automáticas

| Alerta | Ação automática | Ação do morador |
|--------|-----------------|-----------------|
| Sensor de abertura (armado) | Notificação, sirene após delay, gravação | Verificar câmeras |
| Sensor de movimento (armado) | Notificação, sirene após delay, gravação | Verificar câmeras |
| Botão de pânico | Notificação silenciosa, alerta a contatos | Aguardar em local seguro |
| Queda de energia | Notificação via 4G, switch para nobreak | Verificar se é falha geral ou ataque |
| Câmera offline | Notificação de falha | Verificar possível sabotagem |
| Energia + internet offline simultaneamente | **Alerta máximo** via 4G, sirenes, luzes | Considerar ataque coordenado |

---

## Checklist de Implementação

### Segurança passiva (física)

- [ ] Perímetro fechado e em bom estado
- [ ] Iluminação externa funcionando (constante ou sensor)
- [ ] Portões com fechadura de segurança
- [ ] Portas reforçadas com fechadura multiponto
- [ ] Janelas térreo com grades ou vidro laminado
- [ ] Batentes fixados com parafusos longos
- [ ] Paisagismo não cria esconderijos
- [ ] Objetos de valor não visíveis de fora

### Segurança reativa (eletrônica)

- [ ] Câmeras posicionadas conforme diagrama do cenário
- [ ] Sensores de abertura em todos os pontos de entrada
- [ ] Sensores PIR cobrindo áreas críticas
- [ ] Sirene interna e externa instaladas
- [ ] Nobreak dimensionado (ver [Resiliência](Resiliencia))
- [ ] 4G como canal de notificação de backup
- [ ] Contatos de emergência cadastrados no Home Assistant

---

## Referências

- `docs/ARQUITETURA_SEGURANCA_FISICA.md` — fonte principal deste documento
- `docs/ARQUITETURA_TECNICA.md` — especificações por cenário
- [Arquitetura](Arquitetura) — visão geral do stack técnico
- [Resiliência](Resiliencia) — modos degradados e proteção anti-tamper
- [Operação e Manutenção](Operacao-e-Manutencao) — rotina operacional
