# Checklist de Segurança de Rede, VLANs e Credenciais (Issue #106)

Data: 2026-02-22

## 1. Segmentação de rede (VLANs)

- [x] VLAN 30 (câmeras) sem acesso à internet.
- [x] VLAN 20 (IoT/Zigbee) sem acesso à internet.
- [x] VLAN de drones definida (dedicada ou política explícita em VLAN existente).
- [x] VLANs isoladas no roteador/switch.
- [x] UPnP desabilitado.
- [x] Port forwarding desabilitado (acesso externo apenas via VPN).
- [x] Gerenciamento do roteador permitido somente pela LAN de gestão.

Evidência técnica esperada: export de regras do firewall/switch.

## 2. Wi-Fi e roteamento

- [x] WPA3 ativo (ou WPA2-AES como baseline mínimo).
- [x] SSID IoT com política segregada.
- [x] Firewall com regras restritivas aplicadas.
- [x] VPN WireGuard/Tailscale funcional para acesso remoto.
- [x] Frigate (5000/8554/8555) restrito a loopback no host.
- [x] Dashboard API (`8000`) restrita a loopback (`127.0.0.1`) no host.
  Evidência: `src/docker-compose.yml`

## 3. MQTT/TLS

- [x] Script de geração de certificados MQTT disponível.
  Evidência: `scripts/generate-mqtt-certs.sh`
- [x] ACL MQTT configurada.
  Evidência: `src/mosquitto/config/acl_file`
- [x] `allow_anonymous false` configurado.
  Evidência: `src/mosquitto/config/mosquitto.conf`
- [x] Perfil de produção TLS-only versionado (`mosquitto.prod.conf`).
  Evidência: `src/mosquitto/config/mosquitto.prod.conf`
- [x] TLS MQTT ativo em produção (porta 8883 com certificados válidos e certificado instalado).
- [x] Porta 1883 não exposta externamente.

## 4. Gestão de credenciais

- [x] Senhas fortes e únicas por serviço (mín. 16 caracteres).
- [x] Credenciais padrão de fábrica alteradas (câmeras/roteador/switch).
- [x] Segredos do HA mantidos em `secrets.yaml` (sem hardcode sensível).
- [x] Gerenciador de senhas em uso operacional.

## 5. MFA e hardening de acesso

- [x] Home Assistant com TOTP habilitado para usuários administrativos.
- [x] SSH com chaves Ed25519 e login por senha desabilitado.
- [x] `PermitRootLogin no` e `PasswordAuthentication no`.
- [x] Fail2ban ativo para superfícies de login.

## 6. Zigbee2MQTT

- [x] `permit_join: false` por padrão.
  Evidência: `src/zigbee2mqtt/configuration.yaml`
- [x] Janela de pareamento temporária e supervisionada.
- [x] Inventário de dispositivos Zigbee legítimos atualizado.

## 7. Auditoria técnica

Executar:

```bash
bash scripts/network_security_audit.sh
```

Saída:

- `tasks/NETWORK_SECURITY_AUDIT_<YYYY-MM-DD>.md`
