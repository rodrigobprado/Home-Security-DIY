# PRD – Envelope da Casa (Proteção de Portas e Janelas)

> Sistema de Home Security – Open Source / Open Hardware
>
> Versão: 1.0 | Data: 2026-02-18 | Responsável: Agente_Documentador

---

## 1. Visão geral

- **Nome do produto/funcionalidade**: Sistema de Proteção do Envelope Residencial (Portas, Janelas e Fechaduras)
- **Responsável**: Agente_Arquiteto_Seguranca_Fisica (requisitos), Agente_Documentador (documentação)
- **Data**: 2026-02-18
- **PRDs relacionados**: PRD_PERIMETER_URBAN_HOUSE, PRD_SENSORS_AND_ALARMS_PLATFORM, PRD_AUTOMATION_AND_SCENES, PRD_APARTMENT_SMART_LOCK

---

## 2. Problema e oportunidade

### 2.1 Problema

O envelope da casa (conjunto de portas, janelas e aberturas) representa a principal barreira entre a área externa e o interior da residência:
- **Portas frágeis**: Fechaduras simples com apenas 1 ponto de travamento são facilmente forçadas
- **Janelas vulneráveis**: Vidro comum quebra facilmente, trincos fracos são contornáveis
- **Falta de monitoramento**: Morador não sabe se portas/janelas estão abertas ou fechadas
- **Batentes fracos**: Parafusos curtos e madeira frágil cedem com força bruta
- **Pontos cegos**: Portas laterais e de serviço frequentemente negligenciadas

### 2.2 Oportunidade

Implementar um sistema completo de proteção de envelope com:
- **Reforço físico** de portas, fechaduras, batentes e janelas
- **Sensoriamento Zigbee** em todas as aberturas acessíveis
- **Detectores de quebra de vidro** para janelas sem grade
- **Fechaduras inteligentes** com múltiplos métodos de acesso
- **Integração com alarme** (Alarmo) para resposta automática a violações

---

## 3. Público-alvo

| Perfil | Características | Necessidades |
|--------|-----------------|--------------|
| **Proprietário de casa urbana** | Casa com quintal, múltiplas aberturas | Proteção completa de todas as aberturas |
| **Proprietário rural** | Sede com janelas térreo acessíveis | Reforço físico + sensoriamento |
| **Morador de apartamento térreo** | Janelas acessíveis da rua | Grades, sensores, reforço de porta |
| **Família com crianças** | Preocupação com segurança interna | Travamento seguro, alertas de janelas |

---

## 4. Requisitos funcionais

### 4.1 Portas externas – reforço físico

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-001 | Porta principal reforçada | Madeira maciça (mínimo 45mm) ou aço | Alta |
| RF-002 | Fechadura multiponto | Mínimo 3 pontos de travamento (superior, central, inferior) | Alta |
| RF-003 | Cilindro europeu com proteção | Anti-picking, anti-bumping, anti-drill | Alta |
| RF-004 | Protetor de cilindro (escudo) | Escudo metálico fixado com parafusos especiais | Alta |
| RF-005 | Batente reforçado | Metálico ou madeira com parafusos de 75mm+ | Alta |
| RF-006 | Dobradiças protegidas | Internas ou com pino anti-remoção | Alta |
| RF-007 | Porta de serviço reforçada | Mesmos critérios da principal | Alta |
| RF-008 | Porta para quintal/varanda | Grade de segurança ou vidro laminado + fechadura | Alta |
| RF-009 | Tranca auxiliar (ferrolho) | Para uso noturno, reforço interno | Média |

### 4.2 Portas externas – sensoriamento eletrônico

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-010 | Sensor de abertura em todas as portas externas | Zigbee (Aqara MCCGQ11LM ou Sonoff SNZB-04) | Alta |
| RF-011 | Sensor de vibração na porta principal | Detectar tentativa de arrombamento | Média |
| RF-012 | Estado em tempo real no Home Assistant | Aberto/fechado/tamper | Alta |
| RF-013 | Alerta se porta aberta por mais de X minutos | Automação configurável | Média |
| RF-014 | Integração com sistema de alarme (Alarmo) | Zona de delay para entrada principal | Alta |

