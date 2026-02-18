# PRD – Controle de Acesso Rural

> Sistema de Home Security – Open Source / Open Hardware
>
> Versão: 1.0 | Data: 2026-02-18 | Responsável: Agente_Documentador

---

## 1. Visão geral

- **Nome do produto/funcionalidade**: Sistema de Controle de Acesso para Propriedade Rural
- **Responsável**: Agente_Arquiteto_Seguranca_Fisica (requisitos), Agente_Documentador (documentação)
- **Data**: 2026-02-18
- **PRDs relacionados**: PRD_PERIMETER_RURAL, PRD_VIDEO_SURVEILLANCE_AND_NVR, PRD_SENSORS_AND_ALARMS_PLATFORM, PRD_AUTOMATION_AND_SCENES

---

## 2. Problema e oportunidade

### 2.1 Problema

Propriedades rurais enfrentam desafios significativos no controle de acesso:
- **Distância do portão à sede**: Percursos de 50m a 500m+ tornam o atendimento presencial inviável
- **Múltiplos pontos de entrada**: Portões de veículos, pedestres, porteiras de pasto
- **Identificação de visitantes**: Difícil distinguir visitantes legítimos de intrusos à distância
- **Controle de veículos**: Entrada e saída de veículos de fornecedores, funcionários e visitantes
- **Conectividade limitada**: Infraestrutura de comunicação precária entre portão e sede

### 2.2 Oportunidade

Implementar um sistema de controle de acesso que ofereça:
- **Interfone remoto** com vídeo para comunicação portão-sede via rede local ou Wi-Fi
- **Reconhecimento de placas (ALPR)** para autorização automática de veículos conhecidos
- **Automação de portões** com abertura remota via app ou automação
- **Auditoria completa** de entradas e saídas com registro visual
- **Integração com Home Assistant** para automações de segurança

---

## 3. Público-alvo

| Perfil | Características | Necessidades |
|--------|-----------------|--------------|
| **Fazendeiro** | Propriedade produtiva, fluxo diário de veículos | Automação de acesso para funcionários e fornecedores |
| **Sitiante** | Propriedade de lazer, visitantes esporádicos | Identificação visual remota, controle via app |
| **Chacareiro** | Propriedade menor, uso nos finais de semana | Monitoramento remoto quando ausente |
| **Caseiro/funcionário** | Reside na propriedade | Acesso simplificado, sem necessidade de app |

---

## 4. Requisitos funcionais

### 4.1 Controle de portão principal (veículos)

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-001 | Motor de portão automatizado | Deslizante ou pivotante, com central de comando | Alta |
| RF-002 | Sensor de abertura do portão | Magnético ou fim de curso, Zigbee ou 433MHz | Alta |
| RF-003 | Sensor anti-esmagamento | Fotocélula no trilho do portão | Alta |
| RF-004 | Abertura remota via Home Assistant | Botão no dashboard e app mobile | Alta |
| RF-005 | Abertura automática por placa reconhecida | Integração ALPR com Frigate | Média |
| RF-006 | Fechamento automático temporizado | Fechar após 60 segundos (configurável) | Alta |
| RF-007 | Abertura manual de emergência | Chave física ou trava mecânica | Alta |
| RF-008 | Sensor de veículo aguardando (loop indutivo ou PIR) | Detectar veículo no portão | Média |

### 4.2 Portão de pedestres

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-009 | Fechadura eletromagnética ou eletromecânica | 12V/24V, fail-safe ou fail-secure | Alta |
| RF-010 | Abertura por senha numérica | Teclado externo resistente a intempéries | Alta |
| RF-011 | Abertura remota via app | Integração com Home Assistant | Alta |
| RF-012 | Mola retorno automático | Portão fecha sozinho | Média |
| RF-013 | Sensor de abertura | Zigbee magnético | Alta |

### 4.3 Interfone/vídeo porteiro remoto

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-014 | Câmera com áudio bidirecional no portão | Resolução 1080p+, visão noturna | Alta |
| RF-015 | Visualização ao vivo pela sede e pelo app | Streaming via Home Assistant/Frigate | Alta |
| RF-016 | Notificação ao pressionar campainha | Push + snapshot no celular | Alta |
| RF-017 | Comunicação voz bidirecional | Via app Home Assistant Companion | Alta |
| RF-018 | Gravação automática ao detectar pessoa | Integração com Frigate | Alta |
| RF-019 | Funcionamento noturno | IR 10m+ ou iluminação auxiliar | Alta |

