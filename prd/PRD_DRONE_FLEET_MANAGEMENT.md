# PRD -- Gerenciamento de Frota de Drones

> Sistema de Home Security -- Open Source / Open Hardware
>
> Modulo Reativo Avancado -- Coordenacao Multi-Drone
>
> Versao: 1.0 | Data: 2026-02-18 | Responsavel: Agente_Arquiteto_Drones

---

## 1. Visao geral

- **Nome do produto/funcionalidade**: Sistema de Gerenciamento de Frota de Drones Autonomos
- **Responsavel**: Agente_Arquiteto_Drones
- **Data**: 2026-02-18
- **PRDs relacionados**: PRD_AUTONOMOUS_DRONES, PRD_DRONE_COMMUNICATION, PRD_DRONE_AI_VISION, PRD_DRONE_DEFENSE_MODULE, PRD_MONITORING_DASHBOARD

---

## 2. Problema e oportunidade

### 2.1 Problema

Um unico drone de seguranca apresenta limitacoes significativas:

- **Cobertura limitada**: um drone nao consegue patrulhar toda a propriedade simultaneamente
- **Autonomia de bateria**: UGV (2-4h) e UAV (20-40min) precisam de recarga, criando janelas de vulnerabilidade
- **Ponto unico de falha**: se o drone falha, nao ha cobertura
- **Resposta a incidentes**: um drone em patrulha pode estar longe do ponto de alerta
- **Sem coordenacao inteligente**: drones operando independentemente podem cobrir a mesma area e ignorar outras
- **Substituicao manual**: operador precisa intervir para gerenciar recarga e substituicao

### 2.2 Oportunidade

Desenvolver um sistema de gerenciamento de frota que:

- **Coordena multiplos drones** (UGV e UAV) de forma inteligente
- **Divide areas de patrulha** automaticamente conforme capacidades de cada drone
- **Balanceia por bateria**: drones com bateria baixa retornam e sao substituidos automaticamente
- **Responde coordenadamente** a incidentes: drones proximos convergem ao ponto de alerta
- **Garante cobertura continua** 24/7 com substituicao automatica
- **Oferece dashboard unificado** no Home Assistant com visao de toda a frota

---

## 3. Publico-alvo

| Perfil | Descricao | Necessidades especificas |
|--------|-----------|--------------------------|
| **Proprietario rural** | Grandes propriedades (>1 hectare) | Cobertura 24/7 de perimetro extenso com multiplos drones |
| **Proprietario urbano** | Casas com quintal e garagem | Coordenacao entre UGV (terrestre) e cameras fixas |
| **Operador do sistema** | Pessoa monitorando a frota | Dashboard unificado, alertas de status, controle centralizado |
| **Integrador DIY** | Construtor com multiplos drones | APIs claras, documentacao de coordenacao |

---

## 4. Requisitos funcionais

### 4.1 Registro e inventario de frota

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-001 | Registrar cada drone com identificador unico, tipo (UGV/UAV), capacidades e modulos instalados | Alta |
| RF-002 | Manter inventario atualizado com status em tempo real de cada drone | Alta |
| RF-003 | Catalogar capacidades por drone: camera, termica, lidar, modulo de defesa, autonomia | Alta |
| RF-004 | Registrar estacoes de recarga com localizacao e capacidade | Alta |
| RF-005 | Manter historico de manutencao e horas de operacao por drone | Media |
| RF-006 | Alertas de manutencao preventiva baseados em horas de operacao | Baixa |

### 4.2 Divisao de areas de patrulha

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-007 | Definir mapa da propriedade com zonas de patrulha configuráveis | Alta |
| RF-008 | Dividir automaticamente areas entre drones disponiveis | Alta |
| RF-009 | Considerar tipo de drone na alocacao: UGV para terreno plano, UAV para areas elevadas | Alta |
| RF-010 | Priorizar zonas criticas (entradas, pontos vulneraveis) com frequencia maior de patrulha | Alta |
| RF-011 | Reajustar divisao dinamicamente quando drones entram/saem de operacao | Alta |
| RF-012 | Rotas de patrulha com waypoints configuráveis por zona | Alta |
| RF-013 | Evitar sobreposicao desnecessaria de areas entre drones | Media |
| RF-014 | Suportar patrulha aleatoria (aleatorizar rotas) para dificultar previsibilidade | Media |

