# Normas Aplicadas ao Projeto

> Regras concretas derivadas das normas pesquisadas em `STANDARDS_TO_RESEARCH.md`.
>
> Versao: 1.0 | Data: 2026-02-18

---

## 1. Protecao de dados e privacidade (LGPD / GDPR)

| ID | Regra | Norma | Aplicacao |
|----|-------|-------|-----------|
| REGRA-LGPD-01 | Documentar angulo de captura de cada camera | LGPD Art. 6 | Todas as cameras |
| REGRA-LGPD-02 | Instalar placas de aviso se captar area publica | LGPD Art. 9 | Cameras externas |
| REGRA-LGPD-03 | Retencao padrao de 30 dias com rotacao automatica | LGPD Art. 16 | Frigate NVR |
| REGRA-LGPD-04 | Acesso as gravacoes restrito ao proprietario com log | LGPD Art. 46 | Home Assistant |
| REGRA-LGPD-05 | Gravacoes nao devem ser enviadas para nuvem | LGPD Art. 46 | Arquitetura geral |
| REGRA-PRIV-01 | Nenhum servico de nuvem obrigatorio | Privacy by Design | Arquitetura geral |
| REGRA-PRIV-02 | Cameras sem acesso a internet | Privacy by Design | Firewall VLAN 30 |
| REGRA-PRIV-03 | Desabilitar telemetria em todos os dispositivos | ETSI EN 303 645 | Setup inicial |
| REGRA-PRIV-04 | Criptografia de disco recomendada | LGPD Art. 46 | Servidor |
| REGRA-PRIV-05 | Acesso remoto apenas via VPN | Privacy by Design | WireGuard |
| REGRA-PRIV-06 | Autenticacao obrigatoria com senha forte + 2FA | LGPD Art. 46 | Home Assistant |
| REGRA-PRIV-07 | Log de acessos mantido por 90 dias | LGPD Art. 37 | Home Assistant |

---

## 2. Seguranca de IoT (OWASP Top 10 / ETSI EN 303 645)

| ID | Regra | Norma | Aplicacao |
|----|-------|-------|-----------|
| REGRA-IOT-01 | Nunca manter senhas padrao de fabrica | OWASP IoT #1 / ETSI 5.1 | Todos os dispositivos |
| REGRA-IOT-02 | Desabilitar servicos nao utilizados (Telnet, FTP, UPnP) | OWASP IoT #2 / ETSI 5.5 | Cameras, sensores Wi-Fi |
| REGRA-IOT-03 | Dispositivos IoT sem acesso a internet | OWASP IoT #3 | Firewall VLAN 20/30 |
| REGRA-IOT-04 | Toda comunicacao deve usar criptografia (TLS/AES) | OWASP IoT #7 / ETSI 5.8 | MQTT, HTTPS, Zigbee |
| REGRA-IOT-05 | Firmware atualizado mensalmente | OWASP IoT #4 / ETSI 5.3 | Todos os dispositivos |
| REGRA-IOT-06 | Manter inventario de todos os dispositivos | OWASP IoT #8 | Documentacao |

---

## 3. Seguranca fisica

### 3.1 Cercas eletricas (Lei 13.477/2017 / NBR 15.401)

| ID | Regra | Norma | Cenario |
|----|-------|-------|---------|
| REGRA-CERCA-01 | Altura minima 2,20m (verificar legislacao municipal) | Lei 13.477 | Rural, Urbana |
| REGRA-CERCA-02 | Primeiro fio a minimo 1,80m do solo | NBR 15.401 | Rural, Urbana |
| REGRA-CERCA-03 | Sinalizacao a cada 10m, em portoes e mudancas de direcao | Lei 13.477 | Rural, Urbana |
| REGRA-CERCA-04 | Instalacao por profissional habilitado | NBR 15.401 | Rural, Urbana |
| REGRA-CERCA-05 | Voltagem/amperagem conforme ABNT (nao letal) | NBR 15.401 | Rural, Urbana |
| REGRA-CERCA-06 | Integracao com SPDA quando aplicavel | NBR 5419 | Rural, Urbana |

### 3.2 Portas, janelas e vidros (NBR 10821 / NBR 7199 / NBR 15575)

| ID | Regra | Norma | Cenario |
|----|-------|-------|---------|
| REGRA-ESQUADRIA-01 | Portas de entrada devem atender NBR 10821 | NBR 10821 | Todos |
| REGRA-ESQUADRIA-02 | Vidros em areas vulneraveis: laminado ou temperado | NBR 7199 | Todos |
| REGRA-ESQUADRIA-03 | Desempenho conforme NBR 15575-4 | NBR 15575 | Todos |

