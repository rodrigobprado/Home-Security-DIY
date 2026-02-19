# 🏗️ Guia de Deploy K3s – Home Security DIY

Guia para instalar e operar o stack de segurança no K3s (Kubernetes leve).

---

## Arquitetura de ambientes

```
┌─────────────────────────────────────────────────────────────┐
│                     Desenvolvimento                          │
│  docker compose up -d  (src/docker-compose.yml)              │
│  → Testes locais, iteração rápida                            │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                     Homologação (Staging)                     │
│  ./scripts/deploy.sh staging                                 │
│  → Namespace: home-security-staging                          │
│  → Recursos reduzidos, storage menor                         │
│  → Validação de configs e automações                         │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                     Produção (Production)                     │
│  ./scripts/deploy.sh production                              │
│  → Namespace: home-security                                  │
│  → Recursos completos, 500Gi storage Frigate                 │
│  → Ingress com domínio local, operação 24/7                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 1. Instalar K3s

```bash
# Instalar K3s (single-node)
curl -sfL https://get.k3s.io | sh -

# Verificar
sudo kubectl get nodes
# NAME     STATUS   ROLES                  AGE   VERSION
# mynode   Ready    control-plane,master   1m    v1.xx.x+k3s1

# Configurar kubectl para seu usuário
mkdir -p ~/.kube
sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
sudo chown $USER:$USER ~/.kube/config
```

## 2. Preparar o nó

### Labels de hardware

O script de deploy faz isso automaticamente, mas para referência:

```bash
# Nó com coordenador Zigbee USB
kubectl label node <NODE> home-security/zigbee-coordinator=true

# Nó com GPU Intel (para OpenVINO/Frigate)
kubectl label node <NODE> home-security/intel-gpu=true
```

### Verificar dispositivos

```bash
# Zigbee USB dongle
ls -la /dev/serial/by-id/
# Intel GPU
ls -la /dev/dri/
```

## 3. Configurar Secrets

Antes do deploy, gere os Secrets localmente a partir de `src/.env`:

```bash
chmod +x scripts/generate-k8s-secrets.sh
./scripts/generate-k8s-secrets.sh src/.env
kubectl apply -f k8s/generated/secrets/
```

Para o Ingress TLS em produção, crie também o secret de certificado:

```bash
kubectl create secret tls home-security-tls \
  -n home-security \
  --cert=/caminho/para/fullchain.pem \
  --key=/caminho/para/privkey.pem
```

Alternativa manual:

```bash
# MQTT credentials
kubectl create namespace home-security
kubectl create secret generic mqtt-credentials \
  -n home-security \
  --from-literal=MQTT_USER=homeassistant \
  --from-literal=MQTT_PASSWORD='SUA_SENHA_FORTE_AQUI'

# Camera URLs
kubectl create secret generic frigate-cameras \
  -n home-security \
  --from-literal=FRIGATE_CAM_ENTRADA_URL='rtsp://admin:pass@192.168.30.10:554/stream' \
  --from-literal=FRIGATE_CAM_ENTRADA_SUB_URL='rtsp://admin:pass@192.168.30.10:554/sub' \
  --from-literal=FRIGATE_CAM_FUNDOS_URL='rtsp://admin:pass@192.168.30.11:554/stream' \
  --from-literal=FRIGATE_CAM_FUNDOS_SUB_URL='rtsp://admin:pass@192.168.30.11:554/sub' \
  --from-literal=FRIGATE_CAM_LATERAL_URL='rtsp://admin:pass@192.168.30.12:554/stream' \
  --from-literal=FRIGATE_CAM_LATERAL_SUB_URL='rtsp://admin:pass@192.168.30.12:554/sub' \
  --from-literal=FRIGATE_CAM_GARAGEM_URL='rtsp://admin:pass@192.168.30.13:554/stream' \
  --from-literal=FRIGATE_CAM_GARAGEM_SUB_URL='rtsp://admin:pass@192.168.30.13:554/sub'
```

## 4. Deploy

```bash
# Tornar script executável
chmod +x scripts/deploy.sh

# Deploy staging (homologação)
./scripts/deploy.sh staging

# Deploy production
./scripts/deploy.sh production
```

## 5. Acessar os serviços

### Staging (via port-forward)

```bash
kubectl port-forward svc/stg-homeassistant 8123:8123 -n home-security-staging
kubectl port-forward svc/stg-frigate 5000:5000 -n home-security-staging
kubectl port-forward svc/stg-zigbee2mqtt 8080:8080 -n home-security-staging
```

### Production (via Ingress)

Adicione ao `/etc/hosts` ou DNS local:

```
192.168.10.X  security.home.local
192.168.10.X  frigate.home.local
192.168.10.X  zigbee.home.local
```

| Serviço | URL |
|---------|-----|
| Home Assistant | http://security.home.local |
| Frigate | http://frigate.home.local |
| Zigbee2MQTT | http://zigbee.home.local |
| MQTT | ClusterIP interno (exposição externa somente via túnel TLS/mTLS) |

---

## Operação

### Status dos pods

```bash
kubectl get pods -n home-security -o wide
kubectl get pods -n home-security-staging -o wide
```

### Logs

```bash
kubectl logs -f deployment/homeassistant -n home-security
kubectl logs -f deployment/frigate -n home-security
kubectl logs -f deployment/zigbee2mqtt -n home-security
kubectl logs -f deployment/mosquitto -n home-security
```

### Restart de serviço

```bash
kubectl rollout restart deployment/frigate -n home-security
```

### Teardown

```bash
./scripts/deploy.sh teardown staging
./scripts/deploy.sh teardown production
```

---

## Estrutura de arquivos K8s

```
k8s/
├── base/
│   ├── kustomization.yaml          # Kustomize base
│   ├── namespace.yaml              # Namespace
│   ├── mosquitto/
│   │   └── mosquitto.yaml          # Deploy + Svc + ConfigMap + PVC
│   ├── zigbee2mqtt/
│   │   └── zigbee2mqtt.yaml        # Deploy + Svc + ConfigMap + PVC
│   ├── frigate/
│   │   └── frigate.yaml            # Deploy + Svc + ConfigMap + PVC + Secret
│   └── homeassistant/
│       └── homeassistant.yaml      # Deploy + Svc + ConfigMap + PVC
└── overlays/
    ├── staging/
    │   └── kustomization.yaml      # Recursos reduzidos, namespace separado
    └── production/
        ├── kustomization.yaml      # Recursos completos
        └── ingress.yaml            # Traefik Ingress + MQTT NodePort
```

---

## Docker vs K3s — quando usar cada um

| | Docker Compose | K3s |
|---|---|---|
| **Quando** | Desenvolvimento, testes | Homologação, produção |
| **Complexidade** | Baixa | Média |
| **Self-healing** | Não | Sim (liveness/readiness probes) |
| **Ingress/TLS** | Manual (nginx) | Traefik built-in |
| **Secrets** | `.env` file | K8s Secrets (criptografados) |
| **Scaling** | Manual | Declarativo |
| **Updates** | `docker compose pull` | `kubectl set image` / rolling |
| **Monitoring** | Manual | Métricas nativas / Prometheus |