### 4.3 Balanceamento por bateria e substituicao automatica

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-015 | Monitorar nivel de bateria de todos os drones em tempo real | Alta |
| RF-016 | Quando bateria < 20%, iniciar retorno a estacao de recarga (REGRA-DRONE-19) | Alta |
| RF-017 | Antes de iniciar retorno, solicitar drone substituto ao fleet manager | Alta |
| RF-018 | Drone substituto assume a area de patrulha antes do retorno do drone com bateria baixa | Alta |
| RF-019 | Estacoes de recarga automatica para UGV (dock com contatos de carga) | Media |
| RF-020 | Fila de prioridade para recarga quando ha mais drones que estacoes | Media |
| RF-021 | Estimativa de autonomia restante baseada em consumo medio e terreno | Media |
| RF-022 | Planejamento de recarga para garantir cobertura continua 24/7 | Alta |

### 4.4 Resposta coordenada a incidentes

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-023 | Ao receber alerta do sistema de alarme, despachar drone mais proximo ao ponto de incidente | Alta |
| RF-024 | Se incidente classificado como alto risco, despachar multiplos drones | Alta |
| RF-025 | Drone principal: segue e documenta (video + GPS) | Alta |
| RF-026 | Drone secundario: cobre rotas de fuga e saidas da propriedade | Media |
| RF-027 | Coordenar com sistema de defesa: apenas drone autorizado pode acionar modulo de defesa | Alta |
| RF-028 | Priorizar resposta a incidente sobre patrulha regular | Alta |
| RF-029 | Redistribuir areas de patrulha para drones restantes durante incidente | Media |
| RF-030 | Registro completo do incidente: timeline, drones envolvidos, acoes tomadas | Alta |

### 4.5 Planejamento e agendamento de missoes

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-031 | Definir agendamento de patrulha por horario (diurno/noturno com rotas diferentes) | Alta |
| RF-032 | Missoes especiais: inspecao de perimetro sob demanda | Media |
| RF-033 | Missoes de verificacao: confirmar alertas de sensores | Alta |
| RF-034 | Prioridade de missoes: emergencia > verificacao > patrulha > inspecao | Alta |
| RF-035 | Cancelamento e reagendamento de missoes conforme necessidade | Media |

### 4.6 Dashboard no Home Assistant

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-036 | Mapa em tempo real com posicao de todos os drones | Alta |
| RF-037 | Status de cada drone: bateria, modo, missao atual, velocidade | Alta |
| RF-038 | Visualizacao de areas de patrulha e zonas de cobertura | Alta |
| RF-039 | Historico de patrulhas com trajeto percorrido | Media |
| RF-040 | Controle manual: despachar drone a ponto especifico | Alta |
| RF-041 | Controle de frota: pausar/retomar patrulha, RTH de todos os drones | Alta |
| RF-042 | Alertas de status: bateria baixa, drone offline, falha de comunicacao | Alta |
| RF-043 | Timeline de incidentes com drones envolvidos | Media |
| RF-044 | Metricas de frota: cobertura total, tempo de operacao, distancia percorrida | Baixa |
| RF-045 | Stream de video de qualquer drone selecionado no mapa | Alta |

### 4.7 Integracao com sistema de seguranca

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-046 | Receber eventos do Alarmo (sistema de alarme) via MQTT | Alta |
| RF-047 | Receber eventos de deteccao do Frigate via MQTT | Alta |
| RF-048 | Disparar missao de verificacao automatica ao receber alerta | Alta |
| RF-049 | Enviar status da frota para dashboard de monitoramento | Alta |
| RF-050 | Integrar com notificacoes: Telegram, push, e-mail | Alta |

---

## 5. Requisitos nao funcionais

### 5.1 Performance

| ID | Requisito | Especificacao |
|----|-----------|---------------|
| RNF-001 | Tempo de despacho de drone apos alerta | < 10 segundos (decisao) + tempo de deslocamento |
| RNF-002 | Frequencia de atualizacao de telemetria no dashboard | 1Hz (1 atualizacao por segundo) |
| RNF-003 | Tempo de realocacao de areas apos mudanca na frota | < 5 segundos |
| RNF-004 | Numero maximo de drones suportados | >= 10 (escalavel) |
| RNF-005 | Latencia de comando fleet manager -> drone | < 500ms |

### 5.2 Confiabilidade

