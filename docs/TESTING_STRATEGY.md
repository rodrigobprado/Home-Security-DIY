# Estrategia de Testes Automatizados

> Sistema de Home Security – Open Source / Open Hardware
>
> Versao: 1.0 | Data: 2026-02-18 | Referencia: TD-001

---

## 1. Contexto

O projeto Home Security DIY e primariamente baseado em **infraestrutura e configuracao** (Docker Compose, K3s, YAML configs, Home Assistant), nao em codigo de aplicacao tradicional. A estrategia de testes reflete essa natureza, focando em:

- Validacao de configuracoes (YAML, Docker Compose, Kubernetes)
- Testes de integracao entre servicos (MQTT, Zigbee2MQTT, Frigate, HA)
- Verificacao de deploy (smoke tests)
- Conformidade e seguranca

---

## 2. Piramide de testes

```
          /\
         /  \       Testes E2E (deploy completo)
        /    \      Manuais, por cenario
       /------\
      /        \    Testes de Integracao
     /          \   Conectividade entre servicos
    /------------\
   /              \  Validacao de Configuracao
  /                \ Lint YAML, compose, k8s manifests
  ------------------
```

| Camada | Tipo | Frequencia | Automacao |
|--------|------|------------|-----------|
| **Base** | Validacao de configuracao | A cada commit/PR | CI (GitHub Actions) |
| **Meio** | Testes de integracao | Pre-deploy | Script local + CI |
| **Topo** | Testes E2E | Pos-deploy | Manual + checklist |

---

## 3. Validacao de configuracao (camada base)

### 3.1 Lint de YAML

Todas as configuracoes YAML do projeto devem ser validas sintaticamente.

**Ferramenta**: `yamllint`

**Arquivos cobertos**:
- `src/docker-compose.yml`
- `src/mosquitto/config/*.conf` (nao YAML, mas validar sintaxe)
- `src/zigbee2mqtt/configuration.yaml`
- `src/frigate/config.yml`
- `k8s/base/**/*.yaml`
- `k8s/overlays/**/*.yaml`

**Configuracao** (`.yamllint.yml`):
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

### 3.2 Validacao de Docker Compose

```bash
docker compose -f src/docker-compose.yml config --quiet
```

Verifica:
- Sintaxe valida do compose file
- Interpolacao de variaveis de ambiente
- Referencias de volumes e redes

### 3.3 Validacao de Kubernetes manifests

```bash
# Build dos overlays
kubectl kustomize k8s/overlays/staging/ > /tmp/staging-manifests.yaml
kubectl kustomize k8s/overlays/production/ > /tmp/production-manifests.yaml

# Validacao de schema sem cluster
kubeconform -strict -summary -ignore-missing-schemas /tmp/staging-manifests.yaml
kubeconform -strict -summary -ignore-missing-schemas /tmp/production-manifests.yaml
```

Verifica:
- Manifests K8s sintaticamente validos
- Kustomize overlays montam corretamente
- Conformidade de schema dos recursos

### 3.4 Validacao de variaveis de ambiente

```bash
# Verificar que .env.example tem todas as variaveis usadas no compose
grep -oP '\$\{(\w+)' src/docker-compose.yml | sort -u | while read var; do
  grep -q "${var#\$\{}" src/.env.example || echo "MISSING: ${var#\$\{}"
done
```

---

## 4. Testes de integracao (camada media)

### 4.1 Smoke test MQTT (Mosquitto)

```bash
# Publicar e receber mensagem de teste
mosquitto_pub -h localhost -p 1883 -t "test/ping" -m "pong" -u $MQTT_USER -P $MQTT_PASSWORD
mosquitto_sub -h localhost -p 1883 -t "test/ping" -C 1 -u $MQTT_USER -P $MQTT_PASSWORD
```

**Criterio**: Mensagem recebida em < 2 segundos.

### 4.2 Healthcheck de servicos

| Servico | Endpoint | Criterio |
|---------|----------|----------|
| Home Assistant | `http://localhost:8123/api/` | HTTP 200 ou 401 (auth) |
| Frigate | `http://localhost:5000/api/version` | HTTP 200 com versao |
| Zigbee2MQTT | `http://localhost:8080/` | HTTP 200 |
| Mosquitto | `mosquitto_sub -t '$SYS/broker/uptime' -C 1` | Resposta recebida |

### 4.3 Integracao Frigate → MQTT

```bash
# Verificar que Frigate publica eventos no MQTT
mosquitto_sub -h localhost -p 1883 -t "frigate/#" -C 1 --timeout 30
```

