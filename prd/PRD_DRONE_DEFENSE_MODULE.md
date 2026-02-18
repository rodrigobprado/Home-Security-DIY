# PRD -- Modulo de Defesa Nao Letal para Drones

> Sistema de Home Security -- Open Source / Open Hardware
>
> Modulo Reativo Avancado -- Sistema de Defesa
>
> Versao: 1.0 | Data: 2026-02-18 | Responsavel: Agente_Arquiteto_Drones

---

## 1. Visao geral

- **Nome do produto/funcionalidade**: Modulo de Defesa Nao Letal para Drones (UGV/UAV)
- **Responsavel**: Agente_Arquiteto_Drones
- **Data**: 2026-02-18
- **PRDs relacionados**: PRD_AUTONOMOUS_DRONES, PRD_DRONE_AI_VISION, PRD_DRONE_COMMUNICATION, PRD_DRONE_FLEET_MANAGEMENT

---

## 2. Problema e oportunidade

### 2.1 Problema

Sistemas de seguranca residencial tradicionais dependem exclusivamente de deterrencia passiva (cameras, alarmes, sirenes) e da resposta de autoridades policiais, que no Brasil pode levar de 30 minutos a horas, especialmente em areas rurais. Durante esse intervalo:

- **Invasores experientes** ignoram alarmes sonoros sabendo que a resposta policial e lenta
- **Cameras** apenas documentam o crime, nao o impedem
- **Sistemas passivos** nao oferecem resposta proporcional e imediata
- **Propriedades rurais** estao particularmente vulneraveis pela distancia de delegacias
- **Nenhuma solucao DIY** oferece defesa ativa nao letal com controles de seguranca adequados

### 2.2 Oportunidade

Desenvolver um modulo de defesa nao letal que:

- **Escala a resposta** progressivamente: presenca, aviso sonoro/visual, disparo dissuasorio
- **Garante controle humano** em toda acao de forca (modo semi-automatico exclusivo)
- **Registra cada evento** com auditoria completa e imutavel
- **Protege inocentes** com deteccao de criancas e animais para bloqueio automatico de disparo
- **Respeita a legislacao** brasileira em todos os modos de operacao
- **Integra com Home Assistant** para controle centralizado e notificacoes

---

## 3. Publico-alvo

| Perfil | Descricao | Necessidades especificas |
|--------|-----------|--------------------------|
| **Proprietario rural** | Fazendas, chacaras, sitios | Defesa de perimetro extenso, resposta rapida sem depender de policia |
| **Proprietario urbano** | Casas com quintal e muro | Dissuasao ativa, escalonamento de resposta |
| **Operador do sistema** | Pessoa treinada e responsavel | Interface clara para autorizacao de disparo, feedback em tempo real |
| **Entusiasta DIY** | Construtor do sistema | Documentacao completa, componentes acessiveis, seguranca por design |

---

## 4. Requisitos funcionais

### 4.1 Niveis de resposta (Force Continuum)

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-001 | Nivel 0 - Presenca: drone se posiciona visivelmente e acompanha o alvo | Alta |
| RF-002 | Nivel 1 - Advertencia visual: strobes de alta intensidade e holofote direcionado ao alvo | Alta |
| RF-003 | Nivel 2 - Advertencia sonora: mensagens pre-gravadas ("Propriedade privada monitorada. Policia acionada.") e sirene | Alta |
| RF-004 | Nivel 3 - Intervencao ativa: disparo de agente dissuasorio CO2 + OC (pimenta) | Media |
| RF-005 | Escalonamento automatico dos niveis 0-2 conforme classificacao de ameaca pela IA | Alta |
| RF-006 | Nivel 3 requer confirmacao humana explicita obrigatoria (REGRA-DRONE-17/23) | Alta |

### 4.2 Sistema de disparo CO2 + OC

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-007 | Cilindro CO2 como propelente (12g ou 88g, descartavel ou recarregavel) | Alta |
| RF-008 | Capsulas de OC (Oleoresin Capsicum) + gengibre como agente dissuasorio | Alta |
| RF-009 | Valvula solenoide controlada eletronicamente para disparo | Alta |
| RF-010 | Alcance efetivo de 3 a 10 metros | Alta |
| RF-011 | Capacidade de 5-10 disparos por cilindro | Media |
| RF-012 | Mira laser classe 2 para alinhamento visual | Media |
| RF-013 | Camera dedicada no modulo de disparo para registro do alvo | Alta |
| RF-014 | Sensor de pressao no cilindro CO2 para monitorar carga restante | Media |

