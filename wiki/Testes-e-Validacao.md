# Testes e Validação

O projeto é primariamente baseado em **infraestrutura e configuração** (Docker Compose, K3s, YAML, Home Assistant). A estratégia de testes reflete essa natureza, focando em validação de configurações, testes de integração entre serviços e checklists pós-deploy.

---

## Pirâmide de Testes

```
          /\
         /  \       Testes E2E (deploy completo)
        /    \      Manuais, por cenário
       /------\
      /        \    Testes de Integração
     /          \   Conectividade entre serviços
    /------------\
   /              \  Validação de Configuração
  /                \ Lint YAML, compose, k8s manifests
  ------------------
```

| Camada | Tipo | Frequência | Automação |
|--------|------|------------|-----------|
| **Base** | Validação de configuração | A cada commit/PR | CI (GitHub Actions) |
| **Meio** | Testes de integração | Pré-deploy | Script local + CI |
| **Topo** | Testes E2E | Pós-deploy | Manual + checklist |

---

## Camada Base — Validação de Configuração

### 1. Lint de YAML

```bash
# Instalar
pip install yamllint

# Executar
yamllint src/docker-compose.yml
yamllint src/zigbee2mqtt/configuration.yaml
yamllint k8s/base/**/*.yaml
yamllint k8s/overlays/**/*.yaml
```

Configuração (`.yamllint.yml` na raiz do repositório):
```yaml
extends: default
rules:
  line-length:
    max: 200
  truthy:
    check-keys: false
  comments:
    min-spaces-from-content: 1
```

### 2. Validação do Docker Compose

```bash
docker compose -f src/docker-compose.yml config --quiet
```

Verifica: sintaxe válida, interpolação de variáveis de ambiente, referências de volumes e redes.

### 3. Validação dos manifests Kubernetes

```bash
# Build via kubectl kustomize
kubectl kustomize k8s/overlays/staging/ > /tmp/staging-manifests.yaml
kubectl kustomize k8s/overlays/production/ > /tmp/production-manifests.yaml

# Validação de schema (sem cluster)
kubeconform -strict -summary -ignore-missing-schemas /tmp/staging-manifests.yaml
kubeconform -strict -summary -ignore-missing-schemas /tmp/production-manifests.yaml
```

### 4. Verificação de variáveis de ambiente

```bash
# Verificar que .env.example tem todas as variáveis usadas no compose
grep -oP '\$\{(\w+)' src/docker-compose.yml | sort -u | while read var; do
  grep -q "${var#\$\{}" src/.env.example || echo "MISSING: ${var#\$\{}"
done
```

### 5. Script unificado de validação

```bash
./scripts/validate-configs.sh
```

Executa: yamllint → docker compose config → `kubectl kustomize` → shellcheck → verificação de variáveis.

---

## Camada Média — Testes de Integração

### Smoke test MQTT (Mosquitto)

```bash
# Publicar
mosquitto_pub -h localhost -p 1883 -t "test/ping" -m "pong" \
  -u $MQTT_USER -P $MQTT_PASSWORD

# Subscrever
mosquitto_sub -h localhost -p 1883 -t "test/ping" -C 1 \
  -u $MQTT_USER -P $MQTT_PASSWORD
```

**Critério**: Mensagem recebida em < 2 segundos.

### Healthcheck de serviços

| Serviço | Endpoint | Critério |
|---------|----------|----------|
| Home Assistant | `http://localhost:8123/api/` | HTTP 200 ou 401 |
| Frigate | `http://localhost:5000/api/version` | HTTP 200 com versão |
| Zigbee2MQTT | `http://localhost:8080/` | HTTP 200 |
| Dashboard API | `http://localhost:8000/health` | `{"status":"ok"}` |
| Mosquitto | `mosquitto_sub -t '$SYS/broker/uptime' -C 1` | Resposta recebida |

### Integração Frigate → MQTT

```bash
mosquitto_sub -h localhost -p 1883 -t "frigate/#" -C 1 --timeout 30
```

**Critério**: Receber ao menos 1 mensagem em 30 segundos (stats ou evento).

### Integração Zigbee2MQTT → MQTT

```bash
mosquitto_sub -h localhost -p 1883 -t "zigbee2mqtt/bridge/state" -C 1 --timeout 10
```

