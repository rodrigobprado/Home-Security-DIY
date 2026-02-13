# Análise de Custos Operacionais – Sistema de Home Security

> Documento produzido durante revisão do projeto em 2026-02-12
>
> Complemento à estimativa de investimento inicial (ARQUITETURA_TECNICA.md, seção 10)

---

## 1. Objetivo

Estimar custos recorrentes (mensais e anuais) de operação do sistema de segurança para cada cenário residencial, permitindo ao usuário planejar o TCO (Total Cost of Ownership).

---

## 2. Consumo de Energia Elétrica

### 2.1 Consumo por componente

| Componente | Consumo típico | Horas/dia | kWh/mês |
|-----------|---------------|-----------|---------|
| Mini PC Intel N100 | 10-20W (idle: 10W, carga: 20W) | 24 | 7,2-14,4 |
| Switch PoE 8 portas | 30-60W (depende de câmeras) | 24 | 21,6-43,2 |
| Câmera PoE (cada) | 5-12W | 24 | 3,6-8,6 |
| Coordenador Zigbee USB | <1W | 24 | 0,7 |
| Roteador Wi-Fi | 8-15W | 24 | 5,8-10,8 |
| Nobreak (perda por conversão) | 5-10W | 24 | 3,6-7,2 |
| Modem 4G backup (se ativo) | 3-5W | 24 | 2,2-3,6 |
| Sirene (standby) | <1W | 24 | 0,7 |
| Refletores LED com sensor | 20-50W | ~2h/noite | 1,2-3,0 |

### 2.2 Consumo total por cenário

| Cenário | Componentes ativos | Consumo estimado | kWh/mês | Custo/mês* |
|---------|-------------------|-----------------|---------|-----------|
| **Rural** | N100 + Switch PoE + 5 câmeras + roteador + 4G + refletores | ~130-180W | 93-130 | R$ 79-110 |
| **Urbano** | N100 + Switch PoE + 4 câmeras + roteador + 4G + refletores | ~110-155W | 79-112 | R$ 67-95 |
| **Apartamento** | N100 + roteador + 1 câmera (Wi-Fi) | ~25-40W | 18-29 | R$ 15-25 |

*Tarifa média Brasil: R$ 0,85/kWh (com impostos, bandeira verde). Varia por região e bandeira tarifária.

---

## 3. Conectividade

### 3.1 Internet fixa

| Requisito | Mínimo | Recomendado | Observação |
|-----------|--------|-------------|------------|
| **Download** | 10 Mbps | 50+ Mbps | Para updates e acesso remoto |
| **Upload** | 5 Mbps | 10+ Mbps | Para VPN e streaming remoto |
| **Latência** | < 50ms | < 20ms | Para notificações em tempo real |
| **Tipo** | Qualquer | Fibra óptica | Fibra mais estável e simétrica |

> Internet fixa geralmente já existe na residência. Custo incremental: R$ 0.

### 3.2 4G/LTE backup (recomendado para rural e urbano)

| Plano | Dados | Custo/mês | Uso |
|-------|-------|-----------|-----|
| **Pré-pago básico** | 1-2 GB | R$ 20-30 | Apenas notificações e telemetria |
| **Controle** | 5-10 GB | R$ 30-50 | Notificações + streaming curto |
| **IoT dedicado** | 500MB-1GB | R$ 15-25 | Apenas alertas críticos |

**Recomendação**: Plano pré-pago básico (1-2GB) é suficiente para fallback de notificações. Não é necessário streaming contínuo via 4G.

---

## 4. Manutenção e Reposição

### 4.1 Itens de consumo regular

| Item | Frequência de troca | Qtd por cenário (R/U/A) | Custo unitário | Custo anual (R/U/A) |
|------|--------------------|-----------------------|---------------|-------------------|
| Bateria sensor Zigbee (CR2032) | 12-24 meses | 6/8/3 | R$ 5-10 | R$ 30-80 / R$ 40-80 / R$ 15-30 |
| Bateria fechadura eletrônica (4xAA) | 6-12 meses | 1-2 / 1-2 / 1 | R$ 20-40 | R$ 40-80 / R$ 40-80 / R$ 40-80 |
| Cartão microSD câmera (edge backup) | 2-3 anos | 5/4/1 | R$ 30-60 | R$ 50-100 / R$ 40-80 / R$ 10-20 |

### 4.2 Itens de substituição periódica (amortizados)

