# 1. Adoção do Home Assistant

Data: 2026-02-17

## Status

Aceito

## Contexto

O projeto necessita de uma plataforma central de automação e integração para o sistema de segurança residencial. A plataforma deve ser capaz de:
1. Integrar dispositivos de diversos fabricantes e protocolos (Zigbee, MQTT, ONVIF).
2. Processar automações localmente sem dependência de nuvem.
3. Fornecer uma interface de usuário (dashboard) amigável e customizável.
4. Ter uma comunidade ativa e suporte a longo prazo.

As alternativas consideradas foram:
- Home Assistant
- openHAB
- Domoticz
- Soluções proprietárias (Samsung SmartThings, Apple HomeKit)

## Decisão

Escolhemos o **Home Assistant** como a plataforma central de automação.

## Consequências

### Positivas
- **Ecossistema massivo**: Mais de 2500 integrações oficiais.
- **Processamento local**: Funciona 100% offline, garantindo privacidade e resiliência (internet down ≠ system down).
- **Flexibilidade**: Suporta scripts complexos, automações via UI e customização profunda (Lovelace).
- **Hardware agnóstico**: Roda em Raspberry Pi, Mini PCs, VMs, Docker, K8s.
- **Add-ons**: Facilita a instalação de serviços auxiliares (Mosquitto, Zigbee2MQTT, Alarmo).

### Negativas
- **Curva de aprendizado**: Pode ser íngreme para configuração avançada (YAML, templating).
- **Breaking changes**: Atualizações mensais frequentes podem quebrar configurações customizadas.
- **Recursos**: Exige mais hardware que soluções mais leves como Domoticz (especialmente para histórico longo).

## Mitigação
- Usar **Alarmo** para lógica de segurança crítica, simplificando a configuração de zonas e sensores.
- Manter backups regulares antes de atualizações.
- Rodar em hardware x86 (Mini PC) para evitar gargalos de performance.