**Critério**: Receber `{"state":"online"}`.

---

## Camada Topo — Testes E2E (Checklist)

Execute após cada deploy em ambiente real:

### Checklist pós-deploy

- [ ] Home Assistant acessível via browser em `http://localhost:8123`
- [ ] Dashboard mostra status dos sensores em `http://localhost:3000`
- [ ] Dashboard modo kiosk funciona em `http://localhost:3000/simplified`
- [ ] Alarmo arma/desarma corretamente via interface
- [ ] Frigate mostra streams de câmeras em `http://localhost:5000`
- [ ] Detecção de objetos funcionando (pessoa no frame → evento gerado)
- [ ] Notificação push chega ao celular em < 5 s
- [ ] Sensor Zigbee reporta abertura de porta no HA
- [ ] Sirene aciona quando alarme dispara
- [ ] VPN WireGuard permite acesso remoto ao HA
- [ ] Logs de eventos registrados com timestamp correto
- [ ] `curl http://localhost:8000/health` retorna `{"status":"ok"}`
- [ ] `curl -H "X-API-Key: $DASHBOARD_API_KEY" http://localhost:8000/api/sensors` retorna lista de entidades

### Testes de resiliência

| Teste | Ação | Resultado esperado |
|-------|------|-------------------|
| Queda de energia | Desligar energia, ligar nobreak | Sistema volta automaticamente |
| Perda de internet | Desconectar WAN | Sistema local continua operando; notificação via 4G |
| Falha de sensor | Remover sensor Zigbee | Alerta de sensor offline em < 2 min |
| Falha do MQTT broker | `docker stop mosquitto` | Serviços tentam reconectar |
| Reinício do servidor | `reboot` | Todos os containers reiniciam automaticamente |
| Frigate offline | `docker stop frigate` | Alerta + edge recording continua nas câmeras |

---

## CI/CD — GitHub Actions

**Trigger**: Push e Pull Request em `main`

**Jobs configurados:**

| Job | Ferramenta | O que valida |
|-----|-----------|--------------|
| `lint-yaml` | yamllint | Todos os YAML do repositório |
| `validate-compose` | docker compose config | Docker Compose + variáveis |
| `validate-k8s` | kubectl kustomize + kubeconform | Manifests Kubernetes (schema) |
| `lint-shell` | shellcheck | Scripts .sh |
| `docs-links` | script local | Links Markdown internos |
| `frontend-quality` | eslint + vitest | Qualidade e testes do frontend |
| `backend-quality` | pytest | Testes backend do dashboard |

Ver `.github/workflows/validate.yml` para implementação completa.

**Pipeline de segurança:**
- Workflow `Snyk Security` com execução condicional quando `SNYK_TOKEN` está disponível.
- Scans de SAST, SCA, IaC e imagens de container (modo não-bloqueante em cenários sem secret).

---

## Ferramentas Necessárias

| Ferramenta | Propósito | Instalação |
|------------|-----------|------------|
| `yamllint` | Lint de YAML | `pip install yamllint` |
| `shellcheck` | Lint de shell scripts | `apt install shellcheck` |
| `docker compose` | Validação de compose | Incluído no Docker |
| `kustomize` | Build de manifests K8s | `kubectl kustomize` (built-in) |
| `mosquitto-clients` | Testes MQTT | `apt install mosquitto-clients` |

---

## Roadmap de Testes

| Fase | Descrição | Status |
|------|-----------|--------|
| 1 | Validação de configuração (lint, compose, k8s) | ✅ Implementado |
| 2 | CI/CD com GitHub Actions | ✅ Implementado |
| 3 | Scripts de smoke test local | ✅ Implementado |
| 4 | Testes de integração automatizados | 🔄 Planejado |
| 5 | Scan de segurança (trivy, gitleaks) | 🔄 Planejado |
| 6 | Testes E2E automatizados (Testinfra) | 🔮 Futuro |

---

## Referências

- `docs/TESTING_STRATEGY.md` — fonte principal desta página
- `.github/workflows/validate.yml` — implementação do CI/CD
- `scripts/validate-configs.sh` — validação local unificada
- [Instalação Rápida](Instalacao-Rapida) — como subir o stack para testar
- [Operação e Manutenção](Operacao-e-Manutencao) — logs e diagnóstico
