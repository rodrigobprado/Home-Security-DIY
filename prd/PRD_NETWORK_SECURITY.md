# PRD – Segurança de Rede

> Sistema de Home Security – Open Source / Open Hardware
>
> Versão: 1.0 | Data: 2026-02-18 | Responsável: Agente_Documentador

---

## 1. Visão geral

- **Nome do produto/funcionalidade**: Sistema de Segurança de Rede (VLANs, Firewall e VPN)
- **Responsável**: Agente_Arquiteto_Tecnico (especificação), Agente_Documentador (documentação)
- **Data**: 2026-02-18
- **PRDs relacionados**: PRD_LOCAL_PROCESSING_HUB, PRD_VIDEO_SURVEILLANCE_AND_NVR, PRD_BACKUP_AND_RESILIENCE, PRD_SENSORS_AND_ALARMS_PLATFORM

---

## 2. Problema e oportunidade

### 2.1 Problema

Dispositivos IoT e câmeras IP representam vetores de ataque significativos:
- **Câmeras expostas**: Firmware vulnerável pode ser explorado para acesso à rede interna
- **Dispositivos IoT na mesma rede**: Um sensor comprometido pode acessar dados pessoais
- **Acesso remoto inseguro**: Port forwarding expõe serviços diretamente à internet
- **Falta de segmentação**: Todos os dispositivos em uma rede flat sem isolamento
- **Senhas padrão**: Dispositivos mantidos com credenciais de fábrica

### 2.2 Oportunidade

Implementar uma infraestrutura de rede segura com:
- **Segmentação por VLANs** isolando câmeras, IoT, servidor e dispositivos pessoais
- **Firewall com regras restritivas** controlando comunicação entre segmentos
- **VPN para acesso remoto** eliminando port forwarding
- **Bloqueio de internet para IoT/câmeras** impedindo exfiltração de dados
- **Monitoramento de rede** para detectar anomalias

---

## 3. Público-alvo

| Perfil | Necessidades específicas |
|--------|--------------------------|
| **Usuário técnico (TI)** | Configuração avançada, VLANs, firewall |
| **Proprietário com câmeras** | Isolamento de câmeras, acesso remoto seguro |
| **Família conectada** | Rede segura sem complexidade no dia a dia |
| **Preocupado com privacidade** | Bloquear telemetria de dispositivos |

---

## 4. Requisitos funcionais

### 4.1 Segmentação por VLANs

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-001 | VLAN Principal (ID 1) | 192.168.1.0/24 – Dispositivos pessoais, internet completa | Alta |
| RF-002 | VLAN Gestão (ID 10) | 192.168.10.0/24 – Servidor HA, NVR, internet limitada (updates) | Alta |
| RF-003 | VLAN IoT (ID 20) | 192.168.20.0/24 – Sensores Wi-Fi, sem internet | Alta |
| RF-004 | VLAN Câmeras (ID 30) | 192.168.30.0/24 – Câmeras IP, sem internet | Alta |
| RF-005 | VLAN Convidados (ID 40) | 192.168.40.0/24 – Wi-Fi visitantes, internet apenas | Média |
| RF-006 | Switch gerenciável com suporte a VLANs | Mínimo 802.1Q | Alta |
| RF-007 | Roteador/firewall com suporte a VLANs | pfSense, OPNsense ou similar | Alta |

### 4.2 Regras de firewall

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-008 | Câmeras (VLAN 30) → Internet: BLOQUEAR | Zero acesso externo | Alta |
| RF-009 | Câmeras (VLAN 30) → Gestão (VLAN 10): PERMITIR RTSP/ONVIF | TCP 554, 80, 443 | Alta |
| RF-010 | Câmeras (VLAN 30) → Demais VLANs: BLOQUEAR | Isolamento total | Alta |
| RF-011 | IoT (VLAN 20) → Internet: BLOQUEAR | Zero acesso externo | Alta |
| RF-012 | IoT (VLAN 20) → Gestão (VLAN 10): PERMITIR MQTT/HA | TCP 1883, 8123 | Alta |
| RF-013 | IoT (VLAN 20) → Demais VLANs: BLOQUEAR | Isolamento total | Alta |
| RF-014 | Gestão (VLAN 10) → Internet: PERMITIR (limitado) | TCP 443 (updates), NTP, DNS | Alta |
| RF-015 | Gestão (VLAN 10) → Câmeras: PERMITIR (gestão) | Total para gerenciar câmeras | Alta |
| RF-016 | Gestão (VLAN 10) → IoT: PERMITIR | Total para gerenciar IoT | Alta |
| RF-017 | Principal (VLAN 1) → Gestão: PERMITIR dashboard | TCP 8123 (HA), TCP 5000 (Frigate) | Alta |
| RF-018 | Principal (VLAN 1) → Câmeras/IoT: BLOQUEAR | Isolamento | Alta |
| RF-019 | Convidados (VLAN 40) → Todas as VLANs internas: BLOQUEAR | Apenas internet | Média |
| RF-020 | Regra padrão: DENY ALL | Negar tudo que não for explicitamente permitido | Alta |

