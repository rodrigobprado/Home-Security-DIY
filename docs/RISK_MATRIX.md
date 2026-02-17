# Matriz de Riscos – Home Security DIY

**Data**: 2026-02-17
**Referência**: [THREAT_MODEL.md](THREAT_MODEL.md)

---

## 1. Metodologia de Avaliação

A avaliação de riscos considera dois eixos principais para determinar a severidade (Criticidade) de cada ameaça identificada no modelo STRIDE.

### 1.1 Probabilidade (P)
Chance do evento ocorrer considerando o cenário de ameaça (Hardware local, VPN, sem Cloud).

- **1 - Baixa**: Requer acesso físico complexo, conhecimento avançado ou falha múltipla de sistemas. (Evento raro/teórico).
- **2 - Média**: Possível se o atacante tiver motivação específica e recursos moderados. (Evento ocasional).
- **3 - Alta**: Vulnerabilidade exposta ou fácil de explorar; requer pouco esforço. (Evento provável).

### 1.2 Impacto (I)
Dano causado à segurança, privacidade ou operação do sistema caso o evento ocorra.

- **1 - Baixo**: Incômodo operacional, sem perda de dados sensíveis.
- **2 - Médio**: Perda temporária de serviço ou vazamento de dados não-críticos (metadados).
- **3 - Alto**: Perda de vídeo, acesso à rede interna ou interrupção prolongada.
- **4 - Crítico**: Comprometimento total do sistema, segurança física do morador ameaçada ou vazamento massivo de privacidade.

### 1.3 Matriz de Severidade (P x I)

| Impacto →<br>Probabilidade ↓ | 1 - Baixo | 2 - Médio | 3 - Alto | 4 - Crítico |
|---|---|---|---|---|
| **3 - Alta** | Médio (3) | Alto (6) | Crítico (9) | **Crítico (12)** |
| **2 - Média** | Baixo (2) | Médio (4) | Alto (6) | **Alto (8)** |
| **1 - Baixa** | Baixo (1) | Baixo (2) | Médio (3) | **Médio (4)** |

---

## 2. Avaliação de Ameaças (STRIDE)

Classificação dos riscos identificados no Threat Model antes (Risco Inerente) e depois (Risco Residual) das mitigações.

| ID | Ameaça | Prob. (P) | Imp. (I) | Risco Inerente | Status Mitigação | Risco Residual |
|----|--------|:---------:|:--------:|:--------------:|:----------------:|:--------------:|
| **S-01** | Falsificação de Sensor Zigbee | 1 (Bx) | 2 (Mé) | **Baixo (2)** | ⚠️ Parcial | **Baixo (1)** |
| **S-02** | Falsificação de Câmera (Spoof) | 1 (Bx) | 3 (Al) | **Médio (3)** | 🔴 Pendente | **Médio (3)** |
| **S-03** | Acesso ao Dashboard (Brute-force) | 2 (Mé) | 4 (Cr) | **Alto (8)** | ✅ Implementado (MFA/Ban) | **Baixo (2)** |
| **T-01** | Corte de Cabos de Rede | 2 (Mé) | 3 (Al) | **Alto (6)** | ✅ Implementado (Alerta) | **Baixo (2)** |
| **T-02** | Adulteração de Logs | 2 (Mé) | 3 (Al) | **Alto (6)** | 🔴 Pendente | **Alto (6)** |
| **T-03** | **Roubo do Servidor (Físico)** | 2 (Mé) | 4 (Cr) | **Alto (8)** | 🔴 Pendente (Criptografia) | **Alto (8)** |
| **R-01** | Repúdio de Ação (Usuário) | 2 (Mé) | 2 (Mé) | **Médio (4)** | ✅ Implementado (Logs Audit) | **Baixo (1)** |
| **I-01** | Interceptação de Vídeo (Sniffing) | 3 (Al) | 4 (Cr) | **Crítico (12)**| ⚠️ Configuração (VLAN) | **Médio (3)** |
| **I-02** | Leitura de MQTT (IoT Sniffing) | 2 (Mé) | 3 (Al) | **Alto (6)** | ⚠️ Parcial (ACLs) | **Baixo (2)** |
| **I-03** | Vazamento de Backup | 1 (Bx) | 4 (Cr) | **Médio (4)** | 🔴 Pendente (Enc) | **Médio (4)** |
| **D-01** | **Jamming de RF (2.4GHz)** | 3 (Al) | 4 (Cr) | **Crítico (12)**| ⚠️ Parcial (Detecção) | **Alto (6)** |
| **D-02** | Corte de Energia | 3 (Al) | 3 (Al) | **Crítico (9)** | ⚠️ Hardware (UPS) | **Baixo (2)** |
| **D-03** | Flood de Rede (DoS) | 1 (Bx) | 3 (Al) | **Médio (3)** | ⚠️ Configuração | **Baixo (1)** |
| **E-01** | Escape de Container | 1 (Bx) | 4 (Cr) | **Médio (4)** | ⚠️ Parcial | **Baixo (1)** |
| **E-02** | Acesso Físico ao Console | 2 (Mé) | 4 (Cr) | **Alto (8)** | ⚠️ Físico (Trancar) | **Médio (4)** |

---

## 3. Análise dos Top Riscos (Prioridade)

Os riscos que permanecem **Alto** ou **Crítico** após as mitigações atuais exigem ação imediata.

### 🔴 Prioridade 1: Roubo Físico (T-03)
- **Risco Residual**: Alto (8)
- **Cenário**: Invasor leva o Mini PC com todas as provas.
- **Ação Necessária**: Criptografia de disco total (LUKS) e Backup automático offsite/nuvem criptografada.

### 🔴 Prioridade 2: Jamming de RF (D-01)
- **Risco Residual**: Alto (6)
- **Cenário**: Bloqueador de sinal anula todos os sensores sem fio.
- **Ação Necessária**: Usar sensores cabeados para perímetro crítico. Melhorar lógica de detecção de jamming (implementada parcialmente hoje).

### 🟠 Prioridade 3: Adulteração de Logs (T-02)
- **Risco Residual**: Alto (6)
- **Cenário**: Atacante apaga evidências de acesso antes de sair.
- **Ação Necessária**: Exportar logs em tempo real para um servidor remoto (Syslog) ou serviço de mensageria imutável (Telegram/Discord channel oculto).

---

## 4. Mapa de Calor (Heatmap) - Estado Atual

Representação visual da postura de segurança atual (considerando mitigações parciais).

```mermaid
quadrantChart
    title Matriz de Risco Atual
    x-axis Baixo Impacto --> Alto Impacto
    y-axis Baixa Probabilidade --> Alta Probabilidade
    quadrant-1 Crítico (Ação Imediata)
    quadrant-2 Monitorar (Frequente mas leve)
    quadrant-3 Desprezível
    quadrant-4 Planejar (Raro mas grave)
    
    "S-01 Sensor Spoof": [0.15, 0.1]
    "S-03 Dashboard": [0.2, 0.9]
    "T-01 Cabo Corte": [0.4, 0.4]
    
    "T-03 Roubo Server": [0.55, 0.9]
    "I-01 Video Sniff": [0.85, 0.7]
    "D-01 Jamming RF": [0.95, 0.9]
    "D-02 Energia": [0.4, 0.9]
    
    "I-03 Backup leak": [0.2, 0.8]
    "E-02 Console Fisico": [0.3, 0.85]
```

> **Nota**: O objetivo do projeto é mover todos os pontos para o quadrante inferior esquerdo (Baixo Impacto/Probabilidade) através de camadas de defesa (Defense in Depth).
