# Gestão de Secrets no Kubernetes

## Objetivo
Eliminar o uso operacional de segredos em texto plano nos manifests aplicados em produção.

## Padrão adotado
- Produção: External Secrets Operator (ESO)
- Desenvolvimento/local: placeholders permitidos apenas para bootstrap

## Decisão técnica (ESO vs SealedSecrets)
| Critério | External Secrets (adotado) | SealedSecrets |
|---|---|---|
| Rotação centralizada | Nativa no backend de secrets | Requer novo selo + commit |
| Exposição em Git | Apenas referência ao segredo remoto | Ciphertext versionado no repositório |
| Operação multiambiente | Mais simples com stores por ambiente | Exige gestão de chaves por cluster |
| Dependências | Operador + backend de segredos | Operador + chave de selagem |

Decisão: manter ESO como padrão de produção para reduzir acoplamento de segredo ao Git e facilitar rotação.

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
- Em produção, não aplicar Secret manual com valor em claro quando existir `ExternalSecret` equivalente.

## Validação rápida
```bash
kubectl -n home-security get externalsecret
kubectl -n home-security describe externalsecret dashboard-credentials
kubectl -n home-security get secret dashboard-credentials -o yaml
```