### 4.3 Autenticacao e autorizacao

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-015 | Autenticacao 2FA obrigatoria para armar o modulo (REGRA-DRONE-14) | Alta |
| RF-016 | Primeiro fator: autenticacao biometrica ou senha no app Home Assistant | Alta |
| RF-017 | Segundo fator: codigo PIN numerico de 6 digitos com validade temporal (TOTP) | Alta |
| RF-018 | Token criptografado com certificado do drone e timestamp para cada autorizacao | Alta |
| RF-019 | Timeout automatico: sistema desarma apos 60 segundos sem confirmacao de disparo | Alta |
| RF-020 | Revogacao remota imediata de autorizacao via app ou Home Assistant | Alta |
| RF-021 | Bloqueio do sistema apos 3 tentativas invalidas de autenticacao | Media |

### 4.4 Modos de operacao

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-022 | Modo DESATIVADO: modulo de defesa completamente desligado (rele fisico desconectado) | Alta |
| RF-023 | Modo STANDBY: pronto para armamento, requer 2FA para ativacao | Alta |
| RF-024 | Modo SEMI-AUTOMATICO: IA detecta e classifica ameaca, humano autoriza disparo via app | Alta |
| RF-025 | Modo AUTOMATICO: **PROIBIDO e REMOVIDO** (REGRA-DRONE-17/23) -- nao deve existir no firmware | Alta |
| RF-026 | Transicao entre modos registrada em log com timestamp e operador | Alta |
| RF-027 | Modo padrao ao ligar: DESATIVADO | Alta |

### 4.5 Protocolos de seguranca

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-028 | Aviso sonoro obrigatorio 5 segundos antes do disparo (REGRA-DRONE-16) | Alta |
| RF-029 | Aviso visual (laser de advertencia + strobe) simultaneo ao aviso sonoro | Alta |
| RF-030 | Cooldown obrigatorio de 30 segundos entre disparos | Alta |
| RF-031 | Limite maximo de 3 disparos por periodo de 24 horas | Alta |
| RF-032 | Zonas de exclusao (geofence) onde disparo e permanentemente bloqueado | Alta |
| RF-033 | Zonas de exclusao incluem: entradas de servico, calcada publica, areas comuns | Alta |
| RF-034 | Fail-safe: sistema desarma imediatamente em perda de comunicacao | Alta |
| RF-035 | Fail-safe: sistema desarma em bateria abaixo de 20% | Alta |
| RF-036 | Chave fisica (rele de hardware) que corta alimentacao do solenoide quando desarmado | Alta |

### 4.6 Deteccao de criancas e animais (REGRA-DRONE-24)

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-037 | Deteccao de criancas por modelo de classificacao etaria (proporcoes corporais + pose) | Alta |
| RF-038 | Deteccao de animais domesticos via YOLOv8 com classes de animais | Alta |
| RF-039 | Bloqueio automatico e irrevogavel de disparo quando criancas ou animais detectados | Alta |
| RF-040 | Bloqueio implementado em nivel de firmware (nao pode ser desabilitado por software) | Alta |
| RF-041 | Alerta ao operador quando bloqueio por crianca/animal e ativado | Alta |
| RF-042 | Registro do evento de bloqueio com imagem e classificacao | Media |

### 4.7 Auditoria e registro

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-043 | Registro completo de cada disparo: timestamp NTP, coordenadas GPS, operador, video | Alta |
| RF-044 | Gravacao em buffer circular: 30 segundos antes e 60 segundos apos cada disparo | Alta |
| RF-045 | Hash SHA-256 de cada registro para garantir integridade | Alta |
| RF-046 | Logs imutaveis (append-only) com cadeia de hash | Alta |
| RF-047 | Sincronizacao dos logs com Home Assistant via MQTT | Alta |
| RF-048 | Exportacao de logs em formato compativel com pericia (metadados completos) | Media |
| RF-049 | Notificacao imediata ao proprietario apos qualquer disparo | Alta |

### 4.8 Integracao com Home Assistant

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-050 | Card de defesa no dashboard com status em tempo real | Alta |
| RF-051 | Teclado numerico para PIN no card de autorizacao | Alta |
| RF-052 | Notificacao critica "Solicitacao de Intervencao" com botoes de acao | Alta |
| RF-053 | Historico de eventos de defesa no dashboard | Alta |
| RF-054 | Automacao de escalonamento: niveis 0-2 disparados por eventos do sistema de alarme | Media |
| RF-055 | Stream de video do modulo de disparo durante evento ativo | Alta |

