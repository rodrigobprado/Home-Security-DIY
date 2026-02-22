# 7. Adoção de VPN como Único Canal de Acesso Remoto

Data: 2026-02-22

## Status

Aceito

## Contexto

Exposição direta de serviços de automação e NVR na internet aumenta superfície de ataque.

## Decisão

Acesso remoto somente via VPN (WireGuard/Tailscale), sem port forwarding direto.

## Consequências

### Positivas
- Redução significativa de risco de exposição externa.
- Controle de identidade e trilha de acesso centralizada.

### Negativas
- Requer configuração adicional do cliente VPN.
- Dependência operacional do túnel para acesso remoto.

## Mitigação
- Procedimento de onboarding VPN documentado.
- Plano de recuperação para indisponibilidade do túnel.