### 4.3 Acesso remoto via VPN

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-021 | VPN WireGuard configurada | Servidor no roteador/firewall ou HA | Alta |
| RF-022 | Alternativa: Tailscale | Mesh VPN, setup simplificado | Alta |
| RF-023 | Acesso remoto ao dashboard HA | Via VPN, sem port forwarding | Alta |
| RF-024 | Acesso remoto a câmeras | Streaming via VPN | Alta |
| RF-025 | Perfis de acesso VPN | Admin (acesso total) vs. Morador (dashboard apenas) | Média |
| RF-026 | Autenticação forte | Certificados (WireGuard) ou SSO (Tailscale) | Alta |
| RF-027 | Logs de conexão VPN | Registrar todas as conexões com timestamp | Média |
| RF-028 | Nunca expor via port forwarding | REGRA-PRIV-05 | Alta |

### 4.4 Segurança Wi-Fi

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-029 | Wi-Fi principal: WPA3 (ou WPA2-AES mínimo) | Para dispositivos pessoais | Alta |
| RF-030 | Wi-Fi IoT: rede separada | SSID dedicado na VLAN 20 | Alta |
| RF-031 | Wi-Fi convidados: isolamento de clientes | Client isolation habilitado | Média |
| RF-032 | SSID IoT oculto (opcional) | Não transmitir nome da rede IoT | Baixa |
| RF-033 | Desabilitar WPS | Vulnerável a ataque de brute force | Alta |
| RF-034 | MAC filtering (opcional) | Camada adicional para IoT | Baixa |

### 4.5 Hardening de dispositivos

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-035 | Trocar todas as senhas padrão | REGRA-IOT-01: Nunca manter senhas de fábrica | Alta |
| RF-036 | Desabilitar Telnet, FTP, UPnP | REGRA-IOT-02: Serviços desnecessários | Alta |
| RF-037 | Atualizar firmware periodicamente | REGRA-IOT-05: Verificar mensalmente | Alta |
| RF-038 | Inventário de dispositivos | REGRA-IOT-06: Documentar MAC, IP, firmware | Alta |
| RF-039 | Desabilitar telemetria | REGRA-PRIV-03: Phone home bloqueado | Alta |
| RF-040 | Desabilitar SNMP se não usado | Reduzir superfície de ataque | Média |

### 4.6 Monitoramento e detecção

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-041 | Monitorar tráfego de rede entre VLANs | Logs no firewall | Média |
| RF-042 | Alerta de novo dispositivo na rede | DHCP new lease notification | Média |
| RF-043 | Alerta de tentativa de acesso bloqueada | Log de firewall rules dropped | Média |
| RF-044 | Monitorar banda por VLAN | Identificar anomalias de tráfego | Baixa |
| RF-045 | Bloqueio automático de IP com muitas tentativas | Fail2ban ou similar | Média |

---

## 5. Requisitos não funcionais

### 5.1 Performance

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-001 | Throughput inter-VLAN | > 800 Mbps (Gigabit) |
| RNF-002 | Latência de streaming de câmera | < 5ms adicional por VLAN routing |
| RNF-003 | VPN throughput | > 50 Mbps (suficiente para streaming) |
| RNF-004 | Latência VPN | < 50ms (para controle em tempo real) |

### 5.2 Confiabilidade

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-005 | Uptime da rede | > 99.9% |
| RNF-006 | Backup de configuração do firewall | Diário, automatizado |
| RNF-007 | Recuperação de falha de roteador | < 30 minutos com backup |

### 5.3 Segurança

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-008 | Política padrão de firewall | Deny all, allow by exception |
| RNF-009 | Logs de firewall retidos | Mínimo 30 dias |
| RNF-010 | Acesso ao firewall/roteador | Apenas via VLAN de gestão, HTTPS |
| RNF-011 | Certificados VPN | Rotação anual recomendada |

