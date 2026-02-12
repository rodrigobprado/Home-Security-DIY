# PRD – Segurança de Apartamento

> Sistema de Home Security – Open Source / Open Hardware
>
> Versão: 1.0 | Data: 2026-02-12 | Responsável: Agente_Documentador

---

## 1. Visão geral

- **Nome do produto/funcionalidade**: Sistema de Segurança para Apartamento
- **Responsável**: Agente_Arquiteto_Seguranca_Fisica (requisitos), Agente_Documentador (documentação)
- **Data**: 2026-02-12
- **PRDs relacionados**: PRD_SENSORS_AND_ALARMS_PLATFORM, PRD_APARTMENT_SMART_LOCK

---

## 2. Problema e oportunidade

### 2.1 Problema

Apartamentos possuem características específicas que limitam opções de segurança:
- **Perímetro compartilhado**: Segurança externa é responsabilidade do condomínio
- **Ponto de entrada único**: Porta principal é o principal (e geralmente único) ponto vulnerável
- **Restrições de instalação**: Modificações estruturais limitadas pelo regulamento
- **Vizinhança próxima**: Preocupação com ruídos e privacidade

### 2.2 Oportunidade

Implementar um sistema focado em:
- **Proteção do envelope** (porta principal como prioridade absoluta)
- **Monitoramento discreto** adequado ao ambiente condominial
- **Instalação não invasiva** sem modificações estruturais
- **Custo reduzido** devido ao escopo menor

---

## 3. Público-alvo

| Perfil | Características | Necessidades |
|--------|-----------------|--------------|
| **Morador individual** | Apartamento pequeno, solteiro(a) | Simplicidade, custo baixo |
| **Casal** | Apartamento médio | Usabilidade, notificações para ambos |
| **Família** | Apartamento grande, crianças | Controle de acesso, monitoramento |
| **Idoso** | Qualquer tamanho | Facilidade de uso, botão de pânico |

---

## 4. Características do cenário

| Aspecto | Descrição |
|---------|-----------|
| **Perímetro** | Inexistente (responsabilidade do condomínio) |
| **Área** | 40m² a 200m² |
| **Vizinhança** | Muito próxima, portaria como primeira barreira |
| **Acesso** | Porta principal única (normalmente) |
| **Infraestrutura** | Energia e internet estáveis |
| **Riscos principais** | Invasão pela porta, engenharia social na portaria |

---

## 5. Requisitos funcionais

### 5.1 Zona 1-2: Perímetro e área comum (condomínio)

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-001 | Verificar portaria 24h ou controle de acesso | Avaliação do condomínio | Alta |
| RF-002 | Avaliar câmeras em áreas comuns | Avaliação do condomínio | Média |
| RF-003 | Participar de decisões de segurança condominial | Engajamento | Média |

> **Nota**: A segurança perimetral é responsabilidade do condomínio. O morador deve participar ativamente das decisões de segurança condominial.

### 5.2 Zona 3: Envelope (porta principal)

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-004 | Porta blindada ou reforçada | Substituição ou reforço | Alta |
| RF-005 | Fechadura multiponto | Mínimo 3 pontos de travamento | Alta |
| RF-006 | Cilindro europeu | Com proteção anti-arrombamento | Alta |
| RF-007 | Protetor de cilindro | Escudo metálico | Alta |
| RF-008 | Batente reforçado | Metálico ou com parafusos longos | Alta |
| RF-009 | Dobradiças protegidas | Internas ou com pino anti-remoção | Alta |
| RF-010 | Olho mágico digital | Câmera com visão noturna, gravação | Média |
| RF-011 | Tranca adicional | Ferrolho ou trava na parte inferior | Média |
| RF-012 | Sensor de abertura porta | Zigbee | Alta |

### 5.3 Janelas (quando aplicável)

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-013 | Janelas térreo/1º andar | Grades ou telas de segurança | Alta* |
| RF-014 | Varanda acessível | Grade ou fechamento | Alta* |
| RF-015 | Janelas andares altos | Trincos reforçados | Baixa |
| RF-016 | Sensor de abertura janela | Apenas se acessível de fora | Média* |

> *Prioridade alta apenas se o apartamento for em andar baixo ou tiver varanda acessível.

