# PRD – Dashboard de Monitoramento

> Sistema de Home Security – Open Source / Open Hardware
>
> Versão: 1.0 | Data: 2026-02-12 | Responsável: Agente_Documentador

---

## 1. Visão geral

- **Nome do produto/funcionalidade**: Dashboard de Monitoramento de Segurança
- **Responsável**: Agente_Arquiteto_Tecnico (especificação), Agente_Documentador (documentação)
- **Data**: 2026-02-12
- **PRDs relacionados**: PRD_SENSORS_AND_ALARMS_PLATFORM, PRD_VIDEO_SURVEILLANCE_AND_NVR

---

## 2. Problema e oportunidade

### 2.1 Problema

Sistemas de segurança residencial frequentemente possuem:
- **Interfaces fragmentadas**: Câmeras em um app, alarme em outro, automação em terceiro
- **Falta de visão unificada**: Dificuldade em visualizar status geral de segurança
- **Usabilidade complexa**: Interfaces técnicas não adequadas para usuários comuns
- **Histórico limitado**: Difícil acessar eventos passados e entender padrões

### 2.2 Oportunidade

Criar um dashboard unificado que:
- **Centralize** todas as informações de segurança em uma única interface
- **Simplifique** operações de armar/desarmar e visualização de câmeras
- **Apresente** histórico de eventos de forma clara e navegável
- **Funcione** em desktop, tablet e smartphone

---

## 3. Público-alvo

| Perfil | Necessidades específicas |
|--------|--------------------------|
| **Morador principal** | Visão rápida do status, armar/desarmar, visualizar câmeras |
| **Familiar/co-morador** | Interface simples, notificações relevantes |
| **Administrador** | Configuração avançada, logs, diagnóstico |
| **Visitante autorizado** | Acesso limitado (ex: câmera de entrada apenas) |

---

## 4. Requisitos funcionais

### 4.1 Visão geral de status

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-001 | Exibir status atual do alarme (armado/desarmado/disparado) | Alta |
| RF-002 | Exibir modo de armamento atual (total, parcial, perímetro) | Alta |
| RF-003 | Indicador visual de problemas (sensor offline, bateria baixa) | Alta |
| RF-004 | Contagem de eventos nas últimas 24 horas | Média |
| RF-005 | Status de conectividade das câmeras | Alta |
| RF-006 | Status do nobreak (bateria, tempo restante) | Média |
| RF-007 | Widget de "última atividade" com timestamp | Alta |

### 4.2 Controle do alarme

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-008 | Botões para armar em diferentes modos | Alta |
| RF-009 | Botão para desarmar (requer código ou autenticação) | Alta |
| RF-010 | Botão de pânico (discreto, com confirmação) | Alta |
| RF-011 | Exibir contagem regressiva de delay de saída | Alta |
| RF-012 | Permitir bypass de sensores individuais | Média |
| RF-013 | Feedback visual e sonoro das ações | Alta |

### 4.3 Visualização de câmeras

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-014 | Grid de visualização (2x2, 3x3, customizável) | Alta |
| RF-015 | Visualização individual com zoom digital | Média |
| RF-016 | Snapshot sob demanda | Média |
| RF-017 | Link rápido para timeline de cada câmera | Alta |
| RF-018 | Indicador de detecção ativa em cada câmera | Alta |
| RF-019 | Alternância entre streams (main/substream) | Baixa |

### 4.4 Mapa da residência

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-020 | Exibir planta baixa ou diagrama da residência | Média |
| RF-021 | Posicionar sensores no mapa com status visual | Média |
| RF-022 | Indicar zonas do alarme com cores | Média |
| RF-023 | Interagir com sensores/câmeras pelo mapa | Baixa |

### 4.5 Histórico de eventos

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-024 | Lista cronológica de eventos | Alta |
| RF-025 | Filtro por tipo de evento (alarme, detecção, acesso) | Alta |
| RF-026 | Filtro por câmera/sensor específico | Alta |
| RF-027 | Filtro por período (hoje, semana, mês, customizado) | Alta |
| RF-028 | Exibir thumbnail de eventos com detecção de IA | Alta |
| RF-029 | Link para gravação completa de cada evento | Alta |
| RF-030 | Exportar histórico para relatório (CSV/PDF) | Baixa |

