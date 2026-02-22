# Gestão de Secrets no Kubernetes

## Objetivo
Eliminar o uso operacional de segredos em texto plano nos manifests aplicados em produção.

## Padrão adotado
- Produção: External Secrets Operator (ESO)
- Desenvolvimento/local: placeholders permitidos apenas para bootstrap

## Arquivos relevantes
- `k8s/overlays/production/external-secrets.yaml`
- `k8s/overlays/production/kustomization.yaml`
- `k8s/base/dashboard/dashboard.yaml`
- `k8s/base/frigate/frigate.yaml`

## Fluxo
1. Provisionar backend de segredos (Vault, cloud secret manager ou Kubernetes provider dedicado).
2. Instalar External Secrets Operator no cluster.
3. Aplicar overlay de produção.
4. Validar se os `ExternalSecret` sincronizaram os `Secret` alvo.

## Regras
- Não commitar valores reais de credenciais.
- Rotacionar segredos críticos trimestralmente.
- Bloquear merge se for detectado token/senha real em PR.

## Validação rápida
```bash
kubectl -n home-security get externalsecret
kubectl -n home-security describe externalsecret dashboard-credentials
kubectl -n home-security get secret dashboard-credentials -o yaml
```