### 4.3 Janelas – reforço físico

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-015 | Grades em janelas térreo frente | Decorativas, fixadas com chumbadores | Alta |
| RF-016 | Grades em janelas térreo fundos/lateral | Reforçadas, maior risco de acesso | Alta |
| RF-017 | Vidro laminado em janelas sem grade | Mínimo 6mm (3+3 laminado) | Média |
| RF-018 | Trincos reforçados | Em todas as janelas, modelos anti-alavanca | Alta |
| RF-019 | Tela de segurança como alternativa a grades | Aço inox 316, malha de segurança | Média |
| RF-020 | Limitador de abertura em janelas de andar alto | Para segurança de crianças | Média |

### 4.4 Janelas – sensoriamento eletrônico

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-021 | Sensor de abertura em janelas térreo | Zigbee magnético (4-8 unidades típicas) | Alta |
| RF-022 | Sensor de quebra de vidro (acústico) | Em janelas sem grade, Zigbee | Média |
| RF-023 | Sensor de vibração em janelas vulneráveis | Detectar tentativa de arrombamento | Baixa |
| RF-024 | Integração com Alarmo (zona imediata) | Disparo imediato se armado | Alta |

### 4.5 Fechaduras inteligentes

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-025 | Fechadura com múltiplos métodos de acesso | Senha, biometria, app, chave física | Média |
| RF-026 | Protocolo Zigbee ou Z-Wave | Integração local com Home Assistant | Média |
| RF-027 | Travamento automático | Após X segundos do fechamento | Média |
| RF-028 | Auditoria de acessos | Log de quem acessou e quando | Média |
| RF-029 | Código temporário para visitantes | Válido por período específico | Baixa |
| RF-030 | Código de coação | Abre mas notifica silenciosamente | Baixa |

### 4.6 Automações e integração

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-031 | Verificação de portas/janelas ao armar alarme | Alertar se alguma está aberta | Alta |
| RF-032 | Dashboard com status de todas as aberturas | Mapa visual no Home Assistant | Alta |
| RF-033 | Notificação se porta/janela aberta com ninguém em casa | Via geolocalização | Média |
| RF-034 | Travamento automático ao sair de casa | Cena "saindo de casa" | Média |
| RF-035 | Destravamento ao chegar | Via geolocalização ou NFC | Baixa |

---

## 5. Requisitos não funcionais

### 5.1 Segurança física

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-001 | Resistência da porta a arrombamento | Suportar 15+ minutos de tentativa |
| RNF-002 | Resistência da fechadura | Classificação mínima ABNT grau 2 |
| RNF-003 | Resistência de grades | Barras de aço 1/2" ou superior |
| RNF-004 | Vidro laminado | Classificação mínima de segurança NBR 14697 |

### 5.2 Performance eletrônica

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-005 | Tempo de detecção de abertura | < 500ms |
| RNF-006 | Tempo de detecção de quebra de vidro | < 1 segundo |
| RNF-007 | Bateria dos sensores Zigbee | Mínimo 12 meses |
| RNF-008 | Alcance dos sensores | Cobertura total da casa via mesh Zigbee |

### 5.3 Usabilidade

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-009 | Verificar status de aberturas | < 2 cliques no app |
| RNF-010 | Fechadura inteligente: destravar | < 3 segundos (biometria) |
| RNF-011 | Chave física como backup | Sempre disponível em fechaduras inteligentes |

### 5.4 Estética

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-012 | Grades decorativas | Harmonizar com fachada |
| RNF-013 | Sensores discretos | Cor branca ou neutra, tamanho reduzido |
| RNF-014 | Fechadura inteligente | Design moderno, não chamar atenção excessiva |

### 5.5 Conformidade

