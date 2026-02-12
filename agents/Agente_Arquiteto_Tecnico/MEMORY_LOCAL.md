# Memória Local – Agente_Arquiteto_Tecnico

## Contexto de trabalho atual

**Status**: Tarefas T-004 a T-006, T-011 a T-017, T-026, T-027 concluídas em 2026-02-12.

Documento principal de arquitetura técnica criado em `docs/ARQUITETURA_TECNICA.md`.

---

## Pesquisas realizadas (2026-02-12)

### Plataformas de automação (T-013)

**Home Assistant vs openHAB:**
- Home Assistant: Maior comunidade, 2000+ integrações, atualizações mensais
- openHAB: Mais estável, menos integrações, curva maior
- **Decisão: Home Assistant** - melhor para home security (Alarmo, Frigate nativo)

### NVRs open source (T-014)

**Frigate vs ZoneMinder vs Shinobi:**
- Frigate: Detecção de objetos IA nativa, integração perfeita com HA
- ZoneMinder: Mais maduro, sem IA nativa
- Shinobi: Interface moderna, menos estável
- **Decisão: Frigate** - detecção de pessoas/veículos essencial

### Protocolos de sensores (T-015)

| Protocolo | Vencedor para |
|-----------|---------------|
| Zigbee | Sensores porta/janela, PIR, sirene (baixo custo, mesh) |
| PoE | Câmeras (alimentação + dados) |
| Z-Wave | Fechaduras (mais confiável, mas mais caro) |

**Decisão: Zigbee como principal** - custo-benefício, disponibilidade no Brasil

### Hardware (T-016)

**Raspberry Pi 5 vs Mini PC N100:**
- N100 é 2-3x mais rápido
- Intel Quick Sync para vídeo
- OpenVINO para IA (sem precisar Coral)
- Custo similar com acessórios
- **Decisão: Mini PC Intel N100**

### Câmeras (T-017)

**Compatíveis com Frigate:**
- Reolink: Melhor custo-benefício, RTSP nativo
- Hikvision/Dahua: Profissional
- PoE obrigatório para confiabilidade

---

## Decisões de arquitetura tomadas

### Stack recomendado
1. **Plataforma**: Home Assistant OS
2. **NVR**: Frigate
3. **Alarme**: Alarmo (add-on HA)
4. **Zigbee**: Zigbee2MQTT + Sonoff ZBDongle-P
5. **Hardware**: Mini PC Intel N100 8GB
6. **Acesso remoto**: WireGuard VPN

### Arquitetura de rede (T-012)
- 4 VLANs: Principal, Gestão, IoT, Câmeras
- Câmeras isoladas SEM internet
- VPN para acesso remoto (nunca port forwarding)

### Privacidade por design (T-026)
- Processamento 100% local
- Sem dependência de nuvem
- Câmeras bloqueadas de internet
- Criptografia em trânsito (HTTPS, VPN)

### Retenção de gravações (T-027)
- Normal: 30 dias
- Eventos detectados: 60 dias
- Incidentes marcados: 1 ano
- Armazenamento: HDD 2-4TB

---

## Estimativas de investimento

| Cenário | Total estimado |
|---------|----------------|
| Rural | R$ 5.950 |
| Casa urbana | R$ 4.950 |
| Apartamento | R$ 2.450 |

---

## Recomendações para outros agentes

### Para Agente_Documentador
- Documento `ARQUITETURA_TECNICA.md` é a base para PRDs técnicos
- PRD_SENSORS_AND_ALARMS_PLATFORM: usar seção de protocolos e sensores
- PRD_VIDEO_SURVEILLANCE_AND_NVR: usar seção de Frigate e câmeras
- PRD_NETWORK_SECURITY: usar seção de VLANs e firewall

### Para Agente_Pesquisador_Normas
- Google Coral sendo descontinuado - monitorar alternativas
- Matter/Thread em evolução - pode ser padrão no futuro

---

## Cache de pesquisas

### Links úteis
- https://www.home-assistant.io/
- https://docs.frigate.video/
- https://www.zigbee2mqtt.io/
- https://www.cnx-software.com/2024/04/29/raspberry-pi-5-intel-n100-mini-pc-comparison

### Coordenadores Zigbee testados
- Sonoff ZBDongle-P (CC2652P): Recomendado, ~R$100-150
- SLZB-06: PoE, mais robusto, ~R$200-300

### Sensores Zigbee recomendados
- Abertura: Aqara MCCGQ11LM, Sonoff SNZB-04
- Movimento: Aqara RTCGQ11LM, Sonoff SNZB-03
- Sirene: Heiman HS2WD-E, Tuya TS0224

---

## Pendências resolvidas

- [x] Orçamento alvo → Documentado por cenário
- [x] Preferência protocolo → Zigbee recomendado
- [x] Quantidade câmeras → Rural 4-6, Urbana 3-5, Apto 0-1
- [x] Nível técnico usuário → HA mais acessível que openHAB

---

## Notas técnicas importantes

1. **Google Coral descontinuado**: Frigate recomenda OpenVINO (Intel) para novas instalações
2. **Matter/Thread**: Futuro promissor, mas ainda em adoção - manter Zigbee como principal
3. **Aqara no Zigbee**: Pode ter incompatibilidades com alguns roteadores - usar IKEA como repetidores
4. **Câmeras Reolink**: Excelente custo-benefício, RTSP funciona bem com Frigate
5. **VLANs**: Essenciais para segurança - câmeras NUNCA devem ter acesso à internet

