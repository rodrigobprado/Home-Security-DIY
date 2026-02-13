# Arquitetura de Drones Autônomos Modulares

> Sistema de Home Security – Open Source / Open Hardware
>
> Módulo Reativo Avançado
>
> Versão: 1.0 | Data: 2026-02-12

---

## 1. Visão Geral

### 1.1 Objetivo

Desenvolver um ecossistema open source/open hardware de **drones autônomos modulares** com IA embarcada, comunicação redundante e capacidade de operação independente para vigilância, segurança, inspeção e monitoramento ambiental.

### 1.2 Princípios do projeto

| Princípio | Descrição |
|-----------|-----------|
| **Open Source** | Todo software sob licenças abertas (MIT, Apache 2.0, GPL) |
| **Open Hardware** | Especificações abertas, componentes genéricos, fabricação própria possível |
| **Modularidade** | Hardware e software em camadas independentes e intercambiáveis |
| **Autonomia** | Capacidade de operação sem intervenção humana constante |
| **Segurança** | Protocolos de autenticação, criptografia e auditoria |
| **Não letalidade** | Módulos de defesa priorizando dissuasão sem danos permanentes |
| **Privacidade** | Processamento local, conformidade com LGPD |

### 1.3 Categorias de drones

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     FROTA DE DRONES AUTÔNOMOS                           │
├─────────────────────┬─────────────────────┬─────────────────────────────┤
│    TERRESTRES       │      AÉREOS         │        AQUÁTICOS            │
│                     │                     │                             │
│  ┌─────────────┐    │  ┌─────────────┐    │  ┌─────────────┐           │
│  │   Rodas     │    │  │ Multirrotor │    │  │  Barco RC   │           │
│  │   (UGV)     │    │  │   (UAV)     │    │  │  (USV)      │           │
│  └─────────────┘    │  └─────────────┘    │  └─────────────┘           │
│                     │                     │                             │
│  ┌─────────────┐    │  ┌─────────────┐    │  ┌─────────────┐           │
│  │  Esteiras   │    │  │  Asa fixa   │    │  │  Anfíbio    │           │
│  │   (UGV)     │    │  │   (UAV)     │    │  │  (UGV+USV)  │           │
│  └─────────────┘    │  └─────────────┘    │  └─────────────┘           │
│                     │                     │                             │
│  Aplicação:         │  Aplicação:         │  Aplicação:                │
│  - Patrulha         │  - Vigilância       │  - Monitoramento           │
│  - Inspeção         │  - Resposta rápida  │  - Áreas alagadas          │
│  - Perímetro        │  - Mapeamento       │  - Lagos/represas          │
└─────────────────────┴─────────────────────┴─────────────────────────────┘
```

---

## 2. Arquitetura de Hardware

### 2.1 Diagrama de camadas

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        CAMADA DE MISSÃO                                 │
│   Câmeras, microfones, alto-falantes, módulo de defesa, sensores        │
├─────────────────────────────────────────────────────────────────────────┤
│                        CAMADA DE IA                                     │
│   NVIDIA Jetson / Raspberry Pi 5 / ESP32-S3                             │
│   Visão computacional, reconhecimento, decisão autônoma                 │
├─────────────────────────────────────────────────────────────────────────┤
│                        CAMADA DE CONTROLE                               │
│   Controlador de voo (PX4/ArduPilot) / Controlador de movimento         │
│   IMU, GPS/RTK, barômetro, magnetômetro                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                        CAMADA DE COMUNICAÇÃO                            │
│   Wi-Fi (principal) + LoRa/Meshtastic (redundância)                     │
│   Módulos de rádio, antenas, protocolos seguros                         │
├─────────────────────────────────────────────────────────────────────────┤
│                        CAMADA DE ENERGIA                                │
│   Baterias LiPo/Li-Ion, BMS, carregamento, monitoramento                │
├─────────────────────────────────────────────────────────────────────────┤
│                        CAMADA MECÂNICA                                  │
│   Chassis, motores, ESCs, hélices/rodas/esteiras, estrutura             │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Especificações por tipo de drone

#### 2.2.1 Drone Terrestre (UGV - Unmanned Ground Vehicle)

| Componente | Especificação | Opções recomendadas |
|------------|---------------|---------------------|
| **Chassis** | 4WD ou esteiras, ~30-50cm | Chassis robótico open source |
| **Motores** | DC brushless com encoder | JGB37-520, N20 com encoder |
| **Controlador de motor** | Ponte H ou ESC | L298N, BTS7960, ODrive |
| **Computador principal** | SBC com GPU | Raspberry Pi 5, NVIDIA Jetson Nano |
| **Câmera principal** | Wide angle, visão noturna | Raspberry Pi Camera V3, OAK-D |
| **Câmera térmica** | LWIR 80x60 ou superior | Flir Lepton, MLX90640 |
| **Lidar** | 2D ou 3D | RPLidar A1/A2, Intel RealSense |
| **Ultrassônico** | Detecção de obstáculos | HC-SR04, TF-Luna |
| **GPS** | GPS/GLONASS, RTK opcional | u-blox NEO-M8N, ZED-F9P |
| **IMU** | 9-DOF | MPU9250, BNO055 |
| **Bateria** | LiPo 4S-6S, 5000-10000mAh | Autonomia: 2-4 horas |
| **Comunicação** | Wi-Fi + LoRa | ESP32, RFM95W |

#### 2.2.2 Drone Aéreo (UAV - Unmanned Aerial Vehicle)

| Componente | Especificação | Opções recomendadas |
|------------|---------------|---------------------|
| **Frame** | Quadcopter/Hexacopter, 450-550mm | F450, S500, X500 |
| **Motores** | Brushless outrunner | 2212-920KV, 2216-880KV |
| **ESCs** | 30A BLHeli_32 | Hobbywing, T-Motor |
| **Controlador de voo** | Autopilot open source | Pixhawk 6C, CUAV V5+, Holybro |
| **Firmware** | Open source | PX4, ArduPilot |
| **Computador de missão** | Edge computing | NVIDIA Jetson Orin Nano, Raspberry Pi 5 |
| **Câmera gimbal** | 3-axis estabilizado | Câmera 4K + gimbal BGC |
| **Câmera térmica** | LWIR | Flir Boson, DJI Zenmuse XT |
| **GPS** | RTK para precisão | HERE3+, ZED-F9P |
| **Telemetria** | Longo alcance | SiK Radio 915MHz, RFD900 |
| **Bateria** | LiPo 4S-6S, 5000-8000mAh | Autonomia: 20-40 min |

#### 2.2.3 Drone Aquático (USV - Unmanned Surface Vehicle)

| Componente | Especificação | Opções recomendadas |
|------------|---------------|---------------------|
| **Casco** | Catamarã ou monocasco, ~60-100cm | Impressão 3D ou fibra |
| **Propulsão** | Motor brushless marítimo | Turnigy Aquastar, Blue Robotics T200 |
| **ESC** | À prova d'água | Hobbywing SeaKing |
| **Controlador** | Autopilot ou SBC | ArduRover, Raspberry Pi |
| **Câmera** | À prova d'água | GoPro ou câmera IP66+ |
| **Sonar** | Profundidade | Ping Sonar, Lowrance |
| **GPS** | Com antena elevada | u-blox com haste |
| **Bateria** | LiPo selada | Autonomia: 2-6 horas |

### 2.3 Módulos comuns

#### 2.3.1 Módulo de câmera e visão

| Sensor | Resolução | FPS | Aplicação |
|--------|-----------|-----|-----------|
| **Raspberry Pi Camera V3** | 12MP | 30-120 | Visão diurna |
| **Pi NoIR Camera** | 8MP | 30 | Visão noturna (com IR) |
| **OAK-D** | 4K + Depth | 30 | Visão estéreo + IA |
| **Flir Lepton 3.5** | 160x120 | 9 | Térmica |
| **IMX477** | 12.3MP | 30 | Alta qualidade |

#### 2.3.2 Módulo de áudio

| Componente | Especificação |
|------------|---------------|
| **Microfone** | MEMS array, I2S (SPH0645, INMP441) |
| **Alto-falante** | 3-5W, driver I2S (MAX98357A) |
| **Processamento** | VAD, cancelamento de ruído |
| **Uso** | Comunicação bidirecional, alertas sonoros |

#### 2.3.3 Módulo GPS/RTK

| Modo | Precisão | Aplicação |
|------|----------|-----------|
| **GPS padrão** | ±2-5m | Navegação geral |
| **DGPS** | ±0.5-1m | Navegação melhorada |
| **RTK** | ±2cm | Navegação de precisão |

### 2.4 Análise de viabilidade legal: VLOS vs. BVLOS

> **Documento de referência**: `rules/RULES_COMPLIANCE_AND_STANDARDS.md` — REGRA-DRONE-02

#### 2.4.1 Descrição do conflito

Existe uma contradição fundamental entre a arquitetura proposta e a regulamentação vigente no Brasil:

- **REGRA-DRONE-02** (derivada do RBAC-E nº 94 da ANAC e da ICA 100-40 do DECEA) determina que a operação de aeronaves não tripuladas deve ser conduzida em **VLOS (Visual Line of Sight)**, ou seja, o piloto remoto deve manter contato visual direto com a aeronave durante todo o voo.
- Toda a arquitetura de **patrulha autônoma por UAV** descrita neste documento pressupõe operação **BVLOS (Beyond Visual Line of Sight)**: o drone decola, executa rotas predefinidas, toma decisões autônomas via IA e retorna à base — tudo sem observador visual humano permanente.

Essa contradição torna a operação autônoma de drones aéreos (UAV) **ilegal sob a regulamentação atual**, a menos que se obtenha uma autorização especial de BVLOS junto à ANAC/DECEA — algo extremamente restrito no Brasil, conforme detalhado abaixo.

| Aspecto | VLOS (obrigatório) | BVLOS (necessário para patrulha) |
|---------|-------------------|----------------------------------|
| **Definição** | Piloto mantém contato visual direto com o drone | Drone opera fora do alcance visual do piloto |
| **Regulamentação BR** | Operação padrão permitida (Classe 3) | Requer autorização especial ANAC + DECEA |
| **Alcance típico** | 200-500m do operador | Ilimitado (limitado por bateria/comunicação) |
| **Autonomia real** | Operador deve estar presente e atento | Operação verdadeiramente autônoma |
| **Compatibilidade com patrulha** | Inviável para patrulha real | Compatível com a arquitetura proposta |

#### 2.4.2 Análise das opções

##### Opção A: Operar apenas em VLOS

Manter um operador humano com contato visual direto durante toda a operação do drone aéreo.

| Aspecto | Avaliação |
|---------|-----------|
| **Legalidade** | Totalmente legal |
| **Viabilidade técnica** | Trivial — basta ter um operador |
| **Impacto na utilidade** | **Severo** — destrói o propósito do sistema |
| **Custo operacional** | Alto — requer presença humana permanente |
| **Avaliação** | Inviável como solução de segurança autônoma |

A exigência de um operador visual permanente contradiz fundamentalmente o objetivo do projeto: segurança **autônoma**. Se alguém precisa estar presente para vigiar o drone, esse alguém poderia simplesmente vigiar a propriedade diretamente.

##### Opção B: Buscar autorização BVLOS junto à ANAC/DECEA

Solicitar autorização especial para operação BVLOS em área privada residencial.

| Aspecto | Avaliação |
|---------|-----------|
| **Legalidade** | Legal se aprovado |
| **Processo** | Requer projeto de segurança operacional (SORA ou equivalente), demonstração de detect-and-avoid, análise de risco aeronáutico |
| **Prazo estimado** | 6-18 meses (sem garantia) |
| **Custo estimado** | R$ 10.000-50.000 (consultoria aeronáutica + taxas) |
| **Probabilidade de aprovação** | **Muito baixa** para uso residencial privado |
| **Avaliação** | Inviável no curto/médio prazo |

A ANAC tem concedido autorizações BVLOS quase exclusivamente para operações agrícolas, inspeção de infraestrutura (linhas de transmissão, dutos) e pesquisa acadêmica — sempre com requisitos rigorosos de detect-and-avoid e operação em espaço aéreo controlado. Não há precedente público de autorização BVLOS para vigilância residencial privada no Brasil.

##### Opção C: Argumentar operação em propriedade privada abaixo de 120m

Interpretar que a operação autônoma sobre propriedade privada própria, abaixo de 120m AGL e em área não controlada, constitui uma zona cinzenta regulatória que poderia ser explorada.

| Aspecto | Avaliação |
|---------|-----------|
| **Argumento jurídico** | O RBAC-E nº 94 foca em segurança de espaço aéreo. Sobre propriedade privada, sem risco a terceiros, poder-se-ia argumentar que o risco é assumido pelo proprietário |
| **Precedentes** | Não há jurisprudência consolidada no Brasil |
| **Risco legal** | **Médio-alto** — multas ANAC de R$ 2.000 a R$ 50.000 por infração |
| **Risco de seguro** | Sinistros envolvendo drone não autorizado podem ter cobertura negada |
| **Avaliação** | Possível objetivo futuro, mas arriscado sem mudança regulatória |

Pontos a considerar nesta opção:
- A ANAC tem focado sua fiscalização em espaço aéreo compartilhado e áreas urbanas densas, não em propriedades rurais privadas.
- Porém, a regulamentação NÃO faz distinção entre espaço aéreo sobre propriedade privada e pública — todo espaço aéreo é controlado pela União.
- Uma mudança regulatória (em discussão em vários países) poderia eventualmente criar categorias simplificadas para operação autônoma em propriedade privada.

##### Opção D: Limitar MVP a UGV (Veículo Terrestre Não Tripulado)

Priorizar drones terrestres (UGV) no MVP, que **não estão sujeitos à regulamentação da ANAC**.

| Aspecto | Avaliação |
|---------|-----------|
| **Legalidade** | **Totalmente legal** — UGVs não são regulados pela ANAC/DECEA |
| **Viabilidade técnica** | Alta — toda a arquitetura de IA, comunicação e navegação se aplica |
| **Cobertura** | Limitada ao nível do solo, mas suficiente para patrulha de perímetro |
| **Custo** | Menor que UAV (R$ 2.150-4.100 vs. R$ 4.600-9.400) |
| **Autonomia de bateria** | Superior (2-4 horas vs. 20-40 min) |
| **Complexidade regulatória** | Nenhuma para a plataforma em si |
| **Avaliação** | **Melhor opção para MVP** |

Vantagens adicionais do UGV para o MVP:
- Não há risco de queda sobre pessoas ou propriedade.
- Operação silenciosa (não perturba vizinhança como hélices).
- Pode operar 24/7 com estação de recarga automática.
- Toda a stack de software (ROS2, Nav2, IA de detecção, comunicação) é diretamente reutilizável quando o UAV for viabilizado.
- Regulamentação aplicável se limita ao Código Civil (uso em propriedade privada própria) e LGPD (captura de imagens).

#### 2.4.3 Decisão recomendada

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    DECISÃO: ESTRATÉGIA EM DUAS FASES                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  FASE 1 (MVP): OPÇÃO D — UGV como plataforma principal         │    │
│  │                                                                 │    │
│  │  • Drone terrestre com toda a stack de IA e comunicação         │    │
│  │  • Sem restrição regulatória aeronáutica                        │    │
│  │  • Patrulha de perímetro autônoma                               │    │
│  │  • Integração com Home Security                                 │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                              │                                          │
│                              ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  FASE 2 (FUTURO): OPÇÃO C — UAV com análise regulatória        │    │
│  │                                                                 │    │
│  │  • Acompanhar evolução regulatória ANAC para BVLOS             │    │
│  │  • Avaliar viabilidade de operação em propriedade privada       │    │
│  │  • Consultar advogado aeronáutico antes de operar               │    │
│  │  • Implementar UAV apenas quando houver segurança jurídica      │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

#### 2.4.4 Impacto na arquitetura

A priorização do UGV impacta a arquitetura nos seguintes pontos:

| Componente | Impacto | Ação necessária |
|------------|---------|-----------------|
| **Camada mecânica** | Chassis terrestre (rodas/esteiras) em vez de frame aéreo | Priorizar especificações da seção 2.2.1 |
| **Controlador de voo** | Não necessário — substituído por controlador de motor | Usar L298N/BTS7960/ODrive em vez de Pixhawk |
| **Navegação** | Nav2 com SLAM 2D em vez de navegação 3D | RPLidar + odometria (mais simples que GPS RTK) |
| **Sensores** | Lidar 2D e ultrassônico em vez de barômetro e altímetro | Foco em RPLidar A1/A2 e sensores de proximidade |
| **Energia** | Bateria com autonomia de horas em vez de minutos | LiPo 4S-6S 5000-10000mAh (2-4h de operação) |
| **Comunicação** | Mesma arquitetura (Wi-Fi + LoRa) | Sem alteração |
| **IA e visão** | Mesma stack (YOLO, tracking, SLAM) | Sem alteração |
| **ROS2** | Mesma arquitetura de nós | Substituir nós de voo por nós de navegação terrestre |
| **Módulo de defesa** | Funciona igualmente em UGV | Sem alteração |
| **Dashboard/integração** | Funciona igualmente | Sem alteração |
| **Custo total** | **Redução de ~50%** (R$ 2.150-4.100 vs. R$ 4.600-9.400) | Orçamento mais acessível para MVP |

**Componentes que NÃO mudam** (reutilizáveis quando UAV for viabilizado):
- Toda a camada de IA (visão computacional, detecção, tracking, decisão).
- Toda a camada de comunicação (Wi-Fi, LoRa, Meshtastic, MQTT).
- Toda a arquitetura de software (ROS2, Docker, APIs).
- Integração com Home Assistant e Frigate.
- Módulo de defesa não letal.
- Protocolos de segurança e autenticação.

**Estimativa**: ~80% do software desenvolvido para UGV é diretamente reutilizável no UAV.

#### 2.4.5 Roadmap legal para operação de UAV

| Etapa | Ação | Prazo estimado | Dependência |
|-------|------|----------------|-------------|
| **1** | Monitorar publicações da ANAC sobre regulamentação BVLOS simplificada | Contínuo | — |
| **2** | Acompanhar consultas públicas da ANAC sobre drones autônomos | Contínuo | — |
| **3** | Consultar advogado especialista em direito aeronáutico sobre viabilidade da Opção C | Antes de qualquer operação UAV | MVP do UGV concluído |
| **4** | Desenvolver protótipo UAV em ambiente de teste controlado (indoor ou área restrita) | Após etapa 3 | Parecer jurídico favorável |
| **5** | Obter registro ANAC e cadastro SISANT para o protótipo | Antes de qualquer voo outdoor | Protótipo funcional |
| **6** | Solicitar autorização BVLOS (se necessária) com documentação completa de segurança | Após etapa 5 | Registro ANAC ativo |
| **7** | Implementar detect-and-avoid e sistema de encerramento de voo de emergência | Requisito para BVLOS | Desenvolvimento paralelo |
| **8** | Operar UAV em conformidade com autorização obtida | Após aprovação | Aprovação ANAC/DECEA |

**Marcos regulatórios a monitorar**:
- Evolução do RBAC-E nº 94 (revisões periódicas da ANAC).
- Regulamentação da U-Space/UTM brasileira (sistema de gerenciamento de tráfego de drones).
- Experiências internacionais: FAA (EUA), EASA (Europa) e CASA (Austrália) estão avançando em frameworks BVLOS simplificados que podem influenciar a ANAC.
- Projetos-piloto de BVLOS aprovados pela ANAC (precedentes que podem abrir caminho).

---

## 3. Sistema de Defesa Não Letal

### 3.1 Especificação do módulo reativo

> **AVISO LEGAL**: O uso deste módulo deve estar em conformidade com todas as legislações locais, estaduais e federais aplicáveis. O sistema é projetado exclusivamente para defesa não letal e dissuasão.

#### 3.1.1 Componentes

| Componente | Especificação | Função |
|------------|---------------|--------|
| **Cilindro CO₂** | 12g ou 88g, descartável/recarregável | Propelente |
| **Câmara de disparo** | Alumínio anodizado, válvula solenóide | Mecanismo de disparo |
| **Munição** | Cápsulas de OC (pimenta) + gengibre | Agente dissuasório |
| **Mira** | Laser classe 2 + câmera | Alinhamento e registro |
| **Controlador** | Microcontrolador dedicado | Segurança e autenticação |

#### 3.1.2 Especificações técnicas

| Parâmetro | Valor |
|-----------|-------|
| **Alcance efetivo** | 3-10 metros |
| **Capacidade** | 5-10 disparos por cilindro |
| **Tempo de recarga** | Manual (troca de cilindro) |
| **Pressão de trabalho** | 50-60 bar |
| **Temperatura de operação** | 0°C a 45°C |

#### 3.1.3 Protocolos de segurança

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    PROTOCOLO DE DISPARO SEGURO                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  1. AUTENTICAÇÃO                                                        │
│     └── Token criptografado + certificado do drone + timestamp          │
│                                                                         │
│  2. AUTORIZAÇÃO                                                         │
│     └── Verificação em 2 níveis:                                        │
│         ├── Sistema central (Home Security)                             │
│         └── IA embarcada (confirmação de ameaça)                        │
│                                                                         │
│  3. CONFIRMAÇÃO                                                         │
│     └── Aviso sonoro prévio (3 segundos)                                │
│     └── Sinal visual (laser de aviso)                                   │
│                                                                         │
│  4. DISPARO                                                             │
│     └── Registro completo:                                              │
│         ├── Timestamp (NTP sincronizado)                                │
│         ├── Coordenadas GPS                                             │
│         ├── Vídeo 5s antes + 10s depois                                 │
│         ├── Identificação do alvo (se disponível)                       │
│         └── Hash SHA-256 do registro                                    │
│                                                                         │
│  5. PÓS-DISPARO                                                         │
│     └── Notificação imediata ao proprietário                            │
│     └── Alerta ao sistema central                                       │
│     └── Log imutável em blockchain local (opcional)                     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

#### 3.1.4 Modos de operação

| Modo | Descrição | Autorização necessária |
|------|-----------|------------------------|
| **Desativado** | Sistema de defesa completamente desligado | Nenhuma |
| **Standby** | Pronto, mas requer autorização manual | Autenticação 2FA |
| **Semi-automático** | IA detecta, humano autoriza | Confirmação via app |
| **Automático** | ~~IA detecta e dispara autonomamente~~ **DESCONTINUADO** – Removido por risco legal e ético. Ver análise abaixo. | N/A |

> **RECOMENDAÇÃO ATUALIZADA**: O modo automático foi **descontinuado permanentemente**. O modo máximo permitido é o **semi-automático**, no qual um humano deve confirmar explicitamente cada ação de defesa.

#### 3.1.5 Análise de riscos do módulo de defesa

> **Seção adicionada em 2026-02-12** após revisão ética e legal do projeto.

##### 3.1.5.1 Riscos de falso positivo da IA

O sistema de visão computacional, mesmo com modelos de alta acurácia (YOLOv8, MoveNet), está sujeito a **falsos positivos** que podem causar danos a pessoas inocentes. Cenários identificados:

| Cenário de falso positivo | Risco | Gravidade |
|---------------------------|-------|-----------|
| **Entregadores** (Correios, iFood, Rappi, etc.) | Identificados erroneamente como invasores | **Alta** |
| **Crianças** (filhos, vizinhos, visitantes) | Tamanho, movimentação e comportamento atípicos confundem a IA | **Crítica** |
| **Animais domésticos** (cães, gatos) | Movimento pode acionar detecção de intrusão | **Alta** |
| **Vizinhos e familiares** | Não cadastrados na whitelist ou falha no reconhecimento facial | **Alta** |
| **Funcionários autorizados** (jardineiro, diarista, manutenção) | Presença legítima em horários variáveis | **Alta** |
| **Condições ambientais adversas** | Chuva, neblina, sombras e iluminação precária degradam a acurácia | **Média** |

##### 3.1.5.2 Responsabilidade civil e criminal do proprietário

O proprietário do sistema é **civil e criminalmente responsável** por todos os danos causados pelo módulo de defesa, independentemente do modo de operação:

- **Código Civil (Art. 927, parágrafo único)**: Responsabilidade objetiva por atividade de risco. O proprietário responde por danos mesmo sem comprovação de culpa.
- **Código Penal (Art. 129)**: Lesão corporal, mesmo que leve, causada por disparo indevido configura crime.
- **Código de Defesa do Consumidor**: Entregadores e prestadores de serviço atingidos indevidamente podem acionar o proprietário.
- **Estatuto da Criança e do Adolescente (ECA)**: Danos a menores de idade acarretam agravantes legais severas.

> **AVISO**: Nenhuma configuração de software, log ou registro exime o proprietário de responsabilidade. A decisão de instalar e operar o módulo de defesa é inteiramente do proprietário, que assume todos os riscos legais.

##### 3.1.5.3 Proporcionalidade da resposta

O princípio da **proporcionalidade** exige que a resposta defensiva seja compatível com o nível real de ameaça:

| Situação | Resposta proporcional | Spray de pimenta é proporcional? |
|----------|-----------------------|----------------------------------|
| Pessoa desconhecida no perímetro | Alerta sonoro e visual | **Não** |
| Pessoa tentando abrir porta/janela | Alerta + notificação ao proprietário | **Não** |
| Invasão confirmada com dano patrimonial | Alerta + acionamento de autoridades | **Possivelmente, com confirmação humana** |
| Ameaça física iminente a moradores | Defesa ativa autorizada | **Sim, com confirmação humana** |

O uso desproporcional de spray de pimenta pode configurar **exercício arbitrário das próprias razões** (Art. 345, Código Penal) ou **lesão corporal** (Art. 129, Código Penal).

##### 3.1.5.4 Recomendação formal

**O modo semi-automático (humano confirma) é o máximo permitido para operação do módulo de defesa.**

Justificativas:
1. A IA atual não possui acurácia suficiente para decisões autônomas de disparo sem risco inaceitável de danos a inocentes.
2. A legislação brasileira não prevê excludente de responsabilidade para sistemas autônomos de defesa.
3. O princípio da proporcionalidade exige avaliação humana do contexto antes de qualquer ação de força.
4. O risco de falsos positivos torna o modo automático eticamente inaceitável.

##### 3.1.5.5 Salvaguardas obrigatórias

As seguintes salvaguardas são **obrigatórias** e devem estar ativas em todos os modos de operação:

| Salvaguarda | Descrição | Implementação |
|-------------|-----------|---------------|
| **Detecção de crianças** | Sistema deve identificar crianças e **bloquear disparo automaticamente** | Modelo de classificação etária (pose + proporções corporais) |
| **Detecção de animais** | Sistema deve identificar animais domésticos e **bloquear disparo automaticamente** | YOLOv8 treinado com classes de animais |
| **Cooldown obrigatório** | Intervalo mínimo de 30 segundos entre disparos | Firmware com timer hardware |
| **Limite diário de disparos** | Máximo de 3 disparos por período de 24 horas | Contador com reset automático |
| **Zona de exclusão** | Áreas onde o disparo é permanentemente bloqueado (entradas de serviço, calçada) | Geofence por software |
| **Registro audiovisual completo** | Gravação obrigatória de 30 segundos antes e 60 segundos após qualquer disparo | Buffer circular em memória |

##### 3.1.5.6 Disclaimer legal

> **DISCLAIMER LEGAL**
>
> Este módulo é fornecido "como está" (as-is), sem qualquer garantia de adequação legal para qualquer jurisdição específica. Os desenvolvedores e contribuidores deste projeto open source **NÃO se responsabilizam** por:
>
> - Danos físicos, morais ou materiais causados pelo uso do módulo de defesa;
> - Consequências legais (civis ou criminais) decorrentes da instalação ou operação do sistema;
> - Falhas de detecção, falsos positivos ou falsos negativos do sistema de IA;
> - Uso indevido, modificação ou operação do sistema fora dos parâmetros documentados.
>
> **O proprietário é o único responsável** por verificar a legalidade do uso em sua jurisdição (município, estado e país), obter todas as autorizações necessárias e operar o sistema de forma ética e legal.
>
> **Recomenda-se fortemente** consultar um advogado especializado antes de instalar ou operar o módulo de defesa.
>
> Ver também: `rules/RULES_COMPLIANCE_AND_STANDARDS.md`, seção 8.4 – Módulo de defesa não letal.

---

## 4. Arquitetura de Software

### 4.1 Stack tecnológico

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         CAMADA DE APLICAÇÃO                             │
│   Dashboard Web │ App Mobile │ API REST │ Integração Home Assistant     │
├─────────────────────────────────────────────────────────────────────────┤
│                         CAMADA DE SERVIÇOS                              │
│   Planejamento │ Coordenação │ Telemetria │ Streaming │ Notificações   │
├─────────────────────────────────────────────────────────────────────────┤
│                         CAMADA DE IA                                    │
│   Visão computacional │ Detecção │ Tracking │ Decisão │ Navegação      │
├─────────────────────────────────────────────────────────────────────────┤
│                         CAMADA DE MIDDLEWARE                            │
│   ROS2 │ MQTT Broker │ Message Queue │ Estado distribuído              │
├─────────────────────────────────────────────────────────────────────────┤
│                         CAMADA DE FIRMWARE                              │
│   Controladores │ Drivers │ HAL │ RTOS                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                         CAMADA DE HARDWARE                              │
│   Sensores │ Atuadores │ Comunicação │ Energia                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Componentes de software

#### 4.2.1 Sistema operacional e framework

| Componente | Tecnologia | Plataforma |
|------------|------------|------------|
| **SO embarcado** | Linux (Ubuntu/Debian), FreeRTOS | Jetson, RPi, ESP32 |
| **Framework robótico** | ROS2 Humble/Iron | Todos |
| **Containerização** | Docker, Podman | Jetson, RPi |
| **Orquestração** | Docker Compose, K3s | Estação base |

#### 4.2.2 Linguagens de programação

| Linguagem | Uso |
|-----------|-----|
| **Python** | IA, visão computacional, scripts, integração |
| **C++** | Nós ROS2 de alto desempenho, drivers |
| **Rust** | Firmware seguro, componentes críticos |
| **C** | Drivers de baixo nível, microcontroladores |

#### 4.2.3 Bibliotecas e frameworks de IA

| Biblioteca | Uso |
|------------|-----|
| **OpenCV** | Processamento de imagem |
| **TensorFlow Lite** | Inferência em edge |
| **PyTorch Mobile** | Modelos customizados |
| **OpenVINO** | Aceleração Intel |
| **ONNX Runtime** | Interoperabilidade de modelos |
| **YOLOv8** | Detecção de objetos |
| **MiDaS** | Estimativa de profundidade |

### 4.3 Arquitetura ROS2

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           SISTEMA ROS2                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐                   │
│  │  /camera    │   │  /lidar     │   │  /imu       │                   │
│  │  _node      │   │  _node      │   │  _node      │                   │
│  └──────┬──────┘   └──────┬──────┘   └──────┬──────┘                   │
│         │                 │                 │                           │
│         ▼                 ▼                 ▼                           │
│  ┌─────────────────────────────────────────────────────────────┐       │
│  │                    /sensor_fusion                           │       │
│  │                    Fusão de dados sensoriais                │       │
│  └─────────────────────────┬───────────────────────────────────┘       │
│                            │                                            │
│         ┌──────────────────┼──────────────────┐                        │
│         ▼                  ▼                  ▼                        │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐                   │
│  │ /perception │   │ /localization│  │  /mapping   │                   │
│  │ Detecção IA │   │  SLAM/GPS   │   │  Mapeamento │                   │
│  └──────┬──────┘   └──────┬──────┘   └──────┬──────┘                   │
│         │                 │                 │                           │
│         ▼                 ▼                 ▼                           │
│  ┌─────────────────────────────────────────────────────────────┐       │
│  │                    /decision_maker                          │       │
│  │              Planejamento e tomada de decisão               │       │
│  └─────────────────────────┬───────────────────────────────────┘       │
│                            │                                            │
│         ┌──────────────────┼──────────────────┐                        │
│         ▼                  ▼                  ▼                        │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐                   │
│  │ /navigation │   │  /defense   │   │ /telemetry  │                   │
│  │ Nav2 Stack  │   │  _module    │   │  _bridge    │                   │
│  └──────┬──────┘   └──────┬──────┘   └──────┬──────┘                   │
│         │                 │                 │                           │
│         ▼                 ▼                 ▼                           │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐                   │
│  │ /motor      │   │ /actuator   │   │ /comm       │                   │
│  │ _controller │   │ _controller │   │ _manager    │                   │
│  └─────────────┘   └─────────────┘   └─────────────┘                   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 4.4 Tópicos e serviços principais

| Tópico/Serviço | Tipo | Descrição |
|----------------|------|-----------|
| `/camera/image_raw` | sensor_msgs/Image | Stream de câmera |
| `/camera/thermal` | sensor_msgs/Image | Imagem térmica |
| `/lidar/scan` | sensor_msgs/LaserScan | Varredura 2D |
| `/imu/data` | sensor_msgs/Imu | Dados de IMU |
| `/gps/fix` | sensor_msgs/NavSatFix | Posição GPS |
| `/perception/detections` | vision_msgs/Detection2DArray | Objetos detectados |
| `/cmd_vel` | geometry_msgs/Twist | Comandos de velocidade |
| `/defense/arm` | std_srvs/SetBool | Armar/desarmar defesa |
| `/defense/fire` | custom_msgs/FireCommand | Comando de disparo |
| `/telemetry/status` | custom_msgs/DroneStatus | Status completo |

---

## 5. Arquitetura de Comunicação

### 5.1 Diagrama de rede

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         ESTAÇÃO BASE                                    │
│   ┌─────────────────────────────────────────────────────────────┐      │
│   │                  HOME SECURITY SYSTEM                        │      │
│   │   Home Assistant + Frigate + NVR + Dashboard de drones      │      │
│   └─────────────────────────────────────────────────────────────┘      │
│                              │                                          │
│              ┌───────────────┼───────────────┐                         │
│              │               │               │                         │
│         ┌────▼────┐    ┌─────▼─────┐   ┌─────▼─────┐                  │
│         │ Wi-Fi   │    │  LoRa     │   │ Meshtastic│                  │
│         │ AP/Mesh │    │  Gateway  │   │  Gateway  │                  │
│         │ 5GHz    │    │  915MHz   │   │  915MHz   │                  │
│         └────┬────┘    └─────┬─────┘   └─────┬─────┘                  │
│              │               │               │                         │
└──────────────┼───────────────┼───────────────┼─────────────────────────┘
               │               │               │
               │      ÁREA DE COBERTURA        │
               │               │               │
     ┌─────────┴───────────────┴───────────────┴─────────┐
     │                                                    │
     │  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
     │  │  DRONE   │  │  DRONE   │  │  DRONE   │        │
     │  │ TERRESTRE│  │  AÉREO   │  │ PLUVIAL  │        │
     │  │          │  │          │  │          │        │
     │  │ Wi-Fi    │  │ Wi-Fi    │  │ Wi-Fi    │        │
     │  │ + LoRa   │  │ + LoRa   │  │ + LoRa   │        │
     │  └──────────┘  └──────────┘  └──────────┘        │
     │                                                    │
     └────────────────────────────────────────────────────┘
```