### 4.4 Reconhecimento de placas (ALPR)

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-020 | Câmera dedicada para captura de placas | Posição e ângulo otimizados | Média |
| RF-021 | Processamento ALPR local via Frigate/CodeProject.AI | Sem envio para nuvem | Média |
| RF-022 | Lista de placas autorizadas (whitelist) | Editável via Home Assistant | Média |
| RF-023 | Abertura automática para placas autorizadas | Automação no Home Assistant | Média |
| RF-024 | Registro fotográfico de todas as placas | Log com timestamp e imagem | Média |
| RF-025 | Alerta para placas desconhecidas | Notificação com snapshot | Média |

### 4.5 Porteiras secundárias (pasto/lavoura)

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-026 | Sensor de abertura em porteiras críticas | Zigbee com repetidor ou LoRa | Baixa |
| RF-027 | Alerta ao abrir porteira fora de horário | Automação no Home Assistant | Baixa |
| RF-028 | Trava elétrica em porteiras de acesso externo | 12V com chave | Baixa |

### 4.6 Integração e automações

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-029 | Log de todos os acessos no Home Assistant | Registro com timestamp, tipo, método | Alta |
| RF-030 | Integração com sistema de alarme (Alarmo) | Desarmar ao reconhecer morador | Média |
| RF-031 | Iluminação automática ao abrir portão à noite | Acender refletores da entrada | Média |
| RF-032 | Câmera segue veículo entrando (se PTZ) | Tracking automático | Baixa |

---

## 5. Requisitos não funcionais

### 5.1 Performance

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-001 | Tempo de abertura do portão após comando | < 3 segundos |
| RNF-002 | Tempo de notificação de campainha | < 5 segundos |
| RNF-003 | Tempo de reconhecimento de placa | < 5 segundos |
| RNF-004 | Latência do vídeo ao vivo no app | < 1 segundo |

### 5.2 Confiabilidade

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-005 | Operação em queda de energia | Nobreak no motor, abertura manual |
| RNF-006 | Operação em queda de internet | Controle local (teclado, chave) mantido |
| RNF-007 | Alcance do sinal Wi-Fi/rede até portão | Repetidor ou cabeamento PoE |
| RNF-008 | Resistência a intempéries | IP65+ para equipamentos externos |

### 5.3 Segurança

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-009 | Proteção anti-clone de controle remoto | Não usar 433MHz fixo, preferir rolling code |
| RNF-010 | Teclado com bloqueio após tentativas | Bloquear após 5 tentativas erradas |
| RNF-011 | Criptografia de comunicação | Zigbee AES-128, Wi-Fi WPA3 |
| RNF-012 | Log imutável de acessos | Registro em banco de dados do HA |

### 5.4 Conformidade

| ID | Requisito | Norma/Regra |
|----|-----------|-------------|
| RNF-013 | LGPD para reconhecimento de placas | REGRA-LGPD-01 a 05 |
| RNF-014 | Câmera de entrada | REGRA-CFTV-05 a 12 |
| RNF-015 | Portão automatizado | NR-12 segurança de máquinas |

---

## 6. Arquitetura técnica

### 6.1 Diagrama de componentes

```
                        ESTRADA VICINAL
                              │
                    ┌─────────┴─────────┐
                    │     PORTÃO        │
                    │   PRINCIPAL       │
                    │                   │
                    │ ┌───────────────┐ │
                    │ │ Motor Portão  │ │
                    │ │ (Deslizante)  │ │
                    │ └───────┬───────┘ │
                    │         │         │
                    │ ┌───────┴───────┐ │
                    │ │ Central Portão│ │
                    │ │ + Relé Zigbee │ │
                    │ └───────────────┘ │
                    │                   │
                    │ ┌─────────┐ ┌────┐│
                    │ │Câmera   │ │Cam ││
                    │ │Interfone│ │ALPR││
                    │ │(PoE)    │ │(PoE)│
                    │ └─────────┘ └────┘│
                    │                   │
                    │ ┌─────────┐       │
                    │ │Teclado  │       │
                    │ │Externo  │       │
                    │ └─────────┘       │
                    └─────────┬─────────┘
                              │
                    Cabo PoE / Wi-Fi
                              │
                    ┌─────────▼─────────┐
                    │   SWITCH PoE      │
                    │   (no meio ou     │
                    │    na sede)       │
                    └─────────┬─────────┘
                              │
                    ┌─────────▼─────────┐
                    │   MINI PC N100    │
                    │ ┌───────────────┐ │
                    │ │ Home Assistant│ │
                    │ │ + Frigate     │ │
                    │ │ + ALPR        │ │
                    │ │ + Zigbee2MQTT │ │
                    │ └───────────────┘ │
                    └───────────────────┘
```

### 6.2 Fluxo de acesso com interfone

