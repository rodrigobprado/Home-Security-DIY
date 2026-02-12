# Normas, Compliance e Padrões – Sistema de Home Security

> Comentário: Este arquivo consolida normas e padrões relevantes para segurança residencial física e digital, com regras derivadas acionáveis.

> **Última atualização**: 2026-02-12 por Agente_Arquiteto_Drones (regras de drones REGRA-DRONE-01 a 22)

## Objetivo

Consolidar normas e padrões externos (internacionais, nacionais, setoriais) relevantes para o projeto de segurança residencial, traduzindo-os em regras concretas e acionáveis.

---

## 1. Proteção de dados pessoais (LGPD)

### 1.1 Aplicabilidade

A LGPD (Lei 13.709/2018) define imagens como **dados pessoais**. Portanto, câmeras de segurança estão sujeitas à lei.

**Exceção importante (Art. 4º, I)**: A LGPD **não se aplica** quando o tratamento é realizado por pessoa natural para fins **exclusivamente particulares e não econômicos**.

| Cenário | LGPD se aplica? | Motivo |
|---------|-----------------|--------|
| Câmera interna em residência | **Não** | Uso pessoal exclusivo |
| Câmera externa captando apenas quintal próprio | **Não** | Uso pessoal, área privada |
| Câmera captando via pública | **Sim** | Captura dados de terceiros |
| Câmera captando propriedade do vizinho | **Sim** | Viola privacidade de terceiros |
| Câmera em área comum de condomínio | **Sim** | Área compartilhada |
| Sistema com acesso de empresa de monitoramento | **Sim** | Compartilhamento com terceiros |

### 1.2 Regras obrigatórias quando LGPD se aplica

| Regra | Descrição | Implementação |
|-------|-----------|---------------|
| **Transparência** | Informar sobre monitoramento | Placas de aviso visíveis |
| **Finalidade** | Uso exclusivo para segurança | Documentar finalidade |
| **Necessidade** | Captar apenas áreas essenciais | Ajustar ângulos de câmera |
| **Retenção limitada** | Não manter dados além do necessário | Rotação automática (30 dias) |
| **Controle de acesso** | Acesso restrito a autorizados | Senhas, logs de acesso |
| **Segurança** | Proteger contra vazamento | Criptografia, armazenamento local |

### 1.3 Regras derivadas para o projeto

```
REGRA-LGPD-01: Toda câmera deve ter seu ângulo de captura documentado, indicando se capta apenas área privada ou também área pública/vizinhos.

REGRA-LGPD-02: Câmeras que captam via pública devem ter placa de aviso visível com: (a) indicação de monitoramento, (b) finalidade, (c) responsável.

REGRA-LGPD-03: Período de retenção padrão: 30 dias com rotação automática.

REGRA-LGPD-04: Acesso às gravações restrito ao proprietário. Qualquer acesso deve ser registrado em log.

REGRA-LGPD-05: Gravações não devem ser enviadas para nuvem de terceiros sem consentimento explícito.
```

---

## 2. Segurança da informação para IoT

### 2.1 OWASP IoT Top 10 – Regras derivadas

Baseado nas 10 principais vulnerabilidades em dispositivos IoT:

```
REGRA-IOT-01: NUNCA manter senhas padrão de fábrica. Alterar imediatamente após instalação.

REGRA-IOT-02: Desabilitar serviços de rede não utilizados (Telnet, FTP, UPnP).

REGRA-IOT-03: Dispositivos IoT NÃO devem ter acesso à internet, exceto quando estritamente necessário.

REGRA-IOT-04: Toda comunicação deve usar criptografia (HTTPS/TLS).

REGRA-IOT-05: Firmware deve ser atualizado regularmente (verificar mensalmente).

REGRA-IOT-06: Manter inventário documentado de todos os dispositivos IoT instalados.
```

### 2.2 ETSI EN 303 645 – Requisitos de segurança

Padrão europeu para segurança de IoT de consumo. Requisitos principais:

| Requisito | Descrição | Status no projeto |
|-----------|-----------|-------------------|
| Sem senhas padrão | Dispositivos não devem usar senhas universais | Obrigatório |
| Mecanismo de atualização | Possibilidade de atualizar firmware | Verificar na seleção |
| Comunicação segura | Criptografia em todas as comunicações | Obrigatório |
| Minimização de superfície de ataque | Desabilitar serviços desnecessários | Obrigatório |

---

## 3. Segurança física residencial

### 3.1 Cercas elétricas (Lei 13.477/2017 e NBR 15.401)