### 3.3 Fechaduras (NBR 14913 / EN 1303)

| ID | Regra | Norma | Cenario |
|----|-------|-------|---------|
| REGRA-FECHADURA-01 | Grau de seguranca medio ou superior em entradas | NBR 14913 | Todos |
| REGRA-FECHADURA-02 | Fechaduras multiponto recomendadas em entradas | NBR 14913 | Rural, Urbana |
| REGRA-FECHADURA-03 | Cilindros com seguranca de chave grau 5-6 | EN 1303 | Todos |
| REGRA-FECHADURA-04 | Resistencia a ataque grau A ou superior | EN 1303 | Todos |
| REGRA-FECHADURA-05 | Protetor de cilindro obrigatorio em entradas | EN 1303 | Todos |
| REGRA-FECHADURA-06 | Fechaduras eletronicas: chave fisica de backup | Boas praticas | Apartamento |
| REGRA-FECHADURA-07 | Fechaduras externas: IP65 ou superior | IEC 60529 | Rural, Urbana |
| REGRA-FECHADURA-08 | Comunicacao wireless: AES-128 ou superior | ETSI EN 303 645 | Todos |
| REGRA-FECHADURA-09 | Log de acessos com timestamp | LGPD | Todos |
| REGRA-FECHADURA-10 | Alerta bateria baixa com 1 semana antecedencia | Boas praticas | Todos |

---

## 4. Videovigilancia (CFTV)

| ID | Regra | Norma | Aplicacao |
|----|-------|-------|-----------|
| REGRA-CFTV-01 | Retencao padrao: 30 dias | LGPD + mercado | Frigate |
| REGRA-CFTV-02 | Rotacao automatica FIFO | LGPD Art. 16 | Frigate |
| REGRA-CFTV-03 | Preservar gravacoes de incidentes (nao sobrescrever) | Boas praticas | Frigate |
| REGRA-CFTV-04 | Backup de gravacoes criticas em midia separada | NBR ISO 27001 | Operacional |
| REGRA-CFTV-05 | Resolucao minima 1080p para identificacao | IES / CFTV | Cameras |
| REGRA-CFTV-06 | Visao noturna obrigatoria para cameras externas | Boas praticas | Cameras |
| REGRA-CFTV-07 | Cobrir todos os pontos de entrada/saida | Boas praticas | Cameras |
| REGRA-CFTV-08 | Manutencao mensal (lentes, conexoes) | Boas praticas | Operacional |
| REGRA-CFTV-09 | NVR protegido por senha forte | OWASP IoT | Frigate |
| REGRA-CFTV-10 | Log de acessos as gravacoes | LGPD Art. 37 | Frigate |
| REGRA-CFTV-11 | Acesso remoto apenas via VPN | OWASP IoT | WireGuard |
| REGRA-CFTV-12 | Cameras em VLAN separada sem internet | OWASP IoT | VLAN 30 |

---

## 5. Instalacoes eletricas (NBR 5410 / NBR 5419)

| ID | Regra | Norma | Aplicacao |
|----|-------|-------|-----------|
| REGRA-ELETRICA-01 | DPS obrigatorio no quadro de distribuicao | NBR 5410 | Instalacao |
| REGRA-ELETRICA-02 | Aterramento de equipamentos de seguranca | NBR 5410 | Instalacao |
| REGRA-ELETRICA-03 | Dimensionamento de cabos conforme norma | NBR 5410 | Instalacao |
| REGRA-ELETRICA-04 | DR para protecao contra choques | NBR 5410 | Instalacao |
| REGRA-SPDA-01 | Avaliar necessidade de SPDA | NBR 5419-2 | Rural |
| REGRA-SPDA-02 | Protecao de eletronicos conforme Parte 4 | NBR 5419-4 | Servidor |
| REGRA-NOBREAK-01 | Nobreak com 30 min de autonomia minima | Boas praticas | Servidor |
| REGRA-NOBREAK-02 | Alerta automatico em queda de energia | Boas praticas | Home Assistant |
| REGRA-NOBREAK-03 | Cameras criticas com PoE em switch com nobreak | Boas praticas | Cameras |

---

## 6. Iluminacao de seguranca (NBR 8995-1 / IES)