```
1. Visitante chega ao portão
           │
           ▼
2. Câmera detecta pessoa (Frigate)
           │
           ├──► Notificação push com snapshot
           │
           ▼
3. Visitante pressiona campainha
           │
           ├──► Notificação com áudio/vídeo
           │
           ▼
4. Morador visualiza no app
           │
           ├── Aceita → Abre portão remotamente
           │             (HA → Relé Zigbee → Motor)
           │
           └── Recusa → Ignora ou comunica via áudio
```

### 6.3 Fluxo de acesso com ALPR

```
1. Veículo se aproxima do portão
           │
           ▼
2. Câmera ALPR captura placa
           │
           ▼
3. Frigate/CodeProject.AI processa
           │
           ├── Placa na whitelist
           │       │
           │       ▼
           │   Abre portão automaticamente
           │   + Registra acesso
           │   + Acende iluminação (noite)
           │
           └── Placa desconhecida
                   │
                   ▼
               Notifica morador com snapshot
               + Aguarda decisão manual
```

---

## 7. Produtos/componentes recomendados

### 7.1 Motor e automação de portão

| Componente | Modelo sugerido | Preço estimado | Observações |
|------------|-----------------|----------------|-------------|
| Motor portão deslizante | PPA DZ Rio 400 | R$ 600-900 | Até 400kg, uso residencial |
| Motor portão deslizante | Garen Kdz Fit | R$ 500-700 | Até 350kg, custo-benefício |
| Motor portão pivotante | PPA Piston Jet Flex | R$ 800-1.200 | Para portões de folha |
| Fotocélula anti-esmagamento | PPA F30 | R$ 50-80 | Par transmissor/receptor |
| Controle remoto rolling code | PPA TOK | R$ 40-60 | Frequência 433MHz com rolling code |

### 7.2 Interfone/vídeo porteiro IP

| Componente | Modelo sugerido | Preço estimado | Observações |
|------------|-----------------|----------------|-------------|
| Vídeo porteiro IP PoE | Hikvision DS-KV6113-WPE1 | R$ 800-1.200 | ONVIF, SIP, 2MP, IP65 |
| Alternativa Wi-Fi | Aqara G4 Video Doorbell | R$ 500-700 | Integração HomeKit/HA |
| Alternativa acessível | Intelbras IV 7010 HF HD | R$ 400-600 | Tela + câmera, Wi-Fi |

### 7.3 Câmera para ALPR

| Componente | Modelo sugerido | Preço estimado | Observações |
|------------|-----------------|----------------|-------------|
| Câmera dedicada ALPR | Hikvision DS-2CD2043G2-IU | R$ 500-700 | 4MP, posicionar a 3-5m do portão |
| Alternativa | Reolink RLC-810A | R$ 400-500 | 4K, bom para ALPR com ajustes |

### 7.4 Integração e automação

| Componente | Modelo sugerido | Preço estimado | Observações |
|------------|-----------------|----------------|-------------|
| Relé Zigbee para portão | Sonoff ZBMINI-L2 | R$ 60-90 | Dry contact, integra com central |
| Teclado externo | Hikvision DS-K1T502DBFWX | R$ 400-600 | Senha + biometria, IP65 |
| Alternativa teclado | Teclado Zigbee Tuya | R$ 150-250 | Senha, cartão RFID |
| Sensor abertura portão | Sonoff SNZB-04 | R$ 40-60 | Magnético, Zigbee |
| Fechadura eletromagnética | Intelbras FE 20150 | R$ 150-250 | Para portão de pedestres |

### 7.5 Software ALPR

| Componente | Tecnologia | Preço | Observações |
|------------|------------|-------|-------------|
| CodeProject.AI + ALPR | Open source | Gratuito | Integra com Frigate via MQTT |
| Plate Recognizer (local) | SDK local | Gratuito (2500 leituras/mês) | API local, sem nuvem |
| OpenALPR | Open source | Gratuito | Requer configuração manual |

---

## 8. Estimativa de investimento

### 8.1 Configuração básica (interfone + portão automatizado)

| Componente | Quantidade | Preço unitário | Subtotal |
|------------|------------|----------------|----------|
| Motor de portão deslizante | 1 | R$ 700 | R$ 700 |
| Fotocélula | 1 par | R$ 60 | R$ 60 |
| Relé Zigbee (controle do motor) | 1 | R$ 80 | R$ 80 |
| Vídeo porteiro IP (Intelbras) | 1 | R$ 500 | R$ 500 |
| Sensor abertura portão | 1 | R$ 50 | R$ 50 |
| Fechadura eletromagnética (pedestres) | 1 | R$ 200 | R$ 200 |
| Cabeamento/infraestrutura | - | R$ 300 | R$ 300 |
| **Total básico** | | | **R$ 1.890** |

### 8.2 Configuração recomendada (+ ALPR)

