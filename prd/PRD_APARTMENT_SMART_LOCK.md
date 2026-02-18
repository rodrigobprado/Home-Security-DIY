# PRD – Fechadura Inteligente para Apartamento

> Sistema de Home Security – Open Source / Open Hardware
>
> Versão: 1.0 | Data: 2026-02-18 | Responsável: Agente_Documentador

---

## 1. Visão geral

- **Nome do produto/funcionalidade**: Sistema de Fechadura Inteligente para Apartamento
- **Responsável**: Agente_Arquiteto_Seguranca_Fisica (requisitos), Agente_Documentador (documentação)
- **Data**: 2026-02-18
- **PRDs relacionados**: PRD_APARTMENT_SECURITY, PRD_SENSORS_AND_ALARMS_PLATFORM, PRD_AUTOMATION_AND_SCENES, PRD_HOUSE_ENVELOPE

---

## 2. Problema e oportunidade

### 2.1 Problema

A porta de entrada do apartamento é o ponto mais vulnerável e, frequentemente, o unico ponto de acesso:
- **Chaves tradicionais**: Podem ser copiadas, perdidas ou esquecidas
- **Fechaduras simples**: Um ponto de travamento oferece pouca resistencia
- **Sem auditoria**: Impossivel saber quem entrou ou quando
- **Acesso para terceiros**: Dificultar entrega de chaves para prestadores, diaristas, visitantes
- **Falta de integração**: Fechadura desconectada do sistema de segurança

### 2.2 Oportunidade

Implementar uma fechadura inteligente que ofereça:
- **Multiplos metodos de acesso**: Biometria, senha, app, NFC e chave fisica
- **Auditoria completa**: Log de todos os acessos com timestamp e metodo
- **Codigos temporarios**: Para visitantes e prestadores de serviço
- **Integração com Home Assistant**: Automações de armar/desarmar alarme
- **Processamento local**: Sem dependencia de nuvem para funcionamento

---

## 3. Público-alvo

| Perfil | Características | Necessidades |
|--------|-----------------|--------------|
| **Morador individual** | Praticidade, sem chaves | Biometria rapida, app como backup |
| **Casal** | Dois usuarios principais | Multiplas digitais, codigos individuais |
| **Familia com filhos** | Controle de acesso de menores | Saber quando filhos chegam/saem |
| **Idoso** | Facilidade de uso | Biometria ou senha simples, sem app |
| **Quem recebe prestadores** | Diarista, entregadores | Codigos temporarios com validade |

---

## 4. Requisitos funcionais

### 4.1 Metodos de acesso

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-001 | Acesso por biometria (impressão digital) | Sensor capacitivo, < 1s para leitura | Alta |
| RF-002 | Acesso por senha numérica | Teclado touch, 4-8 digitos | Alta |
| RF-003 | Acesso por app mobile | Bluetooth e/ou Wi-Fi local | Alta |
| RF-004 | Acesso por chave fisica | Cilindro mecanico de emergencia | Alta |
| RF-005 | Acesso por NFC/RFID | Tag ou cartão, como método auxiliar | Média |
| RF-006 | Acesso por Home Assistant | Comando via dashboard ou automação | Média |
| RF-007 | Capacidade minima de digitais | 100 impressões digitais | Alta |
| RF-008 | Capacidade minima de senhas | 50 codigos diferentes | Alta |

### 4.2 Segurança da fechadura

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-009 | Travamento multiponto | Minimo 3 pontos (superior, central, inferior) | Alta |
| RF-010 | Anti-peeping para senha | Digitos aleatorios antes/depois da senha real | Alta |
| RF-011 | Bloqueio apos tentativas falhas | Bloquear 5 minutos apos 5 tentativas erradas | Alta |
| RF-012 | Alerta de tentativa de arrombamento | Sensor anti-tamper, notificação imediata | Alta |
| RF-013 | Codigo de coação | Abre normalmente mas envia alerta silencioso | Média |
| RF-014 | Alarme sonoro de violação | Sirene interna 85-90dB ativada por tamper | Alta |
| RF-015 | Detecção de porta não trancada | Sensor de lingueta/trava | Média |

