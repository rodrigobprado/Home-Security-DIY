# Normas Pesquisadas – Sistema de Home Security

> Comentário: Lista organizada de normas e padrões pesquisados pelo Agente_Pesquisador_Normas. Para cada item, incluímos resumo, links oficiais e relevância para o projeto.

> **Última atualização**: 2026-02-12 por Agente_Arquiteto_Drones (Tarefas T-042, T-043 - Regulamentação de drones)

---

## 1. Normas de proteção de dados e privacidade

### 1.1 LGPD – Lei Geral de Proteção de Dados (Lei 13.709/2018)

**Escopo**: Lei brasileira que regula o tratamento de dados pessoais, incluindo imagens captadas por câmeras de segurança.

**Relevância para o projeto**: Fundamental para qualquer sistema de videovigilância. Imagens são consideradas dados pessoais.

**Requisitos principais**:

| Princípio | Descrição | Aplicação no projeto |
|-----------|-----------|---------------------|
| **Finalidade** | Dados devem ser coletados para propósitos legítimos e explícitos | Câmeras devem ser configuradas exclusivamente para segurança |
| **Adequação** | Tratamento compatível com as finalidades informadas | Evitar captura de áreas desnecessárias |
| **Necessidade** | Limitar ao mínimo necessário | Monitorar apenas pontos críticos de entrada/saída |
| **Transparência** | Informar sobre a coleta | Placas de aviso obrigatórias |
| **Segurança** | Proteger dados contra acesso não autorizado | Criptografia, controle de acesso, armazenamento local |

**Exceção para uso pessoal (Art. 4º, I)**: A LGPD **não se aplica** ao tratamento de dados pessoais realizado por pessoa natural para fins **exclusivamente particulares e não econômicos**. Isso significa que câmeras em residências particulares, para segurança do próprio morador, podem estar fora do escopo da LGPD, **desde que**:
- Não capturem áreas públicas ou vizinhos
- Não tenham finalidade comercial
- Não sejam compartilhadas com terceiros

**Atenção**: Câmeras que captam via pública, áreas de vizinhos ou áreas comuns de condomínio **não se enquadram na exceção** e devem seguir a LGPD integralmente.

**Requisitos de transparência para condomínios**:
- Placas informativas com: aviso de monitoramento, finalidade, responsável pelo tratamento
- Acesso restrito às imagens (síndico, conselho ou empresa de segurança)
- Histórico de acesso obrigatório (log de acessos)

