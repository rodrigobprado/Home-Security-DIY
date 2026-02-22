# 9. Adoção de Docker Compose (dev) + K3s (produção)

Data: 2026-02-22

## Status

Aceito

## Contexto

O projeto exige experiência simples para desenvolvimento local e maior resiliência em produção.

## Decisão

Manter Docker Compose para desenvolvimento e K3s para produção.

## Consequências

### Positivas
- Entrada rápida para contribuidores.
- Produção com probes, rollout e políticas Kubernetes.

### Negativas
- Dois caminhos operacionais para manter.
- Possível divergência de configuração entre ambientes.

## Mitigação
- Contratos de teste para paridade crítica.
- Kustomize overlays para controle por ambiente.