### 4.3 Gestão de usuarios e codigos

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-016 | Cadastro de usuarios permanentes | Moradores com multiplos metodos de acesso | Alta |
| RF-017 | Codigos temporarios com validade | Data/hora inicio e fim | Alta |
| RF-018 | Codigos de uso unico | Para entregas ou prestadores pontuais | Média |
| RF-019 | Codigos recorrentes | Ex: diarista toda terça, 8h-12h | Média |
| RF-020 | Revogação imediata de acesso | Remover usuario/codigo instantaneamente | Alta |
| RF-021 | Perfis de usuario | Admin, morador, convidado, temporario | Alta |

### 4.4 Auditoria e logs

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-022 | Registro de todo acesso | Timestamp, usuario, metodo utilizado | Alta |
| RF-023 | Registro de tentativas falhas | Timestamp, metodo, motivo da falha | Alta |
| RF-024 | Historico acessivel via Home Assistant | Logbook integrado | Alta |
| RF-025 | Notificação de acesso configurable | Push quando alguem entra | Média |
| RF-026 | Exportação de logs | CSV ou consulta via API | Baixa |

### 4.5 Integração com automação

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-027 | Desarmar alarme ao destravar (usuario autorizado) | Automação no Home Assistant | Alta |
| RF-028 | Armar alarme ao travar de fora | Automação no Home Assistant | Alta |
| RF-029 | Acender luzes ao entrar (noite) | Cena "chegando em casa" | Média |
| RF-030 | Travamento automatico | Após 30 segundos se porta fechada | Alta |
| RF-031 | Alerta se porta aberta sem travar por 5+ minutos | Automação de segurança | Média |
| RF-032 | Integração com olho magico digital | Visualizar visitante antes de abrir | Baixa |

### 4.6 Alimentação e bateria

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-033 | Alimentação por pilhas/bateria | 4x AA ou bateria recarregavel | Alta |
| RF-034 | Autonomia minima | 6 meses com uso tipico (10 acessos/dia) | Alta |
| RF-035 | Alerta de bateria baixa | Notificação quando < 20% | Alta |
| RF-036 | Alimentação emergencial | Porta USB-C ou conector externo 9V | Alta |
| RF-037 | Funcionamento offline | Todos os metodos locais funcionam sem rede | Alta |

---

## 5. Requisitos não funcionais

### 5.1 Usabilidade

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-001 | Tempo de desbloqueio por biometria | < 1,5 segundos |
| RNF-002 | Tempo de desbloqueio por senha | < 3 segundos |
| RNF-003 | Feedback visual/sonoro | LED e bip de confirmação |
| RNF-004 | Operação silenciosa | Motor < 50dB ao travar/destravar |

### 5.2 Segurança

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-005 | Comunicação criptografada | AES-128 (Zigbee) ou AES-256 (Wi-Fi) |
| RNF-006 | Armazenamento de biometria | Apenas local no dispositivo, não em nuvem |
| RNF-007 | Anti-fingerprint no teclado | Teclado nao revela digitos mais usados |
| RNF-008 | Resistencia ao arrombamento | Mola e lingueta em aço inox |

### 5.3 Instalação

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-009 | Compatibilidade com portas brasileiras | Encaixe para portas com preparação europeia |
| RNF-010 | Instalação sem modificação estrutural | Substituir fechadura existente |
| RNF-011 | Reversibilidade | Possivel retornar fechadura original |
| RNF-012 | Espessura da porta | Compativel com portas de 35mm a 60mm |

