# Modelo de Ameacas (Threat Model) -- Sistema de Home Security

> Documento produzido durante a revisao do projeto em 2026-02-12
>
> Framework: STRIDE (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege)
>
> Escopo: Todos os componentes do sistema de seguranca residencial open source nos tres cenarios (rural, urbano, apartamento)

---

## Indice

1. [Introducao e Objetivo](#1-introducao-e-objetivo)
2. [Perfis de Adversarios](#2-perfis-de-adversarios)
3. [Superficie de Ataque por Cenario](#3-superficie-de-ataque-por-cenario)
4. [Analise STRIDE por Componente](#4-analise-stride-por-componente)
5. [Ataques Especificos Detalhados](#5-ataques-especificos-detalhados)
6. [Mapeamento: Ameaca, Defesa Existente e Gap](#6-mapeamento-ameaca-defesa-existente-e-gap)
7. [Nivel de Sofisticacao que o Sistema Pretende Resistir](#7-nivel-de-sofisticacao-que-o-sistema-pretende-resistir)
8. [Recomendacoes de Mitigacao por Gap](#8-recomendacoes-de-mitigacao-por-gap)
9. [Matriz de Risco Consolidada](#9-matriz-de-risco-consolidada)
10. [Referencias](#10-referencias)

---

## 1. Introducao e Objetivo

Este documento estabelece o modelo de ameacas para o Sistema de Home Security DIY, um projeto open source que integra Home Assistant, Frigate, sensores Zigbee, cameras IP, comunicacao LoRa e drones autonomos para protecao de residencias em tres cenarios distintos.

### 1.1 Por que um Threat Model?

Um sistema de seguranca que nao modela suas proprias vulnerabilidades e um paradoxo. O objetivo deste documento e:

- Identificar **quem** atacaria o sistema, **como** e **por que**
- Mapear a superficie de ataque de cada componente usando o framework STRIDE
- Documentar defesas existentes e **gaps** que precisam de mitigacao
- Definir explicitamente o **nivel de sofisticacao** contra o qual o sistema oferece protecao
- Fornecer recomendacoes concretas e priorizadas para cada vulnerabilidade

### 1.2 Escopo

| Item | Incluido | Observacao |
|------|----------|------------|
| Sensores Zigbee | Sim | Abertura, movimento, vibracaoo, sirene |
| Cameras IP (PoE/Wi-Fi) | Sim | RTSP/ONVIF, Reolink, Hikvision, etc. |
| Servidor central (Mini PC N100) | Sim | Home Assistant + Frigate + Zigbee2MQTT |
| Rede Wi-Fi e VLANs | Sim | Segmentacao, firewall, VPN |
| Comunicacao LoRa/Meshtastic | Sim | Redundancia para drones e alertas |
| Drones autonomos (UGV, UAV, USV) | Sim | Terrestres, aereos, aquaticos |
| Modulo de defesa nao letal | Sim | CO2 + pimenta/gengibre |
| Home Assistant + Alarmo | Sim | Plataforma de automacao |
| Frigate NVR | Sim | Deteccao de objetos por IA |
| Seguranca fisica passiva | Parcial | Muros, cercas, grades (contexto apenas) |

---

## 2. Perfis de Adversarios

### 2.1 Classificacao de adversarios

| ID | Perfil | Motivacao | Recursos | Conhecimento tecnico | Tempo disponivel | Disposicao para risco |
|----|--------|-----------|----------|---------------------|------------------|----------------------|
| **ADV-01** | Oportunista casual | Furto de conveniencia, itens visiveis | Minimos (ferramentas basicas) | Nenhum a baixo | Segundos a minutos | Baixa (foge ao primeiro sinal de alarme) |
| **ADV-02** | Ladrao experiente | Furto planejado de bens de valor | Moderados (ferramentas especializadas, scanner RF) | Medio | Minutos a horas | Media (persiste se recompensa e alta) |
| **ADV-03** | Quadrilha organizada | Assalto a mao armada, roubo de alto valor | Altos (jammers, veiculos, armas, insiders) | Medio a alto | Horas a dias de planejamento | Alta (aceita confronto) |
| **ADV-04** | Insider / empregado domestico | Furto interno, informacao privilegiada | Acesso fisico ao interior, conhecimento de rotinas | Baixo a medio | Semanas a meses (acesso prolongado) | Media (tenta evitar deteccao) |
| **ADV-05** | Hacker remoto | Acesso a cameras, dados, desabilitar sistema | Altos (ferramentas de pentest, exploits) | Alto a muito alto | Horas a semanas | Baixa fisicamente (atua remotamente) |

### 2.2 Detalhamento por perfil

#### ADV-01: Oportunista casual

- **Comportamento tipico**: Caminha pela rua, ve portao aberto ou janela entreaberta, entra rapidamente
- **Alvos**: Celulares, carteiras, objetos no quintal, bicicletas
- **Capacidade tecnica contra o sistema**: Nenhuma; nao sabe que existe um sistema de seguranca
- **Contramedida mais eficaz**: Visibilidade do sistema (cameras visiveis, placa de alarme, iluminacao)

#### ADV-02: Ladrao experiente

- **Comportamento tipico**: Faz reconhecimento previo (dias), observa rotinas, identifica pontos vulneraveis
- **Alvos**: Eletronicos, joias, cofres, veiculos
- **Capacidade tecnica contra o sistema**: Pode cortar energia, identificar cameras, conhece alarmes residenciais convencionais
- **Contramedida mais eficaz**: Redundancia (nobreak, 4G backup, sensores tamper), deteccao precoce no perimetro

#### ADV-03: Quadrilha organizada

- **Comportamento tipico**: Planejamento de dias/semanas, multiplos membros com funcoes definidas, possivel uso de jammers RF e veiculos
- **Alvos**: Cofres, valores altos, veiculos, refens para extorsao
- **Capacidade tecnica contra o sistema**: Pode usar jammers de RF (Zigbee/Wi-Fi), cortar energia e internet, ter insider
- **Contramedida mais eficaz**: Comunicacao redundante (LoRa), deteccao de jamming, panic button, integracao com forcas de seguranca

#### ADV-04: Insider / empregado domestico

- **Comportamento tipico**: Acesso legitimo, coleta informacoes ao longo do tempo, pode desarmar sistema ou fornecer dados a terceiros
- **Alvos**: Objetos de valor, informacoes sobre rotinas, codigos de alarme, desabilitar sensores
- **Capacidade tecnica contra o sistema**: Conhece layout dos sensores, pode ter acesso ao painel/teclado, sabe horarios do alarme
- **Contramedida mais eficaz**: Principio do menor privilegio, logs de auditoria, codigos individuais por usuario, cameras internas (com consentimento)

#### ADV-05: Hacker remoto

- **Comportamento tipico**: Explora vulnerabilidades de rede, firmware desatualizado, credenciais fracas, acesso a cameras
- **Alvos**: Acesso a streams de video (voyeurismo ou venda), desabilitar alarmes remotamente, ransomware no servidor, dados pessoais
- **Capacidade tecnica contra o sistema**: Exploits em cameras IP (Hikvision CVEs), forca bruta em Home Assistant, interceptacao de MQTT nao criptografado
- **Contramedida mais eficaz**: Segmentacao de rede (VLANs), VPN obrigatoria, atualizacoes de firmware, 2FA, cameras sem acesso a internet

---

## 3. Superficie de Ataque por Cenario

### 3.1 Cenario Rural

| Vetor de ataque | Probabilidade | Impacto | Risco | Justificativa |
|-----------------|---------------|---------|-------|---------------|
| Invasao por perimetro nao monitorado | Alta | Alto | **Critico** | Perimetro extenso (500m-5000m), impossivel cobrir 100% com sensores |
| Corte de energia eletrica | Alta | Alto | **Critico** | Infraestrutura fragil, sem redundancia da concessionaria |
| Corte de internet (unico provedor) | Alta | Alto | **Critico** | Zona rural frequentemente com unico link, facil de cortar |
| RF jamming (Zigbee/Wi-Fi) | Media | Alto | **Alto** | Distancia permite uso de jammers sem ser visto |
| Tamper fisico em cameras externas | Media | Medio | **Medio** | Cameras em posicoes remotas, dificil vigiar |
| Roubo de equipamentos agricolas/animais | Alta | Medio | **Alto** | Motivacao primaria em area rural |
| Ataque a drones em patrulha | Media | Medio | **Medio** | Drone terrestre pode ser danificado/roubado |
| Social engineering (caseiro/funcionario) | Media | Alto | **Alto** | Funcionarios rurais com acesso amplo |

### 3.2 Cenario Urbano (Casa com quintal)

| Vetor de ataque | Probabilidade | Impacto | Risco | Justificativa |
|-----------------|---------------|---------|-------|---------------|
| Invasao por muro/portao | Alta | Alto | **Critico** | Ponto de entrada mais comum em residencias urbanas |
| Arrombamento de janela terreo | Media | Alto | **Alto** | Janelas sem grade sao vulneraveis |
| Shoulder surfing (observar codigo de alarme) | Media | Medio | **Medio** | Vizinhanca proxima, teclado visivel |
| Corte de energia (quadro externo) | Media | Alto | **Alto** | Quadro de energia frequentemente acessivel da rua |
| Interceptacao de Wi-Fi | Baixa | Alto | **Medio** | Proximidade de vizinhos, redes visiveis |
| Insider (empregada domestica, diarista) | Media | Alto | **Alto** | Acesso regular ao interior, conhece rotinas |
| Furto de correspondencia/encomendas | Alta | Baixo | **Medio** | Oportunismo, nao necessariamente relacionado ao sistema |
| Hacker remoto (Home Assistant exposto) | Baixa | Critico | **Alto** | Se porta exposta, comprometimento total |

### 3.3 Cenario Apartamento

| Vetor de ataque | Probabilidade | Impacto | Risco | Justificativa |
|-----------------|---------------|---------|-------|---------------|
| Engenharia social na portaria | Media | Alto | **Alto** | Porteiro autoriza entrada de pessoas nao autorizadas |
| Arrombamento de porta | Baixa | Alto | **Medio** | Porta blindada dificulta, mas nao impede |
| Insider (empregada, entregador) | Media | Medio | **Medio** | Acesso interior em horarios especificos |
| Credential stuffing (Home Assistant) | Baixa | Alto | **Medio** | Se acesso remoto configurado incorretamente |
| Clone de chave/controle do predio | Baixa | Alto | **Medio** | Controles de acesso condominiais frequentemente fracos |
| Acesso por varanda (andares baixos) | Baixa | Alto | **Medio** | Relevante ate 3o andar |
| Hacker remoto (camera olho magico) | Baixa | Medio | **Baixo** | Dispositivo Wi-Fi pode ser vulneravel |

### 3.4 Legenda de classificacao

| Nivel | Probabilidade | Impacto |
|-------|---------------|---------|
| **Baixa** | Improvavel, requer condicoes especificas | Inconveniencia, perda menor |
| **Media** | Possivel, ja observado em contextos similares | Perda material significativa ou falha do sistema |
| **Alta** | Provavel, ocorre com frequencia na regiao | Perda total, risco a integridade fisica, comprometimento completo |
| **Critico** | - | Risco a vida, perda irrecuperavel |

---

## 4. Analise STRIDE por Componente

### 4.1 Sensores Zigbee

| Categoria STRIDE | Ameaca | Probabilidade | Impacto | Descricao |
|------------------|--------|---------------|---------|-----------|
| **S** - Spoofing | Replay de mensagens Zigbee | Baixa | Alto | Atacante captura e retransmite mensagem de "porta fechada" para mascarar abertura real |
| **T** - Tampering | Tamper fisico no sensor | Media | Alto | Remocao ou destruicao do sensor fisico (arrancar da parede, cobrir PIR) |
| **T** - Tampering | Injecao de frames Zigbee maliciosos | Baixa | Alto | Requer hardware especializado (HackRF) e conhecimento do protocolo |
| **R** - Repudiation | Ausencia de log por sensor offline | Media | Medio | Sensor com bateria descarregada nao reporta eventos, sem registro de falha |
| **I** - Info Disclosure | Sniffing do trafego Zigbee | Baixa | Baixo | Zigbee 3.0 usa AES-128, mas chave de rede pode ser capturada durante pairing |
| **D** - Denial of Service | Jamming na faixa 2.4GHz | Media | Alto | Jammer de 2.4GHz afeta Zigbee e Wi-Fi simultaneamente |
| **D** - Denial of Service | Esgotamento de bateria por flood | Baixa | Medio | Forcar sensor a transmitir continuamente ate esgotar bateria |
| **E** - Elevation | Comprometimento do coordenador Zigbee | Baixa | Critico | Se coordenador comprometido, atacante controla toda a rede Zigbee |

### 4.2 Cameras IP

| Categoria STRIDE | Ameaca | Probabilidade | Impacto | Descricao |
|------------------|--------|---------------|---------|-----------|
| **S** - Spoofing | Injecao de stream RTSP falso | Baixa | Critico | Substituir feed real por video pre-gravado (ataque "Ocean's Eleven") |
| **T** - Tampering | Tamper fisico (cobrir, mover, destruir) | Media | Alto | Camera acessivel externamente pode ser vandalizada |
| **T** - Tampering | Firmware malicioso do fabricante | Baixa | Critico | Cameras chinesas com backdoor conhecido (Hikvision CVE-2021-36260) |
| **R** - Repudiation | Lacuna em gravacao por falha de armazenamento | Media | Alto | SSD/HDD cheio, corrompido ou em falha causa perda de evidencias |
| **I** - Info Disclosure | Acesso nao autorizado ao stream RTSP | Media | Alto | RTSP sem autenticacao ou com credenciais padrao |
| **I** - Info Disclosure | Exfiltracao de video via internet | Baixa | Alto | Camera com acesso a internet envia dados para servidor externo |
| **D** - Denial of Service | Sobrecarga do servidor com streams | Baixa | Alto | Multiplas conexoes simultaneas ao RTSP causam crash |
| **D** - Denial of Service | Corte do cabo PoE | Media | Alto | Cabo exposto pode ser cortado, desabilitando camera e alimentacao |
| **E** - Elevation | Exploit em firmware desatualizado | Media | Critico | CVEs conhecidos permitem RCE (Remote Code Execution) em cameras |

### 4.3 Servidor Central (Mini PC N100)

| Categoria STRIDE | Ameaca | Probabilidade | Impacto | Descricao |
|------------------|--------|---------------|---------|-----------|
| **S** - Spoofing | Acesso com credenciais roubadas | Media | Critico | Credential stuffing ou senha fraca no Home Assistant |
| **T** - Tampering | Modificacao de automacoes/regras | Baixa | Critico | Atacante com acesso altera regras de alarme para desabilitar alertas |
| **T** - Tampering | Adulteracao fisica do servidor | Baixa | Critico | Acesso fisico permite boot de USB, extracao de disco |
| **R** - Repudiation | Logs insuficientes ou apagados | Media | Alto | Sem log centralizado, atacante apaga rastros |
| **I** - Info Disclosure | Exposicao de secrets.yaml | Media | Critico | Credenciais, tokens de API, senhas de cameras em texto plano |
| **D** - Denial of Service | Corte de energia sem nobreak | Media | Alto | Servidor desliga, sistema inteiro fica offline |
| **D** - Denial of Service | Esgotamento de disco (gravacoes) | Media | Medio | Frigate preenche disco, servidor fica instavel |
| **E** - Elevation | Escalacao via add-on vulneravel do HA | Baixa | Critico | Add-ons de terceiros podem ter vulnerabilidades |

### 4.4 Rede Wi-Fi

| Categoria STRIDE | Ameaca | Probabilidade | Impacto | Descricao |
|------------------|--------|---------------|---------|-----------|
| **S** - Spoofing | Rogue AP (Evil Twin) | Baixa | Alto | Atacante cria AP falso para capturar credenciais |
| **T** - Tampering | Injecao de pacotes / deauth | Media | Alto | Desautenticacao de clientes Wi-Fi com ferramentas como aireplay-ng |
| **R** - Repudiation | Falta de log no roteador | Media | Medio | Sem registro de conexoes e tentativas de acesso |
| **I** - Info Disclosure | Sniffing de trafego nao criptografado | Baixa | Medio | MQTT sem TLS, HTTP em vez de HTTPS na rede interna |
| **D** - Denial of Service | Jamming 2.4GHz/5GHz | Media | Critico | Jammer desabilita toda comunicacao Wi-Fi e Zigbee |
| **D** - Denial of Service | Ataque de desautenticacao em massa | Media | Alto | Deauth flood causa desconexao de todos os dispositivos |
| **E** - Elevation | Exploracao de vulnerabilidade no roteador | Baixa | Critico | Firmware desatualizado de roteador com CVE conhecida |

### 4.5 Comunicacao LoRa/Meshtastic

| Categoria STRIDE | Ameaca | Probabilidade | Impacto | Descricao |
|------------------|--------|---------------|---------|-----------|
| **S** - Spoofing | Envio de mensagens falsas na rede Meshtastic | Baixa | Alto | Sem autenticacao forte, mensagens podem ser forjadas |
| **T** - Tampering | Modificacao de comandos em transito | Baixa | Critico | Alteracao de comando de drone ou alerta |
| **R** - Repudiation | Mensagens nao assinadas | Media | Medio | Impossivel provar origem de comando |
| **I** - Info Disclosure | Interceptacao de telemetria | Media | Baixo | Dados de posicao de drones podem ser captados |
| **D** - Denial of Service | Jamming na faixa 915MHz | Baixa | Alto | Jammer especifico para LoRa, menos comum |
| **E** - Elevation | Acesso ao gateway LoRa | Baixa | Alto | Gateway comprometido permite injecao de comandos |

### 4.6 Drones Autonomos

| Categoria STRIDE | Ameaca | Probabilidade | Impacto | Descricao |
|------------------|--------|---------------|---------|-----------|
| **S** - Spoofing | GPS spoofing | Baixa | Critico | Desviar drone de rota, enviar para local errado |
| **S** - Spoofing | Spoofing de comandos de controle | Baixa | Critico | Enviar comandos falsos para o drone |
| **T** - Tampering | Captura fisica do drone | Media | Alto | Drone terrestre pode ser fisicamente capturado |
| **T** - Tampering | Adulteracao de firmware | Baixa | Critico | Firmware comprometido altera comportamento do drone |
| **R** - Repudiation | Falha no registro de disparo do modulo de defesa | Baixa | Critico | Disparo sem registro gera responsabilidade legal |
| **I** - Info Disclosure | Interceptacao de stream de video do drone | Media | Medio | Video transmitido via Wi-Fi pode ser capturado |
| **D** - Denial of Service | Destruicao fisica | Media | Alto | Drone acessivel pode ser destruido ou danificado |
| **D** - Denial of Service | Jamming de comunicacao | Media | Alto | Isolar drone da estacao base |
| **E** - Elevation | Comprometimento da IA de decisao | Baixa | Critico | Adversario engana modelo de IA (adversarial attacks) |

### 4.7 Modulo de Defesa Nao Letal

| Categoria STRIDE | Ameaca | Probabilidade | Impacto | Descricao |
|------------------|--------|---------------|---------|-----------|
| **S** - Spoofing | Comando de disparo falso | Baixa | Critico | Disparo nao autorizado contra pessoa inocente |
| **T** - Tampering | Adulteracao da municao | Baixa | Alto | Substituicao por substancia mais perigosa |
| **T** - Tampering | Desabilitacao fisica do mecanismo | Media | Medio | Invasor desativa o modulo antes de entrar |
| **R** - Repudiation | Registro de disparo adulterado | Baixa | Critico | Sem prova integra de quando/por que houve disparo |
| **I** - Info Disclosure | Vazamento do protocolo de ativacao | Baixa | Alto | Conhecimento do protocolo permite bypass |
| **D** - Denial of Service | Descarga do cilindro de CO2 | Baixa | Medio | Esvaziar cilindro sem disparo efetivo |
| **E** - Elevation | Bypass da autenticacao 2FA | Baixa | Critico | Permitiria disparo sem autorizacao |

### 4.8 Home Assistant + Alarmo

| Categoria STRIDE | Ameaca | Probabilidade | Impacto | Descricao |
|------------------|--------|---------------|---------|-----------|
| **S** - Spoofing | Login com credenciais comprometidas | Media | Critico | Atacante desarma alarme remotamente |
| **T** - Tampering | Modificacao de automacoes | Baixa | Critico | Desabilitar notificacoes ou sirenes via automacao |
| **T** - Tampering | Alteracao de configuracao do Alarmo | Baixa | Critico | Mudar delay de entrada para valor muito alto |
| **R** - Repudiation | Falta de audit log granular | Media | Alto | HA nao registra todas as acoes administrativas por padrao |
| **I** - Info Disclosure | Exposicao da API REST sem autenticacao | Baixa | Critico | API permite controlar todo o sistema |
| **D** - Denial of Service | Crash do HA por add-on defeituoso | Media | Alto | Sistema inteiro de alarme fica offline |
| **E** - Elevation | Exploit em integracao de terceiros | Baixa | Critico | HACS ou custom components com vulnerabilidades |

### 4.9 Frigate NVR

| Categoria STRIDE | Ameaca | Probabilidade | Impacto | Descricao |
|------------------|--------|---------------|---------|-----------|
| **S** - Spoofing | Feed de camera substituido | Baixa | Critico | IA processa video falso e nao detecta invasao real |
| **T** - Tampering | Envenenamento do modelo de IA | Baixa | Alto | Adversarial examples enganam deteccao de pessoas |
| **R** - Repudiation | Gravacao deletada ou corrompida | Media | Alto | Perda de evidencias para policia/justica |
| **I** - Info Disclosure | Acesso nao autorizado a gravacoes | Media | Alto | Gravacoes contem dados sensiveis (LGPD) |
| **D** - Denial of Service | Sobrecarga de CPU/GPU | Baixa | Medio | Muitas deteccoes simultaneas degradam performance |
| **E** - Elevation | Acesso ao container Docker do Frigate | Baixa | Alto | Container com privilegios pode comprometer host |

---

## 5. Ataques Especificos Detalhados

### 5.1 RF Jamming (Bloqueio de Radiofrequencia)

| Aspecto | Detalhe |
|---------|---------|
| **Descricao** | Uso de transmissor de alta potencia para bloquear comunicacao na faixa 2.4GHz (Wi-Fi + Zigbee) ou 915MHz (LoRa) |
| **Dificuldade** | Baixa a media. Jammers de 2.4GHz sao baratos (R$100-500 no mercado paralelo) |
| **Efeito** | Todos os sensores Zigbee ficam offline, cameras Wi-Fi perdem conexao, servidor perde comunicacao com dispositivos |
| **Deteccao** | Perda simultanea de multiplos dispositivos e indicador forte de jamming |
| **Adversarios tipicos** | ADV-02 (ladrao experiente), ADV-03 (quadrilha organizada) |
| **Cenarios mais vulneraveis** | Rural (maior distancia, jammer pode ser posicionado longe), Urbano (proximidade facilita) |

**Cadeia de ataque tipica:**
1. Adversario posiciona jammer de 2.4GHz proximo a residencia
2. Todos os sensores Zigbee e cameras Wi-Fi ficam offline
3. Sem sensores, o Alarmo nao detecta abertura de portas/janelas
4. Sem cameras, o Frigate nao detecta intrusos
5. Adversario invade a propriedade sem acionar alertas

### 5.2 Corte de Energia

| Aspecto | Detalhe |
|---------|---------|
| **Descricao** | Desligar disjuntor externo ou cortar cabos de alimentacao |
| **Dificuldade** | Muito baixa. Quadro de energia frequentemente acessivel sem ferramentas |
| **Efeito** | Servidor desliga, cameras PoE desligam, switch desliga, roteador desliga. Sensores Zigbee com bateria continuam, mas sem coordenador |
| **Deteccao** | Sensor de queda de energia no nobreak, notificacao se sistema tiver 4G backup |
| **Adversarios tipicos** | ADV-02, ADV-03, ADV-04 |
| **Cenarios mais vulneraveis** | Rural (infraestrutura precaria), Urbano (quadro acessivel na fachada) |

**Cadeia de ataque tipica:**
1. Adversario desliga disjuntor geral na caixa de forca externa
2. Sem nobreak: sistema inteiro desliga instantaneamente
3. Com nobreak: autonomia de 30 minutos para invasao rapida
4. Cameras, servidor, roteador ficam sem energia
5. Notificacoes nao sao enviadas se roteador/internet tambem caem

### 5.3 Corte de Internet

| Aspecto | Detalhe |
|---------|---------|
| **Descricao** | Corte fisico do cabo de fibra/cobre da operadora ou sabotagem no ponto de entrada |
| **Dificuldade** | Baixa. Cabo geralmente acessivel na fachada da residencia |
| **Efeito** | Sistema continua funcionando localmente (deteccao, alarme, gravacao), mas notificacoes remotas nao sao enviadas |
| **Deteccao** | Monitoramento de status de conexao, failover 4G |
| **Adversarios tipicos** | ADV-02, ADV-03 |
| **Cenarios mais vulneraveis** | Todos, especialmente Rural (unico provedor) |

**Cadeia de ataque tipica:**
1. Adversario corta cabo de internet na fachada
2. Sistema local continua operando (sensores, alarme local, gravacao)
3. Notificacoes por push/SMS/Telegram nao chegam ao proprietario
4. Proprietario nao sabe que invasao esta em andamento (se estiver fora)
5. Resposta atrasada ate que alguem perceba fisicamente

### 5.4 Tamper Fisico

| Aspecto | Detalhe |
|---------|---------|
| **Descricao** | Manipulacao fisica de sensores, cameras ou equipamentos (cobrir, mover, destruir, arrancar) |
| **Dificuldade** | Muito baixa para sensores externos; media para equipamentos internos |
| **Efeito** | Zona sem monitoramento, falso senso de seguranca |
| **Deteccao** | Sensores com funcao anti-tamper, monitoramento de "ultimo contato" de cada dispositivo |
| **Adversarios tipicos** | ADV-02, ADV-03, ADV-04 |
| **Cenarios mais vulneraveis** | Rural (equipamentos remotos e desprotegidos), Urbano (cameras externas) |

### 5.5 Firmware Comprometido

| Aspecto | Detalhe |
|---------|---------|
| **Descricao** | Firmware de camera IP ou sensor com backdoor do fabricante ou modificado por atacante |
| **Dificuldade** | Alta (instalar firmware malicioso), Baixa (explorar backdoor existente) |
| **Efeito** | Acesso remoto nao autorizado, exfiltracao de dados, desabilitacao de funcoes |
| **Deteccao** | Verificacao de hash de firmware, monitoramento de trafego de rede anomalo |
| **Adversarios tipicos** | ADV-05 (hacker remoto) |
| **Cenarios mais vulneraveis** | Todos (cameras IP de fabricantes chineses tem historico de CVEs) |

**CVEs relevantes:**
- **CVE-2021-36260** (Hikvision): Command injection via HTTP, permite RCE
- **CVE-2023-28808** (Hikvision): Bypass de autenticacao em ONVIF
- **CVE-2021-44228** (Log4j): Afeta sistemas que usam Java para integracao

### 5.6 Credential Stuffing

| Aspecto | Detalhe |
|---------|---------|
| **Descricao** | Uso de listas de credenciais vazadas para tentar login no Home Assistant ou cameras |
| **Dificuldade** | Baixa (ferramentas automatizadas, listas publicas) |
| **Efeito** | Acesso total ao sistema de seguranca, capacidade de desarmar alarme |
| **Deteccao** | Rate limiting, monitoramento de tentativas de login, alerta de login de IP desconhecido |
| **Adversarios tipicos** | ADV-05 |
| **Cenarios mais vulneraveis** | Todos onde o HA estiver acessivel remotamente sem VPN |

### 5.7 Shoulder Surfing

| Aspecto | Detalhe |
|---------|---------|
| **Descricao** | Observacao visual do codigo de alarme quando digitado no teclado/painel |
| **Dificuldade** | Muito baixa |
| **Efeito** | Adversario conhece o codigo de desarme do alarme |
| **Deteccao** | Dificil de detectar; logs de desarmamento mostram uso normal |
| **Adversarios tipicos** | ADV-02, ADV-04 |
| **Cenarios mais vulneraveis** | Urbano (teclado perto do portao, vizinhos proximos), Apartamento (corredor compartilhado) |

### 5.8 Engenharia Social

| Aspecto | Detalhe |
|---------|---------|
| **Descricao** | Manipulacao de pessoas para obter acesso, informacoes ou desabilitar seguranca |
| **Dificuldade** | Baixa a media |
| **Efeito** | Acesso fisico autorizado por engano, obtencao de codigos, informacoes sobre rotinas |
| **Deteccao** | Treinamento de moradores e funcionarios, verificacao de identidade |
| **Adversarios tipicos** | ADV-03, ADV-04 |
| **Cenarios mais vulneraveis** | Apartamento (portaria), Urbano (empregados domesticos) |

**Tecnicas comuns:**
- Fingir ser entregador, tecnico de manutencao ou funcionario da operadora
- Pedir para porteiro "liberar" acesso porque "esqueceu a chave"
- Empregado domestico informa rotinas e layout a terceiros
- Falsa emergencia (bombeiros, vazamento) para acessar residencia

---

## 6. Mapeamento: Ameaca, Defesa Existente e Gap

### 6.1 Sensores Zigbee

| ID | Ameaca | Defesa existente no projeto | Gap identificado |
|----|--------|----------------------------|------------------|
| ZB-01 | Jamming 2.4GHz | Comunicacao LoRa como redundancia (drones) | Sensores Zigbee nao tem canal alternativo; perda total em jamming 2.4GHz |
| ZB-02 | Replay de mensagens | Criptografia AES-128 do Zigbee 3.0 | AES-128 protege, mas chave compartilhada na rede; replay com chave capturada durante join e possivel |
| ZB-03 | Tamper fisico | Nao especificado | Nenhum requisito de sensores com anti-tamper definido |
| ZB-04 | Sensor offline nao detectado | Nao especificado | Sem monitoramento de "ultimo contato" / heartbeat |
| ZB-05 | Captura de chave durante pairing | Zigbee 3.0 com Install Code | Nao especificado se Install Code e obrigatorio; pairing aberto expoe chave |
| ZB-06 | Esgotamento de bateria por flood | Nao especificado | Sem deteccao de taxa anomala de mensagens |

### 6.2 Cameras IP

| ID | Ameaca | Defesa existente no projeto | Gap identificado |
|----|--------|----------------------------|------------------|
| CAM-01 | Firmware com backdoor | VLAN isolada sem internet | Camera nao acessa internet, mas backdoor pode agir na rede interna |
| CAM-02 | Credenciais RTSP padrao | Checklist de seguranca (alterar senhas) | Sem verificacao automatizada de que senhas foram alteradas |
| CAM-03 | Corte de cabo PoE | Nao especificado | Sem protecao fisica do cabeamento PoE |
| CAM-04 | Tamper fisico | Posicionamento elevado (diagrama) | Sem sensor de tamper ou acelerometro na camera |
| CAM-05 | Injecao de stream falso | VLAN isolada | Possivel dentro da mesma VLAN; sem verificacao de integridade do stream |
| CAM-06 | CVE nao corrigido | Checklist (atualizar firmware) | Sem processo automatizado de verificacao de CVEs |

### 6.3 Servidor Central (Mini PC N100)

| ID | Ameaca | Defesa existente no projeto | Gap identificado |
|----|--------|----------------------------|------------------|
| SRV-01 | Corte de energia | Nobreak com 30 min de autonomia | 30 min pode ser insuficiente; sem alerta proativo de queda de energia externa |
| SRV-02 | Credenciais fracas no HA | 2FA recomendado | 2FA nao e obrigatorio; sem politica de complexidade de senha |
| SRV-03 | Secrets.yaml exposto | Gestao de secrets do HA | Sem criptografia do disco; acesso fisico permite leitura |
| SRV-04 | Disco cheio (gravacoes) | Rotacao de gravacoes no Frigate | Sem alerta proativo de espaco em disco baixo |
| SRV-05 | Acesso fisico nao autorizado | Nao especificado | Sem travamento fisico do servidor; sem FDE (Full Disk Encryption) |
| SRV-06 | Add-on vulneravel no HA | Nao especificado | Sem politica de avaliacao de seguranca de add-ons/HACS |

### 6.4 Rede Wi-Fi

| ID | Ameaca | Defesa existente no projeto | Gap identificado |
|----|--------|----------------------------|------------------|
| NET-01 | Jamming 2.4/5GHz | LoRa como fallback (drones) | Fallback LoRa e apenas para drones; sistema principal nao tem redundancia RF |
| NET-02 | Deauth attack | WPA3 recomendado | WPA3 previne deauth, mas nao e obrigatorio; muitos dispositivos IoT nao suportam WPA3 |
| NET-03 | Rogue AP | VLAN de gestao separada | Sem deteccao de AP falso (Wireless IDS) |
| NET-04 | MQTT sem TLS | Nao especificado | Comunicacao MQTT interna pode estar em texto plano |
| NET-05 | Corte de internet | 4G como failover (opcional) | 4G failover e "opcional"; nao ha requisito obrigatorio |
| NET-06 | Firmware de roteador vulneravel | Nao especificado | Sem processo de atualizacao de firmware do roteador |

### 6.5 Comunicacao LoRa/Meshtastic

| ID | Ameaca | Defesa existente no projeto | Gap identificado |
|----|--------|----------------------------|------------------|
| LORA-01 | Mensagens falsas injetadas | Criptografia end-to-end (REGRA-DRONE-08) | Meshtastic usa criptografia, mas chaves pre-compartilhadas podem ser comprometidas |
| LORA-02 | Jamming 915MHz | Fallback para modo autonomo (drones) | Gateway LoRa nao tem redundancia; se jammado, drones ficam isolados |
| LORA-03 | Mensagens nao assinadas | Nao especificado | Sem assinatura digital individual por mensagem |

### 6.6 Drones Autonomos

| ID | Ameaca | Defesa existente no projeto | Gap identificado |
|----|--------|----------------------------|------------------|
| DRN-01 | GPS spoofing | GPS RTK para precisao | RTK melhora precisao mas nao previne spoofing; sem verificacao de plausibilidade |
| DRN-02 | Captura fisica | Modo fail-safe (retorno a base) | Drone terrestre lento pode ser alcancado; sem mecanismo de auto-destruicao de dados |
| DRN-03 | Interceptacao de video | Wi-Fi 5GHz como canal principal | Stream via Wi-Fi pode ser capturado; sem criptografia E2E no stream de video |
| DRN-04 | Firmware adulterado | Assinatura digital de firmware (REGRA-DRONE-07) | Defesa adequada; gap menor: processo de verificacao automatica no boot |
| DRN-05 | Adversarial attacks na IA | Nao especificado | Sem teste de robustez adversarial nos modelos de deteccao |
| DRN-06 | Perda de comunicacao | Matriz de redundancia (Wi-Fi > LoRa > autonomo) | Defesa adequada para cenario basico |

### 6.7 Modulo de Defesa Nao Letal

| ID | Ameaca | Defesa existente no projeto | Gap identificado |
|----|--------|----------------------------|------------------|
| DEF-01 | Disparo nao autorizado | 2FA, autenticacao em 2 niveis, protocolo de disparo | Defesa robusta; gap menor: teste periodico de integridade do protocolo |
| DEF-02 | Registro de disparo adulterado | Hash SHA-256, blockchain local opcional | Blockchain "opcional"; sem garantia de imutabilidade obrigatoria |
| DEF-03 | Disparo contra inocente | Aviso sonoro (3s), sinal visual, IA confirma ameaca | Falso positivo da IA pode causar disparo indevido; sem taxa de confianca minima definida |
| DEF-04 | Uso indevido por morador | Modos de operacao com diferentes autorizacoes | Sem log de quem autorizou cada disparo em modo semi-automatico |

### 6.8 Home Assistant + Alarmo

| ID | Ameaca | Defesa existente no projeto | Gap identificado |
|----|--------|----------------------------|------------------|
| HA-01 | Login nao autorizado | 2FA recomendado | 2FA nao obrigatorio; sem bloqueio apos N tentativas |
| HA-02 | API exposta na internet | VPN obrigatoria, nunca port forwarding | Defesa adequada se implementada; gap: sem validacao automatica |
| HA-03 | Automacao desabilitada por insider | Nao especificado | Sem alerta quando automacao critica de seguranca e desabilitada |
| HA-04 | HACS com componente malicioso | Nao especificado | Sem politica de whitelisting de componentes customizados |
| HA-05 | Crash do HA deixa sistema offline | Nao especificado | Sem watchdog externo ao HA para monitorar disponibilidade |

### 6.9 Frigate NVR

| ID | Ameaca | Defesa existente no projeto | Gap identificado |
|----|--------|----------------------------|------------------|
| FRG-01 | Gravacoes deletadas | Rotacao automatica com retencao | Sem backup offsite de eventos criticos |
| FRG-02 | Acesso nao autorizado a gravacoes | VLAN de gestao, autenticacao HA | Sem controle de acesso granular (quem pode ver quais cameras) |
| FRG-03 | Modelo de IA enganado | Nao especificado | Sem mecanismo de deteccao de adversarial examples |
| FRG-04 | Container Docker comprometido | Nao especificado | Sem hardening do container (AppArmor, seccomp, read-only fs) |

---

## 7. Nivel de Sofisticacao que o Sistema Pretende Resistir

### 7.1 Definicao de niveis

O sistema define quatro niveis de sofisticacao de ataque. A meta do projeto e oferecer **protecao completa ate o Nivel 2** e **protecao parcial no Nivel 3**. O Nivel 4 esta **fora do escopo** deste projeto.

| Nivel | Descricao | Adversarios correspondentes | Objetivo do sistema |
|-------|-----------|----------------------------|---------------------|
| **Nivel 1: Ataque oportunista** | Sem planejamento, sem ferramentas, reage ao primeiro sinal de alarme | ADV-01 (oportunista casual) | **Protecao completa**: deteccao, alerta, dissuasao eficaz |
| **Nivel 2: Ataque planejado simples** | Reconhecimento previo, ferramentas basicas, corte de energia, tamper fisico simples | ADV-02 (ladrao experiente), ADV-04 (insider basico) | **Protecao completa**: redundancia de energia e comunicacao, anti-tamper, logs de auditoria |
| **Nivel 3: Ataque planejado avancado** | Jammers RF, corte combinado (energia + internet), multiplos atacantes, insider com acesso privilegiado | ADV-03 (quadrilha organizada), ADV-04 (insider avancado), ADV-05 (hacker remoto) | **Protecao parcial**: deteccao de jamming, failover 4G, drones autonomos, alertas LoRa. Nao garante prevencao total |
| **Nivel 4: Ataque com recursos estatais** | Acesso a exploits zero-day, vigilancia avancada, recursos ilimitados | Agencias governamentais, crime organizado de alto nivel | **Fora do escopo**: nenhum sistema residencial DIY resiste a este nivel |

### 7.2 O que cada nivel garante

#### Nivel 1 -- Protecao completa

- [x] Deteccao de intrusao em menos de 5 segundos
- [x] Acionamento de sirene local (90-110dB)
- [x] Notificacao instantanea ao proprietario
- [x] Gravacao de video do evento
- [x] Iluminacao reativa
- [x] Dissuasao efetiva (oportunista foge)

#### Nivel 2 -- Protecao completa

- [x] Tudo do Nivel 1
- [x] Nobreak com autonomia minima de 30 minutos
- [x] Sensores com anti-tamper
- [x] Cameras com posicionamento resistente a vandalo
- [x] 4G failover para notificacoes
- [x] Logs de auditoria para detectar insider
- [x] Codigos individuais por usuario no alarme
- [x] Cameras PoE (mais resistentes que Wi-Fi)

#### Nivel 3 -- Protecao parcial

- [x] Tudo do Nivel 2
- [x] Deteccao de jamming RF (perda simultanea de multiplos sensores)
- [x] Comunicacao LoRa como canal alternativo
- [x] Drones autonomos para vigilancia de perimetro
- [x] Modulo de defesa nao letal (onde legal)
- [ ] **NAO garante** prevencao de invasao por quadrilha armada
- [ ] **NAO garante** funcionamento de 100% dos sensores sob jamming
- [ ] **NAO garante** resistencia a insider com acesso root ao servidor

### 7.3 Limitacoes explicitas

| Limitacao | Justificativa |
|-----------|---------------|
| Nao substitui seguranca profissional 24/7 | Sistema DIY sem monitoramento humano constante |
| Nao resiste a ataque armado direto | Sistema de seguranca residencial, nao militar |
| Nao garante integridade sob jamming 2.4GHz total | Zigbee e Wi-Fi compartilham a faixa; LoRa e parcial |
| Nao previne engenharia social | Depende de treinamento humano, nao de tecnologia |
| Nao protege contra zero-day em cameras IP | Dependencia de firmware de terceiros |
| Drones nao operam em condicoes climaticas severas | Chuva forte, ventos acima de 40km/h |

---

## 8. Recomendacoes de Mitigacao por Gap

### 8.1 Prioridade Critica (implementar imediatamente)

| ID Gap | Gap | Mitigacao recomendada | Custo estimado | Complexidade |
|--------|-----|----------------------|----------------|--------------|
| NET-05 | 4G failover opcional | **Tornar 4G failover obrigatorio** em todos os cenarios. Usar modem 4G com SIM pre-pago conectado ao roteador. Configurar failover automatico | R$150-300 (modem) + R$20/mes | Baixa |
| SRV-02 | 2FA nao obrigatorio | **Tornar 2FA obrigatorio** para todos os usuarios do Home Assistant. Usar TOTP (Google Authenticator, Authy) | R$0 | Baixa |
| ZB-01 | Sensores sem redundancia RF | **Implementar deteccao de jamming**: automacao que detecta perda simultanea de 3+ sensores Zigbee e dispara alerta via LoRa/4G. Tratar como alerta de invasao | R$0 (software) | Media |
| SRV-05 | Sem FDE no servidor | **Habilitar Full Disk Encryption** (LUKS no Linux). Protege secrets.yaml e gravacoes em caso de roubo do servidor | R$0 | Media |
| HA-01 | Sem bloqueio de login | **Configurar ip_bans.yaml** no HA: bloquear IP apos 5 tentativas falhas. Configurar notificacao de login falho | R$0 | Baixa |

### 8.2 Prioridade Alta (implementar em 30 dias)

| ID Gap | Gap | Mitigacao recomendada | Custo estimado | Complexidade |
|--------|-----|----------------------|----------------|--------------|
| ZB-03 | Sem sensores anti-tamper | **Exigir sensores com funcao anti-tamper** na especificacao. Aqara e Sonoff possuem; configurar alerta para evento tamper | R$0 (trocar se necessario) | Baixa |
| ZB-04 | Sem monitoramento de heartbeat | **Criar automacao de monitoramento** de "last_seen" para cada sensor. Alertar se sensor nao reportar em 60 minutos | R$0 | Media |
| CAM-03 | Cabo PoE desprotegido | **Usar conduites** para cabeamento externo. Fixar cabos em areas inacessiveis. Usar cameras com armazenamento em SD como fallback | R$50-200 | Media |
| CAM-06 | Sem processo de CVE | **Implementar verificacao trimestral** de CVEs para modelos de cameras utilizados. Assinar newsletters de seguranca dos fabricantes | R$0 | Baixa |
| NET-04 | MQTT sem TLS | **Configurar MQTT com TLS** no Mosquitto. Gerar certificados autoassinados para comunicacao interna | R$0 | Media |
| HA-03 | Automacao critica desabilitavel | **Criar automacao watchdog** que verifica a cada 5 minutos se automacoes criticas de seguranca estao habilitadas. Alertar se desabilitadas | R$0 | Media |
| HA-05 | Sem watchdog externo | **Implementar script de monitoramento** externo (cron job ou systemd timer) que verifica status do HA via API e reinicia se necessario | R$0 | Media |
| DEF-02 | Blockchain de registro opcional | **Tornar registro imutavel obrigatorio**. Usar hash chain (SHA-256 encadeado) no minimo; blockchain local como melhoria | R$0 | Alta |

### 8.3 Prioridade Media (implementar em 90 dias)

| ID Gap | Gap | Mitigacao recomendada | Custo estimado | Complexidade |
|--------|-----|----------------------|----------------|--------------|
| ZB-05 | Pairing aberto expoe chave | **Usar Zigbee Install Code** para pairing de novos dispositivos. Desabilitar permit_join apos inclusao | R$0 | Media |
| CAM-01 | Backdoor na rede interna | **Monitorar trafego de rede** das cameras com ferramenta como ntopng ou Suricata. Alertar para trafego anomalo (conexoes nao-RTSP) | R$0 (software open source) | Alta |
| CAM-05 | Sem verificacao de integridade de stream | **Implementar watermark digital** no stream ou verificar hash de frames periodicamente (pesquisa necessaria) | R$0 | Alta |
| NET-03 | Sem deteccao de Rogue AP | **Configurar WIDS** (Wireless Intrusion Detection) ou usar AP com funcao de deteccao de rogue (Ubiquiti, MikroTik) | R$0-800 | Alta |
| DRN-01 | GPS spoofing nao detectado | **Implementar verificacao de plausibilidade GPS**: comparar posicao GPS com IMU dead reckoning. Alertar para divergencias | R$0 | Alta |
| DRN-03 | Stream de video sem E2E | **Implementar criptografia E2E** no stream de video dos drones usando WireGuard tunnel ou SRTP | R$0 | Alta |
| FRG-01 | Sem backup offsite | **Configurar backup automatico** de eventos criticos (marcados) para armazenamento externo (NAS, disco USB separado) | R$200-500 (disco externo) | Media |
| FRG-04 | Container Docker sem hardening | **Aplicar AppArmor/seccomp** ao container do Frigate. Configurar filesystem read-only onde possivel. Limitar capabilities | R$0 | Alta |
| SRV-06 | Sem avaliacao de add-ons | **Criar checklist de seguranca** para avaliacao de add-ons e HACS: verificar reputacao, reviews, codigo fonte, permissoes | R$0 | Baixa |

### 8.4 Prioridade Baixa (implementar em 180 dias)

| ID Gap | Gap | Mitigacao recomendada | Custo estimado | Complexidade |
|--------|-----|----------------------|----------------|--------------|
| DRN-05 | Sem teste adversarial da IA | **Realizar testes de robustez adversarial** nos modelos YOLO utilizados. Testar com adversarial patches impressos | R$0 | Muito alta |
| DEF-03 | Sem taxa de confianca minima | **Definir threshold de confianca** minimo (ex: 85%) para que o sistema de defesa seja ativado. Nunca disparar com confianca <70% | R$0 | Media |
| LORA-03 | Mensagens sem assinatura digital | **Implementar assinatura Ed25519** por mensagem LoRa (overhead aceitavel) | R$0 | Alta |
| FRG-02 | Sem controle de acesso granular | **Configurar usuarios com permissoes diferentes** no HA: usuario de monitoramento (somente leitura) vs. administrador | R$0 | Media |
| NET-06 | Firmware de roteador desatualizado | **Agendar verificacao trimestral** de firmware do roteador. Considerar OpenWrt para maior controle | R$0 | Media |
| CAM-04 | Sem sensor de tamper em camera | **Adicionar acelerometro externo** (Zigbee) fixado na camera para detectar movimento/remocao | R$30-60 por camera | Media |
| ZB-06 | Sem deteccao de flood | **Monitorar taxa de mensagens** por sensor no Zigbee2MQTT. Alertar para taxa anomala (>10 msg/min para sensor de abertura) | R$0 | Media |

---

## 9. Matriz de Risco Consolidada

### 9.1 Mapa de calor por cenario

```
                    IMPACTO
                Baixo  Medio  Alto  Critico
              +-------+------+------+--------+
    Alta      |       | R:05 | R:01 | R:02   |
              |       | U:07 | U:01 | U:08   |
              |       |      | R:06 |        |
 P  +-------+------+------+--------+
 R  Media     | A:07 | U:05 | R:04 | R:03   |
 O            |      | R:08 | U:02 | U:06   |
 B            |      | A:04 | U:04 |        |
 A            |      |      | A:02 |        |
 B  +-------+------+------+--------+
 .  Baixa     |      | A:06 | A:03 | A:01   |
              |      |      | A:05 |        |
              |      |      | R:07 |        |
              +-------+------+------+--------+

Legenda:
  R:XX = Rural, vetor XX da secao 3.1
  U:XX = Urbano, vetor XX da secao 3.2
  A:XX = Apartamento, vetor XX da secao 3.3
```

### 9.2 Top 10 riscos priorizados (todos os cenarios)

| Prioridade | Risco | Cenarios | Nivel de sofisticacao | Gap critico |
|------------|-------|----------|-----------------------|-------------|
| 1 | Corte combinado energia + internet + jamming RF | Rural, Urbano | Nivel 3 | NET-05, ZB-01, SRV-01 |
| 2 | Login nao autorizado no Home Assistant (remoto) | Todos | Nivel 2-3 | SRV-02, HA-01 |
| 3 | Insider com conhecimento do sistema | Urbano, Apartamento | Nivel 2 | HA-03, ZB-04 |
| 4 | Camera IP com firmware comprometido (CVE) | Todos | Nivel 3 | CAM-01, CAM-06 |
| 5 | Perimetro rural com cobertura insuficiente | Rural | Nivel 1-2 | ZB-01 (alcance) |
| 6 | Engenharia social na portaria | Apartamento | Nivel 2 | Fora do escopo tecnico |
| 7 | Tamper fisico em sensores e cameras externos | Rural, Urbano | Nivel 2 | ZB-03, CAM-04 |
| 8 | Gravacoes perdidas/corrompidas sem backup | Todos | Nivel 2 | FRG-01 |
| 9 | MQTT sem criptografia na rede interna | Todos | Nivel 3 | NET-04 |
| 10 | Disparo indevido do modulo de defesa | Rural | Nivel 2-3 | DEF-03 |

### 9.3 Acoes imediatas (Quick Wins)

Acoes que podem ser implementadas em menos de 1 dia com custo zero:

1. Habilitar 2FA no Home Assistant para todos os usuarios
2. Configurar `ip_bans.yaml` com bloqueio apos 5 tentativas
3. Verificar e alterar senhas padrao de todas as cameras
4. Desabilitar `permit_join` no Zigbee2MQTT
5. Configurar alerta de "sensor offline" para todos os sensores Zigbee
6. Verificar se MQTT usa TLS (se nao, agendar migracao)
7. Criar automacao de deteccao de jamming (perda simultanea de 3+ sensores)
8. Verificar se cameras nao tem rota para internet na VLAN
9. Fazer backup da configuracao do Home Assistant
10. Documentar codigos de alarme atribuidos a cada usuario

---

## 10. Referencias

### Frameworks e metodologias

- [Microsoft STRIDE Threat Model](https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats)
- [OWASP IoT Top 10](https://owasp.org/www-project-internet-of-things/)
- [OWASP Threat Modeling](https://owasp.org/www-community/Threat_Modeling)
- [NIST SP 800-154: Guide to Data-Centric System Threat Modeling](https://csrc.nist.gov/pubs/sp/800/154/ipd)

### Vulnerabilidades conhecidas em IoT

- [CVE-2021-36260 - Hikvision Command Injection](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-36260)
- [CVE-2023-28808 - Hikvision ONVIF Auth Bypass](https://www.hikvision.com/en/support/cybersecurity/security-advisory/security-notification-for-access-control-and-intercom-products/)
- [Zigbee Security Analysis - IEEE](https://ieeexplore.ieee.org/document/8115749)
- [LoRa Security - Butun et al.](https://www.mdpi.com/1424-8220/20/15/4273)

### Seguranca em Home Assistant

- [Home Assistant Security Architecture](https://www.home-assistant.io/docs/authentication/)
- [Home Assistant IP Bans](https://www.home-assistant.io/integrations/http/#ip-filtering-and-banning)
- [Frigate Security Best Practices](https://docs.frigate.video/)

### Seguranca em drones

- [GPS Spoofing Attacks on Drones - Kerns et al.](https://dl.acm.org/doi/10.1145/2508859.2516722)
- [Adversarial Attacks on Object Detection - Goodfellow et al.](https://arxiv.org/abs/1412.6572)
- [ANAC - Regulamento de Drones (RBAC-E 94)](https://www.gov.br/anac/pt-br/assuntos/drones)

### Documentos relacionados do projeto

- `docs/ARQUITETURA_TECNICA.md` -- Arquitetura de hardware, software e rede
- `docs/ARQUITETURA_SEGURANCA_FISICA.md` -- Defesa em profundidade e camadas fisicas
- `docs/ARQUITETURA_DRONES_AUTONOMOS.md` -- Drones, IA e modulo de defesa
- `rules/RULES_TECHNICAL.md` -- Regras tecnicas e boas praticas
- `PROJECT_OVERVIEW.md` -- Visao geral do projeto

---

> **Proximos passos**:
> - Implementar as acoes da secao 8.1 (Prioridade Critica) imediatamente
> - Criar tarefas no backlog para cada gap identificado
> - Revisar este documento a cada 6 meses ou quando houver mudanca significativa na arquitetura
> - Realizar testes de penetracao nos componentes criticos apos implementacao
>
> **Responsavel**: Equipe de seguranca do projeto
>
> **Revisao**: Este documento deve ser revisado e atualizado conforme novos componentes forem adicionados ou novas vulnerabilidades forem descobertas.
