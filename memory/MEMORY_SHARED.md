# Memória Compartilhada do Projeto – Sistema de Home Security

> Comentário: Este arquivo registra contexto importante que todos os agentes e humanos devem conhecer.

---

## Resumo do projeto

**Sistema de Home Security Open Source e Open Hardware**

Este projeto desenvolve um sistema completo de segurança residencial baseado em software open source (Home Assistant, Frigate, ZoneMinder) e hardware aberto/genérico. A arquitetura segue o princípio de **defesa em profundidade** com três camadas: segurança **passiva** (barreiras físicas), **ativa** (sensores, câmeras, alarmes) e **reativa** (notificações, resposta a incidentes). O sistema atende a **três cenários residenciais**: propriedade rural, casa urbana com quintal e apartamento. Privacidade é garantida por design com processamento e armazenamento 100% local, sem dependência de nuvem.

---

## Decisões importantes

- [2026-02-12] **Regulamentação de drones pesquisada**: T-042 e T-043 concluídas. RBAC-E nº 94 (ANAC), SISANT (DECEA), ANATEL para rádios. Spray de pimenta permitido em propriedade privada (verificar legislação estadual). 22 regras criadas (REGRA-DRONE-01 a 22).

- [2026-02-12] **Módulo de drones autônomos adicionado**: Nova camada reativa avançada com frota modular de drones (UGV, UAV, USV). Arquitetura completa em `docs/ARQUITETURA_DRONES_AUTONOMOS.md`. PRD principal em `prd/PRD_AUTONOMOUS_DRONES.md`. 15 novas tarefas (T-031 a T-045) adicionadas ao backlog.

- [2026-02-12] **Stack de drones definido**: ROS2 Humble/Iron + Python/C++/Rust + TensorFlow Lite/YOLOv8. Hardware: Raspberry Pi 5 / Jetson Nano (UGV), Jetson Orin Nano (UAV), ESP32 + Pixhawk 6C. Comunicação: Wi-Fi 5GHz + LoRa/Meshtastic redundante.

- [2026-02-12] **Módulo de defesa não letal especificado**: Sistema CO₂ + OC (pimenta) com autenticação 2FA, auditoria completa, aviso sonoro/visual antes de disparo. Uso sujeito a legislação estadual.

- [2026-02-12] **Estimativas de custo de drones**: UGV básico R$ 2.500-4.000, UAV básico R$ 5.000-9.000, Frota inicial (1 UGV + 1 UAV) R$ 8.500-15.000.

- [2026-02-12] **🎉 PROJETO 100% CONCLUÍDO**: Todas as 30 tarefas finalizadas. Agente_Pesquisador_Normas concluiu T-028 a T-030 (fechaduras e iluminação). Projeto pronto para revisão e implementação.

- [2026-02-12] **Normas de fechaduras pesquisadas**: NBR 14913 (fechaduras de embutir), EN 1303 (cilindros europeu). Regras REGRA-FECHADURA-01 a 11 criadas. Recomendação: grau de segurança médio+, cilindro grau 5-6, protetor obrigatório.

- [2026-02-12] **Níveis de iluminação definidos**: NBR 8995-1 + IES. Entradas: 50-100 lux; identificação facial: 20 lux mínimo; perímetro: 10-30 lux. Regras REGRA-ILUM-01 a 10 criadas.

- [2026-02-12] **PRDs principais concluídos**: Agente_Documentador finalizou tarefas T-022 a T-025. Criados 6 PRDs: sensores/alarmes, videovigilância, dashboard e três cenários. Ver arquivos em `prd/`.

- [2026-02-12] **Estimativas de investimento definidas**: Rural R$ 5.460-6.480, Casa urbana R$ 4.510-5.360, Apartamento R$ 1.700-3.170. Valores baseados em preços de mercado 2026.

- [2026-02-12] **Arquitetura técnica concluída**: Agente_Arquiteto_Tecnico finalizou tarefas T-004 a T-006, T-011 a T-017, T-026, T-027. Documento completo criado em `docs/ARQUITETURA_TECNICA.md` com stack recomendado (Home Assistant + Frigate + Zigbee), arquitetura de rede com VLANs, e política de retenção.

- [2026-02-12] **Stack tecnológico definido**: Home Assistant (automação), Frigate (NVR), Zigbee 3.0 (sensores), Mini PC Intel N100 (hardware), WireGuard (VPN). Ver detalhes em `docs/ARQUITETURA_TECNICA.md`.

- [2026-02-12] **Arquitetura de segurança física concluída**: Agente_Arquiteto_Seguranca_Fisica finalizou tarefas T-001 a T-003, T-007 a T-010. Documento completo criado em `docs/ARQUITETURA_SEGURANCA_FISICA.md` com requisitos para os três cenários, diagramas de posicionamento e plano de resposta a incidentes.

- [2026-02-12] **Modelo de 4 zonas definido**: Perímetro → Área externa → Envelope → Interior. Cada zona tem requisitos específicos por cenário.

- [2026-02-12] **Recomendações de câmeras por cenário**: Rural (4-6), Casa urbana (3-5), Apartamento (0-1, olho mágico digital).

- [2026-02-12] **Pesquisa de normas concluída**: Agente_Pesquisador_Normas finalizou tarefas T-018 a T-021. Principais normas documentadas: LGPD (com exceção Art. 4º, I para uso pessoal), OWASP IoT Top 10, ETSI EN 303 645, NBR 5410/5419, Lei 13.477/2017 (cercas). Ver `standards/STANDARDS_TO_RESEARCH.md` e `rules/RULES_COMPLIANCE_AND_STANDARDS.md`.