| ID | Requisito | Norma/Regra |
|----|-----------|-------------|
| RNF-015 | Grades em edifícios | Verificar regulamento do condomínio |
| RNF-016 | Fechaduras | NBR 14913 (fechaduras de segurança) |
| RNF-017 | Vidro laminado | NBR 14697 e NBR 14698 |

---

## 6. Arquitetura técnica

### 6.1 Diagrama de sensoriamento do envelope

```
┌──────────────────────────────────────────────────────────────────┐
│                        PLANTA DA CASA                            │
│                                                                  │
│  FRENTE (RUA)                                                    │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │                                                            │  │
│  │  [P1] Porta principal ── Sensor abertura + Fechadura smart │  │
│  │  [J1] Janela sala    ── Sensor abertura + Grade decorativa │  │
│  │  [J2] Janela quarto  ── Sensor abertura + Grade decorativa │  │
│  │                                                            │  │
│  ├────────────────────────────────────────────────────────────┤  │
│  │                                                            │  │
│  │  LATERAL ESQUERDA                    LATERAL DIREITA       │  │
│  │  [J3] Janela cozinha ── Sensor       [J5] Janela quarto   │  │
│  │  [J4] Janela área    ── Sensor       [J6] Janela banheiro │  │
│  │                                                            │  │
│  ├────────────────────────────────────────────────────────────┤  │
│  │                                                            │  │
│  │  FUNDOS (QUINTAL)                                          │  │
│  │  [P2] Porta serviço  ── Sensor abertura + Tranca reforçada │  │
│  │  [P3] Porta quintal   ── Sensor abertura + Grade/vidro     │  │
│  │  [J7] Janela fundos  ── Sensor abertura + Grade reforçada  │  │
│  │  [V1] Vidro sala     ── Sensor quebra de vidro (acústico)  │  │
│  │                                                            │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
│  LEGENDA: [Px] Porta  [Jx] Janela  [Vx] Vidro monitorado       │
└──────────────────────────────────────────────────────────────────┘
```

### 6.2 Fluxo de detecção de violação

```
1. Sensor detecta evento:
   ├── Abertura de porta/janela
   ├── Vibração (tentativa de arrombamento)
   └── Quebra de vidro (som)
           │
           ▼
2. Zigbee2MQTT recebe → MQTT → Home Assistant
           │
           ▼
3. Alarmo verifica:
   ├── Sistema armado?
   │   ├── Sim → Verifica zona:
   │   │   ├── Zona imediata → ALARME IMEDIATO
   │   │   └── Zona com delay → Inicia contagem regressiva
   │   └── Não → Registra evento apenas
   │
   └── Porta principal com delay?
       └── Sim → Aguarda código (15-45s)
           ├── Código correto → Desarma
           └── Tempo esgotado → ALARME
                   │
                   ▼
4. Alarme disparado:
   ├── Aciona sirene(s)
   ├── Envia notificações (push + Telegram)
   ├── Acende iluminação reativa
   ├── Inicia gravação em câmeras (Frigate)
   └── Registra evento com timestamp
```

### 6.3 Classificação de zonas para o envelope

| Zona | Aberturas | Comportamento no Alarmo |
|------|-----------|------------------------|
| Entrada (delay) | Porta principal | Delay de entrada: 30s |
| Portas (imediata) | Porta serviço, porta quintal | Alarme imediato quando armado |
| Janelas (imediata) | Todas as janelas com sensor | Alarme imediato quando armado |
| Vidros (24h) | Sensores de quebra de vidro | Alarme sempre, mesmo desarmado |

---

## 7. Produtos/componentes recomendados

### 7.1 Fechaduras e reforços

| Componente | Modelo sugerido | Preço estimado | Observações |
|------------|-----------------|----------------|-------------|
| Fechadura multiponto | Yale YMF 40 | R$ 500-800 | 3 pontos, cilindro europeu |
| Fechadura multiponto | Stam 4800/100 | R$ 300-500 | 3 pontos, custo-benefício |
| Cilindro europeu anti-bump | Keso 4000S Omega | R$ 200-350 | Alta segurança |
| Protetor de cilindro | Mottura 94.571 | R$ 100-200 | Escudo anti-arrombamento |
| Ferrolho interno | Stam 845 | R$ 30-60 | Reforço noturno |
| Kit parafusos longos batente | - | R$ 20-40 | Parafusos 75mm para batente |