```
REGRA-CERCA-01: Altura mínima de instalação: 2,20m (verificar legislação municipal).

REGRA-CERCA-02: Primeiro fio energizado a no mínimo 1,80m do solo.

REGRA-CERCA-03: Sinalização obrigatória a cada 10 metros, em portões e mudanças de direção.

REGRA-CERCA-04: Instalação DEVE ser feita por profissional habilitado.

REGRA-CERCA-05: Voltagem e amperagem conforme especificação ABNT (não letal).

REGRA-CERCA-06: Integração com SPDA (proteção contra raios) quando aplicável.
```

### 3.2 Portas, janelas e vidros (NBR 10821, NBR 7199, NBR 15575)

```
REGRA-ESQUADRIA-01: Portas e janelas em pontos de entrada devem atender NBR 10821.

REGRA-ESQUADRIA-02: Vidros em áreas vulneráveis devem ser de segurança (laminado ou temperado) conforme NBR 7199.

REGRA-ESQUADRIA-03: Verificar desempenho conforme NBR 15575-4 (estanqueidade, resistência).
```

---

## 4. Videovigilância (CFTV)

### 4.1 Retenção de gravações

```
REGRA-CFTV-01: Período de retenção padrão: 30 dias.

REGRA-CFTV-02: Rotação automática (FIFO) para sobrescrever gravações antigas.

REGRA-CFTV-03: Mecanismo para preservar gravações de incidentes (flag "não sobrescrever").

REGRA-CFTV-04: Backup de gravações críticas em mídia separada.
```

### 4.2 Qualidade e cobertura

```
REGRA-CFTV-05: Resolução mínima: 1080p para identificação, 720p para monitoramento.

REGRA-CFTV-06: Visão noturna obrigatória para câmeras externas.

REGRA-CFTV-07: Cobertura obrigatória: todos os pontos de entrada/saída.

REGRA-CFTV-08: Manutenção preventiva: limpeza de lentes e verificação de conexões mensalmente.
```

### 4.3 Acesso e segurança

```
REGRA-CFTV-09: Acesso ao NVR/DVR protegido por senha forte.

REGRA-CFTV-10: Log de todos os acessos às gravações.

REGRA-CFTV-11: Acesso remoto APENAS via VPN, nunca exposição direta à internet.

REGRA-CFTV-12: Câmeras em VLAN separada, sem acesso à internet.
```

---

## 5. Instalações elétricas (NBR 5410, NBR 5419)

### 5.1 Proteção elétrica básica

```
REGRA-ELETRICA-01: DPS (Dispositivo de Proteção contra Surtos) obrigatório no quadro de distribuição.

REGRA-ELETRICA-02: Todos os equipamentos de segurança devem ser aterrados.

REGRA-ELETRICA-03: Dimensionamento de cabos conforme NBR 5410.

REGRA-ELETRICA-04: DR (Diferencial Residual) para proteção contra choques.
```

### 5.2 Proteção contra descargas atmosféricas

```
REGRA-SPDA-01: Avaliar necessidade de SPDA conforme NBR 5419 Parte 2 (gerenciamento de risco).

REGRA-SPDA-02: Sistemas eletrônicos sensíveis devem ter proteção conforme NBR 5419 Parte 4.

REGRA-SPDA-03: Equipotencialização entre sistemas de segurança e SPDA.
```

### 5.3 Continuidade operacional

```
REGRA-NOBREAK-01: Sistema central (NVR, hub de automação) deve ter nobreak com autonomia mínima de 30 minutos.

REGRA-NOBREAK-02: Alerta automático em caso de queda de energia.

REGRA-NOBREAK-03: Câmeras críticas devem ter alimentação PoE com switch em nobreak.
```

---

## 6. Fechaduras e controle de acesso

### 6.1 Fechaduras mecânicas (NBR 14913)

```
REGRA-FECHADURA-01: Portas de entrada principais devem ter fechadura de embutir com grau de segurança médio ou superior.

REGRA-FECHADURA-02: Fechaduras multiponto (3+ pontos de travamento) recomendadas para portas de entrada.

REGRA-FECHADURA-03: Cilindros devem ter classificação EN 1303 com segurança de chave grau 5 ou 6.

REGRA-FECHADURA-04: Cilindros devem ter resistência a ataque grau A ou superior (mínimo 3 min contra perfuração).

REGRA-FECHADURA-05: Protetor de cilindro (escudo) obrigatório em portas de entrada principais.
```

### 6.2 Fechaduras eletrônicas

```
REGRA-FECHADURA-06: Fechaduras eletrônicas devem ter chave física de backup obrigatória.

REGRA-FECHADURA-07: Fechaduras externas devem ter certificação IP65 ou superior.

REGRA-FECHADURA-08: Comunicação wireless deve usar criptografia AES-128 ou superior.

REGRA-FECHADURA-09: Log de acessos com timestamp obrigatório.

REGRA-FECHADURA-10: Alerta de bateria baixa deve notificar com antecedência de pelo menos 1 semana.

REGRA-FECHADURA-11: Protocolo Zigbee ou Z-Wave preferível sobre Wi-Fi (menor consumo).
```