### 4.6 Notificações e alertas

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-031 | Centro de notificações com histórico | Alta |
| RF-032 | Marcar notificações como lidas | Alta |
| RF-033 | Configurar preferências de notificação por usuário | Média |
| RF-034 | Silenciamento temporário de alertas não críticos | Média |

### 4.7 Configurações (painel admin)

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-035 | Gerenciar usuários e permissões | Alta |
| RF-036 | Configurar zonas do alarme | Alta |
| RF-037 | Configurar tempos de entrada/saída | Alta |
| RF-038 | Configurar sensores (nome, zona, tipo) | Alta |
| RF-039 | Configurar câmeras (nome, zonas de detecção) | Alta |
| RF-040 | Configurar automações de segurança | Média |
| RF-041 | Backup e restore de configurações | Média |
| RF-042 | Visualizar logs do sistema | Alta |

### 4.8 Acesso e autenticação

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-043 | Login com usuário e senha | Alta |
| RF-044 | Suporte a 2FA (TOTP) | Média |
| RF-045 | Múltiplos usuários com diferentes permissões | Alta |
| RF-046 | Logout automático por inatividade | Média |
| RF-047 | Acesso via VPN de fora da rede | Alta |

---

## 5. Requisitos não funcionais

### 5.1 Usabilidade

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-001 | Tempo para armar/desarmar | < 3 cliques/toques |
| RNF-002 | Tempo para visualizar câmera | < 2 cliques/toques |
| RNF-003 | Responsividade | Funcionar em telas de 320px a 4K |
| RNF-004 | Tema | Claro e escuro disponíveis |
| RNF-005 | Acessibilidade | Contraste adequado, labels em botões |

### 5.2 Performance

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-006 | Tempo de carregamento inicial | < 3 segundos em rede local |
| RNF-007 | Atualização de status | Tempo real (WebSocket) |
| RNF-008 | Latência de streaming | < 500ms em rede local |
| RNF-009 | Consumo de memória (browser) | < 500MB com 4 câmeras |

### 5.3 Segurança

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-010 | Conexão | HTTPS obrigatório |
| RNF-011 | Sessões | Token com expiração configurável |
| RNF-012 | Logs de acesso | Registrar todas as ações |
| RNF-013 | Bloqueio após tentativas | Bloquear após 5 tentativas de login |

### 5.4 Compatibilidade

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-014 | Navegadores desktop | Chrome, Firefox, Safari, Edge (últimas 2 versões) |
| RNF-015 | Dispositivos móveis | iOS 14+, Android 10+ |
| RNF-016 | App nativo | Home Assistant Companion (iOS/Android) |

---

## 6. Arquitetura técnica

### 6.1 Stack recomendado

| Componente | Tecnologia | Função |
|------------|------------|--------|
| **Frontend** | Home Assistant Lovelace | Interface principal |
| **Cards customizados** | alarmo-card, frigate-card | Visualização especializada |
| **Streaming** | WebRTC (Frigate) | Baixa latência para câmeras |
| **Backend** | Home Assistant Core | Lógica e API |
| **App mobile** | HA Companion | Acesso mobile nativo |

### 6.2 Estrutura de dashboards

```
┌─────────────────────────────────────────────────────────────────┐
│                     DASHBOARD PRINCIPAL                         │
├───────────────────────┬─────────────────────────────────────────┤
│                       │                                         │
│   STATUS DO ALARME    │         CÂMERAS (Grid 2x2)             │
│   ┌───────────────┐   │   ┌───────────┐  ┌───────────┐         │
│   │  ○ DESARMADO  │   │   │  Entrada  │  │  Fundos   │         │
│   │               │   │   │   [CAM]   │  │   [CAM]   │         │
│   │ [ARM] [NOITE] │   │   └───────────┘  └───────────┘         │
│   │ [FORA]        │   │   ┌───────────┐  ┌───────────┐         │
│   └───────────────┘   │   │  Lateral  │  │  Garagem  │         │
│                       │   │   [CAM]   │  │   [CAM]   │         │
│   PROBLEMAS (0)       │   └───────────┘  └───────────┘         │
│   ✓ Tudo OK           │                                         │
│                       │                                         │
├───────────────────────┼─────────────────────────────────────────┤
│                       │                                         │
│   SENSORES            │   ÚLTIMOS EVENTOS                       │
│   ○ Porta frente  OK  │   • 14:32 - Pessoa detectada (Entrada) │
│   ○ Porta fundos  OK  │   • 14:28 - Porta fundos aberta        │
│   ○ Janela sala   OK  │   • 13:15 - Sistema armado (modo total)│
│   ○ PIR corredor  OK  │   • 10:42 - Veículo detectado (Entrada)│
│   ○ Movimento ext OK  │   [Ver mais...]                         │
│                       │                                         │
└───────────────────────┴─────────────────────────────────────────┘
```

