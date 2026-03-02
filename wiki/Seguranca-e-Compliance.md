# Segurança e Compliance

O sistema Home Security DIY adota **defesa em profundidade** em duas dimensões: segurança física (coberta em [Cenários Residenciais](Cenarios-Residenciais) e [Resiliência](Resiliencia)) e **segurança cibernética**, detalhada nesta página.

---

## Responsible Disclosure

- Política oficial em `SECURITY.md`.
- Canal privado para reporte: GitHub Security Advisory (`/security/advisories/new`).
- SLA de resposta definido por severidade (Crítica/Alta/Média/Baixa) com prazos de confirmação e correção.

## Princípios

| Princípio | Descrição |
|-----------|-----------|
| **Privacidade por design** | Todo o processamento é local. Nenhum dado é enviado para servidores externos. |
| **Defesa em profundidade** | Múltiplas camadas: físico → rede → sistema → aplicação. |
| **Mínimo privilégio** | Cada componente acessa apenas o que precisa. Usuários separados por serviço. |
| **Segmentação de rede** | VLANs isoladas: câmeras, IoT e gestão em redes separadas. |
| **Zero trust local** | Câmeras e dispositivos IoT não têm acesso à internet por padrão. |

---

## Compliance Operacional (T-047 a T-053)

Além da camada técnica já implementada, o projeto possui runbooks operacionais para coleta de evidências e fechamento de conformidade em campo:

- LGPD operacional (câmeras): `docs/LGPD_OPERATIONAL_EVIDENCE_RUNBOOK.md`
- Regulatório UAV (ANAC/SISANT/DECEA/ANATEL): `docs/UAV_REGULATORY_EVIDENCE_RUNBOOK.md`
- Jurídico + técnico do módulo de defesa: `docs/DEFENSE_LEGAL_EVIDENCE_RUNBOOK.md`
- Hardening físico recorrente: `docs/PHYSICAL_HARDENING_OPERATIONS_RUNBOOK.md`
- Rede em produção (VLAN/TLS/TOTP/SSH): `docs/NETWORK_PRODUCTION_VALIDATION_PLAYBOOK.md`
- Smoke de integração em ambiente real: `docs/INTEGRATION_SMOKE_PRODUCTION_RUNBOOK.md`
- Revisão semestral Matter/Thread: `docs/MATTER_THREAD_SEMESTER_REVIEW_RUNBOOK.md`

Templates de execução/evidência: `tasks/templates/`.

Checklist de conformidade (`rules/RULES_COMPLIANCE_AND_STANDARDS.md`):
- itens de pós-instalação e pós-instalação (drones) marcados como concluídos com evidências operacionais e testes de contrato.
- mapeamento de normas ISO 27001/NBR 9050 consolidado em `standards/STANDARDS_TO_RESEARCH.md` com checklist de aplicação.

---

## Modelo de Ameaças (STRIDE)

Metodologia: **STRIDE** (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege).

### Análise completa

| ID | Categoria | Ameaça | Impacto | Mitigação | Status |
|----|-----------|--------|---------|-----------|--------|
| S-01 | Spoofing | Sensor Zigbee malicioso introduzido na rede | Injeção de dados falsos | Zigbee 3.0 + permit_join apenas temporário | ⚠️ Parcial |
| S-02 | Spoofing | Substituição do feed de câmera por vídeo em loop | Cegueira do sistema | Autenticação ONVIF + Port Security no switch | 🔴 Pendente |
| S-03 | Spoofing | Acesso não autorizado ao dashboard HA | Controle total do sistema | MFA + Fail2Ban | ✅ Implementado |
| T-01 | Tampering | Corte de cabo de câmera externa | Perda de visibilidade | Alerta "Câmera Offline" + edge recording SD | ✅ Implementado |
| T-02 | Tampering | Adulteração de arquivos de log | Perda de auditoria | Syslog remoto ou partição somente leitura | 🔴 Pendente |
| T-03 | Tampering | Roubo do servidor | Perda total de evidências | Criptografia de disco LUKS + backup off-site | 🔴 Pendente |
| R-01 | Repudiation | Usuário desativa alarme e nega | Falta de responsabilização | Log de auditoria imutável + usuários individuais | ✅ Implementado |
| I-01 | Info Disclosure | Interceptação de stream RTSP | Violação de privacidade | VLAN separada para câmeras + firewall | ⚠️ Configuração |
| I-02 | Info Disclosure | Vazamento de credenciais MQTT | Acesso a sensores/comandos | ACLs no Mosquitto + TLS (porta 8883 disponível) | ✅ Implementado |
| I-03 | Info Disclosure | Backup não criptografado vazado | Exposição de senhas e chaves | Backups criptografados com AES-256 (`BACKUP_ENCRYPTION_PASSPHRASE`) | ✅ Implementado |
| D-01 | DoS | Jamming RF 2,4 GHz | Perda de todos os sensores Zigbee/Wi-Fi | Sensores cabeados críticos + detecção de LQI | 🔴 Pendente |
| D-02 | DoS | Corte de energia | Desligamento do sistema | Nobreak (UPS) 1500 VA | ⚠️ Hardware |
| D-03 | DoS | Flood de rede | Travamento do NVR | QoS + controle de broadcast no switch | ⚠️ Configuração |
| E-01 | Elevation | Escape de container Docker | Acesso root ao servidor | AppArmor/SELinux + containers não-root (`appuser`) + `cap_drop: ALL` + `no-new-privileges` | ✅ Implementado |
| E-02 | Elevation | Acesso físico ao console do servidor | Acesso administrativo direto | Senha de BIOS + boot USB desativado + servidor trancado | ⚠️ Físico |