- [2026-02-12] **Retenção de gravações definida**: Padrão de 30 dias com rotação automática. Mecanismo para preservar evidências de incidentes deve ser implementado.

- [2026-02-12] **LGPD - Exceção para uso pessoal confirmada**: Câmeras em residência particular que captam APENAS área privada estão fora do escopo da LGPD (Art. 4º, I). Câmeras que captam via pública ou vizinhos devem seguir LGPD integralmente.

- [2026-02-12] **Inicialização do projeto**: Template de documentação especializado para Sistema de Home Security. Definidos três cenários residenciais (rural, casa urbana, apartamento) e três camadas de segurança (passiva, ativa, reativa). Ver `PROJECT_OVERVIEW.md`.

- [2026-02-12] **Princípio de privacidade**: Decidido que TODO processamento e armazenamento será local (on-premise). Nenhuma funcionalidade essencial dependerá de serviços em nuvem. Conformidade com LGPD por design.

- [2026-02-12] **Foco em open source**: Plataformas primárias definidas como Home Assistant (automação) e Frigate (NVR com detecção). Alternativas documentadas em `RULES_TECHNICAL.md`.

- [2026-02-12] **Estrutura de agentes**: Definidos 5 agentes especializados para o projeto. Ver `agents/AGENTS_CONFIG.md` para configuração detalhada.

---

## Contexto adicional

### Cenários residenciais

| Cenário | Características principais | Complexidade |
|---------|---------------------------|--------------|
| Rural | Perímetro extenso, área aberta, menor vizinhança | Alta |
| Casa urbana | Perímetro médio, muros/grades, quintal | Média |
| Apartamento | Sem perímetro externo, foco em acesso | Baixa |

### Camadas de segurança

| Camada | Descrição | Exemplos |
|--------|-----------|----------|
| Passiva | Barreiras físicas sem energia | Muros, grades, fechaduras, iluminação natural |
| Ativa | Sistemas eletrônicos de detecção | Sensores, câmeras, alarmes, automações |
| Reativa | Resposta e recuperação | Notificações, evidências, plano de ação |

### Estado atual do projeto

- **Fase**: ✅ **PLANEJAMENTO CORE CONCLUÍDO** + 🚀 **MÓDULO DRONES EM DESENVOLVIMENTO**
- **PRDs**: 7 de 20 concluídos (6 principais + 1 drones)
- **Backlog**: 32/45 tarefas concluídas (71%) - 13 tarefas de drones pendentes
- **Normas**: Pesquisa completa em `standards/STANDARDS_TO_RESEARCH.md` (incluindo ANAC/DECEA)
- **Compliance**: 69 regras derivadas em `rules/RULES_COMPLIANCE_AND_STANDARDS.md` (+22 drones)
- **Arquitetura física**: `docs/ARQUITETURA_SEGURANCA_FISICA.md`
- **Arquitetura técnica**: `docs/ARQUITETURA_TECNICA.md`
- **Arquitetura drones**: `docs/ARQUITETURA_DRONES_AUTONOMOS.md`

### Status dos agentes

| Agente | Tarefas | Status |
|--------|---------|--------|
| Agente_Pesquisador_Normas | T-018 a T-021, T-028 a T-030 | ✅ Concluído (7 tarefas) |
| Agente_Arquiteto_Seguranca_Fisica | T-001 a T-003, T-007 a T-010 | ✅ Concluído (7 tarefas) |
| Agente_Arquiteto_Tecnico | T-004 a T-006, T-011 a T-017, T-026, T-027 | ✅ Concluído (12 tarefas) |
| Agente_Documentador | T-022 a T-025 | ✅ Concluído (4 tarefas) |
| Agente_Arquiteto_Drones | T-031 a T-039 (pendentes) | 🚀 Novo agente - 9 tarefas pendentes |

---

## Convenções para escrita

- Sempre incluir data no formato [AAAA-MM-DD].
- Ser objetivo e claro.
- Referenciar arquivos e tarefas quando possível.
- Registrar decisões que afetam múltiplos agentes ou componentes.
- Não registrar detalhes de implementação (usar PRDs ou docs específicos).

---

## Próximas decisões pendentes

> ✅ RESOLVIDO: Plataforma de automação definida como Home Assistant.

> ✅ RESOLVIDO: Hardware definido como Mini PC Intel N100 (cenários rural/urbano) ou equivalente menor para apartamento.

> ✅ RESOLVIDO: Três cenários validados com requisitos detalhados nos PRDs.

---

## Próximos passos sugeridos

### Revisão e aprovação
1. Revisar os 6 PRDs criados e documentação de arquitetura
2. Validar estimativas de investimento por cenário
3. Aprovar projeto para início da implementação

### Implementação
4. Selecionar cenário para piloto (recomendado: apartamento por menor complexidade)
5. Adquirir materiais conforme lista de componentes no PRD do cenário
6. Instalar sistema piloto e validar funcionamento
7. Expandir para outros cenários

### PRDs complementares (opcional)
- PRD_NETWORK_SECURITY (VLANs e firewall)
- PRD_LOCAL_PROCESSING_HUB (hardware central)
- PRD_AUTOMATION_AND_SCENES (automações)
- PRDs de cenários específicos (controle de acesso rural, fechadura apartamento)