### 7.2 Grades e proteção de janelas

| Componente | Modelo sugerido | Preço estimado | Observações |
|------------|-----------------|----------------|-------------|
| Grade decorativa (por m2) | Ferro artesanal | R$ 200-400/m2 | Barras 1/2", fixação chumbada |
| Tela de segurança (por m2) | Crimsafe ou similar | R$ 300-600/m2 | Aço inox 316 |
| Vidro laminado (por m2) | 3+3mm laminado | R$ 150-300/m2 | Substituição de vidro comum |
| Trinco reforçado | Soprano janela | R$ 20-40 | Anti-alavanca |

### 7.3 Sensores Zigbee

| Componente | Modelo sugerido | Preço estimado | Compatibilidade |
|------------|-----------------|----------------|-----------------|
| Sensor abertura porta/janela | Aqara MCCGQ11LM | R$ 50-80 | Z2M, ZHA |
| Sensor abertura porta/janela | Sonoff SNZB-04 | R$ 40-60 | Z2M, ZHA |
| Sensor de vibração | Aqara DJT11LM | R$ 60-100 | Z2M, ZHA |
| Sensor de quebra de vidro | Heiman HS1GS-E | R$ 80-120 | Z2M |
| Sensor de quebra de vidro | Tuya ZSS-QY-GBS-R | R$ 60-100 | Z2M |

### 7.4 Fechaduras inteligentes

| Componente | Modelo sugerido | Preço estimado | Compatibilidade |
|------------|-----------------|----------------|-----------------|
| Fechadura Zigbee | Yale YDM 4109 RL | R$ 800-1.200 | Z2M (via módulo Zigbee) |
| Fechadura Wi-Fi | Papaiz Smart Lock | R$ 600-900 | App próprio + HA |
| Alternativa Z-Wave | Yale Assure Lock 2 | R$ 1.200-1.800 | Z-Wave, HA nativo |

---

## 8. Estimativas por cenário

### 8.1 Cenário casa urbana (típica: 3 portas, 6-8 janelas)

| Componente | Quantidade | Subtotal |
|------------|------------|----------|
| Fechadura multiponto porta principal | 1 | R$ 400-600 |
| Reforço batente (parafusos longos) | 3 portas | R$ 60-120 |
| Ferrolho interno portas | 2 | R$ 60-120 |
| Grades decorativas (janelas frente) | 4m2 | R$ 800-1.600 |
| Grades reforçadas (janelas fundos) | 3m2 | R$ 600-1.200 |
| Sensores abertura Zigbee (portas) | 3 | R$ 120-180 |
| Sensores abertura Zigbee (janelas) | 6-8 | R$ 240-480 |
| Sensores quebra de vidro | 1-2 | R$ 80-200 |
| **Total envelope casa urbana** | | **R$ 2.360-4.500** |

### 8.2 Cenário rural (sede: 3-4 portas, 6-10 janelas)

| Componente | Quantidade | Subtotal |
|------------|------------|----------|
| Fechadura multiponto porta principal | 1 | R$ 400-600 |
| Portas secundárias reforçadas | 2-3 | R$ 200-450 |
| Grades em janelas térreo | 8m2 | R$ 1.600-3.200 |
| Sensores abertura Zigbee (portas) | 3-4 | R$ 150-240 |
| Sensores abertura Zigbee (janelas) | 6-10 | R$ 240-600 |
| Sensores quebra de vidro | 2-3 | R$ 160-360 |
| Sensor de vibração porta | 1-2 | R$ 60-200 |
| **Total envelope rural** | | **R$ 2.810-5.650** |

### 8.3 Cenário apartamento (1 porta principal)

