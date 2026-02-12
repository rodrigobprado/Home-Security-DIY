# Memória Local – Agente_Arquiteto_Drones

## Contexto de trabalho atual

> Módulo de drones autônomos adicionado ao projeto em 2026-02-12.
>
> **Tarefas concluídas**:
> - ✅ T-042: Pesquisa de normas ANAC/DECEA concluída
> - ✅ T-043: Pesquisa de legislação defesa não letal concluída
>
> **Arquivos principais criados**:
> - `docs/ARQUITETURA_DRONES_AUTONOMOS.md` – Arquitetura completa
> - `prd/PRD_AUTONOMOUS_DRONES.md` – PRD principal (46 RF, 20 RNF)
> - `standards/STANDARDS_TO_RESEARCH.md` – Seção 8 (regulamentação drones)
> - `rules/RULES_COMPLIANCE_AND_STANDARDS.md` – 22 regras de drones
>
> **Próximas tarefas prioritárias**:
> - T-031: Definir arquitetura de hardware UGV
> - T-033: Desenvolver firmware de controle
> - T-034: Implementar stack ROS2
> - T-036: Sistema de comunicação redundante

---

## Anotações e rascunhos

### Decisões técnicas tomadas

| Decisão | Justificativa |
|---------|---------------|
| ROS2 Humble/Iron | LTS com suporte até 2027, melhor para robótica |
| ESP32 para controle baixo nível | Custo baixo, Wi-Fi integrado, comunidade ativa |
| Pixhawk 6C para UAV | Padrão de mercado, compatível com PX4/ArduPilot |
| YOLOv8 para detecção | Melhor relação precisão/velocidade em edge |
| LoRa como fallback | Longo alcance (2km+), baixo consumo |

### Hardware de referência

| Componente | UGV | UAV |
|------------|-----|-----|
| Computador | Raspberry Pi 5 / Jetson Nano | Jetson Orin Nano |
| Controlador | ESP32 / Arduino | Pixhawk 6C |
| Câmera | Pi Camera V3 + Flir Lepton | IMX477 + gimbal |
| GPS | u-blox NEO-M8N | HERE3+ RTK |

---

## Cache de pesquisas

### Pesquisa concluída (T-042, T-043)

**ANAC - Classificação de drones**:
| Peso | Classe | Requisitos |
|------|--------|------------|
| ≤ 250g | Classe 3 | Dispensa registro |
| > 250g e ≤ 25kg | Classe 3 | Registro ANAC + SISANT |
| > 25kg | Classe 2/1 | Certificação + piloto habilitado |

**Operação - Regras gerais**:
- VLOS obrigatório (ou autorização BVLOS)
- Altura máxima: 120m AGL
- Distância de pessoas: 30m
- Verificar NOTAM antes de cada voo

**ANATEL - Frequências permitidas**:
- Wi-Fi 2.4GHz: 400mW EIRP
- Wi-Fi 5GHz: 1W EIRP
- LoRa 915MHz: 1W EIRP

**Defesa não letal**:
- Spray pimenta = arma menos letal (não é arma de fogo)
- Permitido em propriedade privada
- Verificar legislação estadual

### Links úteis

- [PX4 Documentation](https://docs.px4.io/)
- [ROS2 Navigation](https://nav2.org/)
- [YOLOv8 Documentation](https://docs.ultralytics.com/)
- [ANAC - RPAS](https://www.gov.br/anac/pt-br/assuntos/drones)
- [SISANT - Cadastro](https://servicos.decea.mil.br/sisant/)
- [AIS Web - Cartas aeronáuticas](https://aisweb.decea.mil.br/)

---

## Pendências e dúvidas

### Resolvidos pela pesquisa T-042/T-043
- [x] Confirmar se drones <250g estão isentos de registro ANAC → **SIM, dispensam registro**
- [x] Pesquisar homologação ANATEL para módulos LoRa RFM95W → **Usar módulos já homologados (ESP32, etc.)**
- [x] Legislação spray pimenta → **Permitido em propriedade privada, verificar legislação estadual**

### Pendentes para Agente_Pesquisador_Normas
- [ ] Verificar legislação estadual específica para spray de pimenta em SP/RJ/MG (detalhes por UF)
- [ ] Pesquisar normas específicas para robôs terrestres (UGV) se existirem

### Para Agente_Arquiteto_Tecnico
- [ ] Validar integração MQTT com Home Assistant
- [ ] Confirmar se Frigate suporta streaming RTSP de drones
- [ ] Discutir VLAN específica para drones (IoT ou separada?)

### Para humano
- [ ] Aprovar estimativa de custos (R$ 8.500-15.000 para frota inicial)
- [ ] Definir cenário de piloto (rural ou urbano?)
- [ ] Confirmar prioridade do módulo de defesa (opcional ou obrigatório?)
- [ ] Verificar zona de operação (CTR próximo? Precisa autorização DECEA?)

---

## Histórico de alterações

| Data | Alteração |
|------|-----------|
| 2026-02-12 | Criação inicial do agente e estrutura de memória |
| 2026-02-12 | Arquitetura completa de drones documentada |
| 2026-02-12 | PRD principal criado com 46 RF e 20 RNF |
| 2026-02-12 | 15 tarefas adicionadas ao backlog (T-031 a T-045) |
| 2026-02-12 | T-042 concluída: Pesquisa ANAC/DECEA (RBAC-E nº 94, SISANT, ANATEL) |
| 2026-02-12 | T-043 concluída: Pesquisa legislação defesa não letal |
| 2026-02-12 | 22 regras de drones criadas (REGRA-DRONE-01 a 22) |

