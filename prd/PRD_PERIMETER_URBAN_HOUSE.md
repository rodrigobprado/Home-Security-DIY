# PRD – Segurança de Perímetro Casa Urbana

> Sistema de Home Security – Open Source / Open Hardware
>
> Versão: 1.0 | Data: 2026-02-12 | Responsável: Agente_Documentador

---

## 1. Visão geral

- **Nome do produto/funcionalidade**: Sistema de Segurança para Casa Urbana com Quintal
- **Responsável**: Agente_Arquiteto_Seguranca_Fisica (requisitos), Agente_Documentador (documentação)
- **Data**: 2026-02-12
- **PRDs relacionados**: PRD_SENSORS_AND_ALARMS_PLATFORM, PRD_VIDEO_SURVEILLANCE_AND_NVR, PRD_HOUSE_ENVELOPE

---

## 2. Problema e oportunidade

### 2.1 Problema

Casas urbanas com quintal apresentam desafios específicos:
- **Múltiplos pontos de vulnerabilidade**: muros, portões, janelas, portas
- **Quintal como área de transição**: local frequentemente usado por invasores
- **Equilíbrio estético**: soluções precisam harmonizar com a residência
- **Vizinhança próxima**: preocupação com falsos alarmes e ruídos

### 2.2 Oportunidade

Implementar um sistema integrado de proteção com:
- **Cobertura completa** de perímetro, envelope e interior
- **Detecção inteligente** que minimize falsos positivos
- **Integração estética** com soluções discretas
- **Tempo de resposta rápido** aproveitando proximidade urbana

---

## 3. Público-alvo

| Perfil | Características | Necessidades |
|--------|-----------------|--------------|
| **Família residente** | Ocupação contínua, crianças/idosos | Segurança + usabilidade diária |
| **Casal trabalhador** | Casa vazia durante dia | Monitoramento remoto |
| **Profissional home office** | Presença parcial | Equilíbrio segurança/conveniência |

---

## 4. Características do cenário

| Aspecto | Descrição |
|---------|-----------|
| **Perímetro típico** | 50m a 200m de extensão |
| **Área** | 200m² a 1.000m² |
| **Vizinhança** | Próxima, vigilância natural moderada |
| **Acesso** | Portão de pedestres, portão de veículos, muros laterais |
| **Infraestrutura** | Energia e internet estáveis |
| **Riscos principais** | Invasão por muro/portão, janelas térreo |

---

## 5. Requisitos funcionais

### 5.1 Zona 1: Perímetro (muro/grade)

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-001 | Muro frontal | 2,0m a 2,5m de altura, sem apoios para escalar | Alta |
| RF-002 | Muros laterais e fundos | Mesma altura, verificar vizinhos | Alta |
| RF-003 | Cerca elétrica sobre muro | Altura total ≥2,50m, sinalização obrigatória | Alta |
| RF-004 | Alternativa: concertina | Verificar legislação local | Média |
| RF-005 | Portão de pedestres | Metálico, fechadura de segurança, altura do muro | Alta |
| RF-006 | Portão de veículos | Metálico, automatizado, sensor anti-esmagamento | Alta |
| RF-007 | Câmera na entrada | Visão de rua, calçada e portões | Alta |

### 5.2 Zona 2: Área externa (quintal)

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-008 | Iluminação frontal | LED constante à noite, baixo consumo | Alta |
| RF-009 | Iluminação lateral/fundos | Com sensor de presença | Alta |
| RF-010 | Câmera na garagem | Monitoramento de veículos e acesso | Alta |
| RF-011 | Câmera no quintal/fundos | Área de serviço, churrasqueira | Alta |
| RF-012 | Câmera lateral | Corredor lateral e janelas (opcional) | Média |
| RF-013 | Sensor de movimento externo | PIR cobrindo quintal | Média |
| RF-014 | Paisagismo defensivo | Plantas espinhosas junto ao muro | Média |
| RF-015 | Visibilidade | Evitar arbustos que criem esconderijos | Alta |
| RF-016 | Objetos no quintal | Guardar escadas, ferramentas | Alta |