---

## 5. Requisitos nao funcionais

### 5.1 Performance

| ID | Requisito | Especificacao |
|----|-----------|---------------|
| RNF-001 | Tempo de resposta do disparo apos confirmacao humana | < 500ms |
| RNF-002 | Tempo de aviso sonoro/visual pre-disparo | Exatamente 5 segundos |
| RNF-003 | Latencia da notificacao de solicitacao ao operador | < 2 segundos |
| RNF-004 | Taxa de deteccao de criancas | > 95% (falso negativo inaceitavel) |
| RNF-005 | Taxa de deteccao de animais | > 90% |
| RNF-006 | Tempo de classificacao de ameaca pela IA | < 1 segundo |

### 5.2 Seguranca

| ID | Requisito | Especificacao |
|----|-----------|---------------|
| RNF-007 | Criptografia de comunicacao de comandos de defesa | TLS 1.3 + mTLS |
| RNF-008 | Armazenamento de credenciais | Secure Element (ATECC608) ou TPM |
| RNF-009 | Integridade de firmware do modulo de defesa | Assinatura digital obrigatoria |
| RNF-010 | Isolamento do modulo de defesa | Microcontrolador dedicado separado do sistema principal |
| RNF-011 | Auditoria de acessos | Log de toda tentativa de autenticacao |
| RNF-012 | Protecao anti-tamper | Sensor de violacao fisica no modulo |

### 5.3 Confiabilidade

| ID | Requisito | Especificacao |
|----|-----------|---------------|
| RNF-013 | Temperatura de operacao do sistema CO2 | 0C a 45C |
| RNF-014 | Pressao de trabalho do cilindro | 50-60 bar |
| RNF-015 | Vida util do solenoide | > 100.000 ciclos |
| RNF-016 | MTBF do modulo completo | > 5.000 horas |
| RNF-017 | Protecao contra descarga acidental | Dupla trava (software + hardware) |

### 5.4 Conformidade legal

| ID | Requisito | Referencia |
|----|-----------|------------|
| RNF-018 | Modo automatico de disparo PROIBIDO | REGRA-DRONE-17, REGRA-DRONE-23 |
| RNF-019 | Deteccao de criancas/animais com bloqueio de disparo | REGRA-DRONE-24 |
| RNF-020 | Responsabilidade civil/criminal do proprietario documentada | REGRA-DRONE-25 |
| RNF-021 | 2FA obrigatoria para armamento | REGRA-DRONE-14 |
| RNF-022 | Registro de cada disparo com video, GPS, timestamp | REGRA-DRONE-15 |
| RNF-023 | Aviso sonoro/visual pre-disparo minimo 5 segundos | REGRA-DRONE-16 |
| RNF-024 | Verificar legislacao estadual sobre uso de spray OC | REGRA-DRONE-13 |
| RNF-025 | Uso exclusivamente em propriedade privada | REGRA-DRONE-12 |
| RNF-026 | LGPD: processamento local, sem envio para nuvem | Lei 13.709/2018 |

---

## 6. Arquitetura tecnica

### 6.1 Diagrama de componentes

```
+-----------------------------------------------------------------------+
|                     MODULO DE DEFESA NAO LETAL                        |
+-----------------------------------------------------------------------+
|                                                                       |
|  +------------------+    +-------------------+    +-----------------+ |
|  | MICROCONTROLADOR |    |  CAMERA DEDICADA  |    |  SENSOR PRESSAO | |
|  |    DEDICADO      |<---|  (registro alvo)  |    |  (cilindro CO2) | |
|  |   (ESP32-S3)     |    +-------------------+    +--------+--------+ |
|  +--------+---------+                                      |          |
|           |                                                |          |
|   +-------+--------+    +-------------------+    +--------+--------+ |
|   | SECURE ELEMENT  |    |  RELE DE          |    |  SENSOR         | |
|   | (ATECC608)      |    |  SEGURANCA        |--->|  ANTI-TAMPER    | |
|   +-----------------+    |  (trava hardware) |    +-----------------+ |
|                          +--------+----------+                        |
|                                   |                                   |
|   +-------------------+  +--------+----------+    +-----------------+ |
|   |  LASER CLASSE 2   |  |  SOLENOIDE 12V    |    |  ALTO-FALANTE   | |
|   |  (mira/advertencia)|  |  (valvula CO2)    |    |  SIRENE 110dB   | |
|   +-------------------+  +-------------------+    +-----------------+ |
|                                   |                                   |
|                          +--------+----------+                        |
|                          |  CILINDRO CO2     |                        |
|                          |  + CAPSULAS OC    |                        |
|                          +-------------------+                        |
+-----------------------------------------------------------------------+
        |                           |
        | Serial/USB                | MQTT
        v                           v
+------------------+        +------------------+
|  COMPUTADOR DE   |        |  HOME ASSISTANT  |
|  BORDO (RPi/Jetson)       |  (Estacao Base)  |
|  ROS2 /defense   |        |                  |
+------------------+        +------------------+
```

