# Arquitetura de Segurança Física – Sistema de Home Security

> Documento produzido pelo Agente_Arquiteto_Seguranca_Fisica
>
> Tarefas: T-001, T-002, T-003, T-007, T-008, T-009, T-010
>
> Data: 2026-02-12

---

## 1. Fundamentos de Defesa em Profundidade

### 1.1 Conceito

A segurança física utiliza uma combinação de **barreiras sucessivas** para defesa em profundidade. Se uma camada falhar ou for ultrapassada, haverá ainda uma segunda (ou terceira) restrição. O princípio básico é separar o agressor potencial do ativo crítico por meio de múltiplas camadas de proteção.

### 1.2 Tipos de barreiras

| Tipo | Descrição | Exemplos |
|------|-----------|----------|
| **Físicas** | Estruturas que impedem ou retardam acesso | Muros, cercas, grades, portões, portas, janelas |
| **Tecnológicas** | Sistemas eletrônicos de detecção e alerta | Câmeras, sensores, alarmes, iluminação automática |
| **Psicológicas** | Elementos que desencorajam tentativas | Placas de aviso, visibilidade, aparência de vigilância |
| **Naturais** | Elementos do ambiente que dificultam acesso | Plantas espinhosas, topografia, corpos d'água |

### 1.3 Zonas de proteção