### 5.3 Zona 3: Envelope (portas e janelas)

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-017 | Porta principal | Madeira maciça ou blindada, fechadura multiponto | Alta |
| RF-018 | Porta de serviço | Reforçada, tranca adicional | Alta |
| RF-019 | Porta para quintal | Grade ou vidro reforçado com fechadura | Alta |
| RF-020 | Janelas térreo frente | Grades decorativas ou vidro laminado | Alta |
| RF-021 | Janelas térreo fundos | Grades (maior risco, menos visíveis) | Alta |
| RF-022 | Janelas superiores | Trincos reforçados, grades em varandas | Média |
| RF-023 | Batentes | Parafusos longos, protetor de cilindro | Alta |
| RF-024 | Sensores de abertura portas | Zigbee em todas as portas externas | Alta |
| RF-025 | Sensores de abertura janelas térreo | Zigbee (4-8 unidades) | Alta |
| RF-026 | Sensor de quebra de vidro | Acústico, em janelas sem grade | Média |

### 5.4 Zona 4: Interior

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-027 | Sensor de movimento sala | PIR | Alta |
| RF-028 | Sensor de movimento corredor | PIR | Alta |
| RF-029 | Cofre | Embutido ou fixado, para documentos e valores | Média |
| RF-030 | Objetos de valor | Não visíveis de janelas | Alta |

### 5.5 Sistema de alarme

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-031 | Sirene externa | 110dB+, discreta no muro | Alta |
| RF-032 | Sirene interna | 90dB+ | Alta |
| RF-033 | Teclado/painel de controle | Para armar/desarmar na entrada | Alta |
| RF-034 | Botão de pânico | Discreto | Média |
| RF-035 | Modos de armamento | Total, noite (parcial), perímetro | Alta |
| RF-036 | Delay de entrada/saída | Configurável | Alta |

---

## 6. Requisitos não funcionais

### 6.1 Performance

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-001 | Detecção de invasão | < 5 segundos |
| RNF-002 | Notificação após alarme | < 30 segundos |
| RNF-003 | Latência de streaming | < 500ms |

### 6.2 Usabilidade

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-004 | Armar/desarmar | < 3 toques no app ou teclado |
| RNF-005 | Integração com rotina | Auto-armar ao sair, desarmar ao chegar |
| RNF-006 | Feedback | Bips de confirmação configuráveis |

### 6.3 Estética

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-007 | Câmeras | Modelos discretos, cor neutra |
| RNF-008 | Grades | Decorativas, harmonizadas com fachada |
| RNF-009 | Cerca elétrica | Fios discretos, sinalização padronizada |

### 6.4 Conformidade

| ID | Requisito | Norma/Regra |
|----|-----------|-------------|
| RNF-010 | Cerca elétrica | Lei 13.477/2017, REGRA-CERCA-01 a 06 |
| RNF-011 | Câmeras | REGRA-CFTV-05 a 12 |
| RNF-012 | LGPD | REGRA-LGPD-01 a 05 (se capturar calçada/rua) |

---

## 7. Arquitetura física

### 7.1 Diagrama de posicionamento

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
    │  │  ┌─────┐           ┌─────┐      │    │ MURO
    │  │  │Sala │           │Coz. │      │    │ LATERAL
    │  │  │ S1  │  Corredor │     │      │◄───┤
    │  │  └─────┘    S2     └─────┘      │    │ Câmera 3
    │  │  ┌─────┐           ┌─────┐      │    │ (lateral)
    │  │  │Quarto│          │Quarto│     │    │
    │  │  └─────┘           └─────┘      │    │
    │  │                                 │    │
    │  └────────────┬────────────────────┘    │
    │               │                         │
    │  ┌────────────┴────────────────────┐    │
    │  │      QUINTAL / ÁREA DE          │◄── │ Câmera 4
    │  │      SERVIÇO / CHURRASQUEIRA    │    │ (fundos)
    │  │              S3                 │    │ + Luz sensor
    │  └─────────────────────────────────┘    │
    │                                         │
    └─────────────────────────────────────────┘
                    MURO FUNDOS

    LEGENDA:
    ━━━ Limite do lote (calçada/rua)
    ─── Muro/grade + cerca elétrica
    ◄── Posição de câmera
    Sx  Posição de sensor PIR