### 6.2 Fluxo de disparo seguro

```
1. IA detecta ameaca classificada como "alto risco"
        |
        v
2. Sistema verifica: criancas/animais detectados?
   +--> SIM: BLOQUEIO AUTOMATICO (firmware). Evento registrado. FIM.
   |
   +--> NAO: Continua
        |
        v
3. Escalonamento automatico: Niveis 0-2 (presenca, visual, sonoro)
        |
        v
4. Notificacao critica ao operador com stream de video
        |
        v
5. Operador avalia contexto em tempo real
   +--> NAO autoriza: Sistema mantem niveis 0-2. FIM.
   |
   +--> Autoriza: Operador autentica com 2FA (biometria + PIN)
        |
        v
6. Sistema verifica autenticacao (token + certificado + timestamp)
        |
        v
7. Verifica geofence (zona de exclusao?)
   +--> ZONA EXCLUSAO: Disparo bloqueado. Operador notificado. FIM.
   |
   +--> ZONA PERMITIDA: Continua
        |
        v
8. Aviso sonoro/visual: 5 segundos de advertencia
        |
        v
9. DISPARO executado
        |
        v
10. Registro completo: timestamp, GPS, video (30s antes + 60s depois),
    operador, hash SHA-256
        |
        v
11. Notificacao ao proprietario. Cooldown de 30 segundos.
```

### 6.3 Topicos ROS2

| Topico/Servico | Tipo | Descricao |
|----------------|------|-----------|
| `/defense/status` | custom_msgs/DefenseStatus | Status: idle, standby, armed, active, blocked |
| `/defense/arm` | std_srvs/SetBool | Armar/desarmar modulo (requer 2FA) |
| `/defense/fire` | custom_msgs/FireCommand | Comando de disparo (requer autorizacao) |
| `/defense/block_reason` | std_msgs/String | Razao do bloqueio (crianca, animal, zona_exclusao) |
| `/defense/audit_log` | custom_msgs/AuditEntry | Registro de auditoria |
| `/defense/pressure` | std_msgs/Float32 | Pressao do cilindro CO2 |
| `/defense/camera` | sensor_msgs/Image | Stream da camera do modulo |

### 6.4 Integracao MQTT com Home Assistant

| Topico MQTT | Direcao | Payload |
|-------------|---------|---------|
| `drone/{id}/defense/status` | Drone -> HA | JSON com status completo |
| `drone/{id}/defense/arm_request` | HA -> Drone | Solicitacao de armamento com token 2FA |
| `drone/{id}/defense/fire_authorize` | HA -> Drone | Autorizacao de disparo com credenciais |
| `drone/{id}/defense/disarm` | HA -> Drone | Desarmamento imediato |
| `drone/{id}/defense/event` | Drone -> HA | Evento de disparo com metadados |
| `drone/{id}/defense/block` | Drone -> HA | Notificacao de bloqueio |

---

## 7. Hardware e componentes recomendados

### 7.1 Modulo de controle

| Componente | Modelo | Preco estimado (R$) | Funcao |
|------------|--------|---------------------|--------|
| Microcontrolador dedicado | ESP32-S3 DevKit | R$ 50-80 | Controlador isolado do modulo |
| Secure Element | ATECC608A | R$ 30-50 | Armazenamento seguro de chaves |
| Rele de seguranca | Rele 12V com trava mecanica | R$ 20-40 | Trava fisica do solenoide |
| Sensor anti-tamper | Switch magnetico + acelerometro | R$ 15-25 | Deteccao de violacao |

### 7.2 Sistema de disparo

