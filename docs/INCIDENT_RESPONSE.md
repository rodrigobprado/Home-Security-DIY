# Plano de Resposta a Incidentes Cibernéticos (IR Plan)

Data: 2026-02-17
Referência: **Tarefa T-057**

Este documento descreve os procedimentos a serem seguidos em caso de suspeita ou confirmação de comprometimento da segurança do sistema Home Security DIY.

---

## 1. Classificação de Incidentes

| Nível | Descrição | Exemplos | Ação Imediata |
|-------|-----------|----------|---------------|
| **Crítico** | Acesso não autorizado confirmado, perda de controle do sistema, vazamento de vídeos. | Login desconhecido no HA, câmeras movendo sozinhas, ransomware. | **Desconectar da Internet** |
| **Alto** | Falha de segurança explorável detectada, indisponibilidade total suspeita. | Serviço exposto na internet sem querer, ataque DDoS local. | **Isolar Rede** |
| **Médio** | Comportamento anômalo de dispositivos, falhas de integridade. | Sensor Zigbee desconectando, logs suspeitos. | **Investigar Logs** |
| **Baixo** | Tentativas de acesso falhas, scans de porta externos. | Logs de "Login failed" no SSH/HA. | **Monitorar** |

---

## 2. Procedimentos de Resposta

### Passo 1: Detecção e Análise

Como saber se algo está errado?
- **Alertas do Home Assistant**: Notificações de "Novo login", "Falha de autenticação".
- **Comportamento das Câmeras**: LEDs de atividade piscando sem motivo, PTZ movendo.
- **Performance**: Lentidão extrema na rede ou no servidor.
- **Logs**: Verificar `/config/home-assistant.log` e logs do sistema (`journalctl -xe`).

### Passo 2: Contenção (STOP THE BLEEDING)

Se confirmado um incidente **Crítico** ou **Alto**:

1. **Cortar o acesso à Internet**:
   - Desconecte o cabo WAN do roteador.
   - OU desligue o modem/ONU.
   - *Objetivo: Impedir exfiltração de dados e comando remoto.*

2. **Isolar o Servidor**:
   - Desconecte o cabo de rede do Mini PC.
   - Se o acesso for físico, mantenha o servidor ligado para análise forense (se tiver conhecimento) ou desligue se o risco de dano for iminente.

3. **Revogar Credenciais**:
   - Se ainda tiver acesso, mude a senha do usuário `admin` do Home Assistant e do Sistema Operacional.
   - Invalidade tokens de longa duração no HA.

### Passo 3: Erradicação

1. **Identificar a causa raiz**:
   - Foi uma porta exposta no roteador?
   - Uma senha fraca?
   - Um dispositivo IoT comprometido?
   - Malware no servidor?

2. **Limpar o sistema**:
   - **Opção A (Segura)**: Reinstalar o SO e restaurar o backup mais recente **pré-incidente**.
   - **Opção B (Arrriscada)**: Tentar remover o malware/backdoor manualmente. *Não recomendado.*

3. **Hardening**:
   - Aplicar correções para a vulnerabilidade explorada (ex: fechar porta, atualizar Docker).
   - Rotacionar TODAS as credenciais (Wi-Fi, MQTT, SSH).

### Passo 4: Recuperação

1. **Restaurar Backup**:
   - Use o backup diário do Home Assistant e Frigate.
2. **Validar Operação**:
   - Verifique se todos os serviços subiram.
   - Teste sensores e câmeras.
3. **Reconectar à Rede**:
   - Apenas após garantir que a vulnerabilidade foi fechada.
   - Monitore o tráfego de rede intensamente nas primeiras 24h.

---

## 3. Preparação (O que ter pronto AGORA)

Para que este plano funcione, você precisa ter:

1. **Backups Automatizados e Testados**:
   - Backup do Home Assistant (Google Drive, NAS).
   - Backup das configurações do Frigate/Zigbee2MQTT.
2. **Acesso Físico**:
   - Monitor e teclado disponíveis para conectar no servidor se a rede cair.
3. **Lista de Inventário**:
   - IPs, MAC addresses e credenciais de todos os dispositivos.

---

## 4. Lições Aprendidas (Post-Mortem)

Após resolver o incidente, documente:
- O que aconteceu?
- Como foi detectado?
- O que funcionou na resposta?
- O que falhou?
- O que faremos para evitar que se repita?

---
*Mantenha uma cópia impressa deste documento.*