### 6.3 Views recomendadas

| View | Conteúdo | Acesso |
|------|----------|--------|
| **Principal** | Status geral, câmeras, sensores, eventos | Todos |
| **Câmeras** | Grid completo, visualização individual | Todos |
| **Histórico** | Timeline de eventos, filtros, busca | Todos |
| **Mapa** | Planta baixa com sensores | Todos |
| **Admin** | Configurações, logs, usuários | Admin apenas |

---

## 7. Wireframes

### 7.1 Dashboard principal (desktop)

```
┌────────────────────────────────────────────────────────────────────────┐
│  🏠 Home Security          [Notif. 🔔3]  [👤 Admin]  [☰ Menu]         │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  ┌─────────────────────┐  ┌─────────────────────────────────────────┐ │
│  │                     │  │                                         │ │
│  │   STATUS ALARME     │  │   CÂMERAS AO VIVO                       │ │
│  │   ─────────────     │  │                                         │ │
│  │                     │  │   ┌─────────────┐  ┌─────────────┐     │ │
│  │   ● DESARMADO       │  │   │   ENTRADA   │  │   FUNDOS    │     │ │
│  │                     │  │   │    📹       │  │    📹       │     │ │
│  │   ┌─────┐ ┌─────┐   │  │   │             │  │             │     │ │
│  │   │ ARM │ │NOITE│   │  │   └─────────────┘  └─────────────┘     │ │
│  │   │TOTAL│ │     │   │  │                                         │ │
│  │   └─────┘ └─────┘   │  │   ┌─────────────┐  ┌─────────────┐     │ │
│  │   ┌─────┐ ┌─────┐   │  │   │  LATERAL    │  │  GARAGEM    │     │ │
│  │   │FORA │ │PERI │   │  │   │    📹       │  │    📹       │     │ │
│  │   │     │ │METRO│   │  │   │             │  │             │     │ │
│  │   └─────┘ └─────┘   │  │   └─────────────┘  └─────────────┘     │ │
│  │                     │  │                                         │ │
│  │   ⚠️ Nenhum problema │  │   [Ver todas as câmeras]                │ │
│  │                     │  │                                         │ │
│  └─────────────────────┘  └─────────────────────────────────────────┘ │
│                                                                        │
│  ┌─────────────────────┐  ┌─────────────────────────────────────────┐ │
│  │                     │  │                                         │ │
│  │   SENSORES          │  │   ÚLTIMOS EVENTOS                       │ │
│  │   ─────────         │  │   ───────────────                       │ │
│  │                     │  │                                         │ │
│  │   ✓ Porta frente    │  │   14:32  👤 Pessoa detectada - Entrada  │ │
│  │   ✓ Porta fundos    │  │   14:28  🚪 Porta fundos aberta         │ │
│  │   ✓ Janela sala     │  │   13:15  🔐 Sistema armado (total)      │ │
│  │   ✓ PIR corredor    │  │   10:42  🚗 Veículo detectado - Entrada │ │
│  │   ✓ Movimento ext.  │  │                                         │ │
│  │                     │  │   [Ver histórico completo →]            │ │
│  │   [Ver todos]       │  │                                         │ │
│  │                     │  │                                         │ │
│  └─────────────────────┘  └─────────────────────────────────────────┘ │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

### 7.2 Dashboard mobile (simplificado)

```
┌────────────────────┐
│ 🏠 Home Security   │
│ [🔔] [☰]           │
├────────────────────┤
│                    │
│  ● DESARMADO       │
│                    │
│  ┌────┐  ┌────┐   │
│  │ARM │  │NOITE│  │
│  └────┘  └────┘   │
│  ┌────┐  ┌────┐   │
│  │FORA│  │PÂNICO│ │
│  └────┘  └────┘   │
│                    │
├────────────────────┤
│ 📹 Câmeras         │
│ ┌────────────────┐ │
│ │   [Entrada]    │ │
│ │      📹        │ │
│ └────────────────┘ │
│ [< >] 1 de 4      │
│                    │
├────────────────────┤
│ ⏱ Últimos eventos │
│ 14:32 👤 Pessoa   │
│ 14:28 🚪 Porta    │
│ [Ver mais...]     │
│                    │
└────────────────────┘
```

---

## 8. Cards Home Assistant recomendados

### 8.1 Cards essenciais

| Card | Função | Instalação |
|------|--------|------------|
| **alarmo-card** | Controle do alarme Alarmo | HACS |
| **frigate-card** | Visualização de câmeras Frigate | HACS |
| **button-card** | Botões customizados | HACS |
| **mushroom-cards** | Cards modernos e limpos | HACS |
| **mini-graph-card** | Gráficos de histórico | HACS |

### 8.2 Exemplo de configuração (YAML)

```yaml
# Dashboard Principal
title: Home Security
views:
  - title: Principal
    path: principal
    icon: mdi:shield-home
    cards:
      # Status do alarme
      - type: custom:alarmo-card
        entity: alarm_control_panel.alarmo

      # Grid de câmeras
      - type: custom:frigate-card
        cameras:
          - camera_entity: camera.entrada
          - camera_entity: camera.fundos
          - camera_entity: camera.lateral
          - camera_entity: camera.garagem
        view:
          default: live
          layout:
            fit: contain

      # Lista de sensores
      - type: entities
        title: Sensores
        entities:
          - entity: binary_sensor.porta_frente
          - entity: binary_sensor.porta_fundos
          - entity: binary_sensor.janela_sala
          - entity: binary_sensor.pir_corredor

      # Eventos recentes
      - type: logbook
        entities:
          - alarm_control_panel.alarmo
        hours_to_show: 24