### Matriz de prioridade de riscos

| Risco | Probabilidade | Impacto | Nível | Ação |
|-------|---------------|---------|-------|------|
| Roubo do servidor (T-03) | Média | Crítico | **Alto** | Implementar LUKS urgente |
| Jamming RF (D-01) | Baixa | Crítico | **Alto** | Sensores cabeados em pontos críticos |
| Corte de energia (D-02) | Média | Alto | **Médio** | Instalar UPS 1500 VA |
| Acesso não autorizado ao HA (S-03) | Baixa | Crítico | **Médio** | Manter 2FA e senhas fortes |

---

## Auditoria Red Team — Issues #7–#77 (2026-02)

Em fevereiro de 2026 foi realizada uma auditoria red team completa do codebase. Foram identificadas e corrigidas **25 vulnerabilidades** (4 críticas, 5 altas, 10 médias, 6 baixas). Todas as issues foram fechadas no commit `f4f743d`.

### Correções aplicadas

| Camada | Correção | Issues |
|--------|----------|--------|
| **Drones** | Validação HMAC-SHA256 em produção (UGV e UAV): `source_id` + drift de timestamp (30s anti-replay) + assinatura do payload. Startup falha sem `COMMAND_HMAC_SECRET_*` configurado. | #11, #76 |
| **Drones** | PIN de defesa obrigatório por variável de ambiente, sem valor padrão. Rate limiting: 3 tentativas → lockout de 5 minutos. | #7, #22 |
| **Dashboard API** | Autenticação por `X-API-Key` ou Bearer token em todas as rotas. WebSocket autenticado antes de `accept()`. Startup falha sem `DASHBOARD_API_KEY` e `HA_TOKEN`. | #8, #28 |
| **Dashboard API** | CORS restrito a `DASHBOARD_ALLOWED_ORIGINS` (não mais `["*"]`). Whitelist de câmeras para evitar SSRF. | #9, #17 |
| **Containers** | Usuário não-root (`appuser:appgroup`) no Dockerfile do dashboard. `cap_drop: ALL`, `no-new-privileges: true` em todos os serviços Docker e K8s. Frigate sem `privileged: true`. | #15, #26 |
| **Nginx** | Security headers completos: `Content-Security-Policy`, `HSTS`, `X-Frame-Options: DENY`, `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy`. | #16 |
| **Docker Compose** | Portas MQTT, Zigbee2MQTT e Frigate vinculadas a loopback (`127.0.0.1`). Healthcheck do Mosquitto sem credenciais expostas. Versões de imagens fixadas em semver. | #10, #12, #20, #23 |
| **Credenciais** | `admin:password` das câmeras substituídos por `CHANGE_ME_*` em todos os arquivos (`.env.example`, K8s Secret do Frigate). | #29, #77 |
| **Scripts K8s** | `generate-k8s-secrets.sh` gera Secrets localmente a partir do `.env`. Em produção, padrão operacional é `External Secrets Operator` (`k8s/overlays/production/external-secrets.yaml`). | #13, #613 |
| **MQTT TLS** | Bloco TLS comentado adicionado ao `mosquitto.conf` (porta 8883). Script `generate-mqtt-certs.sh` gera CA + certificado auto-assinado. | #10 |
| **Home Assistant** | `trusted_proxies` restrito a `127.0.0.1` e `172.17.0.1`. Recorder usando PostgreSQL via `!env_var`. | #18, #25 |
| **K8s / CI** | Ingress com TLS (`home-security-tls`). Snyk CI com paths corretos. | #24, #27 |
| **Backup** | `.env` excluído do backup. Criptografia AES-256 via `BACKUP_ENCRYPTION_PASSPHRASE`. `.gitignore` protege chaves MQTT e secrets gerados. | #14 |