**Links/Referências**:
- [Lei 13.709/2018 - Planalto](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm)
- [Câmeras de vigilância em condomínios - ACINH](https://www.acinh.com.br/noticia/cameras-de-vigilancia-em-condominios-enfoque-sob-a-lei-geral-de-protecao-de-dados-pessoais)
- [Câmeras de Vigilância e a LGPD - Just Arbitration](https://justarbitration.com.br/2024/08/27/cameras-de-vigilancia-e-a-lgpd-o-que-diz-a-lei-e-como-os-condominios-devem-se-adequar/)
- [Guia LGPD para condomínios - AABIC](https://aabic.org.br/wp-content/uploads/2021/05/AABIC-GUIA-LGPD-CONDOMINIOS.pdf)

**Status**: ✅ Pesquisado em 2026-02-12 por Agente_Pesquisador_Normas

---

### 1.2 GDPR – General Data Protection Regulation (EU 2016/679)

**Escopo**: Regulamento europeu de proteção de dados, referência internacional de boas práticas.

**Relevância para o projeto**: Referência para design de privacidade mesmo em projetos brasileiros.

**Requisitos principais similares à LGPD**:
- Minimização de dados
- Limitação de armazenamento
- Integridade e confidencialidade
- Accountability (responsabilização)

**Diretrizes específicas para videovigilância (EDPB Guidelines 3/2019)**:
- Avaliação de impacto obrigatória em certos casos
- Informação clara sobre monitoramento
- Retenção limitada ao necessário

**Links/Referências**:
- [EDPB Guidelines 3/2019 sobre videovigilância (PT)](https://www.edpb.europa.eu/sites/default/files/files/file1/edpb_guidelines_201903_video_devices_pt.pdf)

**Status**: ✅ Pesquisado em 2026-02-12 por Agente_Pesquisador_Normas

---

## 2. Normas de segurança da informação para IoT

### 2.1 OWASP IoT Top 10

**Escopo**: Lista das 10 principais vulnerabilidades em dispositivos IoT, mantida pela OWASP Foundation.

**Relevância para o projeto**: Essencial para proteger câmeras, sensores e dispositivos de automação.

**Top 10 Vulnerabilidades**:

| # | Vulnerabilidade | Descrição | Mitigação no projeto |
|---|-----------------|-----------|---------------------|
| 1 | **Senhas fracas/padrão** | Dispositivos vêm com senhas fáceis de adivinhar | Alterar todas as senhas padrão, usar senhas fortes |
| 2 | **Serviços de rede inseguros** | Portas abertas desnecessárias | Desabilitar serviços não utilizados, firewall |
| 3 | **Interfaces inseguras** | APIs e apps sem autenticação adequada | HTTPS obrigatório, autenticação forte |
| 4 | **Falta de atualização segura** | Sem mecanismo de update | Verificar atualizações regularmente |
| 5 | **Uso de componentes inseguros** | Bibliotecas desatualizadas | Manter firmware atualizado |
| 6 | **Proteção de privacidade insuficiente** | Coleta excessiva de dados | Minimização de dados, armazenamento local |
| 7 | **Transferência de dados insegura** | Dados transmitidos sem criptografia | TLS/HTTPS obrigatório |
| 8 | **Falta de gerenciamento de dispositivos** | Sem inventário ou controle | Documentar todos os dispositivos |
| 9 | **Configurações padrão inseguras** | Settings de fábrica vulneráveis | Hardening pós-instalação |
| 10 | **Falta de segurança física** | Acesso físico ao dispositivo | Instalação em locais protegidos |

**Caso relevante - Botnet Mirai (2016)**: Milhares de câmeras IP, roteadores e DVRs com senhas padrão foram comprometidos e usados para ataques DDoS massivos.

**Links/Referências**:
- [OWASP IoT Project](https://owasp.org/www-project-internet-of-things/)
- [10 Vulnerabilidades críticas em IoT - IBSEC](https://ibsec.com.br/10-vulnerabilidades-criticas-em-dispositivos-iot/)
- [Segurança em IoT - Clavis](https://clavis.com.br/blog/seguranca-em-iot/)

**Status**: ✅ Pesquisado em 2026-02-12 por Agente_Pesquisador_Normas

---

### 2.2 ETSI EN 303 645 – Cybersecurity for Consumer IoT

**Escopo**: Padrão europeu que estabelece requisitos de segurança para dispositivos IoT de consumo.

**Relevância para o projeto**: Padrão de referência para câmeras, sensores e dispositivos de automação residencial.

**Estrutura**: 13 recomendações de alto nível → 68 provisões → 33 requisitos obrigatórios + 35 recomendações.

**Top 3 Requisitos obrigatórios**:
1. **Sem senhas padrão** - Dispositivos não devem ter senhas universais de fábrica
2. **Política de divulgação de vulnerabilidades** - Fabricante deve ter canal para reportar falhas
3. **Manter software atualizado** - Mecanismo de atualização segura

**Dispositivos cobertos**: Gateways IoT, monitores, fechaduras inteligentes, câmeras, smart TVs, eletrodomésticos conectados.

**Links/Referências**:
- [ETSI EN 303 645 v3.1.3 (2024-09) - PDF oficial](https://www.etsi.org/deliver/etsi_en/303600_303699/303645/03.01.03_60/en_303645v030103p.pdf)
- [ETSI Consumer IoT Security](https://www.etsi.org/technologies/consumer-iot-security)
- [Guia TÜV SÜD sobre ETSI EN 303 645](https://www.tuvsud.com/en-us/resource-centre/stories/etsi-en-303-645-cybersecurity-for-consumer-internet-of-things)

**Status**: ✅ Pesquisado em 2026-02-12 por Agente_Pesquisador_Normas

---

## 3. Normas de segurança física residencial

### 3.1 Cercas elétricas – Lei Federal 13.477/2017 e NBR 15.401

**Escopo**: Regulamentação nacional para instalação de cercas elétricas em residências.

**Relevância para o projeto**: Requisitos obrigatórios para cenários rural e casa urbana.

**Requisitos principais**:

| Aspecto | Requisito | Observação |
|---------|-----------|------------|
| **Altura mínima** | 2,20m (varia por município) | Primeiro fio energizado a no mínimo 1,80m |
| **Voltagem** | Choque pulsativo em corrente contínua | Amperagem não letal, conforme ABNT |
| **Sinalização** | Placas a cada 10 metros | Em portões, mudanças de direção |
| **Instalação** | Por profissional habilitado | Documentação obrigatória |
| **Legislação** | Federal + Municipal | Verificar código de obras local |

**Normas técnicas relacionadas**:
- **NBR 15.401** – Requisitos mínimos para cercas elétricas de segurança
- **NBR 5419** – Proteção contra descargas atmosféricas (integração com SPDA)

**Links/Referências**:
- [Lei Federal sobre cercas elétricas - Câmara dos Deputados](https://www.camara.leg.br/radio/radioagencia/525293-michel-temer-sanciona-lei-sobre-novas-regras-para-instalacao-de-cerca-eletrica/)
- [Cerca Elétrica: quais as regras? - Bloquer](https://www.bloquer.com.br/cerca-eletrica-quais-as-regras)
- [Legislação cerca elétrica residencial](https://segurancaeletronicarj.com.br/glossario/legislacao-cerca-eletrica-residencial-normas-regras/)

**Status**: ✅ Pesquisado em 2026-02-12 por Agente_Pesquisador_Normas

---

### 3.2 NBR 10821 – Esquadrias para edificações (portas e janelas)

**Escopo**: Normas para esquadrias externas (janelas, portas, fachadas).

**Relevância para o projeto**: Requisitos de qualidade e desempenho para portas e janelas de segurança.

**Normas relacionadas**:
- **NBR 10820** – Terminologia de janelas
- **NBR 10821** – Esquadrias externas para edificações
- **NBR 6485** – Verificação de penetração de ar
- **NBR 6486** – Verificação de estanqueidade à água
- **NBR 6487** – Desempenho sob cargas uniformemente distribuídas

**Links/Referências**:
- [Mudanças na norma de portas e janelas - AECweb](https://www.aecweb.com.br/revista/materias/mudancas-na-norma-de-portas-e-janelas/2944)
- [As normas NBR para janelas e portas](https://www.ebanataw.com.br/roberto/janelas/janela10normas.htm)

**Status**: ✅ Pesquisado em 2026-02-12 por Agente_Pesquisador_Normas

---

### 3.3 NBR 7199 – Vidros na construção civil

**Escopo**: Especificações para uso de vidros, incluindo vidros de segurança.

**Relevância para o projeto**: Requisitos para vidros resistentes em portas e janelas vulneráveis.

**Tipos de vidro de segurança**:
- Vidro temperado
- Vidro laminado
- Vidro blindado (para casos específicos)

**Links/Referências**:
- [NBR 7199 atual e mais completa - Abravidro](https://abravidro.org.br/nbr-7199-atual-e-mais-completa-2)

**Status**: ✅ Pesquisado em 2026-02-12 por Agente_Pesquisador_Normas

---

### 3.4 NBR 15575 – Desempenho de edificações habitacionais

**Escopo**: Norma de desempenho que estabelece requisitos mínimos para edificações residenciais.

**Relevância para o projeto**: Requisitos de segurança estrutural, incluindo portas e janelas.

**Partes relevantes**:
- **Parte 1** – Requisitos gerais
- **Parte 4** – Sistemas de vedações verticais (portas, janelas, fachadas)

**Aspectos de segurança cobertos**:
- Segurança estrutural
- Segurança contra incêndio
- Resistência a intrusão (limitada)
- Desempenho acústico
- Desempenho térmico

**Links/Referências**:
- [NBR 15575 - Norma de Desempenho](https://maiscontroleerp.com.br/nbr-15575/)
- [Descomplicando a ABNT NBR 15575 - Harmonia](https://harmonia.global/abnt-nbr-15575/)

**Status**: ✅ Pesquisado em 2026-02-12 por Agente_Pesquisador_Normas

---

## 4. Normas de videovigilância (CFTV)

### 4.1 Tempo de retenção de gravações

**Escopo**: Recomendações e requisitos legais para armazenamento de imagens de CFTV.

**Relevância para o projeto**: Definição de política de retenção para NVR.

**Recomendações por contexto**:

| Contexto | Tempo de retenção | Base legal/Recomendação |
|----------|-------------------|-------------------------|
| **Residência particular** | 30 dias | Recomendação de mercado |
| **Condomínio** | 30 dias | LGPD + boas práticas |
| **Comércio** | 30 dias | Projeto de Lei em tramitação |
| **Bancos/Financeiras** | 30 dias (mínimo) | Portaria PF 3.233/2012 |
| **Rodovias (concessionárias)** | 3 anos | Resolução ANTT 2.064/07 |

**Boas práticas LGPD para retenção**:
- Definir período mínimo necessário para a finalidade
- Rotação automática (sobrescrever gravações antigas)
- Mecanismo para preservar gravações de incidentes (não sobrescrever)
- Log de acesso às gravações

**Links/Referências**:
- [Tempo de armazenamento de câmera de segurança - Verisure](https://www.verisure.com.br/blog/tempo-armazenamento-camera-de-seguranca)
- [Por quanto tempo armazenar imagens CFTV - BR Sistemas](https://www.brsistemasdeseguranca.com.br/blog/por-quanto-tempo-armazenar-as-imagens-do-cftv/65/)

**Status**: ✅ Pesquisado em 2026-02-12 por Agente_Pesquisador_Normas

---

### 4.2 Boas práticas de CFTV residencial

**Escopo**: Recomendações técnicas para sistemas de videovigilância eficientes.

**Relevância para o projeto**: Base para PRD de videovigilância.

**Práticas recomendadas**:

| Aspecto | Recomendação |
|---------|--------------|
| **Resolução** | Mínimo 1080p para identificação; 720p para monitoramento geral |
| **Cobertura** | Todos os pontos de entrada/saída; áreas de circulação |
| **Visão noturna** | Obrigatória para câmeras externas |
| **Armazenamento** | Monitorar capacidade; alertas quando próximo do limite |
| **Backup** | Transferir gravações importantes para disco externo |
| **Manutenção** | Limpeza regular de lentes; verificação de conexões |
| **Revisão** | Analisar gravações periodicamente para verificar qualidade |

**Tecnologias de armazenamento**:
- **DVR** (Digital Video Recorder): Sistema analógico, câmeras coaxiais
- **NVR** (Network Video Recorder): Sistema IP, câmeras de rede

**Links/Referências**:
- [Instalação de CFTV e Monitoramento: Guia Completo - MPI Technology](https://www.tecinfoservicos.com.br/blog/categorias/artigos/instalacao-de-cftv-e-monitoramento-guia-completo)
- [CFTV: guia completo - Frahm](https://www.frahm.com.br/cftv/)
- [O que é CFTV - Produttivo](https://www.produttivo.com.br/blog/cftv/)

**Status**: ✅ Pesquisado em 2026-02-12 por Agente_Pesquisador_Normas

---

## 5. Normas de instalações elétricas

### 5.1 NBR 5410 – Instalações elétricas de baixa tensão

**Escopo**: Requisitos para instalações elétricas seguras até 1.000V AC / 1.500V DC.

**Relevância para o projeto**: Base para instalação elétrica de sistemas de segurança.

**Aspectos relevantes para home security**:

| Aspecto | Requisito |
|---------|-----------|
| **DPS (Dispositivo de Proteção contra Surtos)** | Obrigatório em quadros de distribuição |
| **Aterramento** | Todos os equipamentos de segurança devem ser aterrados |
| **Dimensionamento** | Cabos adequados para a carga dos sistemas |
| **DR (Diferencial Residual)** | Proteção contra choques |
| **Circuitos de sinal** | Sistemas de alarme e interfone cobertos pela norma |

**Importante**: Filtros, estabilizadores e nobreaks **não substituem** DPS para proteção contra surtos atmosféricos.

**Links/Referências**:
- [NBR 5410: guia completo - OrçaFascio](https://www.orcafascio.com/papodeengenheiro/nbr-5410)
- [NBR 5410: Guia completo - Engeman](https://blog.engeman.com.br/nbr-5410-instalacoes-eletricas-baixa-tensao/)
- [DPS no Neutro - Sala da Elétrica](https://www.saladaeletrica.com.br/dps-no-neutro-quando-instalar-segundo-nbr-5410/)

**Status**: ✅ Pesquisado em 2026-02-12 por Agente_Pesquisador_Normas

---

### 5.2 NBR 5419 – Proteção contra descargas atmosféricas (SPDA)

**Escopo**: Diretrizes para proteção de estruturas contra raios.

**Relevância para o projeto**: Proteção de sistemas eletrônicos sensíveis (NVR, câmeras, sensores).

**Estrutura da norma (4 partes)**:

| Parte | Escopo |
|-------|--------|
| **Parte 1** | Princípios gerais |
| **Parte 2** | Gerenciamento de risco |
| **Parte 3** | Danos físicos a estruturas e perigo à vida |
| **Parte 4** | **Sistemas elétricos e eletrônicos internos** |

**Parte 4 – Proteção de sistemas eletrônicos**:
- Medidas para reduzir falhas em equipamentos sensíveis
- Proteção contra sobretensões induzidas
- Integração com sistema de aterramento

**Componentes do SPDA**:
- Sistema externo: captores, condutores de descida
- Sistema interno: equipotencialização, DPS

**Links/Referências**:
- [NBR 5419: o que é - Produttivo](https://www.produttivo.com.br/blog/nbr-5419/)
- [NBR 5419: aplicações e atualizações - Engeman](https://blog.engeman.com.br/nbr-5419-protecao-contra-descargas-atmosfericas/)
- [Guia prático NBR 5419 - Token Engenharia](https://tokenengenharia.com.br/guia-pratico-da-nbr-5419-protecao-contra-descargas-atmosfericas/)

**Status**: ✅ Pesquisado em 2026-02-12 por Agente_Pesquisador_Normas

---

## 6. Normas de fechaduras e controle de acesso

### 6.1 ABNT NBR 14913 – Fechadura de embutir (T-028)

**Escopo**: Especificação de requisitos mínimos para fabricação, classificação, dimensionamento, segurança, funcionamento e acabamento de fechaduras de embutir.

**Relevância para o projeto**: Seleção de fechaduras para portas de entrada em todos os cenários.

**Sistema de classificação (3 critérios)**:

| Critério | Descrição | Graus |
|----------|-----------|-------|
| **Classe de utilização** | Durabilidade da fechadura | Leve, médio, intenso |
| **Grau de segurança** | Resistência contra arrombamentos | Leve a máximo |
| **Resistência à corrosão** | Ambiente de utilização | 1 a 4 |

**Requisitos de desempenho**:
- Resistência da lingueta e trinco a esforço lateral
- Funcionamento do trinco por ataque lateral
- Resistência a movimento aplicado ao cubo e chave
- Resistência da lingueta a esforço contrário
- Resistência à corrosão

**Normas relacionadas**:
- **NBR 13051**: Fechadura de sobrepor externa
- **NBR 16833**: Procedimento para seleção, instalação e manutenção

**Links/Referências**:
- [NBR 14913 - Target Normas](https://www.normas.com.br/visualizar/abnt-nbr-nm/22471/abnt-nbr14913-fechadura-de-embutir-requisitos-classificacao-e-metodos-de-ensaio)
- [Fechaduras devem aliar segurança e qualidade - AECweb](https://www.aecweb.com.br/revista/materias/fechaduras-devem-aliar-seguranca-e-qualidade/6367)
- [NBR 16833 - SIAMFESP](https://www.siamfesp.org.br/imprensa/programas-de-normalizacao/738-abnt-nbr-16833-fechadura-de-embutir-procedimento-para-selecao-instalacao-e-manutencao)

**Status**: ✅ Pesquisado em 2026-02-12 por Agente_Pesquisador_Normas

---

### 6.2 BS EN 1303 – Cilindros para fechaduras (T-029)

**Escopo**: Padrão europeu para teste e classificação de cilindros de fechaduras, usado como referência internacional.

**Relevância para o projeto**: Seleção de cilindros de alta segurança para fechaduras multiponto e fechaduras eletrônicas.

**Sistema de classificação (8 dígitos)**:

| Dígito | Aspecto | Graus disponíveis |
|--------|---------|-------------------|
| 1 | **Categoria de uso** | 1 (residencial) a 2 (comercial) |
| 2 | **Durabilidade** | 4 (25.000 ciclos), 5 (50.000), 6 (100.000) |
| 3 | **Dimensões da porta** | Conforme espessura |
| 4 | **Resistência ao fogo** | 0 (não aprovado), A (fumaça), B (fogo+fumaça) |
| 5 | **Segurança contra liberação** | 0 a B |
| 6 | **Resistência à corrosão/temperatura** | 0 a C |
| 7 | **Segurança da chave** | 1 a 6 (6 = máxima) |
| 8 | **Resistência a ataque** | 0 (nenhuma) a D (máxima) |

**Graus de resistência a ataque**:
- **Grau 0**: Sem resistência a perfuração ou ataque mecânico
- **Grau A**: 3/5 min resistência a perfuração
- **Grau B/D**: 5/10 min resistência a perfuração + ataque mecânico

**Recomendação para residências**: Mínimo grau de segurança de chave 5 ou 6, resistência a ataque A ou B.

**Links/Referências**:
- [EN 1303 - Lockwiki](https://lockwiki.com/index.php/EN_1303)
- [Guide to BS EN 1303:2015 - Carlisle Brass](https://www.carlislebrass.com/media/simplepage/standards/bsen1303.pdf)
- [BS EN 1303 Cylinders - HOPPE](https://www.hoppe.com/in-en/contacts-service/standards/bs-en-1303/)

**Status**: ✅ Pesquisado em 2026-02-12 por Agente_Pesquisador_Normas

---

### 6.3 Fechaduras eletrônicas e biométricas (T-029 complemento)

**Escopo**: Normas e certificações para fechaduras digitais com acesso por senha, biometria ou app.

**Relevância para o projeto**: PRD_APARTMENT_SMART_LOCK e integração com automação.

**Certificações aplicáveis**:

| Certificação | Descrição |
|--------------|-----------|
| **IP65/IP66** | Proteção contra água e poeira (obrigatória para externas) |
| **ANSI/BHMA** | Padrão americano de graus de segurança |
| **EN 1303** | Aplicável ao cilindro mecânico de backup |
| **FCC/CE** | Aprovação de radiofrequência (Zigbee, Wi-Fi, BLE) |

**Características de segurança recomendadas**:
- Autenticação multi-fator (PIN + biometria)
- Criptografia AES-128 ou superior na comunicação
- Chave física de backup obrigatória
- Log de acessos com timestamp
- Alarme de tentativas inválidas
- Bateria de backup com alerta de nível baixo

**Protocolos de comunicação**:
- **Zigbee**: Preferível por baixo consumo e segurança
- **Z-Wave**: Boa opção para fechaduras (mais confiável)
- **Wi-Fi**: Evitar se possível (alto consumo de bateria)
- **Bluetooth**: Apenas para acesso local

**Links/Referências**:
- [O futuro da segurança residencial - Papaiz](https://www.papaiz.com.br/pt/papaiz-assa-abloy/blog/o-futuro-da-seguranca-residencial)
- [Fechaduras Digitais e Automação - A3A Engenharia](https://a3aengenharia.com.br/conteudo/artigos-tecnicos/fechaduras-digitais-automacao-residencial-engenharia-inteligente-2/)

**Status**: ✅ Pesquisado em 2026-02-12 por Agente_Pesquisador_Normas

---

## 7. Normas de iluminação para segurança

### 7.1 NBR 8995-1 e IES – Níveis de iluminação (T-030)

**Escopo**: Requisitos de iluminância para ambientes internos e externos, incluindo áreas de segurança.

**Relevância para o projeto**: Especificação de iluminação perimetral e de entrada nos três cenários.

**Normas principais**:
- **NBR 8995-1** (substituiu NBR 5413): Iluminação de ambientes de trabalho
- **IES Lighting Handbook**: Referência internacional para níveis recomendados

**Níveis de iluminância recomendados para segurança**:

| Área | Iluminância (lux) | Observação |
|------|-------------------|------------|
| **Identificação facial** | 20 lux mínimo | Mínimo para CFTV identificar características faciais |
| **Corredores e escadarias** | 100 lux | Conforme NBR 8995-1 |
| **Entradas de pedestres** | 50-100 lux | Foco em segurança |
| **Estacionamentos residenciais** | 50-75 lux | Visibilidade de veículos |
| **Perímetro/jardins** | 10-30 lux | Iluminação geral de segurança |
| **Áreas de risco** | 100-200 lux | Portões, acessos principais |

**Escala padrão de valores (lux)**: 20 – 30 – 50 – 75 – 100 – 150 – 200 – 300 – 500

**Conversão**: 10 lux ≈ 1 foot-candle (fc)

**Recomendações para iluminação de segurança**:
1. **Uniformidade**: Evitar sombras e pontos escuros
2. **Sensor de presença**: Para economia em áreas de baixo tráfego
3. **Visão noturna de câmeras**: IR complementa iluminação insuficiente
4. **Ofuscamento**: Evitar luz direta em câmeras
5. **Backup**: Iluminação de emergência em áreas críticas

**Tipos de iluminação para segurança**:

| Tipo | Aplicação | Vantagem |
|------|-----------|----------|
| **LED com sensor PIR** | Entradas, corredores | Economia, reação a movimento |
| **LED constante** | Entrada principal | Dissuasão permanente |
| **Solar** | Perímetro rural | Autonomia, sem cabeamento |
| **Emergência (bateria)** | Áreas críticas | Funciona em queda de energia |

**Links/Referências**:
- [NBR 8995 - Luxatec](https://www.luxatec.com.br/blog/norma-nbr-8995-o-que-ela-diz-sobre-iluminao)
- [Lux: Norma ABNT - Inlucce](https://inlucce.com.br/lux-norma-brasileira-abnt-nbr/)
- [IES Recommended Light Levels - Waypoint](https://waypointlighting.com/uploads/2/6/8/4/26847904/ies_recommended_light_levels.pdf)
- [Recommended Outdoor Lighting Levels - RCLite](https://rclite.com/blog/recommended-outdoor-lighting-levels/)

**Status**: ✅ Pesquisado em 2026-02-12 por Agente_Pesquisador_Normas

---

## 8. Regulamentação de drones autônomos (ANAC/DECEA)

### 8.1 RBAC-E nº 94 – Regulamento Brasileiro para Drones (T-042)

**Escopo**: Requisitos gerais para aeronaves não tripuladas civis (RPAS/RPA) no Brasil.

**Relevância para o projeto**: Obrigatório para operação legal de drones aéreos (UAV) no sistema de segurança.

**Classificação por peso máximo de decolagem (PMD)**:

| Classe | Peso | Requisitos principais |
|--------|------|----------------------|
| **Classe 3** | ≤ 250g | Dispensa de registro, mas segue regras gerais |
| **Classe 3** | > 250g e ≤ 25kg | Registro ANAC + Cadastro SISANT obrigatórios |
| **Classe 2** | > 25kg e ≤ 150kg | Certificação de aeronavegabilidade + piloto habilitado |
| **Classe 1** | > 150kg | Certificação completa como aeronave tripulada |

**Tipos de operação**:

| Tipo | Descrição | Requisitos |
|------|-----------|------------|
| **VLOS** | Visual Line of Sight | Operador mantém contato visual com drone |
| **EVLOS** | Extended VLOS | Observadores auxiliares em posições estratégicas |
| **BVLOS** | Beyond VLOS | Autorização especial ANAC/DECEA obrigatória |

**Restrições gerais**:
- Altura máxima: 120m (400 pés) AGL em área não controlada
- Distância mínima de pessoas: 30m horizontal
- Proibido: aglomerações, eventos públicos, estádios, instalações sensíveis
- Operação noturna: requer luzes de navegação visíveis

**Documentação obrigatória**:
1. Registro da aeronave (CIS - Certificado de Identificação de Sistema)
2. Cadastro do operador no SISANT
3. Apólice de seguro RETA (para operações além de recreação)
4. Manual de operações (para operações comerciais)

**Links/Referências**:
- [ANAC - Drones](https://www.gov.br/anac/pt-br/assuntos/drones)
- [RBAC-E nº 94 - Texto completo](https://www.anac.gov.br/assuntos/legislacao/legislacao-1/rbac-regulamentos-brasileiros-de-aviacao-civil)
- [Perguntas frequentes ANAC](https://www.gov.br/anac/pt-br/assuntos/drones/perguntas-frequentes)

**Status**: ✅ Pesquisado em 2026-02-12 por Agente_Arquiteto_Drones

---

### 8.2 SISANT/DECEA – Sistema de Aeronaves não Tripuladas (T-042)

**Escopo**: Cadastro e autorização de voos no espaço aéreo brasileiro.

**Relevância para o projeto**: Obrigatório para qualquer operação de drone aéreo (UAV).

**Processo de cadastro**:

| Etapa | Descrição | Responsável |
|-------|-----------|-------------|
| 1. Registro ANAC | Obter número de registro do drone | Proprietário |
| 2. Cadastro SISANT | Registrar drone e operador no sistema DECEA | Operador |
| 3. Verificar espaço aéreo | Consultar restrições na área de operação | Operador |
| 4. Solicitar autorização | Se necessário (área controlada/especial) | Operador |

**Classificação de espaço aéreo**:

| Zona | Descrição | Regra |
|------|-----------|-------|
| **Área não controlada** | Maioria das áreas rurais e suburbanas | Cadastro + altura máx. 120m |
| **Área controlada (CTR)** | Proximidade de aeroportos | Autorização DECEA obrigatória |
| **Área restrita (REA)** | Instalações militares, nucleares | Proibido |
| **Área proibida (PRB)** | Centros de poder, eventos | Proibido |

**Ferramentas de consulta**:
- **AIS Web**: Consulta de cartas aeronáuticas e restrições
- **NOTAM**: Avisos temporários de restrição
- **App DECEA Drones**: Verificação em tempo real

**Links/Referências**:
- [SISANT - Portal](https://servicos.decea.mil.br/sisant/)
- [ICA 100-40 - Instrução de Aviação Civil](https://publicacoes.decea.mil.br/)
- [AIS Web - Cartas aeronáuticas](https://aisweb.decea.mil.br/)

**Status**: ✅ Pesquisado em 2026-02-12 por Agente_Arquiteto_Drones

---

### 8.3 ANATEL – Homologação de equipamentos de radiocomunicação (T-042)

**Escopo**: Requisitos de homologação para módulos de rádio em drones.

**Relevância para o projeto**: Obrigatório para módulos Wi-Fi, LoRa e rádio de controle.

**Faixas de frequência permitidas no Brasil**:

| Tecnologia | Frequência | Potência máx. | Observação |
|------------|------------|---------------|------------|
| **Wi-Fi 2.4GHz** | 2400-2483.5 MHz | 400 mW EIRP | Sem licença |
| **Wi-Fi 5GHz** | 5150-5825 MHz | 1 W EIRP | Canais específicos |
| **LoRa** | 915-928 MHz | 1 W EIRP | Banda ISM Brasil |
| **433 MHz** | 433.05-434.79 MHz | 10 mW | Controle remoto |

**Requisitos de homologação**:
- Módulos já homologados (ex: ESP32 com certificação) não precisam de nova homologação
- Equipamentos montados precisam usar módulos certificados
- Importação de módulos não homologados requer processo na ANATEL

**Links/Referências**:
- [ANATEL - Certificação e Homologação](https://www.gov.br/anatel/pt-br/regulado/certificacao-de-produtos)
- [SCH - Sistema de Certificação e Homologação](https://sistemas.anatel.gov.br/sch/)

**Status**: ✅ Pesquisado em 2026-02-12 por Agente_Arquiteto_Drones

---

### 8.4 Legislação de defesa não letal – Spray de pimenta (T-043)

**Escopo**: Regulamentação sobre posse e uso de agentes químicos não letais.

**Relevância para o projeto**: Módulo de defesa do drone usa spray de pimenta (OC - Oleoresin Capsicum).

**Classificação legal**:

| Aspecto | Classificação | Base legal |
|---------|---------------|------------|
| **Federal** | Arma menos letal (não é arma de fogo) | Lei 10.826/2003 não se aplica |
| **Comercialização** | Regulada pela Polícia Federal | Portaria MJSP 1.222/2019 |
| **Uso pessoal** | Permitido para defesa pessoal | Não requer autorização |
| **Uso em propriedade privada** | Permitido | Verificar legislação estadual |

**Variação por estado (exemplos)**:

| Estado | Restrição | Observação |
|--------|-----------|------------|
| **SP** | Venda permitida, uso regulado | Decreto estadual |
| **RJ** | Venda em lojas especializadas | Com nota fiscal |
| **MG** | Sem restrições adicionais | Segue legislação federal |
| **RS** | Venda permitida | Com identificação do comprador |

**Requisitos para uso em sistema automatizado**:
1. **Autenticação forte**: 2FA obrigatória antes de armar sistema
2. **Registro completo**: Log de cada disparo com timestamp, GPS, vídeo
3. **Aviso prévio**: Alerta sonoro/visual antes do disparo (mínimo 5s)
4. **Modo supervisão**: Preferencialmente com confirmação humana
5. **Apenas em propriedade privada**: Não usar em área pública

**Considerações éticas e legais**:
- Proporcionalidade: usar apenas quando necessário
- Documentação: preservar evidências de cada uso
- Responsabilidade civil: proprietário responde por uso indevido
- Menores e animais: evitar disparo quando detectados

**Links/Referências**:
- [Portaria MJSP 1.222/2019](https://www.gov.br/mj/pt-br)
- [Análise legal de spray de pimenta - JusBrasil](https://www.jusbrasil.com.br/)

**Status**: ✅ Pesquisado em 2026-02-12 por Agente_Arquiteto_Drones

---

### 8.5 Seguro e responsabilidade civil para drones (T-042 complemento)

**Escopo**: Requisitos de seguro para operação de drones.

**Relevância para o projeto**: Proteção contra danos a terceiros.

**Requisitos de seguro (RETA)**:

| Tipo de operação | Seguro obrigatório? | Observação |
|------------------|---------------------|------------|
| Recreativa (≤ 250g) | Não | Recomendado |
| Recreativa (> 250g) | Não | Recomendado |
| Não recreativa (qualquer peso) | Sim | RETA obrigatório |
| Segurança patrimonial | Sim | Considerada operação não recreativa |

**Coberturas recomendadas**:
- Danos a terceiros (pessoas e propriedades)
- Danos ao próprio equipamento
- Responsabilidade civil do operador
- Invasão de privacidade (se aplicável)

**Valores de referência (mercado 2026)**:
- Cobertura básica (R$ 100k): R$ 500-1.000/ano
- Cobertura ampla (R$ 500k): R$ 1.500-3.000/ano

**Status**: ✅ Pesquisado em 2026-02-12 por Agente_Arquiteto_Drones

---

## 9. Normas de baixa prioridade — pesquisadas

> **Última atualização**: 2026-02-22 por Agente_Pesquisador_Normas

---

### 9.1 ISO/IEC 27001 aplicada a IoT

**Escopo**: Norma internacional de Sistemas de Gestão de Segurança da Informação (SGSI), adaptada ao contexto de dispositivos IoT residenciais.

**Relevância para o projeto**: Referência de boas práticas para controles de segurança em sistemas embarcados e redes IoT domésticas.

**Controles aplicáveis ao projeto** (Anexo A da ISO 27001:2022):

| Controle | Descrição | Aplicação |
|----------|-----------|-----------|
| A.8.9 — Gestão de configuração | Manter inventário e baseline seguro de dispositivos | `src/docker-compose.yml`, manifests K8s |
| A.8.12 — Prevenção de vazamento de dados | Controlar transmissão de dados sensíveis | MQTT TLS, VPN para acesso remoto |
| A.8.21 — Segurança de serviços de rede | Autenticar e criptografar comunicações de rede | API Key no dashboard, HMAC nos drones |
| A.8.7 — Proteção contra malware | Monitorar e prevenir código malicioso | Imagens Docker assinadas, updates automáticos |
| A.8.15 — Log de eventos | Registrar eventos de segurança | Logs do Home Assistant, Frigate e dashboard |
| A.8.16 — Monitoramento de atividades | Detectar comportamentos anômalos | Alertas do HA para logins suspeitos |

**Certificação**: Não obrigatória para residências. Útil como referência de boas práticas ou caso o sistema seja comercializado.

**Status**: ✅ Pesquisado em 2026-02-22 por Agente_Pesquisador_Normas

---

### 9.2 NBR 9050 — Acessibilidade em interfaces de controle

**Escopo**: ABNT NBR 9050:2020 — Acessibilidade a edificações, mobiliário, espaços e equipamentos urbanos. Referência para interfaces de controle acessíveis.

**Relevância para o projeto**: Aplicável ao dashboard de monitoramento (frontend React) e interfaces físicas do sistema (teclados, painéis de controle).

**Requisitos aplicáveis à interface digital**:

| Requisito | Parâmetro | Aplicação no projeto |
|-----------|-----------|----------------------|
| Contraste mínimo de texto | 4,5:1 (texto normal), 3:1 (texto grande) | Dashboard React — verificar paleta de cores |
| Tamanho mínimo de fonte | 12px para leitura confortável | Componentes de alerta e status |
| Alvos de toque/clique | Mínimo 44×44px (WCAG 2.1 AA) | Botões do dashboard mobile |
| Navegação por teclado | Tab order lógico, foco visível | Formulários de autenticação |
| Texto alternativo | Imagens e ícones devem ter `aria-label` | Ícones de câmera, drones no dashboard |

**Referência complementar**: WCAG 2.1 Nível AA (W3C) — padrão internacional de acessibilidade web.

**Obrigatoriedade**: Obrigatória para serviços públicos e edificações. Para uso residencial privado, aplicação é voluntária mas recomendada.

**Status**: ✅ Pesquisado em 2026-02-22 por Agente_Pesquisador_Normas

---

### 9.3 Portões automatizados — Normas de segurança

**Escopo**: NBR 15777:2009 (atualizada) — Portões de uso residencial e comercial acionados por sistemas automáticos. Requisitos de segurança para evitar acidentes.

**Relevância para o projeto**: Aplicável à automação de portões via Home Assistant (relés, comandos MQTT, integração com câmeras Frigate).

**Requisitos principais (NBR 15777)**:

| Requisito | Descrição |
|-----------|-----------|
| Sensor de presença obrigatório | Sensor de borda (anti-esmagamento) nas bordas de fechamento |
| Força máxima de impacto | ≤ 400 N (newtons) na borda de fechamento |
| Dispositivo de parada de emergência | Botão de parada acessível ao operador |
| Reversão automática | Ao detectar obstáculo, motor deve reverter em ≤ 0,5s |
| Iluminação de aviso | Luz piscante durante movimento do portão |
| Manual de operação | Instruções para abertura manual em caso de falta de energia |

**Integração com o projeto**:
- Automação HA deve incluir verificação de sensor de presença ANTES de acionar fechamento
- Script de fechamento deve aguardar confirmação de sensor livre
- Câmera Frigate pode ser usada como verificação visual antes de acionar

**Certificação**: Instalação deve ser feita por profissional habilitado (eletricista ou empresa especializada).

**Status**: ✅ Pesquisado em 2026-02-22 por Agente_Pesquisador_Normas

---

### 9.4 Concertinas — Regulamentação para uso residencial

**Escopo**: Regulamentação municipal/estadual sobre instalação de concertinas (arame farpado em espiral) em imóveis residenciais brasileiros.

**Relevância para o projeto**: Componente de segurança passiva do perímetro (PRD_PERIMETER_URBAN_HOUSE.md, PRD_PERIMETER_RURAL.md).

**Regulamentação vigente**:

| Âmbito | Status | Observação |
|--------|--------|-----------|
| Federal | Sem lei específica | Não há proibição federal explícita |
| Estadual (SP) | Leis municipais variam | Algumas cidades proíbem em muros frontais |
| ABNT | Sem norma específica | Não há NBR para concertinas residenciais |

**Restrições comuns em municípios**:
- Proibição em muros frontais (voltados para calçada/via pública) em muitas prefeituras
- Obrigatoriedade de sinalização de aviso a cada 5m ("Perigo — Arame cortante")
- Altura mínima de instalação: geralmente ≥ 2,20m do solo
- Proibição em áreas de escola, hospital e locais de grande circulação de pedestres

**Obrigações do proprietário**:
- Responsabilidade civil por acidentes causados pela concertina (Código Civil, Art. 186/927)
- Recomendado: contratar seguro de responsabilidade civil do imóvel

**Ação recomendada**: Verificar legislação municipal do imóvel específico antes da instalação. Consultar a prefeitura local ou advogado especializado em direito imobiliário.

**Status**: ✅ Pesquisado em 2026-02-22 por Agente_Pesquisador_Normas

---

### 9.5 Paisagismo defensivo — Boas práticas (CPTED)

**Escopo**: Crime Prevention Through Environmental Design (CPTED) — conjunto de estratégias de design ambiental que reduzem oportunidades de crime.

**Relevância para o projeto**: Complemento à segurança eletrônica (câmeras, sensores). Barreiras físicas naturais reduzem pontos cegos e dificultam aproximação furtiva.

**Princípios CPTED aplicados ao perímetro residencial**:

| Princípio | Descrição | Aplicação prática |
|-----------|-----------|-------------------|
| **Vigilância natural** | Eliminar pontos cegos e vegetação densa próxima a entradas | Manter arbustos baixos (< 1m) na linha do muro |
| **Controle de acesso natural** | Direcionar fluxo de pessoas para pontos monitorados | Plantas espinhosas em janelas e muros laterais |
| **Reforço territorial** | Definir claramente limites da propriedade | Gradis, muretas, plantas demarcatórias |
| **Manutenção do ambiente** | Propriedade bem mantida inibe ação criminosa | Iluminação funcional, vegetação podada |

**Plantas recomendadas para segurança**:
- **Espinhosas** (muros e janelas): Bougainvillea (bugambília), Pyracantha, Rosa-brava, Agave
- **Cobertura de solo** (eliminar esconderijos): Gramíneas ornamentais baixas, Grama-esmeralda
- **Cercas vivas densas** (perímetro rural): Bambu, Leucena, Jatobá

**Pontos de atenção**:
- Evitar árvores próximas a muros que possam facilitar escalada
- Manter área ao redor de câmeras e sensores livre de vegetação (campo visual)
- Iluminação integrada com sensor de presença nas áreas de acesso

**Referências**:
- CPTED Brasil: https://cpted.pt/
- Cartilha SSPSP: Paisagismo e segurança em condomínios

**Status**: ✅ Pesquisado em 2026-02-22 por Agente_Pesquisador_Normas

---

### 9.6 Normas específicas para UGV (robôs terrestres)

**Escopo**: Regulamentação aplicável a Unmanned Ground Vehicles (UGVs) de segurança patrimonial no Brasil.

**Relevância para o projeto**: O UGV (`src/drone-ugv/`) realiza patrulhas autônomas no perímetro — sujeito a regulamentação de robôs móveis e segurança funcional.

**Normas internacionais aplicáveis**:

| Norma | Título | Aplicação |
|-------|--------|-----------|
| ISO 13482:2014 | Robots and robotic devices — Safety requirements for personal care robots | Base para UGVs de assistência/segurança |
| ISO 10218-1:2011 | Robots and robotic devices — Safety requirements for industrial robots | Referência para movimentação autônoma |
| IEC 62443 | Industrial Automation and Control Systems — Security | Segurança cibernética do firmware UGV |
| ISO/SAE 21434:2021 | Road vehicles — Cybersecurity engineering | Referência para veículos autônomos terrestres |

**Regulamentação brasileira**:
- **Não existe** norma ABNT específica para UGVs residenciais/patrimoniais (até 2026)
- O Código de Trânsito Brasileiro (CTB) não se aplica a UGVs que operam exclusivamente em propriedade privada
- ABNT NBR 16268:2014 (Sistemas de alarme de intrusão) pode ser referência para o sistema de detecção integrado

**Requisitos de segurança recomendados** (baseados em ISO 13482):
- Parada de emergência por hardware (botão físico + comando MQTT)
- Detecção de obstáculos antes de movimento (sensores ultrassônicos/lidar)
- Velocidade máxima segura: ≤ 1,5 m/s em ambiente habitado
- Sinalização luminosa e sonora durante operação autônoma
- Log imutável de todos os movimentos e comandos executados

**Status**: ✅ Pesquisado em 2026-02-22 por Agente_Pesquisador_Normas

---

### 9.7 Bateria LiPo — Normas de transporte e armazenamento

**Escopo**: Regulamentação sobre transporte e armazenamento de baterias de Lítio-Polímero (LiPo), usadas nos drones UGV e UAV do projeto.

**Relevância para o projeto**: Baterias LiPo de alta capacidade (>100Wh) têm regulamentação específica para transporte aéreo, armazenamento e descarte.

**Normas e regulamentações vigentes**:

| Âmbito | Norma/Regulamento | Limites |
|--------|-------------------|---------|
| Transporte aéreo (IATA DGR) | IATA DGR PI 965/966/967 | < 100Wh: carry-on; 100–160Wh: aprovação da cia; > 160Wh: proibido em bagagem |
| Transporte terrestre (BR) | ANTT Resolução nº 5.232/2016 (mercadorias perigosas) | Classe 9 (materiais perigosos diversos) para grandes quantidades |
| Resíduos perigosos (BR) | ABNT NBR 10004:2004 | Baterias Li = Resíduo Classe I (perigoso) — descarte em ponto específico |
| Armazenamento (referência) | NFPA 855:2021 (EUA) | Distância mínima de materiais inflamáveis, ventilação obrigatória |

**Boas práticas de armazenamento**:
- Armazenar em carga de 40–60% (storage voltage: ~3,8V/célula)
- Usar caixa de armazenamento resistente ao fogo (LiPo Safe Bag ou caixa metálica)
- Temperatura ideal: 15–25°C, longe de luz solar direta
- Nunca armazenar completamente carregada ou descarregada por períodos longos
- Inspecionar mensalmente para detecção de inchaço (swelling)

**Procedimentos de emergência**:
- Bateria inchada: isolá-la em recipiente metálico com areia, nunca perfurar
- Em caso de ignição: não usar água — usar areia seca ou extintor CO₂
- Descarte: levar a ponto de coleta de eletrônicos (ABNT NBR 10004)

**Cálculo de Wh** (para verificar faixa regulatória):
- Wh = Voltagem nominal (V) × Capacidade (Ah)
- Exemplo: 3S LiPo 5000mAh = 11,1V × 5Ah = 55,5Wh (abaixo de 100Wh)

**Status**: ✅ Pesquisado em 2026-02-22 por Agente_Pesquisador_Normas

---

## Resumo de conformidade para o projeto

### Checklist obrigatório – Sistema de segurança

- [ ] **LGPD**: Verificar se câmeras captam apenas área privada (exceção art. 4º, I)
- [ ] **LGPD**: Se captar área pública/vizinhos, implementar controles completos
- [ ] **LGPD**: Placas de aviso em áreas monitoradas
- [ ] **LGPD**: Política de retenção definida (recomendado: 30 dias)
- [ ] **LGPD**: Controle de acesso às gravações com log
- [ ] **Cerca elétrica**: Altura mínima 2,20m, sinalização a cada 10m
- [ ] **Cerca elétrica**: Instalação por profissional habilitado
- [ ] **NBR 5410**: DPS instalado no quadro de distribuição
- [ ] **NBR 5410**: Aterramento de todos os equipamentos
- [ ] **OWASP IoT**: Alterar todas as senhas padrão
- [ ] **OWASP IoT**: Desabilitar serviços de rede não utilizados
- [ ] **OWASP IoT**: Atualizar firmware regularmente

### Checklist obrigatório – Drones autônomos

- [ ] **ANAC**: Registrar drone (se >250g) e obter CIS
- [ ] **SISANT**: Cadastrar drone e operador no sistema DECEA
- [ ] **DECEA**: Verificar restrições de espaço aéreo na área de operação
- [ ] **DECEA**: Se área controlada (CTR), solicitar autorização prévia
- [ ] **ANATEL**: Usar apenas módulos de rádio homologados (ESP32, LoRa)
- [ ] **Seguro**: Contratar RETA se operação não recreativa
- [ ] **Operação**: Manter VLOS (Visual Line of Sight) ou solicitar autorização BVLOS
- [ ] **Altura**: Respeitar limite de 120m AGL em área não controlada
- [ ] **Distância**: Manter mínimo 30m de pessoas não anuentes
- [ ] **Noturno**: Se operação noturna, instalar luzes de navegação
- [ ] **Defesa**: Verificar legislação estadual sobre spray de pimenta
- [ ] **Defesa**: Implementar 2FA para armamento do módulo
- [ ] **Defesa**: Configurar aviso sonoro/visual pré-disparo (mín. 5s)
- [ ] **Logs**: Garantir registro imutável de operações e disparos