### 5.4 Conectividade

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-013 | Protocolo preferencial | Zigbee 3.0 (baixo consumo, local) |
| RNF-014 | Protocolo alternativo | Wi-Fi (mais facil configuração) |
| RNF-015 | Funcionamento sem conectividade | 100% funcional offline (biometria, senha, chave) |
| RNF-016 | Alcance Zigbee | Minimo 10m ate coordenador (direto ou via mesh) |

### 5.5 Conformidade

| ID | Requisito | Norma/Regra |
|----|-----------|-------------|
| RNF-017 | Regulamento do condominio | Verificar restricoes de modificação |
| RNF-018 | Norma de fechaduras | NBR 14913 |
| RNF-019 | LGPD para biometria | Dados biometricos armazenados apenas localmente |

---

## 6. Arquitetura técnica

### 6.1 Diagrama da fechadura inteligente

```
                    CORREDOR DO PRÉDIO
                          │
            ┌─────────────┴─────────────┐
            │      PORTA DO APTO        │
            │                           │
    EXTERNO │                           │ INTERNO
            │  ┌───────────────────┐    │
            │  │  PAINEL EXTERNO   │    │  ┌───────────────────┐
            │  │                   │    │  │  PAINEL INTERNO   │
            │  │  ┌─────────────┐  │    │  │                   │
            │  │  │ Teclado     │  │    │  │  ┌─────────────┐  │
            │  │  │ Touch       │  │    │  │  │ Botão       │  │
            │  │  └─────────────┘  │    │  │  │ Abertura    │  │
            │  │  ┌─────────────┐  │    │  │  └─────────────┘  │
            │  │  │ Leitor      │  │    │  │  ┌─────────────┐  │
            │  │  │ Biométrico  │  │    │  │  │ Trava       │  │
            │  │  └─────────────┘  │    │  │  │ Manual      │  │
            │  │  ┌─────────────┐  │    │  │  └─────────────┘  │
            │  │  │ Leitor NFC  │  │    │  │                   │
            │  │  └─────────────┘  │    │  │  [Pilhas 4xAA]   │
            │  │  ┌─────────────┐  │    │  │                   │
            │  │  │ Cilindro    │  │    │  │  ┌─────────────┐  │
            │  │  │ Mecânico    │  │    │  │  │ Módulo      │  │
            │  │  │ (emergência)│  │    │  │  │ Zigbee/WiFi │  │
            │  │  └─────────────┘  │    │  │  └──────┬──────┘  │
            │  └───────────────────┘    │  └─────────│─────────┘
            │                           │            │
            └───────────────────────────┘            │
                                              Zigbee Mesh
                                                     │
                                              ┌──────▼──────┐
                                              │ Coordenador │
                                              │ Zigbee      │
                                              │ (USB Dongle)│
                                              └──────┬──────┘
                                                     │
                                              ┌──────▼──────┐
                                              │    HOME     │
                                              │  ASSISTANT  │
                                              │  + Alarmo   │
                                              └─────────────┘
```

### 6.2 Fluxo de acesso e automação

```
1. Morador se aproxima da porta
           │
           ▼
2. Utiliza metodo de acesso:
   ├── Biometria → Sensor lê digital
   ├── Senha → Digita código no teclado
   ├── App → Envia comando via Zigbee/BLE
   ├── NFC → Aproxima tag/cartão
   └── Chave → Gira cilindro mecânico
           │
           ▼
3. Fechadura valida localmente
   ├── Válido → Destrava + feedback sonoro/LED
   └── Inválido → Bip de erro + registra tentativa
           │ (se válido)
           ▼
4. Evento publicado via Zigbee/MQTT
           │
           ▼
5. Home Assistant processa:
   ├── Identifica usuário
   ├── Registra log de acesso
   ├── Desarma alarme (Alarmo)
   ├── Acende luzes (se noite)
   └── Executa cena "chegando em casa"
```

### 6.3 Fluxo de código temporário