### 5.4 Conformidade

| ID | Requisito | Norma/Regra |
|----|-----------|-------------|
| RNF-012 | Senhas de dispositivos | REGRA-IOT-01 |
| RNF-013 | Serviços desabilitados | REGRA-IOT-02 |
| RNF-014 | Bloqueio de internet IoT | REGRA-IOT-03 |
| RNF-015 | Acesso remoto via VPN | REGRA-PRIV-05 |
| RNF-016 | Câmeras sem internet | REGRA-PRIV-02 |

---

## 6. Arquitetura técnica

### 6.1 Diagrama de rede

```
                        INTERNET
                           │
                    ┌──────▼──────┐
                    │   MODEM     │
                    │   ISP       │
                    └──────┬──────┘
                           │
                    ┌──────▼──────────────────────────────┐
                    │        FIREWALL / ROTEADOR            │
                    │    (pfSense / OPNsense / Mikrotik)   │
                    │                                       │
                    │  ┌─────────┐  ┌─────────┐            │
                    │  │WireGuard│  │Failover │            │
                    │  │  VPN    │  │  4G     │            │
                    │  └─────────┘  └─────────┘            │
                    │                                       │
                    │  Interfaces VLAN:                     │
                    │  VLAN 1  - 192.168.1.0/24  (Princ.)  │
                    │  VLAN 10 - 192.168.10.0/24 (Gestão)  │
                    │  VLAN 20 - 192.168.20.0/24 (IoT)     │
                    │  VLAN 30 - 192.168.30.0/24 (Câmeras) │
                    │  VLAN 40 - 192.168.40.0/24 (Convidado)│
                    └──────┬──────────────────────────────┘
                           │ Trunk (802.1Q)
                    ┌──────▼──────┐
                    │  SWITCH     │
                    │ GERENCIÁVEL │
                    │ (VLAN-aware)│
                    └──┬──┬──┬──┬┘
                       │  │  │  │
            ┌──────────┘  │  │  └──────────┐
            │             │  │             │
     ┌──────▼──────┐     │  │      ┌──────▼──────┐
     │ VLAN 1      │     │  │      │ VLAN 40     │
     │ Notebooks   │     │  │      │ Convidados  │
     │ Celulares   │     │  │      │ (Wi-Fi)     │
     │ (Wi-Fi/Eth) │     │  │      └─────────────┘
     └─────────────┘     │  │
                   ┌─────▼──▼──────┐
                   │               │
            ┌──────▼──────┐ ┌──────▼──────┐
            │ VLAN 10     │ │ VLAN 30     │
            │ Mini PC     │ │ Switch PoE  │
            │ (Servidor)  │ │ (Câmeras)   │
            │             │ │             │
            │ HA, Frigate │ │ CAM 1..N    │
            │ Z2M, MQTT   │ │ (sem internet)│
            └─────────────┘ └─────────────┘
```

### 6.2 Tabela de regras de firewall detalhada

```
# ═══════════════════════════════════════════════════════
# REGRAS DE FIREWALL - ORDEM DE PRIORIDADE
# ═══════════════════════════════════════════════════════

# --- VLAN CÂMERAS (30) ---
ALLOW  VLAN30 → VLAN10:554    # RTSP para Frigate
ALLOW  VLAN30 → VLAN10:80     # HTTP para ONVIF
ALLOW  VLAN30 → VLAN10:443    # HTTPS para ONVIF
DENY   VLAN30 → ANY           # Bloquear todo o resto

# --- VLAN IoT (20) ---
ALLOW  VLAN20 → VLAN10:1883   # MQTT para Mosquitto
ALLOW  VLAN20 → VLAN10:8123   # HA para dispositivos Wi-Fi
DENY   VLAN20 → ANY           # Bloquear todo o resto

# --- VLAN GESTÃO (10) ---
ALLOW  VLAN10 → INTERNET:443  # Updates (HTTPS)
ALLOW  VLAN10 → INTERNET:123  # NTP (sincronização)
ALLOW  VLAN10 → INTERNET:53   # DNS
ALLOW  VLAN10 → VLAN30:ANY    # Gerenciar câmeras
ALLOW  VLAN10 → VLAN20:ANY    # Gerenciar IoT
ALLOW  VLAN10 → VLAN1:ANY     # Servir dashboard
DENY   VLAN10 → ANY           # Bloquear resto

# --- VLAN PRINCIPAL (1) ---
ALLOW  VLAN1 → INTERNET:ANY   # Acesso total à internet
ALLOW  VLAN1 → VLAN10:8123    # Dashboard HA
ALLOW  VLAN1 → VLAN10:5000    # UI Frigate
ALLOW  VLAN1 → VLAN10:8080    # Z2M Dashboard
DENY   VLAN1 → VLAN20:ANY     # Sem acesso direto a IoT
DENY   VLAN1 → VLAN30:ANY     # Sem acesso direto a câmeras

# --- VLAN CONVIDADOS (40) ---
ALLOW  VLAN40 → INTERNET:ANY  # Acesso à internet
DENY   VLAN40 → RFC1918:ANY   # Bloquear redes privadas
```