```
┌─────────────────────────────────────────────────────────────────────┐
│                         ZONA 1: PERÍMETRO                          │
│  Cercas, muros, portões, iluminação externa, sensores de perímetro │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │                    ZONA 2: ÁREA EXTERNA                       │ │
│  │    Quintal, jardim, garagem, iluminação com sensor            │ │
│  │  ┌─────────────────────────────────────────────────────────┐  │ │
│  │  │                 ZONA 3: ENVELOPE                        │  │ │
│  │  │     Portas, janelas, fechaduras, sensores de abertura   │  │ │
│  │  │  ┌───────────────────────────────────────────────────┐  │  │ │
│  │  │  │              ZONA 4: INTERIOR                     │  │  │ │
│  │  │  │    Sensores internos, cofre, área segura          │  │  │ │
│  │  │  └───────────────────────────────────────────────────┘  │  │ │
│  │  └─────────────────────────────────────────────────────────┘  │ │
│  └───────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 2. Cenário 1: Propriedade Rural

### 2.1 Características do cenário

| Aspecto | Descrição |
|---------|-----------|
| **Perímetro típico** | 500m a 5.000m+ de extensão |
| **Área** | 1 hectare a centenas de hectares |
| **Vizinhança** | Distante, baixa vigilância natural |
| **Acesso** | Uma ou poucas entradas, estradas vicinais |
| **Infraestrutura** | Pode ter limitação de energia e internet |
| **Riscos principais** | Invasão por áreas não monitoradas, roubo de equipamentos/animais, tempo de resposta longo |

### 2.2 Requisitos de segurança passiva (T-001)

#### Zona 1: Perímetro

| Elemento | Especificação | Prioridade |
|----------|---------------|------------|
| **Cerca perimetral** | Alambrado ou tela com 1,70m+ de altura, mourões próximos (impedir passagem de veículos) | Alta |
| **Cerca elétrica** | Sobre a cerca física, altura mínima 2,20m, sinalização a cada 10m | Alta |
| **Portão principal** | Metálico, robusto, com travamento por cadeado ou fechadura de segurança | Alta |
| **Portões secundários** | Minimizar quantidade, manter trancados | Média |
| **Iluminação perimetral** | Solar em pontos críticos (entrada, cantos), sensor crepuscular | Média |

#### Zona 2: Área externa (entorno da sede)

| Elemento | Especificação | Prioridade |
|----------|---------------|------------|
| **Cerca secundária** | Delimitar área da sede com cerca adicional | Média |
| **Iluminação com sensor** | Refletores LED com sensor de movimento em acessos | Alta |
| **Paisagismo defensivo** | Plantas espinhosas junto a janelas e muros baixos | Baixa |
| **Garagem/depósito** | Portas com cadeado ou fechadura reforçada | Alta |
| **Visibilidade** | Manter vegetação aparada para visão clara da entrada | Média |

#### Zona 3: Envelope (sede/casa)

| Elemento | Especificação | Prioridade |
|----------|---------------|------------|
| **Porta principal** | Madeira maciça ou metálica, fechadura de 3+ pontos | Alta |
| **Portas secundárias** | Reforçadas, com tranca adicional | Alta |
| **Janelas térreo** | Grades ou telas de segurança, vidro laminado em áreas críticas | Alta |
| **Janelas superiores** | Trincos reforçados | Média |
| **Batentes** | Fixados com parafusos longos na alvenaria | Alta |

#### Zona 4: Interior

| Elemento | Especificação | Prioridade |
|----------|---------------|------------|
| **Área segura** | Cômodo reforçado para refúgio (panic room) - opcional | Baixa |
| **Cofre** | Para documentos, armas (se aplicável), valores | Média |
| **Objetos de valor** | Não visíveis de janelas | Alta |

### 2.3 Diagrama de posicionamento – Cenário Rural (T-008)

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

**Posicionamento de câmeras:**
- **Câmera 1**: Portão principal - captura entrada de veículos/pessoas, placa de veículos
- **Câmera 2**: Frente da sede - visão geral da área social e entrada principal
- **Câmera 3**: Garagem/depósito - monitoramento de equipamentos
- **Câmera 4-5**: Laterais da sede - cobertura de janelas e acessos secundários

**Posicionamento de sensores:**
- Sensor de abertura no portão principal
- Sensores de movimento (PIR ou IVA) nas laterais da sede
- Sensor de vibração na cerca elétrica (opcional)

---

## 3. Cenário 2: Casa Urbana com Quintal

### 3.1 Características do cenário

| Aspecto | Descrição |
|---------|-----------|
| **Perímetro típico** | 50m a 200m de extensão |
| **Área** | 200m² a 1.000m² |
| **Vizinhança** | Próxima, vigilância natural moderada |
| **Acesso** | Portão de pedestres, portão de veículos, muros laterais |
| **Infraestrutura** | Energia e internet estáveis |
| **Riscos principais** | Invasão por muro/portão, janelas térreo, tempo de resposta médio |

### 3.2 Requisitos de segurança passiva (T-002)

#### Zona 1: Perímetro (muro/grade)

| Elemento | Especificação | Prioridade |
|----------|---------------|------------|
| **Muro frontal** | 2,0m a 2,5m de altura, sem apoios para escalar | Alta |
| **Muro lateral/fundo** | Mesma altura, verificar vizinhos | Alta |
| **Grade vazada** | Alternativa ao muro - permite vigilância natural, mas expõe interior | Média |
| **Cerca elétrica** | Sobre o muro, altura total 2,50m+, sinalização obrigatória | Alta |
| **Concertina** | Alternativa à cerca elétrica (verificar legislação local) | Média |
| **Portão de pedestres** | Metálico, fechadura de segurança, altura do muro | Alta |
| **Portão de veículos** | Metálico, automatizado com sensor anti-esmagamento | Alta |

#### Zona 2: Área externa (quintal)

| Elemento | Especificação | Prioridade |
|----------|---------------|------------|
| **Iluminação frontal** | Constante à noite, LED de baixo consumo | Alta |
| **Iluminação lateral/fundo** | Com sensor de presença | Alta |
| **Garagem** | Porta reforçada, sem acesso direto ao interior da casa (ideal) | Média |
| **Paisagismo** | Plantas espinhosas junto ao muro e sob janelas | Média |
| **Visibilidade** | Evitar arbustos altos que criem esconderijos | Alta |
| **Objetos no quintal** | Guardar escadas, ferramentas (podem ser usadas para invasão) | Alta |

#### Zona 3: Envelope

| Elemento | Especificação | Prioridade |
|----------|---------------|------------|
| **Porta principal** | Madeira maciça ou blindada, fechadura multiponto | Alta |
| **Porta de serviço** | Reforçada, tranca adicional | Alta |
| **Porta para quintal** | Grade ou vidro reforçado com fechadura | Alta |
| **Janelas térreo frente** | Grades decorativas ou vidro laminado | Alta |
| **Janelas térreo fundo** | Grades (menos visíveis, maior risco) | Alta |
| **Janelas superiores** | Trincos reforçados, grades em áreas acessíveis (varandas) | Média |
| **Batentes** | Parafusos longos, protetor de cilindro na fechadura | Alta |

#### Zona 4: Interior

| Elemento | Especificação | Prioridade |
|----------|---------------|------------|
| **Cofre** | Embutido ou fixado, para documentos e valores | Média |
| **Objetos de valor** | Não visíveis de janelas, especialmente à noite | Alta |

### 3.3 Diagrama de posicionamento – Casa Urbana (T-009)

```
                         RUA
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                    │         │
            ┌───────┴───┐ ┌───┴───────┐
            │  PORTÃO   │ │  PORTÃO   │
            │ PEDESTRES │ │ VEÍCULOS  │
            └───────┬───┘ └───┬───────┘
                    │         │
    ┌───────────────┴─────────┴───────────────┐
    │ Câmera 1 ─►  ┌───────────┐              │
    │ (entrada)    │  JARDIM   │    ◄─ Luz    │
    │              │  FRONTAL  │    constante │
    ├──────────────┴───────────┴──────────────┤
    │                                         │
    │  ┌─────────────────────────────────┐    │
    │  │         GARAGEM                 │◄── │ Câmera 2
    │  │                                 │    │
    │  └────────────┬────────────────────┘    │
    │               │                         │
    │  ┌────────────┴────────────────────┐    │
    │  │                                 │    │
    │  │         C A S A                 │    │
    │  │  ┌─────┐           ┌─────┐      │    │
    │  │  │Sala │           │Coz. │      │    │ MURO
    │  │  │     │  Corredor │     │      │    │ LATERAL
    │  │  └─────┘           └─────┘      │◄───┤
    │  │  ┌─────┐           ┌─────┐      │    │ Câmera 3
    │  │  │Quarto│          │Quarto│     │    │ (lateral)
    │  │  └─────┘           └─────┘      │    │
    │  │                                 │    │
    │  └────────────┬────────────────────┘    │
    │               │                         │
    │  ┌────────────┴────────────────────┐    │
    │  │      QUINTAL / ÁREA DE          │◄── │ Câmera 4
    │  │      SERVIÇO / CHURRASQUEIRA    │    │ (fundos)
    │  │                                 │    │ + Luz sensor
    │  └─────────────────────────────────┘    │
    │                                         │
    └─────────────────────────────────────────┘
                    MURO FUNDOS

    LEGENDA:
    ━━━ Limite do lote (calçada/rua)
    ─── Muro/grade perimetral + cerca elétrica
    ◄── Posição de câmera