```
1. Admin cria código via Home Assistant
   ├── Define: código numérico
   ├── Define: validade (data/hora inicio e fim)
   ├── Define: tipo (único, recorrente)
   └── Opcionalmente: nome do visitante
           │
           ▼
2. Código sincronizado com fechadura
   (via Zigbee/Wi-Fi)
           │
           ▼
3. Visitante usa código
           │
           ▼
4. Sistema registra:
   ├── Acesso permitido com código temporário
   ├── Notifica morador
   └── Se código único → invalida após uso
```

---

## 7. Produtos/componentes recomendados

### 7.1 Fechaduras inteligentes com integração

| Modelo | Protocolo | Métodos de acesso | Preço estimado | Compatibilidade HA |
|--------|-----------|-------------------|----------------|---------------------|
| **Yale YDM 4109 RL** | Zigbee (módulo) | Digital, senha, app, chave | R$ 800-1.200 | Via Z2M (módulo Zigbee Yale) |
| **Samsung SHP-DP609** | Wi-Fi/BLE | Digital, senha, app, cartão, chave | R$ 1.500-2.200 | Via integração SmartThings |
| **Papaiz Smart Lock** | Wi-Fi | Senha, app, chave | R$ 600-900 | Via integração HA |
| **Intelbras FR 220** | Wi-Fi | Digital, senha, cartão, chave | R$ 700-1.000 | Via integração ou API |
| **Yale Linus L2** | Wi-Fi/BLE/Matter | App, NFC, chave (adaptador) | R$ 1.200-1.800 | Nativo (Matter) |
| **Tedee Pro** | BLE/Wi-Fi (bridge) | App, chave (adaptador) | R$ 1.000-1.500 | Via integração HA |

### 7.2 Módulos de conectividade

| Componente | Função | Preço estimado | Observações |
|------------|--------|----------------|-------------|
| Yale Connect Wi-Fi Bridge | Conecta Yale ao Wi-Fi/HA | R$ 200-350 | Para modelos Yale sem Wi-Fi |
| Módulo Zigbee Yale | Adiciona Zigbee à fechadura | R$ 150-250 | Compatível com Z2M |
| Tedee Wi-Fi Bridge | Conecta Tedee ao Wi-Fi/HA | R$ 200-300 | Necessário para HA |

### 7.3 Acessórios complementares

| Componente | Função | Preço estimado | Observações |
|------------|--------|----------------|-------------|
| NFC Tag adesivo | Acesso por aproximação | R$ 5-15 (cada) | Programável via HA |
| Sensor abertura Zigbee | Detectar porta aberta/fechada | R$ 40-60 | Sonoff SNZB-04 |
| Bateria recarregável AA | Substituir pilhas descartáveis | R$ 60-100 (kit 4) | Eneloop ou similar |

---

## 8. Estimativas por configuração

### 8.1 Configuração econômica

| Componente | Preço estimado |
|------------|----------------|
| Fechadura Papaiz Smart Lock (Wi-Fi) | R$ 700 |
| Sensor abertura porta (Sonoff SNZB-04) | R$ 50 |
| NFC Tags (3 unidades) | R$ 30 |
| **Total econômico** | **R$ 780** |

### 8.2 Configuração recomendada

| Componente | Preço estimado |
|------------|----------------|
| Fechadura Yale YDM 4109 RL | R$ 1.000 |
| Módulo Zigbee Yale | R$ 200 |
| Sensor abertura porta (Aqara) | R$ 60 |
| NFC Tags (5 unidades) | R$ 50 |
| Pilhas recarregáveis | R$ 80 |
| **Total recomendado** | **R$ 1.390** |

### 8.3 Configuração premium

| Componente | Preço estimado |
|------------|----------------|
| Fechadura Samsung SHP-DP609 | R$ 1.800 |
| Sensor abertura porta (Aqara) | R$ 60 |
| NFC Tags (5 unidades) | R$ 50 |
| Olho mágico digital (Aqara G4) | R$ 600 |
| **Total premium** | **R$ 2.510** |

---

## 9. Critérios de aceitação