### 6.3 Configuração VPN WireGuard (exemplo)

```ini
# /etc/wireguard/wg0.conf (servidor - no firewall)

[Interface]
Address = 10.10.10.1/24
PrivateKey = <chave_privada_servidor>
ListenPort = 51820
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT

# Perfil Admin - acesso total
[Peer]
PublicKey = <chave_publica_admin>
AllowedIPs = 10.10.10.2/32
PresharedKey = <psk>

# Perfil Morador - acesso ao dashboard
[Peer]
PublicKey = <chave_publica_morador>
AllowedIPs = 10.10.10.3/32
PresharedKey = <psk>
```

---

## 7. Produtos/componentes recomendados

### 7.1 Roteador/Firewall

| Modelo | Tipo | Preço estimado | Observações |
|--------|------|----------------|-------------|
| **Mini PC N100 + OPNsense** | Appliance DIY | R$ 800-1.200 | Máxima flexibilidade, 2+ NICs |
| **Mikrotik hAP ac3** | Roteador | R$ 400-600 | VLANs, firewall, failover 4G |
| **Mikrotik RB5009** | Roteador avançado | R$ 800-1.200 | 10Gbps, ideal para muitas VLANs |
| **TP-Link ER605** | Roteador | R$ 250-400 | Multi-WAN, VLANs básicas |
| **Ubiquiti EdgeRouter X** | Roteador | R$ 300-500 | VLANs, firewall, CLI |

### 7.2 Switch gerenciável

| Modelo | Portas | Preço estimado | Observações |
|--------|--------|----------------|-------------|
| **TP-Link TL-SG108E** | 8 (gerenciável) | R$ 200-300 | VLANs 802.1Q, econômico |
| **TP-Link TL-SG116E** | 16 (gerenciável) | R$ 350-500 | Para instalações maiores |
| **Ubiquiti USW-Lite-8-PoE** | 8 (4 PoE) | R$ 700-900 | PoE + VLANs |
| **Mikrotik CSS610-8G-2S+** | 8 + 2 SFP+ | R$ 500-700 | Avançado, 10Gbps uplink |

### 7.3 Access Point Wi-Fi

| Modelo | Padrão | Preço estimado | Observações |
|--------|--------|----------------|-------------|
| **TP-Link EAP245** | Wi-Fi 5 AC | R$ 350-500 | Multi-SSID, VLANs |
| **TP-Link EAP670** | Wi-Fi 6 AX | R$ 600-900 | Multi-SSID, VLANs, WPA3 |
| **Ubiquiti U6-Lite** | Wi-Fi 6 | R$ 500-700 | Integração UniFi |
| **Ubiquiti U6-Pro** | Wi-Fi 6 | R$ 800-1.200 | Alto desempenho |

### 7.4 Software

| Ferramenta | Função | Custo |
|------------|--------|-------|
| **OPNsense** | Firewall/roteador | Gratuito (open source) |
| **pfSense** | Firewall/roteador | Gratuito (CE) |
| **WireGuard** | VPN | Gratuito |
| **Tailscale** | Mesh VPN | Gratuito (até 100 dispositivos) |
| **Pi-hole** | DNS filtering + ad blocking | Gratuito |

---

## 8. Estimativas por cenário

### 8.1 Cenário rural (rede completa)

| Componente | Preço estimado |
|------------|----------------|
| Roteador Mikrotik hAP ac3 (firewall + VLANs) | R$ 500 |
| Switch gerenciável 8 portas (TP-Link SG108E) | R$ 250 |
| Switch PoE 8 portas (câmeras) | R$ 400 |
| Access Point Wi-Fi (TP-Link EAP245) | R$ 400 |
| Cabeamento Cat6 (200m) | R$ 400 |
| Configuração e teste | R$ 200 (materiais) |
| **Total rede rural** | **R$ 2.150** |

