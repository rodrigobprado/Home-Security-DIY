# Decisões de Arquitetura

Este documento registra as principais decisões de design do projeto, incluindo o raciocínio por trás de cada escolha e as alternativas descartadas.

---

## ADR-001 — Processamento 100% Local (Sem Nuvem)

**Decisão**: Todo o processamento — vídeo, IA, automações, banco de dados e dashboard — ocorre localmente no Mini PC. Nenhum dado é enviado para servidores externos.

**Contexto**: Sistemas comerciais de segurança (Ring, Nest, Arlo) dependem de nuvem para armazenamento de vídeo, IA e notificações. Isso cria riscos de privacidade, dependência de mensalidades e vulnerabilidade a indisponibilidade do serviço.

**Motivos da escolha**:
- Privacidade total — câmeras não transmitem para internet
- Funciona sem internet (exceto notificações externas)
- Sem custo mensal de software
- Sem risco de descontinuação do serviço

**Trade-offs**:
- Requer hardware local com capacidade de processamento
- Manutenção pelo próprio usuário
- Sem backup automático em nuvem (por padrão)

---

## ADR-002 — Stack Principal: Home Assistant + Frigate + Zigbee2MQTT

**Decisão**: Usar Home Assistant como orquestrador central, Frigate como NVR com IA, e Zigbee2MQTT como bridge de sensores.

**Alternativas avaliadas**:

| Stack | Motivo da recusa |
|-------|-----------------|
| ioBroker | Comunidade menor, menos integrações |
| OpenHAB | Curva de aprendizado maior, menos atualizações |
| Domoticz | Menos ativo, UI datada |
| Node-RED puro | Não é sistema completo; pode ser complemento |
| Zoneminder | NVR sem IA integrada; substituído pelo Frigate |

**Motivos da escolha**:
- Home Assistant: maior comunidade open source de automação residencial, 3.000+ integrações
- Frigate: detecção por IA (YOLOv8) otimizada para câmeras residenciais, integração nativa com HA via MQTT
- Zigbee2MQTT: suporte a 3.000+ dispositivos Zigbee, sem dependência de hub proprietário

---

## ADR-003 — Zigbee 3.0 como Protocolo de Sensores

**Decisão**: Adotar Zigbee 3.0 como protocolo principal para sensores e dispositivos de automação.

**Alternativas avaliadas**:

| Protocolo | Status | Motivo |
|-----------|--------|--------|
| Z-Wave | Descartado | Menor disponibilidade no Brasil, preços mais altos |
| Wi-Fi (MQTT) | Descartado | Maior consumo de energia, congestionamento da rede |
| Matter/Thread | Futuro | Ver análise completa abaixo |
| 433 MHz (RF) | Descartado | Sem criptografia, sem confirmação de entrega |
| Cabeado (dry contact) | Complementar | Usado em pontos críticos para anti-jamming |

**Motivos da escolha**:
- Ecossistema muito completo (Aqara, Sonoff, IKEA, Tuya)
- Disponibilidade e preços acessíveis no Brasil (R$ 50–150/sensor)
- Mesh autônomo — dispositivos roteadores ampliam o sinal automaticamente
- Bateria de 1–2 anos por sensor
- Integração madura com HA (ZHA e Zigbee2MQTT)

---

## ADR-004 — Avaliação Matter/Thread vs Zigbee

### O que é Matter/Thread

**Matter** (antes CHIP): protocolo de aplicação para smart home mantido pela CSA. Versão atual: Matter 1.4 (2025). Apoiadores: Apple, Google, Amazon, Samsung, Philips, IKEA.

**Thread**: protocolo de rede mesh IPv6 de baixo consumo (IEEE 802.15.4), camada de transporte para Matter.

### Comparativo

| Aspecto | Zigbee 3.0 | Matter/Thread |
|---------|------------|---------------|
| Maturidade | 15+ anos, muito maduro | 3 anos, em evolução |
| Dispositivos disponíveis | Milhares | Centenas (crescendo) |
| Disponibilidade no Brasil | Alta | Baixa–média |
| Preço médio | R$ 50–150/sensor | R$ 80–250/sensor |
| Mesh network | Sim | Sim (Thread, mais robusto) |
| IPv6 nativo | Não | Sim |
| Interoperabilidade | Dentro do Zigbee | Multi-ecossistema |
| Home Assistant | Excelente (ZHA, Z2M) | Bom (Matter nativo) |
| Sirenes disponíveis | Muitas | **Poucas** |
| Câmeras | Não aplicável | Parcial (Matter 1.3+, experimental) |
| Estabilidade | Muito estável | Melhorando |

### Limitações atuais do Matter para segurança

1. **Faltam sirenes Matter** compatíveis — componente crítico para alarme
2. **Câmeras sobre Matter** ainda são experimentais
3. **Sensores especializados** (vibração, quebra de vidro, gás) praticamente inexistentes
4. **Alarmo** (add-on HA) com suporte a Matter não testado amplamente
5. **Preços mais altos** no Brasil por disponibilidade limitada