```

### 7.2 Posicionamento de câmeras

| Câmera | Localização | Função | Especificação |
|--------|-------------|--------|---------------|
| 1 | Entrada (portões) | Rua, calçada, portões | Bullet/Dome PoE 4MP |
| 2 | Garagem | Veículos, acesso interno | Dome PoE 4MP |
| 3 | Lateral | Corredor lateral, janelas | Bullet PoE 4MP |
| 4 | Fundos/quintal | Área de serviço, churrasqueira | Bullet PoE 4MP, wide |

### 7.3 Posicionamento de sensores

| Sensor | Localização | Tipo | Protocolo |
|--------|-------------|------|-----------|
| Porta 1 | Porta principal | Abertura | Zigbee |
| Porta 2 | Porta de serviço | Abertura | Zigbee |
| Porta 3 | Porta do quintal | Abertura | Zigbee |
| J1-J4 | Janelas térreo frente | Abertura | Zigbee |
| J5-J8 | Janelas térreo fundos | Abertura | Zigbee |
| S1 | Sala | Movimento PIR | Zigbee |
| S2 | Corredor | Movimento PIR | Zigbee |
| S3 | Quintal | Movimento PIR | Zigbee |
| V1-V2 | Janelas sem grade | Quebra de vidro | Zigbee |

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
| Câmera PoE 4MP (Reolink) | 3-4 | R$ 350 | R$ 1.050-1.400 |
| Switch PoE 8 portas | 1 | R$ 400 | R$ 400 |
| **Sensores** |
| Coordenador Zigbee | 1 | R$ 150 | R$ 150 |
| Sensor abertura | 8-11 | R$ 50 | R$ 400-550 |
| Sensor PIR | 2-3 | R$ 70 | R$ 140-210 |
| Sensor quebra de vidro | 1-2 | R$ 80 | R$ 80-160 |
| Sirene externa | 1 | R$ 150 | R$ 150 |
| Sirene interna | 1 | R$ 120 | R$ 120 |
| Teclado/painel Zigbee | 1 | R$ 120 | R$ 120 |
| **Infraestrutura** |
| Nobreak 600VA | 1 | R$ 400 | R$ 400 |
| Cabeamento, conectores | - | R$ 200 | R$ 200 |

### 8.2 Total estimado

| Item | Faixa de preço |
|------|----------------|
| **Configuração mínima** (3 câmeras, 11 sensores) | R$ 4.510 |
| **Configuração recomendada** (4 câmeras, 14 sensores) | R$ 5.360 |
| **Instalação profissional** (opcional) | R$ 800-1.500 |

---

## 9. Critérios de aceitação

| ID | Critério | Método de verificação |
|----|----------|----------------------|
| CA-001 | Cobertura de câmeras sem pontos cegos no perímetro | Teste de cobertura |
| CA-002 | Todas as portas e janelas térreo com sensor | Inventário |
| CA-003 | Alarme dispara corretamente nos modos total/noite/perímetro | Teste funcional |
| CA-004 | Delay de entrada/saída funciona conforme configurado | Teste funcional |
| CA-005 | Notificação recebida em < 30 segundos | Teste com cronômetro |
| CA-006 | PIR externo não dispara com gatos/cachorros pequenos | Teste de sensibilidade |
| CA-007 | Sistema opera por 30 min sem energia | Teste de interrupção |
| CA-008 | Acesso remoto via VPN funciona | Teste externo |

---

## 10. Métricas de sucesso

| Métrica | Alvo | Medição |
|---------|------|---------|
| **Falsos positivos** | < 1/semana | Contagem |
| **Cobertura** | 100% pontos de entrada | Mapeamento |
| **Adoção pela família** | 100% usando app | Pesquisa |
| **Satisfação** | > 4/5 | Feedback |

---

## 11. Riscos e mitigações

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Animais de estimação causam alarmes | Alta | Médio | PIR pet-immune, ajuste sensibilidade |
| Vizinhos reclamam de sirene | Média | Médio | Tempo de sirene limitado, notificação prioritária |
| Câmera captando vizinho/rua | Média | Alto | Ajustar ângulo, máscaras de privacidade |
| Portão automatizado falha | Baixa | Médio | Manutenção preventiva |
| Grades prejudicam estética | Média | Baixo | Grades decorativas, vidro laminado |

---

## 12. Referências

### Documentos do projeto
- `docs/ARQUITETURA_SEGURANCA_FISICA.md` - Seções 3, 5, 7
- `docs/ARQUITETURA_TECNICA.md` - Seção 1.2
- `rules/RULES_COMPLIANCE_AND_STANDARDS.md`

---

> **Status**: Rascunho v1.0
>
> **Próxima revisão**: Após validação pelo Agente_Arquiteto_Seguranca_Fisica