### 5.4 Zona 4: Interior

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-017 | Sensor de movimento entrada | PIR na área de entrada | Alta |
| RF-018 | Sensor de movimento sala | PIR (opcional, modo ausente) | Baixa |
| RF-019 | Cofre pequeno | Para documentos e valores | Média |
| RF-020 | Objetos de valor | Não visíveis da porta | Alta |

### 5.5 Sistema de alarme

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-021 | Sirene interna | 85-90dB (considerar vizinhos) | Alta |
| RF-022 | Botão de pânico | Discreto, fácil acesso | Alta |
| RF-023 | Modos de armamento | Desarmado, armado (ausente), parcial (em casa) | Alta |
| RF-024 | Delay de entrada | Configurável (15-45 segundos) | Alta |
| RF-025 | Notificação push | App Home Assistant | Alta |
| RF-026 | Notificação Telegram | Backup de notificação | Alta |

### 5.6 Fechadura inteligente (opcional)

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-027 | Múltiplos modos de acesso | Senha, biometria, app, chave física | Média |
| RF-028 | Auditoria de acessos | Log de quem entrou e quando | Média |
| RF-029 | Integração com automação | Desarmar ao desbloquear | Média |
| RF-030 | Código temporário | Para visitantes/prestadores | Baixa |

---

## 6. Requisitos não funcionais

### 6.1 Usabilidade

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-001 | Armar/desarmar | < 2 toques no app ou automático |
| RNF-002 | Ver quem está na porta | Via olho mágico digital ou câmera |
| RNF-003 | Interface | Simples, adequada para não-técnicos |

### 6.2 Discrição

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-004 | Sirene | Volume moderado (85-90dB), não incomodar vizinhos |
| RNF-005 | Equipamentos | Discretos, sem chamar atenção no corredor |
| RNF-006 | Câmera interna | Não recomendada por privacidade |

### 6.3 Instalação

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-007 | Sem furação excessiva | Sensores wireless (Zigbee) |
| RNF-008 | Reversível | Possível remover ao mudar |
| RNF-009 | Sem modificação estrutural | Exceto porta/fechadura |

### 6.4 Conformidade

| ID | Requisito | Norma/Regra |
|----|-----------|-------------|
| RNF-010 | Regulamento do condomínio | Verificar restrições de instalação |
| RNF-011 | LGPD | Olho mágico digital apenas para área do corredor |

---

## 7. Arquitetura física

### 7.1 Diagrama de posicionamento

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
    │    │  │          [PIR S1]               │     │     │
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
    │    │  + Olho mágico  │    Olho mágico digital       │
    │    │  digital        │    Fechadura inteligente     │
    │    └─────────────────┘                              │
    │                                                     │
    └─────────────────────────────────────────────────────┘

    COMPONENTES:

    1. PORTA BLINDADA:
       - Fechadura multiponto (mínimo 3 pontos)
       - Cilindro europeu com protetor
       - Dobradiças internas ou com pino anti-remoção
       - Batente metálico reforçado

    2. OLHO MÁGICO DIGITAL (opcional):
       - Câmera com visão noturna
       - Gravação em cartão SD
       - Visualização em tela interna ou app

    3. SENSOR DE ABERTURA:
       - Na porta principal (Zigbee)
       - Integrado ao sistema de alarme

    4. SENSOR DE MOVIMENTO (PIR S1):
       - Cobertura da sala/corredor interno
       - Ativado apenas quando ausente