| ID | Critério | Método de verificação |
|----|----------|----------------------|
| CA-001 | Biometria desbloqueia em < 1,5 segundos | Teste com cronômetro |
| CA-002 | Senha desbloqueia corretamente | Teste funcional |
| CA-003 | App desbloqueia remotamente | Teste via Home Assistant |
| CA-004 | Chave física funciona como backup | Teste mecânico |
| CA-005 | Código temporário funciona apenas no período configurado | Teste com expiração |
| CA-006 | Bloqueio após 5 tentativas falhas | Teste de segurança |
| CA-007 | Log registra todos os acessos com timestamp | Verificação de logs |
| CA-008 | Alarme desarma ao destravar (automação) | Teste de integração |
| CA-009 | Alarme arma ao travar saindo (automação) | Teste de integração |
| CA-010 | Bateria dura > 6 meses em uso normal | Monitoramento ao longo do tempo |
| CA-011 | Código de coação envia alerta silencioso | Teste funcional |
| CA-012 | Funcionamento mantido offline (sem rede) | Teste desconectando rede |

---

## 10. Métricas de sucesso

| Métrica | Alvo | Medição |
|---------|------|---------|
| **Tempo médio de desbloqueio** | < 2 segundos | Monitoramento de logs |
| **Taxa de reconhecimento biométrico** | > 98% | Testes periódicos |
| **Duração da bateria** | > 6 meses | Registro de trocas |
| **Adoção pelos moradores** | 100% usando método digital | Pesquisa |
| **Satisfação** | > 4/5 | Feedback |
| **Falhas de desbloqueio** | < 2% | Monitoramento de logs |

---

## 11. Riscos e dependências

### 11.1 Riscos

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Bateria acaba sem aviso | Baixa | Alto | Alerta a 20%, porta USB-C emergencial |
| Biometria não reconhece (dedo molhado/sujo) | Média | Baixo | Multiplos métodos de acesso alternativos |
| Fechadura perde comunicação Zigbee/Wi-Fi | Baixa | Baixo | Funciona 100% offline localmente |
| Incompatibilidade com porta existente | Média | Alto | Verificar medidas antes da compra |
| Condomínio não permite troca de fechadura | Baixa | Alto | Verificar regulamento antecipadamente |
| Vulnerabilidade de firmware | Baixa | Alto | Atualizar firmware, usar protocolo local |

### 11.2 Dependências

| Dependência | Tipo | PRD relacionado |
|-------------|------|-----------------|
| Coordenador Zigbee (se Zigbee) | Infraestrutura | PRD_LOCAL_PROCESSING_HUB |
| Home Assistant | Plataforma | PRD_LOCAL_PROCESSING_HUB |
| Sistema de alarme (Alarmo) | Integração | PRD_SENSORS_AND_ALARMS_PLATFORM |
| Sistema de notificações | Funcional | PRD_NOTIFICATIONS_AND_ALERTS |
| Automações e cenas | Funcional | PRD_AUTOMATION_AND_SCENES |

---

## 12. Referências

### Documentos do projeto
- `prd/PRD_APARTMENT_SECURITY.md` - Contexto de segurança de apartamento
- `prd/PRD_HOUSE_ENVELOPE.md` - Proteção de portas e janelas
- `docs/ARQUITETURA_TECNICA.md` - Seções 1.3, 3
- `rules/RULES_COMPLIANCE_AND_STANDARDS.md`

### Externos
- NBR 14913 - Fechaduras de segurança
- [Zigbee2MQTT - Smart Locks](https://www.zigbee2mqtt.io/supported-devices/#s=lock)
- [Home Assistant - Lock Integration](https://www.home-assistant.io/integrations/lock/)
- [Yale Brasil](https://www.yalebrasil.com.br/)

---

> **Status**: Rascunho v1.0
>
> **Próxima revisão**: Após validação pelo Agente_Arquiteto_Seguranca_Fisica
