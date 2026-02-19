# Custos e Planejamento

Este guia apresenta estimativas de investimento inicial, custos operacionais recorrentes e comparativo com soluções comerciais para cada cenário residencial.

---

## Investimento Inicial por Cenário

| Cenário | Investimento estimado | Complexidade |
|---------|-----------------------|--------------|
| **Apartamento** | R$ 2.450–3.500 | Baixa |
| **Casa Urbana** | R$ 4.950–6.500 | Média |
| **Rural** | R$ 5.950–9.000 | Alta |

> Para a composição detalhada de cada cenário, consulte `docs/ARQUITETURA_TECNICA.md`, seção 10.

---

## Consumo de Energia Elétrica

### Consumo por componente

| Componente | Consumo típico | kWh/mês |
|-----------|----------------|---------|
| Mini PC Intel N100 | 10–20 W | 7,2–14,4 |
| Switch PoE 8 portas | 30–60 W | 21,6–43,2 |
| Câmera PoE (cada) | 5–12 W | 3,6–8,6 |
| Roteador Wi-Fi | 8–15 W | 5,8–10,8 |
| Nobreak (perda conversão) | 5–10 W | 3,6–7,2 |
| Modem 4G backup | 3–5 W | 2,2–3,6 |
| Refletores LED com sensor | 20–50 W (~2 h/noite) | 1,2–3,0 |

### Custo de energia por cenário

| Cenário | Componentes | kWh/mês | Custo/mês* |
|---------|------------|---------|-----------|
| **Rural** | N100 + Switch + 5 câmeras + roteador + 4G + refletores | 93–130 | R$ 79–110 |
| **Casa Urbana** | N100 + Switch + 4 câmeras + roteador + 4G + refletores | 79–112 | R$ 67–95 |
| **Apartamento** | N100 + roteador + 1 câmera Wi-Fi | 18–29 | R$ 15–25 |

*Tarifa média Brasil: R$ 0,85/kWh (bandeira verde, com impostos). Varia por região e bandeira tarifária.

---

## Conectividade

### Internet fixa

| Requisito | Mínimo | Recomendado |
|-----------|--------|-------------|
| Download | 10 Mbps | 50+ Mbps |
| Upload | 5 Mbps | 10+ Mbps |
| Tipo | Qualquer | Fibra óptica |

> Internet fixa geralmente já existe na residência. Custo incremental: **R$ 0**.

### 4G/LTE backup (obrigatório para rural e urbano)

| Plano | Dados | Custo/mês |
|-------|-------|-----------|
| Pré-pago básico | 1–2 GB | R$ 20–30 |
| IoT dedicado | 500 MB–1 GB | R$ 15–25 |

> 1–2 GB é suficiente para notificações críticas. Não é necessário streaming via 4G.

---

## Manutenção e Reposição

### Consumíveis regulares

| Item | Troca | Custo anual (Rural / Urbano / Apto) |
|------|-------|--------------------------------------|
| Bateria sensor Zigbee (CR2032) | 12–24 meses | R$ 30–80 / R$ 40–80 / R$ 15–30 |
| Bateria fechadura eletrônica (4×AA) | 6–12 meses | R$ 40–80 / R$ 40–80 / R$ 40–80 |
| Cartão microSD câmera (High Endurance) | 2–3 anos | R$ 50–100 / R$ 40–80 / R$ 10–20 |

### Reposição periódica (amortizados)

| Item | Vida útil | Custo amortizado/ano |
|------|-----------|---------------------|
| HDD gravações (2–4 TB) | 3–5 anos | R$ 75–125 |
| Bateria nobreak | 2–4 anos | R$ 50–130 |
| SSD sistema (256 GB) | 5–7 anos | R$ 25–50 |

### Software e serviços

| Item | Custo | Obrigatório? |
|------|-------|-------------|
| Home Assistant | Gratuito | Sim |
| Frigate NVR | Gratuito | Sim |
| Zigbee2MQTT | Gratuito | Sim |
| WireGuard VPN | Gratuito | Sim |
| Nabu Casa (acesso remoto facilitado) | ~R$ 35/mês | Não |
| Telegram Bot (notificações) | Gratuito | Não |
| Seguro RETA (se operar drones) | R$ 500–3.000/ano | Sim (se drones) |

> O projeto é desenhado para **não depender de serviços pagos**.

---

## Calendário de Manutenção Preventiva

### Semanal

| Ação | Ferramenta |
|------|------------|
| Verificar status de todos os sensores | Home Assistant dashboard |
| Verificar alertas pendentes/não resolvidos | App HA |
| Verificar logs de acesso suspeitos | Home Assistant |

### Mensal

