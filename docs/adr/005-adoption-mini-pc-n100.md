# 5. Adoção de Mini PC N100 como Hardware Principal

Data: 2026-02-22

## Status

Aceito

## Contexto

O projeto precisa de hardware com baixo consumo, suporte a execução 24/7 e capacidade para IA local no Frigate.

## Decisão

Adotar Mini PC com Intel N100 como baseline de produção.

## Consequências

### Positivas
- Bom custo-benefício para uso contínuo.
- iGPU integrada para aceleração de vídeo/IA.
- Compatibilidade Linux e Docker/K3s.

### Negativas
- Capacidade limitada para cargas muito altas de câmeras.
- Exige planejamento de armazenamento externo para retenção longa.

## Mitigação
- Limites de retenção e otimização de stream.
- Escalar para hardware superior quando necessário.