| Componente | Modelo | Preco estimado (R$) | Funcao |
|------------|--------|---------------------|--------|
| Cilindro CO2 88g | Crosman/Swiss Arms | R$ 30-60 | Propelente |
| Capsulas OC (x10) | Compativel com sistema | R$ 50-100 | Agente dissuasorio |
| Valvula solenoide 12V | Parker/SMC miniatura | R$ 80-150 | Controle de disparo |
| Camara de disparo | Aluminio anodizado custom | R$ 100-200 | Mecanismo principal |
| Sensor de pressao | XGZP6847D 0-60bar | R$ 40-80 | Monitoramento de carga |
| Laser classe 2 | Modulo 650nm 5mW | R$ 15-30 | Mira e advertencia |

### 7.3 Sistema de advertencia

| Componente | Modelo | Preco estimado (R$) | Funcao |
|------------|--------|---------------------|--------|
| Amplificador classe D | PAM8403 / MAX98357A | R$ 15-30 | Amplificacao de audio |
| Alto-falante sirene | Driver piezo 110dB | R$ 40-80 | Alerta sonoro |
| LED strobe 10W | LED Power branco 6500K | R$ 20-40 | Advertencia visual |
| Driver MOSFET | IRLZ44N + gate driver | R$ 10-20 | Controle de LED |

### 7.4 Camera e registro

| Componente | Modelo | Preco estimado (R$) | Funcao |
|------------|--------|---------------------|--------|
| Camera dedicada | OV2640 ou Pi Camera V3 | R$ 80-250 | Registro do alvo |
| Armazenamento | MicroSD 32GB classe 10 | R$ 30-50 | Buffer de video |

### 7.5 Estimativa de custo total do modulo

| Configuracao | Custo estimado |
|--------------|----------------|
| **Modulo basico (niveis 0-2 apenas)** | R$ 200-450 |
| **Modulo completo (niveis 0-3)** | R$ 600-1.250 |
| **Capsulas OC (reposicao, 10 unidades)** | R$ 50-100 |
| **Cilindro CO2 (reposicao)** | R$ 30-60 |

---

## 8. Criterios de aceitacao

| ID | Criterio | Metodo de verificacao |
|----|----------|----------------------|
| CA-001 | Modo automatico de disparo nao existe no firmware (REGRA-DRONE-17/23) | Revisao de codigo + teste de intrusao |
| CA-002 | 2FA funciona corretamente para armamento do modulo | Teste funcional com biometria + PIN |
| CA-003 | Bloqueio automatico funciona ao detectar crianca (REGRA-DRONE-24) | Teste com manequim de crianca em diferentes angulos |
| CA-004 | Bloqueio automatico funciona ao detectar animal domestico | Teste com diferentes tamanhos e especies |
| CA-005 | Bloqueio por crianca/animal nao pode ser desabilitado por software | Teste de intrusao no firmware |
| CA-006 | Aviso sonoro/visual ocorre exatamente 5 segundos antes do disparo | Teste com cronometro |
| CA-007 | Cooldown de 30 segundos e respeitado entre disparos | Teste funcional |
| CA-008 | Limite de 3 disparos em 24 horas e aplicado | Teste funcional em periodo de 24h |
| CA-009 | Zonas de exclusao bloqueiam disparo corretamente | Teste com geofence configurado |
| CA-010 | Fail-safe desarma em perda de comunicacao | Teste de interrupcao de sinal |
| CA-011 | Fail-safe desarma em bateria < 20% | Teste de descarga controlada |
| CA-012 | Log registra todos os eventos com hash SHA-256 | Verificacao de integridade dos logs |
| CA-013 | Video buffer grava 30s antes e 60s apos disparo | Teste de gravacao |
| CA-014 | Rele fisico desconecta solenoide quando modo DESATIVADO | Teste eletrico com multimetro |
| CA-015 | Disparo ocorre em menos de 500ms apos confirmacao | Teste de latencia |

---

## 9. Metricas de sucesso

| Metrica | Alvo | Medicao |
|---------|------|---------|
| **Taxa de bloqueio por crianca/animal** | 100% de deteccoes corretas bloqueiam disparo | Testes periodicos com cenarios simulados |
| **Taxa de falsos positivos de ameaca** | < 5% de alertas indevidos nos niveis 0-2 | Contagem semanal de alertas vs. ameacas reais |
| **Tempo medio de resposta do operador** | < 15 segundos da notificacao a decisao | Analise de logs de auditoria |
| **Disponibilidade do modulo** | > 99% em modo standby | Monitoramento continuo |
| **Integridade dos logs** | 100% de registros com hash valido | Verificacao mensal de cadeia de hash |
| **Conformidade legal** | Zero disparos sem autorizacao humana | Auditoria trimestral de logs |