### Recomendação e roadmap

| Período | Protocolo | Ação |
|---------|-----------|------|
| **2026 (agora)** | Zigbee 3.0 | Manter — ecossistema mais completo para segurança |
| **2027–2028** | Híbrido | Preferir dispositivos com suporte dual (Zigbee + Matter) ao comprar novos |
| **2029+** | Migração gradual | Quando sirenes, sensores e câmeras Matter estiverem disponíveis |

> O coordenador **Sonoff ZBDongle-P (CC2652P)** suporta firmware multiprotocolo (Zigbee + Thread) — é possível migrar sem trocar o hardware.

---

## ADR-005 — Mini PC N100 como Hardware Principal

**Decisão**: Intel N100 (Mini PC) como servidor central rodando Docker Compose (dev) ou K3s (produção).

**Alternativas avaliadas**:

| Hardware | Motivo da recusa |
|----------|-----------------|
| Raspberry Pi 4/5 | Suficiente para HA, mas sem iGPU para aceleração IA do Frigate |
| NUC Intel | Excelente, porém 3–4× mais caro que N100 |
| Home Assistant Green | Plug-and-play, mas sem GPU, limitado para Frigate |
| Servidor rack | Superdimensionado, alto consumo (>100W) |
| VPS/cloud | Contradiz o princípio de processamento local |

**Motivos da escolha**:
- iGPU Intel integrada: aceleração de hardware para detecção IA do Frigate (Intel QuickSync)
- Consumo: 10–20 W (idle/carga) — ideal para operação 24/7
- Preço: R$ 700–1.200 com 8–16 GB RAM
- Suporte Linux nativo, Docker, K3s

---

## ADR-006 — Câmeras PoE (não Wi-Fi)

**Decisão**: Câmeras conectadas via Ethernet PoE, não Wi-Fi.

**Motivos**:
- Resistentes a jamming de RF (Wi-Fi/Zigbee) — cenário de ataque A6
- Alimentação e dados em um único cabo (sem bateria, sem fio de energia separado)
- Latência menor e conexão mais estável
- Facilita VLAN isolada (VLAN 30) para câmeras

**Trade-off**: Requer cabeamento estruturado. Compensado pelo switch PoE.

---

## ADR-007 — VPN como Único Canal de Acesso Remoto

**Decisão**: Acesso remoto exclusivamente via VPN (WireGuard ou Tailscale). Port forwarding direto proibido.

**Motivos**:
- Evita exposição dos serviços à internet pública
- WireGuard: protocolo moderno, auditado, sem overhead
- Tailscale: VPN com NAT traversal automático, zero-config

**Regra derivada**: `REGRA-CIBER-01` — Ver [Segurança e Compliance](Seguranca-e-Compliance).

---

## ADR-008 — PostgreSQL com Schemas Isolados

**Decisão**: PostgreSQL 16 com 3 schemas isolados e usuários com mínimo privilégio para cada componente.

| Schema | Usuário | Responsável |
|--------|---------|-------------|
| `homeassistant` | `ha_user` | Home Assistant |
| `dashboard` | `dashboard_user` | Dashboard API |
| `metrics` | `metrics_user` | Coleta de métricas |

**Alternativa avaliada**: SQLite (padrão do HA). Descartado para ambientes com múltiplos acessos simultâneos (dashboard, métricas, backups), onde PostgreSQL oferece melhor concorrência e confiabilidade.

---

## ADR-009 — Docker Compose (dev) + K3s (produção)

**Decisão**: Dois modos de operação:
- **Docker Compose**: desenvolvimento, teste, início rápido
- **K3s (Kubernetes leve)**: produção, alta disponibilidade, rollout controlado

**Motivos**:
- Docker Compose: zero dependência adicional, curva mínima para novos usuários
- K3s: suporte a liveness/readiness probes, rolling updates, resource limits, Kustomize overlays por ambiente

**Migração**: `./scripts/deploy.sh production` automatiza o deploy em K3s.

---

## ADR-010 — External Secrets em Produção

**Decisão**: Adotar External Secrets Operator (ESO) como padrão operacional de produção para injeção de segredos em runtime.

**Motivos**:
- Evita versionamento de segredos reais em manifests.
- Permite rotação centralizada e auditável.
- Reduz risco de exposição acidental em PRs.

**Trade-off**:
- Adiciona dependência operacional de um operador no cluster.

**Implementação**:
- `k8s/overlays/production/external-secrets.yaml`
- `docs/K8S_SECRETS_MANAGEMENT.md`

---

## Referências

- `docs/MATTER_THREAD_EVALUATION.md` — análise completa Matter/Thread
- `docs/COMMERCIAL_ALTERNATIVES.md` — alternativas comerciais por subsistema
- `docs/ARQUITETURA_TECNICA.md` — stack técnico detalhado
- `docs/adr/` — Architecture Decision Records formais
- [Arquitetura](Arquitetura) — visão geral do sistema
- [Segurança e Compliance](Seguranca-e-Compliance) — regras derivadas das decisões