| ID | Requisito | Especificacao |
|----|-----------|---------------|
| RNF-006 | Disponibilidade do fleet manager | > 99.5% |
| RNF-007 | Recuperacao de falha do fleet manager | < 30 segundos (restart automatico) |
| RNF-008 | Comportamento de drones se fleet manager offline | Continuar missao atual + RTH ao finalizar |
| RNF-009 | Persistencia de estado | Estado da frota salvo em disco a cada 10 segundos |

### 5.3 Escalabilidade

| ID | Requisito | Especificacao |
|----|-----------|---------------|
| RNF-010 | Adicionamento de novos drones | Hot-plug sem reiniciar sistema |
| RNF-011 | Areas de patrulha reconfiguráveis | Sem reiniciar sistema |
| RNF-012 | Suporte a tipos mistos de drones | UGV + UAV + USV na mesma frota |

### 5.4 Seguranca

| ID | Requisito | Especificacao |
|----|-----------|---------------|
| RNF-013 | Autenticacao de drones na frota | Certificados digitais unicos |
| RNF-014 | Autorizacao de comandos de frota | Somente operadores autenticados |
| RNF-015 | Logs de operacao da frota | Imutaveis com hash (REGRA-DRONE-22) |

---

## 6. Arquitetura tecnica

### 6.1 Diagrama de componentes

```
+-----------------------------------------------------------------------+
|                    SERVIDOR CENTRAL (Estacao Base)                     |
|                                                                       |
|  +---------------------+       +----------------------------------+   |
|  |   HOME ASSISTANT    |<----->|        FLEET MANAGER             |   |
|  |   Dashboard + Cards |       |   (Servico Python/ROS2)          |   |
|  +---------------------+       |                                  |   |
|                                |  +----------------------------+  |   |
|  +---------------------+      |  | Planejador de Missoes      |  |   |
|  |     MOSQUITTO       |<---->|  +----------------------------+  |   |
|  |    MQTT Broker       |      |  | Alocador de Areas          |  |   |
|  +---------------------+      |  +----------------------------+  |   |
|                                |  | Monitor de Bateria         |  |   |
|  +---------------------+      |  +----------------------------+  |   |
|  |     FRIGATE          |<---->|  | Coordenador de Incidentes  |  |   |
|  |   Eventos de IA      |      |  +----------------------------+  |   |
|  +---------------------+      |  | Banco de Estado (SQLite)   |  |   |
|                                |  +----------------------------+  |   |
|                                +----------------------------------+   |
|                                          |                            |
+---------+------------------+-------------+----------------------------+
          |                  |             |
          v                  v             v
   +------+------+   +------+------+  +---+----------+
   |   DRONE 1   |   |   DRONE 2   |  |   DRONE N    |
   |   UGV       |   |   UGV       |  |   UAV        |
   |   Zona A    |   |   Zona B    |  |   Zona C     |
   +-------------+   +-------------+  +--------------+
```

### 6.2 Fluxo de resposta coordenada a incidente

```
1. Sistema de alarme ou Frigate detecta evento
        |
        v
2. Evento publicado via MQTT: tipo, localizacao, severidade
        |
        v
3. Fleet Manager recebe evento e classifica prioridade
        |
        v
4. Consulta frota: quais drones disponiveis e onde estao?
        |
        v
5. Calcula drone mais proximo ao ponto de incidente
        |
        v
6. Despacha drone principal para investigar
   +-- Se severidade ALTA: despacha drone secundario para cobrir fugas
        |
        v
7. Redistribui areas de patrulha entre drones restantes
        |
        v
8. Drones em missao de incidente:
   +-- Drone principal: segue alvo, transmite video, registra GPS
   +-- Drone secundario: cobre saidas, posiciona-se estrategicamente
        |
        v
9. Operador avalia situacao via dashboard (video + telemetria)
        |
        v
10. Ao encerrar incidente: drones retornam a patrulha normal
    +-- Areas redistribuidas automaticamente
```

### 6.3 Algoritmo de divisao de areas

```
ENTRADA:
  - Mapa da propriedade (poligono com zonas)
  - Lista de drones disponiveis (tipo, autonomia, posicao)
  - Prioridades por zona (critica, alta, media, baixa)

PROCESSO:
  1. Calcular area total e subdividir em celulas de grid
  2. Ponderar celulas por prioridade (zonas criticas = peso 3x)
  3. Para cada drone disponivel:
     a. Calcular raio de cobertura baseado em tipo e autonomia
     b. Atribuir celulas adjacentes a base/posicao atual
     c. Balancear carga: cada drone cobre ~mesmo "peso total"
  4. Gerar waypoints de patrulha para cada drone
  5. Considerar tempo de deslocamento entre waypoints

SAIDA:
  - Mapa de alocacao: drone -> zona -> waypoints
  - Tempo estimado de ciclo de patrulha por drone
  - Areas nao cobertas (se frota insuficiente) -> alerta ao operador
```