| ID | Regra | Norma | Aplicacao |
|----|-------|-------|-----------|
| REGRA-ILUM-01 | Entradas e portoes: minimo 50 lux, recomendado 100 | NBR 8995-1 | Cameras externas |
| REGRA-ILUM-02 | Corredores e circulacao: minimo 100 lux | NBR 8995-1 | Todos |
| REGRA-ILUM-03 | Perimetro e jardins: 10-30 lux | IES | Rural, Urbana |
| REGRA-ILUM-04 | Evitar sombras e pontos escuros em areas monitoradas | IES | Todos |
| REGRA-ILUM-05 | Iluminacao nao deve ofuscar cameras | Boas praticas | Todos |
| REGRA-ILUM-06 | Iluminacao constante noturna em entradas | Boas praticas | Todos |
| REGRA-ILUM-07 | Sensor de presenca em areas de baixo trafego | NBR 8995-1 | Todos |
| REGRA-ILUM-08 | Iluminacao solar para perimetros sem energia | Boas praticas | Rural |
| REGRA-ILUM-09 | Iluminacao de emergencia em areas criticas | NBR 8995-1 | Todos |

---

## 7. Drones autonomos (ANAC / DECEA / ANATEL)

| ID | Regra | Norma | Aplicacao |
|----|-------|-------|-----------|
| REGRA-DRONE-01 | Registro ANAC + SISANT para drones >250g | RBAC-E 94 | UAV |
| REGRA-DRONE-02 | VLOS obrigatorio; BVLOS requer autorizacao especial | RBAC-E 94 | UAV |
| REGRA-DRONE-03 | Altura maxima 120m AGL em area nao controlada | RBAC-E 94 | UAV |
| REGRA-DRONE-04 | Distancia minima 30m de pessoas nao anuentes | RBAC-E 94 | UAV |
| REGRA-DRONE-08 | Modulos de radio homologados ANATEL | Res. ANATEL | UGV/UAV |
| REGRA-DRONE-09 | Frequencias: 2.4/5.8 GHz (Wi-Fi), 915 MHz (LoRa) | ANATEL | UGV/UAV |
| REGRA-DRONE-14 | 2FA obrigatoria para modulo de defesa | Boas praticas | Modulo defesa |
| REGRA-DRONE-15 | Log de disparos: timestamp, GPS, video, operador | LGPD | Modulo defesa |
| REGRA-DRONE-16 | Aviso sonoro/visual 5s antes de disparo | Etica | Modulo defesa |
| REGRA-DRONE-17 | Modo automatico de disparo PROIBIDO | Etica/Legal | Modulo defesa |
| REGRA-DRONE-18 | RTH automatico em perda de comunicacao | RBAC-E 94 | UAV |
| REGRA-DRONE-19 | RTH automatico quando bateria <20% | Boas praticas | UGV/UAV |
| REGRA-DRONE-20 | Geofence para impedir saida da area autorizada | RBAC-E 94 | UGV/UAV |
| REGRA-DRONE-24 | Bloqueio de disparo na deteccao de criancas/animais | Etica/Legal | Modulo defesa |
| REGRA-DRONE-25 | Proprietario e responsavel civil e criminal | CC Art. 927 | Todos |

---

## 8. Resumo de conformidade por cenario

| Categoria | Rural | Urbana | Apartamento |
|-----------|-------|--------|-------------|
| LGPD | Sim (se captar area publica) | Sim (se captar area publica) | Sim (areas comuns) |
| Cerca eletrica | Obrigatorio | Obrigatorio | N/A |
| NBR 5410 (eletrica) | Obrigatorio | Obrigatorio | Obrigatorio |
| CFTV retencao 30d | Sim | Sim | Sim |
| VLANs isoladas | Recomendado | Recomendado | Recomendado |
| OWASP IoT | Obrigatorio | Obrigatorio | Obrigatorio |
| Fechaduras EN 1303 | Recomendado | Recomendado | Obrigatorio |
| Iluminacao NBR 8995 | Obrigatorio | Obrigatorio | Parcial |
| Drones ANAC | Se aplicavel | Se aplicavel | N/A |

---

## Referencias

- `standards/STANDARDS_TO_RESEARCH.md` — Pesquisa completa de normas
- `rules/RULES_COMPLIANCE_AND_STANDARDS.md` — Regras detalhadas com checklists
- `docs/LEGAL_AND_ETHICS.md` — Aspectos legais e eticos
- `docs/THREAT_MODEL.md` — Modelo de ameacas STRIDE