### Variáveis de ambiente obrigatórias após auditoria

```bash
# Nunca usar valores padrão ou CHANGE_ME em produção
DASHBOARD_API_KEY=<openssl rand -hex 32>
DEFENSE_PIN_UGV=<pin numérico único>
DEFENSE_PIN_UAV=<pin numérico único>
COMMAND_HMAC_SECRET_UGV=<openssl rand -hex 32>
COMMAND_HMAC_SECRET_UAV=<openssl rand -hex 32>
BACKUP_ENCRYPTION_PASSPHRASE=<senha forte>
```

> **Atenção:** O sistema recusa inicialização se qualquer um desses valores estiver ausente ou contiver `CHANGE_ME`/`UNCONFIGURED`.

## Gestão de segredos no Dashboard (Issue #715)

- `k8s/base/dashboard/dashboard.yaml` não versiona mais valores sensíveis em texto claro.
- A API do dashboard passa a consumir `HA_TOKEN`, `DATABASE_URL`, `DASHBOARD_API_KEY` e `DASHBOARD_ADMIN_KEY` exclusivamente por `secretKeyRef`.
- O proxy frontend (`nginx.conf.template`) não injeta mais `X-API-Key` estático.
- O pipeline de validação executa `scripts/check-hardcoded-secrets.sh` para bloquear placeholders e credenciais hardcoded em arquivos YAML/CONF alterados.

## Autenticação WebSocket no browser (Issue #716)

- O endpoint `/ws` aceita autenticação por query token (`?token=`) para navegadores que não conseguem enviar `X-API-Key` no handshake.
- Fluxos não-browser continuam suportando `X-API-Key` e `Authorization: Bearer`.
- Há teste automatizado cobrindo conexão autenticada com recebimento do evento inicial (`initial_state`).

## Paridade de autenticação dev/prod (Issue #717)

- Frontend passou a usar util único (`apiFetch` + token bearer) para chamadas REST e WebSocket.
- O fluxo de autenticação agora é do cliente para backend em ambos os ambientes (Vite e Nginx), sem injeção de chave estática no proxy.
- Teste de contrato valida que `vite.config.js` e `nginx.conf.template` não injetam headers de autenticação.

## Auditoria de IP com trusted proxies (Issue #718)

- A trilha de auditoria de ativos passou a usar `TRUSTED_PROXY_IPS` para decidir quando aceitar `X-Forwarded-For`.
- Quando a origem não é proxy confiável, o sistema registra `request.client.host` como IP efetivo.
- A cadeia normalizada de forwarding (`X-Forwarded-For`) é persistida separadamente em `asset_audit.actor_ip_chain`.
- Testes cobrem cenários com proxy confiável e sem proxy confiável.

## Observabilidade de integrações críticas (Issue #719)

- Rotas e clientes de integração (HA, Frigate e WebSocket) deixaram de usar `except Exception` genérico e `pass` silencioso.
- Falhas de integração agora geram log estruturado com contexto de erro.
- Métricas de falha foram expostas em `/api/services/ws-metrics` para HA/Frigate/checagem de status.
- Teste de contrato garante ausência de swallow genérico nos caminhos críticos de integração.

## RBAC admin para configuração de mapa (Issue #720)

- O endpoint `PUT /api/map/config` agora exige `require_admin_key`.
- Leitura de mapa (`GET /api/map/config`) permanece disponível no perfil operator.
- Testes cobrem cenários de autorização do `PUT` para 403, 503 e 200.
- O frontend passou a enviar `X-Admin-Key` para mutações do mapa quando a chave admin está presente em sessão.

---

## Hardening do Servidor

### Criptografia de disco (LUKS)

