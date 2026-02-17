# Modelo de Ameaças (Threat Model)

Data: 2026-02-17
Metodologia: **STRIDE** (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege)

---

## 1. Definição do Sistema

O Home Security DIY é um sistema de segurança residencial operando em hardware local (Mini PC), conectado a câmeras IP via rede cabeada (VLAN isolada) e sensores via protocolo Zigbee. O sistema é acessível localmente via LAN e remotamente via VPN.

### Ativos Críticos
1. **Vídeo ao vivo e gravações** (Privacidade)
2. **Status de presença e alarme** (Segurança física)
3. **Credenciais de acesso** (Controle)
4. **Configurações do sistema** (Disponibilidade)

---

## 2. Análise STRIDE

### S - Spoofing (Falsificação de identidade)

| ID | Ameaça | Cenário | Impacto | Mitigação | Status |
|----|--------|---------|---------|-----------|--------|
| S-01 | Falsificação de sensor | Atacante introduz sensor Zigbee malicioso na rede. | Injeção de dados falsos (abrir porta sem alarme). | Zigbee 3.0 requer chave de rede para pareamento. Permitir join apenas temporariamente. | ⚠️ Parcial |
| S-02 | Falsificação de câmera | Atacante substitui feed de câmera por vídeo em loop. | Cegueira do sistema de vigilância. | Autenticação Digest/Onvif. Monitoramento de MAC address na porta do switch (Port Security). | 🔴 Pendente |
| S-03 | Acesso não autorizado ao Dashboard | Atacante acessa HA sem credenciais válidas. | Controle total do sistema. | Autenticação forte + MFA. Fail2Ban no acesso web. | ✅ Implementado |

### T - Tampering (Adulteração)

| ID | Ameaça | Cenário | Impacto | Mitigação | Status |
|----|--------|---------|---------|-----------|--------|
| T-01 | Corte de cabos de rede | Atacante corta cabo de câmera externa. | Perda de visibilidade. | Notificação imediata de "Câmera Offline" (automação implementada). Gravação no SD card da câmera (edge recording) como backup. | ✅ Implementado |
| T-02 | Adulteração de arquivos de log | Atacante apaga logs para esconder rastros. | Perda de auditoria/forense. | Envio de logs para servidor remoto (Syslog) ou partição somente leitura. | 🔴 Pendente |
| T-03 | Roubo do servidor | Atacante leva o Mini PC com as gravações. | Perda total de evidências. | Criptografia de disco (LUKS). Backup automático para nuvem criptograda ou local escondido. | 🔴 Pendente |

### R - Repudiation (Repúdio)

| ID | Ameaça | Cenário | Impacto | Mitigação | Status |
|----|--------|---------|---------|-----------|--------|
| R-01 | Negação de ação | Usuário desativa alarme e nega ter feito. | Falta de responsabilização. | Log de auditoria imutável no Home Assistant. Usuários individuais para cada morador. | ✅ Implementado |

### I - Information Disclosure (Divulgação de Informação)

| ID | Ameaça | Cenário | Impacto | Mitigação | Status |
|----|--------|---------|---------|-----------|--------|
| I-01 | Interceptação de vídeo | Atacante na rede Wi-Fi acessa stream RTSP. | Violação grave de privacidade. | VLAN separada para câmeras. Firewall bloqueando acesso da VLAN IoT/Guest à VLAN Câmeras. | ⚠️ Configuração |
| I-02 | Vazamento de credenciais MQTT | Dispositivo IoT comprometido lê todas as mensagens. | Acesso a estados de sensores e comandos. | ACLs no Mosquitto restringindo tópicos por usuário. TLS no MQTT. | ⚠️ Parcial |
| I-03 | Backup não criptografado | Backup do HA vazado contendo segredos. | Exposição de senhas e chaves. | Backups criptografados com senha forte. | 🔴 Pendente |

### D - Denial of Service (Negação de Serviço)

| ID | Ameaça | Cenário | Impacto | Mitigação | Status |
|----|--------|---------|---------|-----------|--------|
| D-01 | Jamming de Jammer RF | Atacante usa jammer de sinal 2.4GHz. | Perda de todos os sensores Zigbee e Wi-Fi. | Sensores cabeados críticos. Detecção de jamming (LQI drop súbito) e alerta. | 🔴 Pendente |
| D-02 | Corte de energia | Atacante corta energia da residência. | Desligamento do sistema. | Nobreak (UPS) para servidor e roteador. Monitoramento de falha de energia. | ⚠️ Hardware |
| D-03 | Flood de rede | Dispositivo infectado inunda a rede. | Lentidão/travamento do NVR. | Controle de tempestade de broadcast no switch. QoS priorizando tráfego de vídeo. | ⚠️ Configuração |

### E - Elevation of Privilege (Elevação de Privilégio)

| ID | Ameaça | Cenário | Impacto | Mitigação | Status |
|----|--------|---------|---------|-----------|--------|
| E-01 | Escape de container | Atacante compromete container Frigate e acessa host. | Acesso root ao servidor. | Rodar containers como não-root (quando possível). AppArmor/SELinux. Manter Docker/K3s atualizado. | ⚠️ Parcial |
| E-02 | Acesso físico ao console | Atacante conecta teclado/monitor ao servidor. | Acesso administrativo direto. | Proteger BIOS com senha. Desativar boot por USB. Trancar servidor em rack/armário ventilado. | ⚠️ Físico |

---

## 3. Matriz de Prioridade de Riscos

| Risco | Probabilidade | Impacto | Nível | Ação |
|-------|---------------|---------|-------|------|
| **Roubo do servidor (T-03)** | Média | Crítico | **Alto** | Implementar criptografia de disco urgente. |
| **Jamming de RF (D-01)** | Baixa | Crítico | **Alto** | Planear redundância cabeada. |
| **Corte de energia (D-02)** | Média | Alto | **Médio** | Instalar UPS. |
| **Acesso não autorizado (S-03)** | Baixa | Crítico | **Médio** | Manter 2FA e senhas fortes. |

---

## 4. Conclusão e Próximos Passos

O sistema possui boas defesas contra ataques remotos (VPN, sem cloud), mas é **vulnerável a ataques físicos locais** (roubo, corte de energia, jamming).

### Ações Imediatas (Próximas Sprints)
1. **T-053**: Implementar proteção contra tamper/roubo (Criptografia de disco).
2. **T-052**: Pesquisar detecção de jamming via Zigbee2MQTT (LQI monitoring).
3. **T-057**: Criar plano de resposta a incidentes (o que fazer se for invadido?).