```

### 7.2 Lista de componentes

| Componente | Localização | Tipo | Obrigatório |
|------------|-------------|------|-------------|
| Sensor abertura | Porta principal | Zigbee | Sim |
| Sensor PIR | Entrada/sala | Zigbee | Sim |
| Olho mágico digital | Porta | Wi-Fi | Opcional |
| Fechadura inteligente | Porta | Zigbee/Wi-Fi | Opcional |
| Sirene interna | Sala ou entrada | Zigbee | Sim |
| Botão de pânico | Quarto ou sala | Zigbee | Recomendado |
| Central | Qualquer local | Mini PC | Sim |

---

## 8. Estimativa de investimento

### 8.1 Configuração mínima

| Componente | Quantidade | Preço unitário | Subtotal |
|------------|------------|----------------|----------|
| **Central de processamento** |
| Mini PC Intel N100 8GB | 1 | R$ 800 | R$ 800 |
| SSD 256GB | 1 | R$ 150 | R$ 150 |
| **Sensores** |
| Coordenador Zigbee | 1 | R$ 150 | R$ 150 |
| Sensor abertura porta | 1 | R$ 50 | R$ 50 |
| Sensor PIR | 1 | R$ 70 | R$ 70 |
| Sirene interna | 1 | R$ 100 | R$ 100 |
| Botão de pânico | 1 | R$ 80 | R$ 80 |
| **Infraestrutura** |
| Nobreak 600VA | 1 | R$ 300 | R$ 300 |
| **Total mínimo** | | | **R$ 1.700** |

### 8.2 Configuração recomendada

| Componente | Quantidade | Preço unitário | Subtotal |
|------------|------------|----------------|----------|
| Configuração mínima | - | - | R$ 1.700 |
| Olho mágico digital (Aqara G4) | 1 | R$ 600 | R$ 600 |
| Sensor PIR adicional | 1 | R$ 70 | R$ 70 |
| **Total recomendado** | | | **R$ 2.370** |

### 8.3 Configuração completa (com fechadura)

| Componente | Quantidade | Preço unitário | Subtotal |
|------------|------------|----------------|----------|
| Configuração recomendada | - | - | R$ 2.370 |
| Fechadura inteligente Zigbee | 1 | R$ 800 | R$ 800 |
| Porta blindada (se necessário) | 1 | R$ 2.500 | R$ 2.500 |
| **Total completo** | | | **R$ 3.170 - 5.670** |

### 8.4 Resumo

| Configuração | Investimento |
|--------------|--------------|
| **Mínima** (sensor + sirene) | R$ 1.700 |
| **Recomendada** (+ olho digital) | R$ 2.370 |
| **Completa** (+ fechadura) | R$ 3.170 |
| **Premium** (+ porta blindada) | R$ 5.670 |

---

## 9. Critérios de aceitação

| ID | Critério | Método de verificação |
|----|----------|----------------------|
| CA-001 | Porta com fechadura multiponto instalada | Inspeção |
| CA-002 | Sensor de abertura detecta porta corretamente | Teste funcional |
| CA-003 | PIR detecta movimento na entrada | Teste funcional |
| CA-004 | Sirene dispara com volume adequado (não excessivo) | Teste com medidor |
| CA-005 | Notificação recebida em < 30 segundos | Teste com cronômetro |
| CA-006 | Olho mágico digital mostra quem está na porta | Teste funcional |
| CA-007 | Sistema opera por 30 min sem energia | Teste de interrupção |
| CA-008 | Acesso remoto via VPN funciona | Teste externo |

---

## 10. Métricas de sucesso

| Métrica | Alvo | Medição |
|---------|------|---------|
| **Falsos positivos** | < 1/mês | Contagem |
| **Facilidade de uso** | > 4/5 | Feedback |
| **Adoção do botão de pânico** | 100% moradores sabem usar | Treinamento |
| **Satisfação** | > 4/5 | Feedback |

---

## 11. Riscos e mitigações

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Sirene incomoda vizinhos | Média | Médio | Volume moderado, tempo limitado |
| Olho digital captando vizinho | Baixa | Médio | Ângulo apenas para corredor próprio |
| Fechadura inteligente trava | Baixa | Alto | Manter chave física de backup |
| Condomínio não permite instalação | Baixa | Alto | Verificar regulamento antes |
| Esquecimento do código de alarme | Média | Baixo | App + código de backup |

---

## 12. Comparativo com outros cenários

| Aspecto | Apartamento | Casa Urbana | Rural |
|---------|-------------|-------------|-------|
| **Nº câmeras** | 0-1 | 3-5 | 4-6 |
| **Nº sensores** | 3-5 | 8-15 | 10-20 |
| **Foco principal** | Porta | Envelope | Perímetro |
| **Investimento** | R$ 1.700-3.000 | R$ 4.500-5.500 | R$ 5.500-6.500 |
| **Complexidade** | Baixa | Média | Alta |
| **Instalação** | Simples | Moderada | Complexa |

---

## 13. Referências

### Documentos do projeto
- `docs/ARQUITETURA_SEGURANCA_FISICA.md` - Seções 4, 5, 7
- `docs/ARQUITETURA_TECNICA.md` - Seção 1.3
- `rules/RULES_COMPLIANCE_AND_STANDARDS.md`

### Externos
- Guias de segurança residencial para apartamentos
- Especificações de portas blindadas

---

> **Status**: Rascunho v1.0
>
> **Próxima revisão**: Após validação pelo Agente_Arquiteto_Seguranca_Fisica
