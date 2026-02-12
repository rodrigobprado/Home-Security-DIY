# Memória Local – Agente_Documentador

## Contexto de trabalho atual

**Status**: Tarefas T-022, T-023, T-024, T-025 concluídas em 2026-02-12.

PRDs principais criados com base nos documentos de arquitetura técnica e física.

---

## PRDs elaborados (2026-02-12)

### T-022: PRD de Plataforma de Sensores e Alarmes

**Arquivo**: `prd/PRD_SENSORS_AND_ALARMS_PLATFORM.md`

**Conteúdo**:
- Requisitos funcionais: 40 itens (tipos de sensores, protocolos, Alarmo, notificações)
- Requisitos não funcionais: 24 itens (performance, segurança, conformidade)
- Arquitetura técnica com diagramas
- Lista de sensores Zigbee recomendados com preços
- Estimativas de investimento por cenário
- Critérios de aceitação e métricas

### T-023: PRD de Videovigilância e NVR

**Arquivo**: `prd/PRD_VIDEO_SURVEILLANCE_AND_NVR.md`

**Conteúdo**:
- Requisitos funcionais: 50 itens (câmeras, gravação, detecção IA, streaming)
- Requisitos não funcionais: 22 itens (performance, armazenamento, conformidade)
- Arquitetura Frigate + OpenVINO
- Lista de câmeras recomendadas por cenário
- Política de retenção com cálculo de armazenamento
- Configuração exemplo Frigate

### T-024: PRD de Dashboard de Monitoramento

**Arquivo**: `prd/PRD_MONITORING_DASHBOARD.md`

**Conteúdo**:
- Requisitos funcionais: 47 itens (status, controle, câmeras, histórico)
- Requisitos não funcionais: 16 itens (usabilidade, performance, segurança)
- Wireframes desktop e mobile
- Cards Home Assistant recomendados
- Exemplo de configuração YAML

### T-025: PRDs dos Três Cenários

**Arquivos criados**:

1. `prd/PRD_PERIMETER_RURAL.md`
   - 32 requisitos funcionais específicos para propriedade rural
   - Diagrama de posicionamento ASCII
   - Estimativa de investimento: R$ 5.460 - R$ 6.480

2. `prd/PRD_PERIMETER_URBAN_HOUSE.md`
   - 36 requisitos funcionais para casa urbana
   - Diagrama de posicionamento ASCII
   - Estimativa de investimento: R$ 4.510 - R$ 5.360

3. `prd/PRD_APARTMENT_SECURITY.md`
   - 30 requisitos funcionais para apartamento
   - Foco em proteção de porta
   - Estimativa de investimento: R$ 1.700 - R$ 3.170

---

## Convenções aplicadas

### Formatação
- Template PRD seguido rigorosamente
- Requisitos com IDs únicos (RF-XXX, RNF-XXX, CA-XXX)
- Tabelas para dados estruturados
- Diagramas ASCII para posicionamento

### Referências cruzadas
- Links para documentos de arquitetura
- Referência às regras de compliance (REGRA-XXX-NN)
- PRDs relacionados listados

### Estimativas de investimento
- Valores em Reais (R$)
- Faixas de preço para flexibilidade
- Baseados em preços de mercado 2026

---

## Checklist de qualidade aplicado

- [x] Seguir template `prd/PRD_TEMPLATE.md`
- [x] Incluir requisitos funcionais e não funcionais
- [x] Referenciar normas aplicáveis
- [x] Listar dependências de outros PRDs
- [x] Incluir critérios de aceitação
- [x] Incluir métricas de sucesso
- [x] Incluir riscos e mitigações
- [x] Valores em português (pt-BR), termos técnicos em inglês

---

## PRDs pendentes (baixa prioridade)

Os seguintes PRDs não foram solicitados nas tarefas atuais, mas podem ser criados futuramente:

| PRD | Prioridade | Notas |
|-----|------------|-------|
| PRD_RURAL_ACCESS_CONTROL.md | Média | Controle de portões e interfones |
| PRD_HOUSE_ENVELOPE.md | Média | Detalhamento de portas/janelas |
| PRD_APARTMENT_SMART_LOCK.md | Média | Fechaduras inteligentes |
| PRD_NOTIFICATIONS_AND_ALERTS.md | Baixa | Coberto parcialmente nos PRDs existentes |
| PRD_AUTOMATION_AND_SCENES.md | Baixa | Automações específicas |
| PRD_ENVIRONMENTAL_SENSORS.md | Baixa | Fumaça, gás, água |
| PRD_BACKUP_AND_RESILIENCE.md | Baixa | Nobreak, redundância |
| PRD_NETWORK_SECURITY.md | Média | VLANs, firewall - importante |
| PRD_LOCAL_PROCESSING_HUB.md | Média | Hardware central - importante |

---

## Cache de pesquisas

### Preços de referência (2026-02-12)

| Componente | Faixa de preço |
|------------|----------------|
| Mini PC Intel N100 8GB | R$ 800-1.200 |
| Sonoff ZBDongle-P | R$ 100-150 |
| Sensor abertura Zigbee | R$ 40-80 |
| Sensor PIR Zigbee | R$ 50-100 |
| Câmera PoE 4MP Reolink | R$ 300-500 |
| Switch PoE 8 portas | R$ 350-450 |
| Sirene Zigbee | R$ 80-150 |
| Nobreak 600VA | R$ 300-400 |

---

## Pendências resolvidas

- [x] Aguardando requisitos dos arquitetos para iniciar PRDs → Concluído
- [x] Template de PRD está adequado → Sim, usado com sucesso

---

> Última atualização: 2026-02-12