| Componente | Quantidade | Subtotal |
|------------|------------|----------|
| Fechadura multiponto | 1 | R$ 400-600 |
| Cilindro europeu anti-bump | 1 | R$ 200-350 |
| Protetor de cilindro | 1 | R$ 100-200 |
| Sensor abertura porta | 1 | R$ 50-80 |
| Sensor vibração porta (opcional) | 1 | R$ 60-100 |
| **Total envelope apartamento** | | **R$ 810-1.330** |

---

## 9. Critérios de aceitação

| ID | Critério | Método de verificação |
|----|----------|----------------------|
| CA-001 | Todas as portas externas com fechadura multiponto ou reforço | Inspeção física |
| CA-002 | Todas as janelas acessíveis com grade ou tela de segurança | Inspeção visual |
| CA-003 | Sensores de abertura em todas as portas externas | Teste funcional no HA |
| CA-004 | Sensores de abertura em todas as janelas térreo | Teste funcional no HA |
| CA-005 | Alarmo dispara ao abrir porta/janela com sistema armado | Teste funcional |
| CA-006 | Delay de entrada funciona na porta principal | Teste com cronômetro |
| CA-007 | Sensor de quebra de vidro detecta impacto corretamente | Teste com simulação |
| CA-008 | Dashboard exibe status de todas as aberturas | Verificação visual |
| CA-009 | Alerta gerado quando porta esquecida aberta | Teste de automação |
| CA-010 | Fechadura inteligente funciona em todos os modos | Teste de cada método |

---

## 10. Métricas de sucesso

| Métrica | Alvo | Medição |
|---------|------|---------|
| **Cobertura de sensoriamento** | 100% das aberturas acessíveis | Inventário |
| **Falsos positivos de quebra de vidro** | < 1/mês | Contagem |
| **Bateria dos sensores** | > 12 meses | Registro de trocas |
| **Tempo médio de detecção** | < 500ms | Monitoramento de logs |
| **Adoção pelos moradores** | 100% sabem verificar status | Treinamento |

---

## 11. Riscos e dependências

### 11.1 Riscos

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Sensor de quebra de vidro com falsos positivos | Média | Baixo | Ajustar sensibilidade, posicionar corretamente |
| Fechadura inteligente trava (bateria) | Baixa | Alto | Manter chave física, alertar bateria < 20% |
| Grade prejudica estética da fachada | Média | Baixo | Usar grades decorativas ou telas de segurança |
| Sensor cai da janela (fita adesiva) | Média | Baixo | Usar parafusos quando possível |
| Batente cede mesmo reforçado | Baixa | Alto | Usar cantoneira metálica + parafusos longos |

### 11.2 Dependências

| Dependência | Tipo | PRD relacionado |
|-------------|------|-----------------|
| Plataforma de sensores e alarmes | Funcional | PRD_SENSORS_AND_ALARMS_PLATFORM |
| Dashboard de monitoramento | Interface | PRD_MONITORING_DASHBOARD |
| Sistema de notificações | Funcional | PRD_NOTIFICATIONS_AND_ALERTS |
| Automações de segurança | Integração | PRD_AUTOMATION_AND_SCENES |
| Coordenador Zigbee | Infraestrutura | PRD_LOCAL_PROCESSING_HUB |

---

## 12. Referências

### Documentos do projeto
- `docs/ARQUITETURA_SEGURANCA_FISICA.md` - Seções de envelope e reforço
- `docs/ARQUITETURA_TECNICA.md` - Seções 1.2, 3
- `prd/PRD_PERIMETER_URBAN_HOUSE.md` - Contexto de casa urbana
- `rules/RULES_COMPLIANCE_AND_STANDARDS.md`

### Externos
- NBR 14913 - Fechaduras de segurança
- NBR 14697 - Vidro laminado
- [Zigbee2MQTT - Dispositivos suportados](https://www.zigbee2mqtt.io/supported-devices/)
- [Home Assistant - Alarmo](https://github.com/nielsfaber/alarmo)

---

> **Status**: Rascunho v1.0
>
> **Próxima revisão**: Após validação pelo Agente_Arquiteto_Seguranca_Fisica