### 5.2 Protocolos de comunicação

| Canal | Protocolo | Uso | Alcance |
|-------|-----------|-----|---------|
| **Wi-Fi 5GHz** | TCP/UDP, WebRTC | Streaming de vídeo, comandos rápidos | 100-500m |
| **Wi-Fi 2.4GHz** | MQTT | Telemetria, comandos | 200-1000m |
| **LoRa** | LoRaWAN, Meshtastic | Telemetria crítica, fallback | 2-15km |
| **Bluetooth** | BLE 5.0 | Configuração, diagnóstico local | 50m |

### 5.3 Redundância e failover

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    MATRIZ DE REDUNDÂNCIA                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  PRIORIDADE 1: Wi-Fi 5GHz (baixa latência)                             │
│       │                                                                 │
│       ├── Falha detectada (timeout 3s)                                 │
│       │                                                                 │
│       ▼                                                                 │
│  PRIORIDADE 2: Wi-Fi 2.4GHz (maior alcance)                            │
│       │                                                                 │
│       ├── Falha detectada (timeout 5s)                                 │
│       │                                                                 │
│       ▼                                                                 │
│  PRIORIDADE 3: LoRa/Meshtastic (ultra-longo alcance)                   │
│       │                                                                 │
│       ├── Modo degradado: apenas telemetria e comandos críticos        │
│       │                                                                 │
│       ▼                                                                 │
│  FALLBACK: Modo autônomo (retorno à base ou posição segura)            │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 5.4 Integração com Home Security