| Item | Vida útil | Custo reposição | Custo amortizado/ano |
|------|-----------|----------------|---------------------|
| HDD gravações (2-4TB) | 3-5 anos | R$ 300-500 | R$ 75-125 |
| Bateria nobreak | 2-4 anos | R$ 150-400 | R$ 50-130 |
| SSD sistema (256GB) | 5-7 anos | R$ 150-300 | R$ 25-50 |

---

## 5. Software e Serviços

| Item | Custo | Obrigatório? | Observação |
|------|-------|-------------|------------|
| Home Assistant | Gratuito | Sim | Open source, sem custo |
| Frigate | Gratuito | Sim | Open source, sem custo |
| Zigbee2MQTT | Gratuito | Sim | Open source, sem custo |
| WireGuard VPN | Gratuito | Sim | Open source, sem custo |
| Nabu Casa (alternativa VPN) | R$ 35/mês (~US$6.50) | Não | Facilita acesso remoto, pago |
| DDNS (se usar WireGuard sem IP fixo) | Gratuito | Talvez | DuckDNS, No-IP gratuito |
| Seguro RETA (drones) | R$ 500-3.000/ano | Sim (se drones) | Obrigatório para operação não recreativa |

---

## 6. Resumo TCO (Total Cost of Ownership)

### 6.1 Custo mensal por cenário

| Item | Rural (R$/mês) | Urbano (R$/mês) | Apartamento (R$/mês) |
|------|---------------|----------------|---------------------|
| Energia elétrica | R$ 79-110 | R$ 67-95 | R$ 15-25 |
| 4G backup | R$ 20-30 | R$ 20-30 | R$ 0 (opcional) |
| Reposição consumíveis (amortizado) | R$ 20-35 | R$ 18-30 | R$ 8-15 |
| Substituição periódica (amortizado) | R$ 15-25 | R$ 15-25 | R$ 10-15 |
| Software | R$ 0 | R$ 0 | R$ 0 |
| **Total mensal** | **R$ 134-200** | **R$ 120-180** | **R$ 33-55** |

### 6.2 Custo anual por cenário

| Item | Rural (R$/ano) | Urbano (R$/ano) | Apartamento (R$/ano) |
|------|---------------|----------------|---------------------|
| **Total operacional** | **R$ 1.600-2.400** | **R$ 1.440-2.160** | **R$ 400-660** |
| + Seguro RETA (se drones) | + R$ 500-3.000 | + R$ 500-3.000 | N/A |

### 6.3 TCO em 5 anos (investimento + operação)

| Cenário | Investimento inicial | Operação 5 anos | TCO 5 anos |
|---------|---------------------|-----------------|-----------|
| **Rural** | R$ 5.950 | R$ 8.000-12.000 | **R$ 13.950-17.950** |
| **Urbano** | R$ 4.950 | R$ 7.200-10.800 | **R$ 12.150-15.750** |
| **Apartamento** | R$ 2.450 | R$ 2.000-3.300 | **R$ 4.450-5.750** |

> **Nota**: TCO não inclui custo de mão-de-obra do próprio morador para manutenção (sistema DIY).

---

## 7. Comparativo com Soluções Comerciais

Para contexto, uma comparação com soluções comerciais de monitoramento 24h:

| Solução | Mensal | Anual | 5 anos |
|---------|--------|-------|--------|
| **DIY (este projeto) – Urbano** | R$ 120-180 | R$ 1.440-2.160 | R$ 12.150-15.750 |
| **Monitoramento comercial básico** (ADT, Verisure) | R$ 150-300 | R$ 1.800-3.600 | R$ 9.000-18.000 |
| **Monitoramento comercial completo** (câmeras + resposta) | R$ 300-600 | R$ 3.600-7.200 | R$ 18.000-36.000 |

**Vantagens do DIY**:
- Sem contrato de fidelidade
- Controle total dos dados (privacidade)
- Sem mensalidade de software
- Hardware é do proprietário
- Customizável e extensível

**Desvantagens do DIY**:
- Investimento inicial mais alto
- Requer conhecimento técnico para manutenção
- Sem resposta armada (empresa de segurança)
- Responsabilidade total do morador

---

## Referências

- [Tarifa média de energia residencial - ANEEL](https://www.aneel.gov.br/)
- [Planos de celular pré-pago - Comparação](https://www.melhorplano.net/)
- [Custo de monitoramento residencial - Verisure](https://www.verisure.com.br/)
- Valores estimados para mercado brasileiro em 2026.

---

> Última atualização: 2026-02-12