### 8.2 Cenário casa urbana

| Componente | Preço estimado |
|------------|----------------|
| Roteador com VLANs (TP-Link ER605) | R$ 300 |
| Switch gerenciável 8 portas | R$ 250 |
| Switch PoE 8 portas (câmeras) | R$ 400 |
| Access Point Wi-Fi | R$ 400 |
| Cabeamento Cat6 (100m) | R$ 200 |
| **Total rede urbana** | **R$ 1.550** |

### 8.3 Cenário apartamento (simplificado)

| Componente | Preço estimado |
|------------|----------------|
| Roteador com VLANs (TP-Link ER605) | R$ 300 |
| Switch gerenciável 5 portas | R$ 150 |
| Access Point Wi-Fi (se necessário) | R$ 400 |
| **Total rede apartamento** | **R$ 450-850** |

---

## 9. Critérios de aceitação

| ID | Critério | Método de verificação |
|----|----------|----------------------|
| CA-001 | VLANs configuradas e funcionando (4 mínimo) | Teste de ping entre VLANs |
| CA-002 | Câmeras não conseguem acessar internet | Teste de ping/traceroute da câmera |
| CA-003 | IoT não consegue acessar internet | Teste de ping/traceroute do dispositivo |
| CA-004 | Câmeras acessíveis pelo Frigate via RTSP | Teste de streaming |
| CA-005 | Dashboard HA acessível pela VLAN principal | Teste de acesso web |
| CA-006 | VPN WireGuard funciona externamente | Teste fora da rede local |
| CA-007 | Convidados não acessam rede interna | Teste de scan de rede |
| CA-008 | Firewall bloqueia tráfego não autorizado | Teste com nmap entre VLANs |
| CA-009 | Todas as senhas padrão alteradas | Auditoria de dispositivos |
| CA-010 | Wi-Fi com WPA3 (ou WPA2-AES) | Verificação de configuração |

---

## 10. Métricas de sucesso

| Métrica | Alvo | Medição |
|---------|------|---------|
| **Dispositivos com senha padrão** | 0 | Auditoria trimestral |
| **VLANs corretamente isoladas** | 100% | Teste de penetração |
| **Uptime da rede** | > 99.9% | Monitoramento |
| **Acessos VPN bem-sucedidos** | > 99% | Logs |
| **Incidentes de segurança de rede** | 0 | Monitoramento de logs |

---

## 11. Riscos e dependências

### 11.1 Riscos

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Configuração errada de VLAN isola serviço | Média | Alto | Testar exaustivamente, backup de config |
| Firewall muito restritivo impede funcionalidade | Média | Médio | Adicionar regras incrementalmente, testar cada uma |
| VPN com latência alta para streaming | Média | Médio | Usar Tailscale para otimização de rota |
| Switch não suporta 802.1Q corretamente | Baixa | Alto | Verificar compatibilidade antes de comprar |
| Complexidade dificulta manutenção | Alta | Médio | Documentar toda a configuração |

### 11.2 Dependências

| Dependência | Tipo | PRD relacionado |
|-------------|------|-----------------|
| Hardware de rede (switch, roteador) | Infraestrutura | - |
| Servidor central (Mini PC) | Infraestrutura | PRD_LOCAL_PROCESSING_HUB |
| Câmeras IP (PoE) | Dispositivos | PRD_VIDEO_SURVEILLANCE_AND_NVR |
| Sensores Wi-Fi | Dispositivos | PRD_SENSORS_AND_ALARMS_PLATFORM |
| Failover 4G | Resiliência | PRD_BACKUP_AND_RESILIENCE |

---

## 12. Referências

### Documentos do projeto
- `docs/ARQUITETURA_TECNICA.md` - Seção 7 (Arquitetura de rede segura)
- `rules/RULES_COMPLIANCE_AND_STANDARDS.md` - REGRA-IOT-*, REGRA-PRIV-*

### Externos
- [OPNsense Documentation](https://docs.opnsense.org/)
- [WireGuard VPN](https://www.wireguard.com/)
- [Tailscale](https://tailscale.com/)
- [OWASP IoT Top 10](https://owasp.org/www-project-internet-of-things/)
- [VLAN Security Best Practices - Cisco](https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst4500/12-2/25ew/configuration/guide/conf/vlans.html)

---

> **Status**: Rascunho v1.0
>
> **Próxima revisão**: Após validação pelo Agente_Arquiteto_Tecnico