| Ação | Ferramenta |
|------|------------|
| Verificar atualizações de firmware (câmeras, HA, Frigate) | HA Supervisor / Docker |
| Limpar lentes das câmeras externas | Pano de microfibra |
| Testar disparo do alarme (modo teste) | Alarmo |
| Verificar nível de bateria dos sensores Zigbee | HA → Zigbee2MQTT |
| Verificar integridade da gravação (reproduzir amostra) | Frigate |
| Verificar espaço livre em disco de gravações | HA ou SSH |

### Trimestral

| Ação | Ferramenta |
|------|------------|
| Teste completo do nobreak (simular queda de energia) | Desligar disjuntor por 5 min |
| Verificar estado do HDD via S.M.A.R.T. | `smartctl` via SSH |
| Testar notificações por todos os canais (push, Telegram) | Automação HA |
| Verificar integridade da VPN (conectar remotamente) | WireGuard |
| Revisar regras de firewall e dispositivos desconhecidos na rede | Roteador / `nmap` |
| Testar backup de configuração (restaurar em ambiente de teste) | HA backup |

### Semestral

| Ação | Ferramenta |
|------|------------|
| Rotação de senhas (HA e VPN) | HA, WireGuard |
| Revisar ângulos de câmera (vegetação pode ter crescido) | Verificação visual |
| Verificar estado físico de câmeras externas (corrosão, umidade) | Inspeção visual |
| Verificar estado de cabos e conectores PoE | Inspeção visual |

### Anual

| Ação | Ferramenta |
|------|------------|
| Auditoria completa de segurança (todas as camadas) | Checklist |
| Revisar e atualizar plano de resposta a incidentes | Documentação |
| Verificar se fabricantes ainda fornecem atualizações | Sites dos fabricantes |
| Testar todas as automações de segurança (cenário completo) | HA |
| Avaliar necessidade de upgrade de hardware | Monitoramento de recursos |
| Backup completo offsite (configuração + gravações importantes) | Disco externo |

> **Checklist mensal imprimível:** Marcar cada item após execução e registrar data/responsável.

---

## Ciclo de Vida dos Componentes

| Componente | Vida útil estimada | Indicadores de substituição | Custo de reposição |
|-----------|-------------------|----------------------------|--------------------|
| Bateria sensor Zigbee (CR2032) | 1–2 anos | Alerta < 20% no HA | R$ 5–15 |
| Bateria fechadura eletrônica (4×AA) | 6–12 meses | Alerta < 30% (1 semana antes) | R$ 20–50 |
| Bateria nobreak | 2–4 anos | Autonomia reduzida, alerta UPS | R$ 150–400 |
| HDD de gravações (2–4 TB) | 3–5 anos | Erros S.M.A.R.T., setores realocados | R$ 200–500 |
| SSD do sistema (256 GB) | 5–7 anos | S.M.A.R.T., TBW próximo do limite | R$ 150–300 |
| Câmera IP externa | 3–5 anos | Degradação de imagem, vedação comprometida | R$ 200–700 |
| Câmera IP interna | 5–7 anos | Degradação de imagem | R$ 150–500 |
| Mini PC servidor | 5–7 anos | Performance insuficiente | R$ 800–1.500 |
| Sensor Zigbee | 5–10 anos | Falha de comunicação frequente | R$ 50–150 |
| Coordenador Zigbee | 5–7 anos | Falha com sensores | R$ 100–300 |
| Switch PoE | 5–10 anos | Portas falhando, superaquecimento | R$ 400–800 |
| Roteador/Firewall | 3–5 anos | Sem atualizações de segurança | R$ 300–800 |
| Sirene | 5–10 anos | Redução de volume, falha no acionamento | R$ 100–200 |

### Alertas automáticos recomendados

| Alerta | Condição | Canal |
|--------|----------|-------|
| Bateria de sensor baixa | < 20% | Push notification |
| Bateria de fechadura baixa | < 30% | Push + SMS |
| HDD com erros S.M.A.R.T. | Qualquer erro preditivo | Push + Email |
| Disco quase cheio | > 85% de uso | Push notification |
| Nobreak em bateria | Queda de energia detectada | Push imediato |
| Câmera offline | > 5 minutos sem stream | Push notification |

### Gestão de End-of-Life (EOL)

| Dispositivo sem atualizações | Ação recomendada |
|------------------------------|-----------------|
| Câmera IP | Isolar na VLAN + planejar substituição (firmware alternativo: OpenIPC) |
| Sensor Zigbee | Manter se funcional (protocolo padronizado) |
| Roteador | Substituir IMEDIATAMENTE (risco crítico) ou migrar para OpenWrt |
| Switch PoE | Manter se funcional (managed) |
| Mini PC | Manter Linux atualizado (independe do fabricante) |

---

## TCO — Total Cost of Ownership

### Custo mensal por cenário