### 6.4 Topicos MQTT do Fleet Manager

| Topico | Direcao | Descricao |
|--------|---------|-----------|
| `fleet/status` | FM -> HA | Status geral da frota (JSON) |
| `fleet/drones` | FM -> HA | Lista de drones com status individual |
| `fleet/zones` | FM -> HA | Mapa de zonas e alocacoes |
| `fleet/incident` | FM -> HA | Incidente ativo com timeline |
| `fleet/command` | HA -> FM | Comandos manuais do operador |
| `fleet/dispatch` | FM -> Drone | Despacho de missao para drone especifico |
| `drone/{id}/mission` | FM -> Drone | Missao atribuida (waypoints, tipo, prioridade) |
| `drone/{id}/mission_status` | Drone -> FM | Progresso da missao atual |
| `drone/{id}/telemetry` | Drone -> FM | Telemetria (posicao, bateria, velocidade) |

### 6.5 Nos ROS2 do Fleet Manager

| No | Funcao |
|----|--------|
| `/fleet_manager` | No principal de coordenacao |
| `/mission_planner` | Planejamento e agendamento de missoes |
| `/zone_allocator` | Divisao e alocacao de areas |
| `/battery_monitor` | Monitoramento de bateria e agendamento de recarga |
| `/incident_coordinator` | Coordenacao de resposta a incidentes |
| `/fleet_mqtt_bridge` | Ponte MQTT <-> ROS2 para integracao com HA |

---

## 7. Hardware e componentes recomendados

### 7.1 Servidor do Fleet Manager

| Componente | Modelo | Preco estimado (R$) | Funcao |
|------------|--------|---------------------|--------|
| Servidor central | Mini PC N100 (ja existente no hub) | R$ 0 (compartilhado) | Roda fleet manager como servico Docker |
| Armazenamento adicional | SSD NVMe 256GB | R$ 150-250 | Banco de estado e logs |

### 7.2 Estacao de recarga UGV

| Componente | Modelo | Preco estimado (R$) | Funcao |
|------------|--------|---------------------|--------|
| Base de recarga | Dock custom com contatos spring-loaded | R$ 100-200 | Contato eletrico para recarga |
| Carregador | Carregador LiPo/Li-Ion balanceado 4S | R$ 150-300 | Carga segura da bateria |
| Guias de alinhamento | Trilhos em V (impressao 3D) | R$ 30-50 | Alinhamento do drone com dock |
| Sensor de presenca | Switch mecanico ou magnetico | R$ 10-20 | Detectar drone no dock |
| Controlador | ESP32 com monitoramento de carga | R$ 50-80 | Gerenciar ciclo de carga |

### 7.3 Frota minima recomendada

| Configuracao | Drones | Custo estimado |
|--------------|--------|----------------|
| **Casa urbana (basica)** | 1x UGV | R$ 2.100-3.460 (ref. ARQUITETURA_HARDWARE_UGV) |
| **Casa urbana (redundante)** | 2x UGV + 1 dock | R$ 4.600-7.300 |
| **Propriedade rural (basica)** | 2x UGV + 1 dock | R$ 4.600-7.300 |
| **Propriedade rural (completa)** | 3x UGV + 1x UAV + 2 docks | R$ 10.000-16.000 |
| **Estacao de recarga UGV (por unidade)** | - | R$ 340-650 |

---

## 8. Criterios de aceitacao