| Integração | Protocolo | Dados |
|------------|-----------|-------|
| **Home Assistant** | MQTT, REST API | Status, comandos, automações |
| **Frigate** | MQTT, RTSP | Eventos de detecção, streaming |
| **Dashboard** | WebSocket | Telemetria em tempo real |
| **Notificações** | MQTT → Telegram/Push | Alertas, eventos, disparos |

---

## 6. IA Embarcada

### 6.1 Capacidades de IA

| Capacidade | Modelo/Técnica | Plataforma |
|------------|----------------|------------|
| **Detecção de pessoas** | YOLOv8n, MobileNet-SSD | Jetson, RPi5 |
| **Detecção de veículos** | YOLOv8n | Jetson, RPi5 |
| **Reconhecimento facial** | FaceNet, ArcFace | Jetson |
| **Tracking de objetos** | DeepSORT, ByteTrack | Jetson, RPi5 |
| **Estimativa de pose** | MoveNet, MediaPipe | Jetson |
| **Detecção de anomalias** | Autoencoder, Isolation Forest | Todos |
| **Navegação autônoma** | Nav2, comportamentos reativos | ROS2 |
| **SLAM** | ORB-SLAM3, RTAB-Map | Jetson |

### 6.2 Pipeline de visão computacional

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    PIPELINE DE VISÃO COMPUTACIONAL                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐            │
│  │ Captura  │──►│ Pré-proc │──►│ Inferência│──►│ Pós-proc │            │
│  │ Imagem   │   │ (resize, │   │ (YOLO,    │   │ (NMS,    │            │
│  │ 30 FPS   │   │ normalize│   │ tracking) │   │ filter)  │            │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘            │
│                                                       │                 │
│                                                       ▼                 │
│                                              ┌──────────────┐          │
│                                              │  Decisão     │          │
│                                              │  - Alerta    │          │
│                                              │  - Seguir    │          │
│                                              │  - Defesa    │          │
│                                              └──────────────┘          │
│                                                                         │
│  Latência alvo: < 100ms (detecção) < 500ms (decisão)                   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 6.3 Árvore de decisão autônoma

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    ÁRVORE DE DECISÃO AUTÔNOMA                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│                         ┌─────────────┐                                │
│                         │  Detecção   │                                │
│                         │  de pessoa  │                                │
│                         └──────┬──────┘                                │
│                                │                                        │
│                    ┌───────────┴───────────┐                           │
│                    │                       │                           │
│              ┌─────▼─────┐           ┌─────▼─────┐                     │
│              │ Conhecido │           │Desconhecido│                    │
│              │(whitelist)│           │           │                     │
│              └─────┬─────┘           └─────┬─────┘                     │
│                    │                       │                           │
│              ┌─────▼─────┐           ┌─────▼─────┐                     │
│              │  Ignorar  │           │  Seguir   │                     │
│              │  ou Log   │           │  e alertar│                     │
│              └───────────┘           └─────┬─────┘                     │
│                                            │                           │
│                              ┌─────────────┴─────────────┐             │
│                              │                           │             │
│                        ┌─────▼─────┐               ┌─────▼─────┐       │
│                        │Comportam. │               │Comportam. │       │
│                        │ Normal    │               │ Suspeito  │       │
│                        └─────┬─────┘               └─────┬─────┘       │
│                              │                           │             │
│                        ┌─────▼─────┐               ┌─────▼─────┐       │
│                        │ Monitorar │               │  Escalar  │       │
│                        │           │               │  alerta   │       │
│                        └───────────┘               └─────┬─────┘       │
│                                                          │             │
│                                            ┌─────────────┴──────┐      │
│                                            │                    │      │
│                                      ┌─────▼─────┐        ┌─────▼─────┐│
│                                      │ Aviso     │        │ Invasão  ││
│                                      │ sonoro    │        │ confirmada││
│                                      └───────────┘        └─────┬─────┘│
│                                                                 │      │
│                                                           ┌─────▼─────┐│
│                                                           │  Defesa   ││
│                                                           │(se autoriz)││
│                                                           └───────────┘│
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Segurança e Compliance

### 7.1 Requisitos de segurança

| Categoria | Requisito |
|-----------|-----------|
| **Autenticação** | TLS 1.3, certificados mTLS, tokens JWT |
| **Criptografia** | AES-256-GCM para dados, ChaCha20 para telemetria |
| **Integridade** | Assinatura de firmware, verificação de boot |
| **Auditoria** | Logs imutáveis, timestamps NTP, hash chain |
| **Privacidade** | Processamento local, dados criptografados em repouso |

### 7.2 Conformidade legal

| Aspecto | Requisito | Referência |
|---------|-----------|------------|
| **LGPD** | Processamento local, sem envio para nuvem | Lei 13.709/2018 |
| **Uso de drones** | Registro na ANAC para drones >250g | RBAC-E nº 94 |
| **Espaço aéreo** | Respeitar zonas restritas | DECEA |
| **Armas não letais** | Verificar legislação estadual | Varia por estado |
| **Gravação de vídeo** | Não capturar áreas públicas/vizinhos | LGPD |

### 7.3 Regras derivadas

```
REGRA-DRONE-01: Drones aéreos >250g devem ser registrados na ANAC.

REGRA-DRONE-02: Voos devem respeitar altitude máxima de 120m e zonas restritas.

REGRA-DRONE-03: Operação noturna requer luzes de navegação visíveis.

REGRA-DRONE-04: Módulo de defesa requer autenticação de 2 fatores para armamento.

REGRA-DRONE-05: Todo disparo deve ser registrado com vídeo, GPS e timestamp.

REGRA-DRONE-06: Drones devem ter modo fail-safe (retorno à base) em perda de sinal.

REGRA-DRONE-07: Firmware deve ser assinado digitalmente para evitar adulteração.

REGRA-DRONE-08: Comunicação deve usar criptografia end-to-end.

REGRA-DRONE-09: Dados de vídeo devem ser armazenados localmente, nunca em nuvem.

REGRA-DRONE-10: Whitelist de pessoas autorizadas deve ser configurável.
```

---

## 8. Estimativa de Custos

### 8.1 Drone terrestre (UGV)

| Componente | Custo estimado |
|------------|----------------|
| Chassis 4WD | R$ 200-400 |
| Motores + drivers | R$ 150-300 |
| Raspberry Pi 5 8GB | R$ 500-700 |
| Câmera + térmica | R$ 300-800 |
| Lidar RPLidar A1 | R$ 400-600 |
| GPS + IMU | R$ 200-400 |
| Bateria + BMS | R$ 200-400 |
| Estrutura + impressão 3D | R$ 100-300 |
| Comunicação (ESP32 + LoRa) | R$ 100-200 |
| **Total** | **R$ 2.150-4.100** |

### 8.2 Drone aéreo (UAV)

| Componente | Custo estimado |
|------------|----------------|
| Frame + motores + ESCs | R$ 600-1.200 |
| Controlador Pixhawk | R$ 600-1.500 |
| NVIDIA Jetson Orin Nano | R$ 2.000-3.000 |
| Câmera + gimbal | R$ 500-1.500 |
| GPS RTK | R$ 400-1.200 |
| Bateria 4S 5000mAh (x2) | R$ 300-600 |
| Telemetria + LoRa | R$ 200-400 |
| **Total** | **R$ 4.600-9.400** |

### 8.3 Drone aquático (USV)

| Componente | Custo estimado |
|------------|----------------|
| Casco (impressão 3D ou fibra) | R$ 300-800 |
| Motor + ESC marítimo | R$ 300-600 |
| Raspberry Pi 5 | R$ 500-700 |
| Câmera IP66 | R$ 200-500 |
| GPS + sonar | R$ 300-600 |
| Bateria selada | R$ 200-400 |
| **Total** | **R$ 1.800-3.600** |

### 8.4 Infraestrutura de comunicação

| Componente | Custo estimado |
|------------|----------------|
| AP Wi-Fi longo alcance | R$ 300-800 |
| Gateway LoRa | R$ 200-500 |
| Nós Meshtastic (x3) | R$ 150-300 |
| Antenas externas | R$ 100-300 |
| **Total** | **R$ 750-1.900** |

---

## 9. Roadmap de Desenvolvimento

### 9.1 Fases do projeto

| Fase | Duração | Entregas |
|------|---------|----------|
| **Fase 1: Fundação** | - | Arquitetura, documentação, seleção de hardware |
| **Fase 2: Prototipagem** | - | Drone terrestre básico, comunicação Wi-Fi |
| **Fase 3: IA básica** | - | Detecção de pessoas, navegação autônoma |
| **Fase 4: Integração** | - | Integração com Home Security |
| **Fase 5: Comunicação** | - | Rede LoRa/Meshtastic redundante |
| **Fase 6: Defesa** | - | Módulo reativo (onde legalmente permitido) |
| **Fase 7: Frota** | - | Coordenação multi-drone |
| **Fase 8: Aéreo** | - | Drone aéreo com VTOL |

### 9.2 MVP (Minimum Viable Product)

O MVP consiste em:
1. Um drone terrestre com câmera
2. Detecção básica de pessoas (YOLO)
3. Comunicação Wi-Fi com Home Assistant
4. Dashboard de telemetria
5. Alertas via Telegram

---

## 10. Referências

### Projetos open source relacionados

- [PX4 Autopilot](https://px4.io/)
- [ArduPilot](https://ardupilot.org/)
- [ROS2](https://docs.ros.org/)
- [Meshtastic](https://meshtastic.org/)
- [OpenCV](https://opencv.org/)
- [YOLOv8](https://docs.ultralytics.com/)
- [Nav2](https://nav2.org/)

### Hardware open source

- [Open Source Rover (NASA JPL)](https://github.com/nasa-jpl/open-source-rover)
- [Duckietown](https://www.duckietown.org/)
- [OpenPilot](https://github.com/commaai/openpilot)

### Documentação adicional

- `prd/PRD_AUTONOMOUS_DRONES.md` - PRD detalhado
- `prd/PRD_DRONE_DEFENSE_MODULE.md` - Módulo de defesa
- `prd/PRD_DRONE_COMMUNICATION.md` - Rede de comunicação

---

> **Status**: Documento de arquitetura v1.0
>
> **Próximos passos**: Criar PRDs detalhados, definir tarefas de implementação
>
> **Aviso legal**: O desenvolvimento e uso de drones e módulos de defesa devem seguir todas as regulamentações locais aplicáveis.