```

**Posicionamento de câmeras:**
- **Câmera 1**: Entrada (portões) - visão da rua, calçada e portões
- **Câmera 2**: Garagem - monitoramento de veículos e acesso
- **Câmera 3**: Lateral - cobertura do corredor lateral e janelas
- **Câmera 4**: Fundos/quintal - área de serviço e churrasqueira

**Posicionamento de sensores:**
- Sensor de abertura: portões, porta principal, porta de serviço, porta do quintal
- Sensor de movimento: quintal (cobertura ampla)
- Sensor de quebra de vidro: janelas térreo (opcional se houver grades)

---

## 4. Cenário 3: Apartamento

### 4.1 Características do cenário

| Aspecto | Descrição |
|---------|-----------|
| **Perímetro** | Inexistente (responsabilidade do condomínio) |
| **Área** | 40m² a 200m² |
| **Vizinhança** | Muito próxima, portaria como primeira barreira |
| **Acesso** | Porta principal única (normalmente) |
| **Infraestrutura** | Energia e internet estáveis |
| **Riscos principais** | Invasão pela porta, engenharia social na portaria |

### 4.2 Requisitos de segurança passiva (T-003)

#### Zona 1-2: Perímetro e área externa (condomínio)

> **Nota**: A segurança perimetral é responsabilidade do condomínio. O morador deve:
> - Verificar se o condomínio possui portaria 24h ou controle de acesso
> - Avaliar câmeras em áreas comuns
> - Participar de decisões de segurança condominial

#### Zona 3: Envelope (porta e janelas)

| Elemento | Especificação | Prioridade |
|----------|---------------|------------|
| **Porta principal** | Blindada ou reforçada, fechadura multiponto (3+ pontos) | Alta |
| **Fechadura** | Cilindro europeu com proteção anti-arrombamento | Alta |
| **Protetor de cilindro** | Escudo metálico ao redor da fechadura | Alta |
| **Olho mágico** | Digital com câmera (opcional) ou tradicional grande angular | Média |
| **Batente** | Metálico ou reforçado com parafusos longos | Alta |
| **Dobradiças** | Internas (não acessíveis pelo lado de fora) ou com pino anti-remoção | Alta |
| **Tranca adicional** | Ferrolho ou trava de segurança na parte inferior | Média |
| **Janelas térreo/1º andar** | Grades ou telas de segurança, vidro laminado | Alta |
| **Janelas andares altos** | Trincos reforçados (menor risco de invasão) | Baixa |
| **Varanda acessível** | Grade ou fechamento, atenção a varandas próximas | Média |

#### Zona 4: Interior

| Elemento | Especificação | Prioridade |
|----------|---------------|------------|
| **Cofre** | Pequeno, embutido ou fixado, para documentos e valores | Média |
| **Objetos de valor** | Não visíveis da porta ou janelas | Alta |

### 4.3 Diagrama de posicionamento – Apartamento (T-010)

```
    ┌─────────────────────────────────────────────────────┐
    │                    CORREDOR                         │
    │                   DO PRÉDIO                         │
    │                                                     │
    │    ┌──────────────────────────────────────────┐     │
    │    │              APARTAMENTO                 │     │
    │    │                                          │     │
    │    │  ┌────────┐  ┌────────┐  ┌────────┐     │     │
    │    │  │        │  │        │  │        │     │     │
    │    │  │ QUARTO │  │ QUARTO │  │ BANHO  │     │     │
    │    │  │   1    │  │   2    │  │        │     │     │
    │    │  │        │  │        │  │        │     │     │
    │    │  └────────┘  └────────┘  └────────┘     │     │
    │    │                                          │     │
    │    │  ┌─────────────────────────────────┐     │     │
    │    │  │                                 │     │     │
    │    │  │      SALA / LIVING              │     │     │
    │    │  │                                 │     │     │
    │    │  │                      ┌──────┐   │     │     │
    │    │  │                      │Coz.  │   │     │     │
    │    │  │                      │      │   │     │     │
    │    │  │                      └──────┘   │     │     │
    │    │  │                                 │     │     │
    │    │  └─────────────────────────────────┘     │     │
    │    │                                          │     │
    │    │  ════════════════════════════════════   │     │
    │    │              VARANDA                     │     │
    │    │  (se houver - verificar acesso)         │     │
    │    │  ════════════════════════════════════   │     │
    │    │                                          │     │
    │    └──────────────────────────────────────────┘     │
    │              ▲                                       │
    │              │                                       │
    │    ┌────────┴────────┐                              │
    │    │  PORTA BLINDADA │◄── Sensor de abertura        │
    │    │  + Olho mágico  │    Câmera olho mágico (opc.) │
    │    │  digital        │                              │
    │    └─────────────────┘                              │
    │                                                     │
    └─────────────────────────────────────────────────────┘

    COMPONENTES RECOMENDADOS:

    1. PORTA BLINDADA com:
       - Fechadura multiponto (mínimo 3 pontos)
       - Cilindro europeu com protetor
       - Dobradiças internas ou com pino anti-remoção
       - Batente metálico reforçado

    2. OLHO MÁGICO DIGITAL (opcional):
       - Câmera com visão noturna
       - Gravação em cartão SD
       - Visualização em tela interna

    3. SENSOR DE ABERTURA:
       - Na porta principal
       - Integrado ao sistema de alarme

    4. SENSOR DE MOVIMENTO (opcional):
       - Cobertura da sala/corredor interno
       - Ativado apenas quando ausente