---

## 7. Iluminação de segurança

### 7.1 Níveis de iluminância (NBR 8995-1 / IES)

```
REGRA-ILUM-01: Áreas de identificação facial (entradas, portões): mínimo 50 lux, recomendado 100 lux.

REGRA-ILUM-02: Corredores e circulação: mínimo 100 lux.

REGRA-ILUM-03: Perímetro e jardins: mínimo 10-30 lux.

REGRA-ILUM-04: Uniformidade obrigatória - evitar sombras e pontos escuros em áreas monitoradas.

REGRA-ILUM-05: Iluminação não deve causar ofuscamento em câmeras de CFTV.
```

### 7.2 Tipos de iluminação

```
REGRA-ILUM-06: Entradas principais devem ter iluminação constante durante a noite.

REGRA-ILUM-07: Áreas de baixo tráfego podem usar iluminação com sensor de presença (PIR).

REGRA-ILUM-08: Perímetros rurais sem energia devem usar iluminação solar com bateria.

REGRA-ILUM-09: Áreas críticas devem ter iluminação de emergência com bateria backup.

REGRA-ILUM-10: Refletores reativos (com sensor) devem ter potência adequada para cobrir zona de detecção da câmera.
```

---

## 8. Drones autônomos (regulamentação ANAC/DECEA)

### 8.1 Classificação de drones (RBAC-E nº 94)

| Classe | Peso máximo de decolagem | Requisitos |
|--------|-------------------------|------------|
| Classe 1 | > 150 kg | Registro ANAC + certificação + piloto habilitado |
| Classe 2 | > 25 kg e ≤ 150 kg | Registro ANAC + certificação + piloto habilitado |
| Classe 3 | ≤ 25 kg | Registro ANAC (se >250g) + cadastro SISANT |

> **Nota**: Drones residenciais típicos (UGV/UAV do projeto) se enquadram na Classe 3.

### 8.2 Regras de operação

```
REGRA-DRONE-01: Drones com peso > 250g devem ser registrados na ANAC e cadastrados no SISANT/DECEA.

REGRA-DRONE-02: Operação VLOS (Visual Line of Sight) é obrigatória. Operação BVLOS requer autorização especial.

REGRA-DRONE-03: Altura máxima de voo: 120m (400 pés) AGL em área não controlada.

REGRA-DRONE-04: Distância mínima de pessoas não anuentes: 30m horizontal.

REGRA-DRONE-05: Proibido sobrevoar aglomerações de pessoas, estádios, eventos públicos.

REGRA-DRONE-06: Verificar NOTAM e restrições de espaço aéreo antes de cada voo (AIS DECEA).

REGRA-DRONE-07: Operação noturna requer luzes de navegação visíveis e autorização.
```

### 8.3 Comunicação e homologação

```
REGRA-DRONE-08: Módulos de rádio (Wi-Fi, LoRa) devem ser homologados pela ANATEL.

REGRA-DRONE-09: Frequências permitidas: 2.4GHz, 5.8GHz (Wi-Fi), 915MHz (LoRa Brasil).

REGRA-DRONE-10: Potência de transmissão deve respeitar limites ANATEL (tipicamente ≤1W).
```

### 8.4 Módulo de defesa não letal

```
REGRA-DRONE-11: Spray de pimenta (OC) é classificado como "arma menos letal" (portaria MJSP).

REGRA-DRONE-12: Uso de spray de pimenta em propriedade PRIVADA não requer autorização federal.

REGRA-DRONE-13: Verificar legislação ESTADUAL sobre uso de spray OC (varia por UF).

REGRA-DRONE-14: Módulo de defesa deve ter autenticação de 2 fatores (2FA) obrigatória.

REGRA-DRONE-15: Todo disparo deve ser registrado com: timestamp, localização GPS, vídeo, operador.

REGRA-DRONE-16: Aviso sonoro/visual obrigatório antes de disparo (mínimo 5 segundos).

REGRA-DRONE-17: Modo automático de disparo só pode ser ativado em ausência confirmada de moradores.
```

### 8.5 Segurança e fail-safe

```
REGRA-DRONE-18: Drone deve retornar à base automaticamente (RTH) em perda de comunicação.

REGRA-DRONE-19: Drone deve retornar à base automaticamente quando bateria < 20%.

REGRA-DRONE-20: Sistema de geofence deve impedir saída da área de operação autorizada.

REGRA-DRONE-21: Firmware deve ter assinatura digital para evitar adulteração.

REGRA-DRONE-22: Logs de operação devem ser imutáveis (append-only) com hash de integridade.
```

---

## 9. Checklist de conformidade