| Componente | Quantidade | Preço unitário | Subtotal |
|------------|------------|----------------|----------|
| Configuração básica | - | - | R$ 1.890 |
| Câmera dedicada ALPR (Reolink) | 1 | R$ 450 | R$ 450 |
| Teclado externo com senha | 1 | R$ 200 | R$ 200 |
| **Total recomendado** | | | **R$ 2.540** |

### 8.3 Configuração completa (+ vídeo porteiro premium)

| Componente | Quantidade | Preço unitário | Subtotal |
|------------|------------|----------------|----------|
| Configuração recomendada | - | - | R$ 2.540 |
| Vídeo porteiro IP Hikvision (upgrade) | 1 | R$ 1.000 | R$ 500 (diferença) |
| Teclado biométrico IP65 | 1 | R$ 500 | R$ 300 (diferença) |
| Iluminação LED portão (Zigbee) | 2 | R$ 100 | R$ 200 |
| **Total completo** | | | **R$ 3.540** |

---

## 9. Critérios de aceitação

| ID | Critério | Método de verificação |
|----|----------|----------------------|
| CA-001 | Portão abre e fecha via app Home Assistant | Teste funcional |
| CA-002 | Interfone transmite vídeo e áudio bidirecional | Teste de comunicação |
| CA-003 | Notificação com snapshot chega ao pressionar campainha | Teste com cronômetro |
| CA-004 | Portão fecha automaticamente após tempo configurado | Teste temporizado |
| CA-005 | ALPR reconhece placas da whitelist corretamente | Teste com veículos cadastrados |
| CA-006 | ALPR abre portão automaticamente para placa autorizada | Teste funcional end-to-end |
| CA-007 | Teclado bloqueia após 5 tentativas erradas | Teste de segurança |
| CA-008 | Sistema opera em queda de energia (abertura manual) | Teste de interrupção |
| CA-009 | Log registra todos os acessos com timestamp e método | Verificação de registros |
| CA-010 | Iluminação acende automaticamente à noite ao abrir portão | Teste noturno |

---

## 10. Métricas de sucesso

| Métrica | Alvo | Medição |
|---------|------|---------|
| **Taxa de reconhecimento ALPR** | > 90% em condições normais | Testes periódicos |
| **Tempo de resposta do portão** | < 3 segundos do comando à abertura | Cronômetro |
| **Falsos positivos ALPR** | < 1/semana | Contagem de aberturas indevidas |
| **Disponibilidade do interfone** | > 99% | Monitoramento de uptime |
| **Satisfação dos moradores** | > 4/5 | Feedback |

---

## 11. Riscos e dependências

### 11.1 Riscos

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Wi-Fi insuficiente até o portão | Alta | Alto | Cabeamento PoE ou repetidor dedicado |
| ALPR falha com placas sujas/danificadas | Média | Médio | Manter interfone como fallback |
| Motor do portão trava mecanicamente | Baixa | Alto | Manutenção preventiva, abertura manual |
| Queda de energia impede abertura | Média | Alto | Nobreak no motor ou bateria interna |
| Vandalismo no interfone/câmera | Baixa | Alto | Instalação em altura, caixa reforçada |

### 11.2 Dependências

| Dependência | Tipo | PRD relacionado |
|-------------|------|-----------------|
| Hardware central (Mini PC N100) | Infraestrutura | PRD_LOCAL_PROCESSING_HUB |
| NVR Frigate (para ALPR e gravação) | Funcional | PRD_VIDEO_SURVEILLANCE_AND_NVR |
| Rede até o portão (PoE ou Wi-Fi) | Infraestrutura | PRD_NETWORK_SECURITY |
| Sistema de alarme | Integração | PRD_SENSORS_AND_ALARMS_PLATFORM |
| Notificações | Funcional | PRD_NOTIFICATIONS_AND_ALERTS |

---

## 12. Referências

### Documentos do projeto
- `docs/ARQUITETURA_TECNICA.md` - Seções 1.1, 5, 6
- `docs/ARQUITETURA_SEGURANCA_FISICA.md` - Diagramas de posicionamento rural
- `prd/PRD_PERIMETER_RURAL.md` - Contexto de perímetro rural
- `rules/RULES_COMPLIANCE_AND_STANDARDS.md` - REGRA-CFTV-*, REGRA-LGPD-*

### Externos
- [Frigate - Documentação ALPR](https://docs.frigate.video/)
- [CodeProject.AI - ALPR Module](https://www.codeproject.com/AI/docs/)
- [Home Assistant - Cover Integration](https://www.home-assistant.io/integrations/cover/)
- NR-12 - Segurança no Trabalho em Máquinas e Equipamentos

---

> **Status**: Rascunho v1.0
>
> **Próxima revisão**: Após validação pelo Agente_Arquiteto_Seguranca_Fisica