A medida mais eficaz contra roubo de dados e alteração offline.

1. Ao instalar Linux, selecione **"Guided - use entire disk and set up encrypted LVM"**
2. Configure Dropbear SSH para unlock remoto em servidores headless:

```bash
sudo apt install dropbear-initramfs
# Adicionar chave pública em /etc/dropbear-initramfs/authorized_keys
sudo update-initramfs -u

# No boot, conectar via SSH e digitar:
cryptroot-unlock
```

### BIOS/UEFI

| Medida | Objetivo |
|--------|----------|
| Senha de administrador na BIOS | Impedir alteração da ordem de boot |
| Secure Boot habilitado | Impedir bootloaders não assinados |
| Boot USB desativado | Evitar ataque via Live Linux |

### Segurança física do hardware

| Prática | Descrição |
|---------|-----------|
| Localização oculta | Forro, armário embutido, nicho com porta — nunca sala/rack visível |
| Fixação física | Parafusado na parede ou prateleira (Kensington Lock se suportado) |
| Sem identificação visual | Sem etiquetas, sem LEDs visíveis |
| Tamper switch (avançado) | Sensor de abertura do case conectado a GPIO; aciona pânico se aberto |

### Backup off-site automatizado

```bash
# rclone sincroniza clipes Frigate a cada 10 min para bucket S3/B2 criptografado
*/10 * * * * rclone copy /media/frigate/clips remote:bucket-seguranca --transfers 4
```

---

## Segmentação de Rede (VLANs)

| VLAN | Rede | Uso | Acesso à Internet |
|------|------|-----|-------------------|
| 1 (Principal) | 192.168.1.0/24 | Dispositivos de usuário | Sim |
| 10 (Gestão) | 192.168.10.0/24 | Servidor HA, Mini PC | Via VPN apenas |
| 20 (IoT) | 192.168.20.0/24 | Sensores, dispositivos smart | **NÃO** |
| 30 (Câmeras) | 192.168.30.0/24 | Câmeras IP PoE | **NÃO** |

**Regras de firewall obrigatórias:**
- VLAN 30 → WAN: `DENY ALL`
- VLAN 20 → WAN: `DENY ALL`
- Acesso remoto: **exclusivamente via VPN** (WireGuard/Tailscale)
- Port forwarding direto: **PROIBIDO**

Checklist de validação da segmentação:
- [x] Política de backup off-site agendada e validada
- [x] VLAN 10 definida para gestão com acesso controlado
- [x] VLAN 20 definida para IoT sem acesso à internet
- [x] VLAN 30 definida para câmeras sem acesso à internet
- [x] Regra `VLAN 30 -> WAN: DENY ALL` aplicada
- [x] Regra `VLAN 20 -> WAN: DENY ALL` aplicada
- [x] Acesso remoto restrito a VPN
- [x] Port forwarding direto desabilitado

---

## Checklist de Hardening Preventivo

### Gerenciamento de senhas

- [x] Mínimo 16 caracteres para serviços críticos (HA, SSH, MQTT)
- [x] Senha única por serviço (nunca reutilizar)
- [x] Gerenciador de senhas em uso (Bitwarden, KeePass)
- [x] **Todas** as credenciais padrão de fábrica alteradas (câmeras, roteador, switch)
- [x] Credenciais do HA em `secrets.yaml` — nunca hardcoded

### Autenticação de dois fatores (2FA)

- [x] Home Assistant: TOTP habilitado para todos os usuários
- [x] VPN WireGuard: chave criptográfica (inerente ao protocolo)
- [x] SSH: chave pública Ed25519 — login por senha desabilitado

### Acesso SSH

- [x] `PasswordAuthentication no`
- [x] `PermitRootLogin no`
- [x] Porta não padrão (ex.: 2222)
- [x] Fail2ban configurado (bloqueio após 3 tentativas)
- [x] Chave Ed25519 ou RSA 4096 bits

### Firewall e rede

- [x] VLAN 30 (câmeras) sem acesso à internet
- [x] VLAN 20 (IoT) sem acesso à internet
- [x] UPnP desabilitado no roteador
- [x] Port forwarding: nenhum
- [x] Gerenciamento do roteador apenas pela LAN

### Firmware e atualizações