| ID | Criterio | Metodo de verificacao |
|----|----------|----------------------|
| CA-001 | Fleet manager registra e gerencia pelo menos 3 drones simultaneamente | Teste com 3 drones ativos |
| CA-002 | Divisao automatica de areas funciona ao adicionar/remover drone | Teste de hot-plug |
| CA-003 | Drone com bateria < 20% inicia retorno e solicita substituto | Teste de descarga controlada |
| CA-004 | Drone substituto assume patrulha antes do retorno do original | Teste de substituicao |
| CA-005 | Despacho de drone apos alerta ocorre em < 10 segundos | Teste com evento simulado |
| CA-006 | Multiplos drones convergem em incidente de alta severidade | Teste de incidente simulado |
| CA-007 | Dashboard exibe mapa com posicao de todos os drones | Verificacao visual |
| CA-008 | Dashboard permite despacho manual de drone a ponto especifico | Teste funcional |
| CA-009 | Areas de patrulha sao redistribuidas ao perder um drone | Teste de falha simulada |
| CA-010 | Integracao com Alarmo e Frigate funciona via MQTT | Teste de integracao |
| CA-011 | Historico de patrulhas e incidentes e acessivel no dashboard | Verificacao de dados |
| CA-012 | Cobertura continua 24/7 com frota de 2+ UGVs e dock de recarga | Teste de 24 horas |

---

## 9. Metricas de sucesso

| Metrica | Alvo | Medicao |
|---------|------|---------|
| **Cobertura de area** | 100% das zonas criticas patrulhadas a cada 30 minutos | Analise de logs de waypoints |
| **Tempo de resposta a incidente** | < 60 segundos (despacho + deslocamento) | Analise de timeline de incidentes |
| **Uptime de cobertura** | > 95% do tempo com pelo menos 1 drone patrulhando | Monitoramento de missoes ativas |
| **Taxa de substituicao bem-sucedida** | > 99% de substituicoes sem gap de cobertura | Analise de logs de bateria |
| **Disponibilidade do fleet manager** | > 99.5% | Monitoramento do servico |
| **Incidentes com resposta coordenada** | 100% de incidentes com despacho automatico | Auditoria de eventos |

---

## 10. Riscos e dependencias

### 10.1 Riscos

| Risco | Probabilidade | Impacto | Mitigacao |
|-------|---------------|---------|-----------|
| Frota insuficiente para cobertura total | Media | Alto | Alertar operador sobre areas descobertas, priorizar zonas criticas |
| Falha do fleet manager centralizado | Baixa | Critico | Watchdog com restart automatico + drones continuam missao atual |
| Colisao entre drones em area compartilhada | Baixa | Alto | Zonas de exclusao mutua + desvio de obstaculos |
| Estacao de recarga com defeito | Media | Alto | Monitoramento de carga + alerta de falha + recarga manual como backup |
| Coordenacao falha durante incidente critico | Baixa | Critico | Drone opera autonomamente se fleet manager indisponivel |
| Latencia de comunicacao atrasa despacho | Media | Medio | Pré-posicionamento de drones em zonas criticas |

### 10.2 Dependencias

| Dependencia | Tipo | PRD relacionado |
|-------------|------|-----------------|
| Drones autonomos operacionais | Base | PRD_AUTONOMOUS_DRONES |
| Rede de comunicacao redundante | Infraestrutura | PRD_DRONE_COMMUNICATION |
| IA e visao computacional | Funcional | PRD_DRONE_AI_VISION |
| Sistema de alarme (Alarmo) | Integracao | PRD_SENSORS_AND_ALARMS_PLATFORM |
| NVR e Frigate | Integracao | PRD_VIDEO_SURVEILLANCE_AND_NVR |
| Dashboard de monitoramento | Interface | PRD_MONITORING_DASHBOARD |
| Hub de processamento local | Infraestrutura | PRD_LOCAL_PROCESSING_HUB |

---

## 11. Referencias

### Documentos do projeto

- `docs/ARQUITETURA_DRONES_AUTONOMOS.md` -- Secoes 4 e 9 (Software e Roadmap)
- `docs/ARQUITETURA_HARDWARE_UGV.md` -- Especificacoes do drone terrestre
- `docs/ARQUITETURA_HARDWARE_UAV.md` -- Especificacoes do drone aereo
- `rules/RULES_COMPLIANCE_AND_STANDARDS.md` -- REGRA-DRONE-18, 19, 20, 22
- `prd/PRD_AUTONOMOUS_DRONES.md` -- Secao 4.8 (Coordenacao de frota)

### Externos

- [ROS2 Multi-Robot Systems](https://docs.ros.org/)
- [Nav2 Fleet Management](https://nav2.org/)
- [MQTT v5 Specification](https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html)
- [Home Assistant Custom Cards](https://www.home-assistant.io/dashboards/)
- [Open-RMF (Open Robotics Middleware Framework)](https://www.open-rmf.org/)

---

> **Status**: Rascunho v1.0
>
> **Proxima revisao**: Apos MVP do primeiro UGV e testes de coordenacao com 2 drones