### Antes da instalação

- [ ] Verificar legislação municipal sobre cercas elétricas
- [ ] Documentar ângulos de câmera (área privada vs. pública)
- [ ] Definir política de retenção de gravações
- [ ] Avaliar necessidade de SPDA
- [ ] Selecionar fechaduras com grau de segurança adequado (NBR 14913)
- [ ] Planejar iluminação com níveis adequados (mín. 50 lux em entradas)

### Antes da instalação (drones)

- [ ] Verificar peso do drone (>250g requer registro ANAC)
- [ ] Registrar drone no SISANT/DECEA
- [ ] Verificar zonas de voo permitidas (AIS DECEA)
- [ ] Homologar módulos de rádio (Wi-Fi, LoRa) junto à ANATEL
- [ ] Verificar legislação estadual sobre spray de pimenta

### Durante a instalação

- [ ] Instalar DPS no quadro de distribuição
- [ ] Configurar VLANs para IoT e câmeras
- [ ] Alterar TODAS as senhas padrão
- [ ] Desabilitar serviços desnecessários em cada dispositivo
- [ ] Instalar placas de aviso de monitoramento
- [ ] Instalar protetor de cilindro em portas de entrada
- [ ] Verificar uniformidade de iluminação (sem pontos escuros)
- [ ] Confirmar que iluminação não causa ofuscamento em câmeras

### Durante a instalação (drones)

- [ ] Configurar geofence com área de operação autorizada
- [ ] Configurar RTH (Return To Home) automático
- [ ] Configurar limites de bateria para retorno (20%)
- [ ] Configurar autenticação 2FA para módulo de defesa
- [ ] Testar failover de comunicação (Wi-Fi → LoRa)

### Após a instalação

- [ ] Documentar inventário de dispositivos
- [ ] Configurar rotação automática de gravações
- [ ] Configurar alertas de falha de energia
- [ ] Testar acesso via VPN
- [ ] Verificar logs de acesso
- [ ] Configurar alertas de bateria baixa em fechaduras eletrônicas
- [ ] Testar iluminação noturna com câmeras

### Após a instalação (drones)

- [ ] Documentar rotas de patrulha programadas
- [ ] Testar navegação autônoma em modo seguro
- [ ] Verificar logs de operação (imutabilidade)
- [ ] Testar integração com Home Assistant
- [ ] Calibrar detecção de IA (evitar falsos positivos)

---

## 10. Responsabilidades

| Ator | Responsabilidades |
|------|-------------------|
| **Proprietário** | Definir política de retenção, autorizar acessos, manter placas de aviso |
| **Instalador** | Seguir normas técnicas, documentar instalação, alterar senhas |
| **Manutenção** | Atualizar firmware, verificar logs, limpar câmeras |

---

## Referências

### Legislação
- [LGPD - Lei 13.709/2018](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm)
- [Lei 13.477/2017 - Cercas elétricas](https://www.camara.leg.br/radio/radioagencia/525293-michel-temer-sanciona-lei-sobre-novas-regras-para-instalacao-de-cerca-eletrica/)

### Regulamentação de drones
- [ANAC - RBAC-E nº 94](https://www.gov.br/anac/pt-br/assuntos/drones) – Regulamento Brasileiro da Aviação Civil Especial
- [DECEA - SISANT](https://servicos.decea.mil.br/sisant/) – Sistema de Aeronaves não Tripuladas
- [DECEA - ICA 100-40](https://www.decea.mil.br/) – Sistemas de Aeronaves Remotamente Pilotadas
- [ANATEL - Homologação](https://www.gov.br/anatel/pt-br) – Homologação de equipamentos de radiocomunicação

### Normas técnicas
- NBR 5410 – Instalações elétricas de baixa tensão
- NBR 5419 – Proteção contra descargas atmosféricas
- NBR 10821 – Esquadrias para edificações
- NBR 7199 – Vidros na construção civil
- NBR 15575 – Desempenho de edificações habitacionais
- NBR 15.401 – Cercas elétricas de segurança

### Padrões internacionais
- [OWASP IoT Top 10](https://owasp.org/www-project-internet-of-things/)
- [ETSI EN 303 645](https://www.etsi.org/technologies/consumer-iot-security)
- [EDPB Guidelines 3/2019 - Videovigilância](https://www.edpb.europa.eu/sites/default/files/files/file1/edpb_guidelines_201903_video_devices_pt.pdf)

### Documentação de drones
- [PX4 Documentation](https://docs.px4.io/)
- [ROS2 Navigation](https://nav2.org/)
- [ArduPilot Documentation](https://ardupilot.org/)

---

> **Próximos passos**: Agente_Pesquisador_Normas deve continuar pesquisando itens pendentes em `standards/STANDARDS_TO_RESEARCH.md`.