| Dispositivo | Frequência |
|-------------|------------|
| Home Assistant OS | Mensal |
| Frigate, Zigbee2MQTT | Mensal |
| Firmware de câmeras | Mensal |
| Firmware do roteador | Mensal |
| Coordenador Zigbee | Trimestral |
| BIOS/UEFI do Mini PC | Trimestral |

> CVEs com CVSS ≥ 9.0: aplicar em até **48 horas**.

### Rede Zigbee

- [x] `permit_join: false` como padrão permanente
- [x] Pareamento habilitado apenas temporariamente e de forma supervisionada
- [x] Inventário de endereços IEEE de todos os dispositivos legítimos

### Backup e criptografia

- [x] Backup automático do HA (diário, retenção 30 dias)
- [x] Cópia off-site (NAS, nuvem criptografada ou mídia removível)
- [x] Criptografia AES-256 para backups em nuvem
- [x] Teste de restauração trimestral
- [x] Backup da configuração do roteador após cada alteração

### Rotação e retenção de logs

| Log | Retenção |
|-----|----------|
| Home Assistant | 90 dias |
| Frigate | 60 dias |
| Zigbee2MQTT | 30 dias |
| Syslog / auth.log | 90 dias |
| Logs do firewall | 90 dias |
| Eventos de alarme | 1 ano |

---

## Plano de Resposta a Incidentes Cibernéticos

### Framework PICERL

O processo segue o padrão NIST SP 800-61 adaptado para uso residencial.

| Fase | Objetivo |
|------|----------|
| **Preparation** | Implementar hardening, backups, ferramentas de monitoramento |
| **Identification** | Detectar e classificar o incidente |
| **Containment** | Limitar o dano e impedir propagação |
| **Eradication** | Remover completamente a causa |
| **Recovery** | Restaurar operação normal |
| **Lessons Learned** | Documentar e melhorar (prazo: 7 dias após o incidente) |

### Cenários cobertos

| # | Cenário | Severidade |
|---|---------|------------|
| 2.1 | Acesso não autorizado ao Home Assistant | Crítica |
| 2.2 | Câmera IP comprometida (firmware malicioso, botnet Mirai) | Alta |
| 2.3 | Dispositivo Zigbee comprometido na rede mesh | Alta |
| 2.4 | Ransomware no servidor central | Crítica |
| 2.5 | Ataque Man-in-the-Middle (MitM) na rede local | Alta |
| 2.6 | Dispositivo não autorizado na rede (Rogue Device) | Média-Alta |
| 2.7 | DNS Hijacking / Comprometimento do roteador | Crítica |

### Ações imediatas por tipo de incidente

| Tipo | Contenção imediata |
|------|--------------------|
| Acesso não autorizado ao HA | Revogar todos os tokens + forçar logout + desconectar WireGuard |
| Câmera comprometida | Desconectar porta PoE ou desabilitar porta no switch |
| Dispositivo Zigbee suspeito | Desabilitar `permit_join` + desemparelhar o dispositivo |
| Ransomware | **Desconectar da rede imediatamente** — não desligar (preservar evidências) |
| MitM / ARP spoofing | Bloquear MAC do atacante + forçar ARP estático no gateway |
| Rogue device | Desabilitar porta do switch + registrar MAC, IP, horário |
| Roteador comprometido | Desconectar cabo WAN + reset de fábrica se credenciais alteradas |

### Indicadores de comprometimento (IoC) — resumo

| IoC | Onde verificar |
|-----|----------------|
| Logins de IPs desconhecidos | `home-assistant.log` |
| Tráfego de saída da VLAN 30 | Logs do firewall, ntopng |
| Dispositivo Zigbee desconhecido | Dashboard Zigbee2MQTT |
| Arquivos com extensão `*.encrypted` | Sistema de arquivos |
| Alertas de conflito ARP | arpwatch, logs do roteador |
| Novo MAC na rede | arpwatch, scan nmap |
| Servidores DNS alterados no roteador | Interface admin do roteador |

### Ferramentas de monitoramento recomendadas

| Ferramenta | Função | Quando instalar |
|------------|--------|-----------------|
| **arpwatch** | Detecta novos dispositivos e mudanças de MAC/IP | Imediatamente |
| **nmap** (cron semanal) | Inventário de rede e portas abertas | Imediatamente |
| **Suricata / Snort** | IDS/IPS — detecção de assinaturas de ataque | Avançado |
| **ntopng** | Análise de tráfego por VLAN em tempo real | Recomendado |
| **Pi-hole** | DNS local com log de consultas | Recomendado |
| **AIDE / Tripwire** | Verificação de integridade de arquivos | Avançado |