```

**Posicionamento de sensores:**
- **Sensor de abertura**: Porta principal (obrigatório)
- **Sensor de movimento**: Sala/corredor interno (opcional, ativado quando ausente)
- **Câmera interna**: Não recomendada por privacidade; preferir olho mágico digital

---

## 5. Requisitos de Segurança Reativa (T-007)

### 5.1 Conceito

A segurança reativa define **o que acontece quando** uma barreira é ultrapassada ou uma ameaça é detectada. Inclui notificações, procedimentos de resposta e registro de evidências.

### 5.2 Requisitos por camada

#### Detecção

| Requisito | Descrição | Implementação |
|-----------|-----------|---------------|
| **Detecção imediata** | Sistema deve detectar invasão em < 5 segundos | Sensores em todos os pontos de entrada |
| **Redundância** | Múltiplos sensores em caminhos críticos | PIR + abertura, ou PIR + câmera |
| **Anti-mascaramento** | Detectar tentativa de bloquear sensor | Sensores com recurso anti-tamper |

#### Alerta

| Requisito | Descrição | Implementação |
|-----------|-----------|---------------|
| **Alerta sonoro local** | Sirene audível para dissuasão | Sirene interna (90dB+) + externa (110dB+) |
| **Alerta silencioso** | Opção para não alertar invasor | Modo pânico silencioso |
| **Notificação instantânea** | Proprietário notificado em < 30 segundos | Push notification, SMS, chamada |
| **Múltiplos canais** | Redundância de notificação | App + SMS + e-mail |
| **Contatos de emergência** | Lista de pessoas a notificar | Mínimo 2-3 contatos |

#### Resposta

| Requisito | Descrição | Implementação |
|-----------|-----------|---------------|
| **Plano de ação documentado** | Procedimento claro por tipo de alerta | Documento acessível a todos os moradores |
| **Contato com autoridades** | Procedimento para acionar polícia | Número salvo, script de comunicação |
| **Vizinhança** | Rede de apoio com vizinhos | Grupo de comunicação (WhatsApp) |
| **Refúgio seguro** | Local para se abrigar se invasão em curso | Cômodo com tranca, comunicação externa |

#### Registro de evidências

| Requisito | Descrição | Implementação |
|-----------|-----------|---------------|
| **Gravação contínua** | Câmeras gravando 24/7 | NVR com armazenamento local |
| **Preservação de incidentes** | Gravações de alarmes não sobrescritas | Flag automático ou manual |
| **Retenção mínima** | Manter gravações por período adequado | 30 dias (rotação), incidentes preservados |
| **Acesso às evidências** | Fácil exportação para autoridades | Interface de download por período |
| **Log de eventos** | Histórico de todos os eventos do sistema | Log com timestamp, tipo, zona |

### 5.3 Plano de resposta a incidentes

#### Tipos de alerta e ações

| Tipo de alerta | Ação automática | Ação do morador |
|----------------|-----------------|-----------------|
| **Sensor de abertura (armado)** | Notificação, sirene após delay, gravação | Verificar câmeras, desarmar se falso alarme |
| **Sensor de movimento (armado)** | Notificação, sirene após delay, gravação | Verificar câmeras, desarmar se falso alarme |
| **Botão de pânico** | Notificação silenciosa, gravação, alerta a contatos | Aguardar em local seguro, não confrontar |
| **Queda de energia** | Notificação (se bateria), switch para nobreak | Verificar se é falha geral ou ataque |
| **Câmera offline** | Notificação de falha | Verificar conectividade, possível sabotagem |
| **Cerca elétrica disparada** | Notificação, gravação | Verificar câmeras do perímetro |

#### Procedimento em caso de invasão confirmada

```
1. NÃO CONFRONTAR o invasor
2. Ir para local seguro (cômodo com tranca, se disponível)
3. Ligar para polícia (190)
   - Informar: endereço completo, situação, número de invasores (se souber)