```

---

## 9. Critérios de aceitação

| ID | Critério | Método de verificação |
|----|----------|----------------------|
| CA-001 | Dashboard carrega em < 3 segundos | Medição de tempo |
| CA-002 | Armar/desarmar funciona pelo dashboard | Teste funcional |
| CA-003 | Câmeras aparecem com streaming ativo | Verificação visual |
| CA-004 | Eventos são exibidos em tempo real | Teste gerando eventos |
| CA-005 | Acesso mobile funciona via app | Teste em smartphone |
| CA-006 | Filtros de histórico funcionam | Teste de filtros |
| CA-007 | Login requer autenticação | Teste de acesso |
| CA-008 | Acesso via VPN funciona | Teste externo |
| CA-009 | Interface responsiva em diferentes telas | Teste em múltiplos dispositivos |
| CA-010 | Notificações aparecem no centro de notificações | Verificação visual |

---

## 10. Métricas de sucesso

| Métrica | Alvo | Medição |
|---------|------|---------|
| **Tempo de carregamento** | < 3 segundos | Monitoramento |
| **Taxa de adoção** | 100% dos moradores usando | Pesquisa |
| **Satisfação** | > 4/5 em usabilidade | Feedback |
| **Erros de interface** | 0 críticos | Logs e feedback |

---

## 11. Riscos e dependências

### 11.1 Riscos

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Complexidade da configuração | Média | Médio | Fornecer configuração exemplo |
| Performance com muitas câmeras | Média | Médio | Otimizar streams, usar substream |
| Curva de aprendizado HA | Média | Baixo | Documentação e tutoriais |

### 11.2 Dependências

| Dependência | Tipo | PRD relacionado |
|-------------|------|-----------------|
| Sistema de alarme (Alarmo) | Funcional | PRD_SENSORS_AND_ALARMS_PLATFORM |
| NVR (Frigate) | Funcional | PRD_VIDEO_SURVEILLANCE_AND_NVR |
| Hardware central | Infraestrutura | PRD_LOCAL_PROCESSING_HUB |
| Rede VPN | Acesso remoto | PRD_NETWORK_SECURITY |

---

## 12. Referências

### Documentos do projeto
- `docs/ARQUITETURA_TECNICA.md` - Arquitetura geral

### Externos
- [Home Assistant Lovelace](https://www.home-assistant.io/lovelace/)
- [Alarmo Card](https://github.com/nielsfaber/alarmo-card)
- [Frigate Card](https://github.com/dermotduffy/frigate-hass-card)
- [HACS - Home Assistant Community Store](https://hacs.xyz/)

---

> **Status**: Rascunho v1.0
>
> **Próxima revisão**: Após validação pelo Agente_Arquiteto_Tecnico
