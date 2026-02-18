# Avaliacao Matter/Thread vs Zigbee

> Sistema de Home Security – Open Source / Open Hardware
>
> Versao: 1.0 | Data: 2026-02-18 | Referencia: T-065

---

## 1. Contexto

O projeto utiliza **Zigbee 3.0** como protocolo principal de sensores (ADR-003). Esta avaliacao analisa a maturidade de Matter/Thread como alternativa e recomenda um plano de migracao futura.

---

## 2. O que e Matter/Thread

### Matter (antigo CHIP/Project Connected Home over IP)

- **Padrao**: Protocolo de aplicacao para smart home, mantido pela CSA (Connectivity Standards Alliance)
- **Versao atual**: Matter 1.4 (2025)
- **Objetivo**: Interoperabilidade entre dispositivos de diferentes fabricantes
- **Transporte**: Funciona sobre Wi-Fi, Thread e Ethernet
- **Apoiadores**: Apple, Google, Amazon, Samsung, Philips, IKEA

### Thread

- **Padrao**: Protocolo de rede mesh IPv6 de baixo consumo (IEEE 802.15.4)
- **Funcao**: Camada de transporte para Matter (similar ao que Zigbee faz)
- **Vantagens sobre Zigbee**: IPv6 nativo, mesh mais robusto, border router simples

---

## 3. Comparativo Matter/Thread vs Zigbee 3.0

| Aspecto | Zigbee 3.0 | Matter/Thread |
|---------|------------|---------------|
| **Maturidade** | 15+ anos, muito maduro | 3 anos, em evolucao rapida |
| **Dispositivos disponiveis** | Milhares (Aqara, Sonoff, Tuya, IKEA) | Centenas (crescendo) |
| **Disponibilidade no Brasil** | Alta (facil encontrar) | Baixa-media (importacao) |
| **Preco medio** | R$ 50-150 por sensor | R$ 80-250 por sensor |
| **Consumo de energia** | Muito baixo (1-2 anos bateria) | Muito baixo (similar) |
| **Mesh network** | Sim (Zigbee mesh) | Sim (Thread mesh, mais robusto) |
| **Criptografia** | AES-128 | AES-128 + autenticacao mais forte |
| **Frequencia** | 2.4 GHz | 2.4 GHz (Thread) |
| **IPv6 nativo** | Nao | Sim |
| **Interoperabilidade** | Dentro do Zigbee | Multi-ecossistema |
| **Home Assistant** | Excelente (ZHA, Z2M) | Bom (integracao Matter nativa) |
| **Coordenador necessario** | Sim (dongle USB) | Border router (ex: HomePod, Nest Hub) |
| **Estabilidade** | Muito estavel | Melhorando, mas ainda com bugs |

---

## 4. Estado atual de Matter (fevereiro 2026)

### Categorias de dispositivos suportados

| Categoria | Suporte Matter | Opcoes no mercado |
|-----------|---------------|-------------------|
| Iluminacao (lampadas, switches) | Completo | Philips Hue, IKEA, Nanoleaf |
| Tomadas e plugs | Completo | Eve, TP-Link, Meross |
| Fechaduras | Completo | Yale, Schlage, Aqara |
| Sensores de abertura | Completo | Eve, Aqara |
| Sensores de movimento | Completo | Eve, Aqara |
| Sensores de temperatura | Completo | Eve, Aqara |
| Termostatos | Completo | Nest, Ecobee |
| **Sirenes** | **Limitado** | **Poucas opcoes** |
| **Cameras** | **Parcial (Matter 1.3+)** | **Poucas opcoes** |
| **Sensores de fumaca** | **Limitado** | **Eve, First Alert** |
| **Botoes de panico** | **Limitado** | **Poucas opcoes** |

### Limitacoes atuais para o projeto

1. **Faltam sirenes Matter** compatíveis — componente critico para alarme
2. **Cameras sobre Matter** ainda sao experimentais
3. **Sensores especializados** (vibração, quebra de vidro, gás) praticamente inexistentes
4. **Alarmo** (add-on HA) funciona com Zigbee, suporte Matter nao testado amplamente
5. **Precos mais altos** no Brasil por disponibilidade limitada
6. **Border router** necessario (custo adicional se nao tiver HomePod/Nest Hub)

---

## 5. Recomendacao

### Curto prazo (2026): Manter Zigbee 3.0

**Justificativa:**
- Ecossistema muito mais completo para seguranca residencial
- Sensores disponíveis e baratos no Brasil
- Integracao madura com Home Assistant (ZHA e Z2M)
- Todos os tipos de sensores necessarios estao disponiveis
- Risco baixo de obsolescencia (Zigbee continua sendo suportado)

### Medio prazo (2027-2028): Adocao hibrida

**Acoes recomendadas:**
1. Ao comprar **novos dispositivos**, preferir modelos com suporte dual (Zigbee + Matter)
2. Testar border router Thread em paralelo
3. Avaliar sensores Matter conforme forem lancados
4. Manter Zigbee2MQTT como bridge principal

### Longo prazo (2029+): Migracao gradual

**Condicoes para migrar:**
- [ ] Sirenes Matter disponiveis e testadas
- [ ] Sensores de seguranca (fumaça, gás, abertura) amplamente disponiveis
- [ ] Precos competitivos com Zigbee no Brasil
- [ ] Home Assistant com suporte Matter estavel e completo
- [ ] Alarmo com suporte nativo a dispositivos Matter

---

## 6. Estrategia de compatibilidade

### Dispositivos com suporte dual

Vários fabricantes lancam dispositivos com suporte Zigbee + Matter. Priorizar estes na compra:

| Fabricante | Produtos com dual support | Observacao |
|------------|--------------------------|------------|
| **Aqara** | Sensores abertura, PIR, fechaduras | Firmware update para Matter |
| **IKEA** | Lampadas, tomadas, sensores | Thread border router incluido |
| **Eve** | Sensores, tomadas, interruptores | Thread nativo |
| **Sonoff** | Alguns modelos mais recentes | Verificar compatibilidade |

### Coordenador compativel

O **Sonoff ZBDongle-P (CC2652P)** suporta firmware multiprotocolo (Zigbee + Thread). Se necessario no futuro, e possivel flashear firmware Thread sem trocar hardware.

---

## 7. Riscos

| Risco | Probabilidade | Impacto | Mitigacao |
|-------|---------------|---------|-----------|
| Zigbee ser descontinuado | Muito baixa | Alto | Monitorar mercado, manter bridge |
| Matter nao amadurecer | Baixa | Baixo | Sem dependencia atual |
| Precos Matter nao cairem no BR | Media | Medio | Avaliar importacao vs local |
| Fragmentacao de protocolos | Media | Medio | Home Assistant abstrai o protocolo |

---

## 8. Conclusao

**Matter/Thread e o futuro do smart home, mas Zigbee 3.0 e a escolha certa para seguranca residencial hoje.** O ecossistema Zigbee e mais completo, mais barato e mais maduro para as necessidades do projeto. A migracao deve ser gradual e oportunista, priorizando dispositivos dual-protocol.

**Proxima revisao**: Janeiro 2027 (reavaliar estado do Matter)

---

## Referencias

- [Matter Specification](https://csa-iot.org/all-solutions/matter/)
- [Thread Group](https://www.threadgroup.org/)
- [Home Assistant Matter Integration](https://www.home-assistant.io/integrations/matter/)
- [Zigbee2MQTT](https://www.zigbee2mqtt.io/)
- [ADR-003 - Zigbee como protocolo](docs/adr/ADR-003-zigbee-protocolo.md)