4. Notificar contatos de emergência
5. Permanecer em silêncio e aguardar autoridades
6. Preservar gravações após o incidente
7. Registrar boletim de ocorrência
```

### 5.4 Continuidade operacional

| Requisito | Descrição | Implementação |
|-----------|-----------|---------------|
| **Nobreak** | Sistema funciona em queda de energia | Autonomia mínima 30 min (central + roteador) |
| **Bateria de sensores** | Sensores wireless com bateria | Monitorar nível, trocar preventivamente |
| **Internet backup** | Notificações funcionam sem internet principal | 4G como failover (opcional) |
| **Backup de configuração** | Recuperação rápida após falha | Backup automático semanal |

---

## 6. Tabela comparativa dos cenários

| Aspecto | Rural | Casa Urbana | Apartamento |
|---------|-------|-------------|-------------|
| **Perímetro** | Cerca + cerca elétrica | Muro + cerca elétrica | Responsabilidade do condomínio |
| **Pontos de entrada** | Portão principal, sede | Portões, portas, janelas térreo | Porta principal |
| **Nº câmeras sugerido** | 4-6 | 3-5 | 0-1 (olho mágico digital) |
| **Nº sensores sugerido** | 4-8 | 6-10 | 2-4 |
| **Iluminação** | Solar/sensor | Constante + sensor | Responsabilidade do condomínio |
| **Tempo de resposta polícia** | Longo (30min+) | Médio (10-20min) | Curto (5-15min) |
| **Investimento relativo** | Alto | Médio | Baixo |
| **Complexidade** | Alta | Média | Baixa |

---

## 7. Checklist de implementação

### Segurança passiva

- [ ] Perímetro fechado e em bom estado
- [ ] Cerca elétrica instalada e sinalizada (se aplicável)
- [ ] Portões com fechadura de segurança
- [ ] Iluminação externa funcionando
- [ ] Portas reforçadas com fechadura multiponto
- [ ] Janelas térreo com grades ou vidro reforçado
- [ ] Batentes fixados com parafusos longos
- [ ] Paisagismo não cria esconderijos
- [ ] Objetos de valor não visíveis de fora

### Segurança reativa

- [ ] Plano de resposta documentado e conhecido por moradores
- [ ] Contatos de emergência cadastrados no sistema
- [ ] Números de emergência salvos (190, vizinhos)
- [ ] Nobreak instalado e testado
- [ ] Backup de configurações realizado
- [ ] Teste periódico do sistema (mensal)

---

## Referências

- [Defesa em Profundidade Aplicada a Segurança Privada](https://gestaodesegurancaprivada.com.br/defesa-em-profundidade-aplicada-a-seguranca-privada/)
- [Segurança Passiva no Contexto da Segurança Física](https://gestaodesegurancaprivada.com.br/seguranca-passiva-no-contexto-da-seguranca-fisica-conheca-as-principais-estrategias/)
- [Guia completo de proteção residencial - Meerkat](https://www.meerkat.com.br/2025/10/20/guia-completo-de-protecao-residencial-avaliacao-medidas-de-baixo-custo-tecnologia-eficaz-e-checklist-rapido-em-7-dias/)
- [Segurança em propriedades rurais - Provincial](https://www.provincial.com.br/seguranca-em-areas-rurais-como-proteger-propriedades-com-tecnologia-avancada/)
- [Prevenção do crime através do desenho urbano (CPTED) - Wikipedia](https://pt.wikipedia.org/wiki/Preven%C3%A7%C3%A3o_do_crime_atrav%C3%A9s_do_desenho_urbano)
- [Posicionamento de câmeras - Locatronic](https://locatronic.com.br/blog/dicas-seguranca-posicionamento-ideal-cameras-para-cobertura-completa/)

---

> **Próximos passos**: Este documento deve ser usado como base para os PRDs de cada cenário (PRD_PERIMETER_RURAL, PRD_PERIMETER_URBAN_HOUSE, PRD_APARTMENT_SECURITY).