---

## Regras Derivadas de Segurança Cibernética

```
REGRA-CIBER-01: Todo acesso remoto ao Home Assistant e serviços DEVE ser via VPN
(WireGuard ou Tailscale). Port forwarding direto é PROIBIDO.

REGRA-CIBER-02: Câmeras IP (VLAN 30) e dispositivos IoT (VLAN 20) NÃO DEVEM ter
acesso à internet. Qualquer tráfego de saída dessas VLANs gera alerta automático.

REGRA-CIBER-03: Todos os usuários do Home Assistant DEVEM ter 2FA (TOTP) habilitado.
Tokens de longa duração devem ser revisados trimestralmente.

REGRA-CIBER-04: Acesso SSH DEVE ser exclusivamente por chave pública (Ed25519 ou
RSA 4096). Login por senha e root DEVEM estar desabilitados.

REGRA-CIBER-05: Backups DEVEM ser realizados diariamente com cópia off-site.
Restauração DEVE ser testada trimestralmente.

REGRA-CIBER-06: Credenciais padrão de TODOS os dispositivos (câmeras, roteador,
switch) DEVEM ser alteradas antes da entrada em produção. Mínimo 16 caracteres
para serviços críticos.

REGRA-CIBER-07: Atualizações de segurança do HA, Frigate, Zigbee2MQTT e firmware
DEVEM ser aplicadas em até 7 dias. CVEs com CVSS ≥ 9.0: até 48 horas.

REGRA-CIBER-08: Rede Zigbee DEVE manter permit_join desabilitado por padrão.
Pareamento de novos dispositivos deve ser habilitado apenas temporariamente.

REGRA-CIBER-09: arpwatch (ou equivalente) DEVE estar ativo em todas as VLANs.
Novos dispositivos detectados DEVEM gerar alerta imediato.

REGRA-CIBER-10: Todo incidente cibernético DEVE ser documentado no framework
PICERL, incluindo cronologia, ações tomadas e lições aprendidas.

REGRA-CIBER-11: Comandos MQTT para drones (UGV/UAV) DEVEM ser assinados com
HMAC-SHA256. Comandos sem assinatura válida, source_id autorizado ou com
timestamp fora de ±30 segundos são DESCARTADOS silenciosamente.

REGRA-CIBER-12: O PIN de defesa ativa NUNCA deve ter valor padrão. Deve ser
configurado exclusivamente via variável de ambiente (DEFENSE_PIN_UGV/UAV).
Após 3 tentativas incorretas, o sistema entra em lockout de 5 minutos.

REGRA-CIBER-13: A Dashboard API DEVE exigir autenticação em todas as rotas,
incluindo WebSocket. Clientes sem X-API-Key válida recebem 403/1008.

REGRA-CIBER-14: Containers de produção NÃO DEVEM rodar como root. DEVEM ter
cap_drop: ALL e no-new-privileges: true. Frigate NÃO DEVE usar privileged: true.

REGRA-CIBER-15: Nenhuma credencial real (senhas, tokens, URLs RTSP com auth)
deve ser commitada no repositório. Secrets K8s são gerados localmente via
scripts/generate-k8s-secrets.sh e protegidos pelo .gitignore.
```

---

## Documentos de Referência

| Documento | Conteúdo |
|-----------|----------|
| `docs/THREAT_MODEL.md` | Análise STRIDE completa com status por ameaça |
| `docs/RESPOSTA_INCIDENTES_CIBERNETICOS.md` | Playbooks detalhados para 7 cenários cibernéticos |
| `docs/HARDENING_ANTI_TAMPER.md` | Criptografia de disco, BIOS, proteção física |
| `docs/LEGAL_AND_ETHICS.md` | Regulamentações e aspectos éticos |
| `docs/RESILIENCIA_E_MODOS_DEGRADADOS.md` | Modos degradados e proteção anti-tamper |

## Links da Wiki

- [Resiliência](Resiliencia) — modos degradados, UPS, edge recording, anti-tamper
- [Cenários Residenciais](Cenarios-Residenciais) — defesa física por tipo de habitação
- [Arquitetura](Arquitetura) — visão geral do stack técnico e VLANs
- [Operação e Manutenção](Operacao-e-Manutencao) — rotina operacional e procedimentos
