# 4. Adoção do K3s para Infraestrutura

Data: 2026-02-17

## Status

Aceito

## Contexto

Precisamos de uma plataforma de orquestração de containers para executar o stack de segurança em produção. A solução deve gerenciar ciclo de vida, updates, health checks, e exposição de serviços.

As alternativas consideradas foram:
- Docker Compose (usado em dev)
- K3s (Kubernetes leve)
- Kubernetes padrão (kubeadm)
- Proxmox (Virtualização completa)

## Decisão

Escolhemos o **K3s** para o ambiente de produção.

## Consequências

### Positivas
- **Leveza**: Binário único <100MB, ideal para Mini PCs e até Raspberry Pi.
- **Resiliência**: Self-healing nativo (reinicia pods travados), rolling updates sem downtime.
- **GitOps-ready**: Permite gerenciar configuração como código (Kustomize/Helm/ArgoCD).
- **Networking**: Ingress Controller (Traefik) integrado simplifica acesso HTTPS e domínios locais.

### Negativas
- **Complexidade**: Curva de aprendizado maior que Docker Compose.
- **Hardware**: USB passthrough e GPU passthrough requerem configuração específica de node/pod.

## Implementação
- Manter **Docker Compose** para desenvolvimento rápido e testes locais.
- Usar **Kustomize** para gerenciar diferenças entre ambientes (staging vs production).
- Usar **Node Selectors** para garantir que pods dependentes de hardware (Zigbee, GPU) rodem no nó correto em caso de cluster multi-node.