**Criterio**: Receber ao menos 1 mensagem em 30 segundos (stats ou evento).

### 4.4 Integracao Zigbee2MQTT → MQTT

```bash
# Verificar bridge status
mosquitto_sub -h localhost -p 1883 -t "zigbee2mqtt/bridge/state" -C 1 --timeout 10
```

**Criterio**: Receber `{"state":"online"}`.

---

## 5. Testes E2E (camada topo)

### 5.1 Checklist de deploy

Executar apos cada deploy em ambiente real:

- [ ] Home Assistant acessivel via browser
- [ ] Dashboard mostra status dos sensores
- [ ] Alarmo arma/desarma corretamente
- [ ] Frigate mostra streams de cameras
- [ ] Deteccao de objetos funcionando (pessoa no frame)
- [ ] Notificacao push chega ao celular em < 5s
- [ ] Sensor Zigbee reporta abertura de porta
- [ ] Sirene aciona quando alarme dispara
- [ ] VPN WireGuard permite acesso remoto
- [ ] Logs de eventos registrados com timestamp

### 5.2 Testes de resiliencia

| Teste | Acao | Resultado esperado |
|-------|------|-------------------|
| Queda de energia | Desligar energia, ligar nobreak | Sistema volta automaticamente |
| Perda de internet | Desconectar WAN | Sistema local continua operando |
| Falha de sensor | Remover sensor Zigbee | Alerta de sensor offline |
| Falha do broker MQTT | `docker stop mosquitto` | Servicos tentam reconectar |
| Reinicio do servidor | `reboot` | Todos os containers reiniciam |

---

## 6. CI/CD (GitHub Actions)

### 6.1 Pipeline de validacao

**Trigger**: Push e Pull Request em `main`

**Jobs**:
1. `lint-yaml` — Validar todos os YAML com yamllint
2. `validate-compose` — `docker compose config`
3. `validate-k8s` — `kubectl kustomize` + `kubeconform`
4. `lint-shell` — Validar scripts shell com `shellcheck`
5. `docs-links` — Validar links Markdown locais
6. `frontend-quality` — `eslint` + `typecheck` + `vitest`
7. `backend-quality` — `pytest` do backend dashboard

Ver `.github/workflows/validate.yml` para implementacao completa.

### 6.2 Pipeline de seguranca

- Workflow `Snyk Security` com execucao condicional quando `SNYK_TOKEN` esta configurado
- Scans de SAST, SCA, IaC e containers
- Etapas de monitoramento podem executar como nao-bloqueantes em cenarios sem secret

---

## 7. Scripts de teste local

### 7.1 `scripts/validate-configs.sh`

Script unico para rodar todas as validacoes localmente antes de commit:

```bash
./scripts/validate-configs.sh
```

Executa:
1. yamllint em todos os YAML
2. docker compose config
3. kubectl kustomize (se kubectl instalado)
4. shellcheck em scripts .sh
5. Verificacao de variaveis de ambiente

---

## 8. Ferramentas necessarias

| Ferramenta | Proposito | Instalacao |
|------------|-----------|------------|
| `yamllint` | Lint de YAML | `pip install yamllint` |
| `shellcheck` | Lint de shell scripts | `apt install shellcheck` |
| `docker compose` | Validacao de compose | Incluido no Docker |
| `kubeconform` | Validacao de schema K8s | binario oficial |
| `kubectl` | Build de overlays Kustomize | `kubectl kustomize` (built-in) |
| `mosquitto-clients` | Testes MQTT | `apt install mosquitto-clients` |

---

## 9. Convencoes

- Scripts de teste ficam em `scripts/`
- Pipeline CI fica em `.github/workflows/`
- Configuracao de ferramentas na raiz do repositorio (`.yamllint.yml`)
- Testes E2E sao documentados como checklists neste arquivo
- Resultados de CI devem ser visíveis no PR (badge/status check)

---

## 10. Roadmap de testes

| Fase | Descricao | Status |
|------|-----------|--------|
| 1 | Validacao de configuracao (lint, compose, k8s) | Implementado |
| 2 | CI/CD com GitHub Actions | Implementado |
| 3 | Scripts de smoke test local | Implementado |
| 4 | Testes de integracao automatizados | Planejado |
| 5 | Scan de seguranca (trivy, gitleaks) | Planejado |
| 6 | Testes E2E automatizados (Testinfra) | Futuro |

---

> **Referencia**: Este documento resolve a divida tecnica TD-001.
>
> **Proxima revisao**: Apos primeiro deploy em ambiente real.