| Item | Rural | Urbano | Apartamento |
|------|-------|--------|-------------|
| Energia elétrica | R$ 79–110 | R$ 67–95 | R$ 15–25 |
| 4G backup | R$ 20–30 | R$ 20–30 | R$ 0 (opcional) |
| Consumíveis (amortizado) | R$ 20–35 | R$ 18–30 | R$ 8–15 |
| Substituição periódica (amortizado) | R$ 15–25 | R$ 15–25 | R$ 10–15 |
| Software | R$ 0 | R$ 0 | R$ 0 |
| **Total mensal** | **R$ 134–200** | **R$ 120–180** | **R$ 33–55** |

### TCO em 5 anos

| Cenário | Investimento inicial | Operação 5 anos | TCO total |
|---------|---------------------|-----------------|-----------|
| **Rural** | R$ 5.950 | R$ 8.000–12.000 | **R$ 13.950–17.950** |
| **Casa Urbana** | R$ 4.950 | R$ 7.200–10.800 | **R$ 12.150–15.750** |
| **Apartamento** | R$ 2.450 | R$ 2.000–3.300 | **R$ 4.450–5.750** |

---

## Comparativo com Soluções Comerciais

| Solução | Mensalidade | 5 anos |
|---------|------------|--------|
| **DIY (este projeto) — Urbano** | R$ 120–180 | R$ 12.150–15.750 |
| Monitoramento comercial básico (ADT, Verisure) | R$ 150–300 | R$ 9.000–18.000 |
| Monitoramento comercial completo | R$ 300–600 | R$ 18.000–36.000 |

### Vantagens do DIY

- Sem contrato de fidelidade
- Controle total dos dados (privacidade)
- Sem mensalidade de software
- Hardware é do proprietário
- Customizável e extensível

### Desvantagens do DIY

- Investimento inicial mais alto
- Requer conhecimento técnico para manutenção
- Sem resposta armada (empresa de segurança)
- Responsabilidade total do morador

---

## Alternativas Comerciais Compatíveis

Produtos que se integram ao ecossistema do projeto quando a abordagem DIY não é viável:

### Por perfil de usuário

**Perfil 1 — "Quero fácil e rápido"** (mínimo DIY)

| Componente | Produto | Preço |
|------------|---------|-------|
| Hub | Home Assistant Green | R$ 600 |
| NVR | Reolink RLN8-410 (4 câmeras incluso) | R$ 2.500 |
| Sensores | Kit Aqara Starter | R$ 500 |
| Fechadura | Papaiz Smart Lock | R$ 800 |
| Nobreak | APC 1500 VA | R$ 1.100 |
| **Total** | | **~R$ 5.500** |

**Perfil 2 — "DIY com ajuda"** (parcialmente DIY)

| Componente | Produto | Preço |
|------------|---------|-------|
| Servidor | Mini PC N100 + Docker | R$ 1.000 |
| Câmeras | 4× Reolink RLC-520A | R$ 1.400 |
| Sensores | Dongle Sonoff + 8 sensores Zigbee | R$ 600 |
| Rede | MikroTik hAP ax3 + switch PoE | R$ 1.000 |
| Nobreak | SMS 1400 VA | R$ 800 |
| **Total** | | **~R$ 4.800** |

### Câmeras IP compatíveis com Frigate

| Modelo | Tipo | RTSP | Preço unitário |
|--------|------|------|----------------|
| Reolink RLC-520A | Dome PoE 5MP | Sim | R$ 300–400 |
| Reolink RLC-810A | Bullet PoE 4K | Sim | R$ 400–600 |
| Hikvision DS-2CD1043 | Bullet PoE 4MP | Sim | R$ 350–500 |
| Intelbras VIP 1230 | Dome PoE 2MP | Sim | R$ 250–400 |

> Preferir Reolink para melhor compatibilidade com Frigate + slot SD para edge recording.

### Nobreaks recomendados

| Modelo | Potência | Preço | Nota |
|--------|----------|-------|------|
| APC Back-UPS 1500 VA | 1500 VA / 900 W | R$ 900–1.300 | Recomendado |
| SMS Station II 1400 VA | 1400 VA / 840 W | R$ 700–1.000 | Alternativa nacional |
| Ts Shara 1800 VA | 1800 VA / 1080 W | R$ 800–1.200 | Senoidal pura |

---

## Referências

- `docs/CUSTOS_OPERACIONAIS.md` — custos operacionais detalhados
- `docs/MANUTENCAO_CICLO_VIDA.md` — calendário de manutenção e ciclo de vida
- `docs/COMMERCIAL_ALTERNATIVES.md` — alternativas comerciais por subsistema
- `docs/ARQUITETURA_TECNICA.md` — estimativas detalhadas por cenário
- [Cenários Residenciais](Cenarios-Residenciais) — comparativo por tipo de habitação
- [Resiliência](Resiliencia) — dimensionamento de nobreak e armazenamento