---

## 10. Riscos e dependencias

### 10.1 Riscos

| Risco | Probabilidade | Impacto | Mitigacao |
|-------|---------------|---------|-----------|
| Falso positivo da IA causa disparo em inocente | Media | Critico | Confirmacao humana obrigatoria (REGRA-DRONE-23) + deteccao de criancas/animais |
| Legislacao estadual proibe spray OC | Media | Alto | Verificar legislacao local antes de implementar; modulo funciona sem nivel 3 |
| Falha do rele de seguranca permite disparo acidental | Baixa | Critico | Dupla trava (software + hardware) + testes periodicos |
| Vazamento de CO2 por defeito no cilindro | Baixa | Medio | Sensor de pressao + valvula de alivio + inspecao periodica |
| Operador autoriza disparo desproporcional | Media | Alto | Escala de forca documentada + treinamento + registro completo |
| Temperaturas extremas afetam pressao CO2 | Media | Medio | Sensor de temperatura + limites operacionais (0-45C) |
| Hacking do sistema de autorizacao | Baixa | Critico | Secure element, mTLS, firmware assinado, chave fisica |
| Processo judicial por uso do modulo | Media | Alto | Logs imutaveis como evidencia, seguro RETA, consultoria juridica previa |

### 10.2 Dependencias

| Dependencia | Tipo | PRD relacionado |
|-------------|------|-----------------|
| Sistema de IA e visao computacional | Funcional | PRD_DRONE_AI_VISION |
| Comunicacao redundante para autorizacao | Infraestrutura | PRD_DRONE_COMMUNICATION |
| Plataforma de drones autonomos | Base | PRD_AUTONOMOUS_DRONES |
| Home Assistant para interface de controle | Integracao | PRD_MONITORING_DASHBOARD |
| Gerenciamento de frota para coordenacao | Operacional | PRD_DRONE_FLEET_MANAGEMENT |

---

## 11. Referencias

### Documentos do projeto

- `docs/ARQUITETURA_DRONES_AUTONOMOS.md` -- Secao 3 (Sistema de Defesa Nao Letal)
- `rules/RULES_COMPLIANCE_AND_STANDARDS.md` -- REGRA-DRONE-11 a 25
- `standards/STANDARDS_TO_RESEARCH.md` -- Secao 8.4 (Legislacao de defesa nao letal)
- `prd/PRD_AUTONOMOUS_DRONES.md` -- Secao 4.7 (Modulo de defesa)

### Legislacao e regulamentacao

- [Codigo Civil Art. 927](https://www.planalto.gov.br/ccivil_03/leis/2002/l10406compilada.htm) -- Responsabilidade objetiva
- [Codigo Penal Art. 129](https://www.planalto.gov.br/ccivil_03/decreto-lei/del2848compilado.htm) -- Lesao corporal
- [Estatuto da Crianca e do Adolescente](https://www.planalto.gov.br/ccivil_03/leis/l8069.htm) -- Protecao de menores
- [Portaria MJSP 1.222/2019](https://www.gov.br/mj/pt-br) -- Classificacao de armas menos letais
- [LGPD - Lei 13.709/2018](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm)

### Externos

- [ATECC608 Datasheet](https://www.microchip.com/en-us/product/atecc608a)
- [ESP32-S3 Documentation](https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/)
- [ROS2 Security](https://design.ros2.org/articles/ros2_security_enclaves.html)

---

> **DISCLAIMER LEGAL**
>
> Este modulo e fornecido "como esta" (as-is), sem qualquer garantia de adequacao legal para qualquer jurisdicao especifica. Os desenvolvedores e contribuidores deste projeto open source NAO se responsabilizam por danos fisicos, morais ou materiais causados pelo uso do modulo de defesa, nem por consequencias legais decorrentes da instalacao ou operacao do sistema.
>
> O proprietario e o UNICO RESPONSAVEL por verificar a legalidade do uso em sua jurisdicao (municipio, estado e pais), obter todas as autorizacoes necessarias e operar o sistema de forma etica e legal (REGRA-DRONE-25).
>
> Recomenda-se fortemente consultar um advogado especializado antes de instalar ou operar o modulo de defesa.

---

> **Status**: Rascunho v1.0
>
> **Proxima revisao**: Apos validacao juridica e testes de prototipo
