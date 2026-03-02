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

- [x] Home Assistant acessível via browser em `http://localhost:8123`
- [x] Dashboard mostra status dos sensores em `http://localhost:3000`
- [x] Dashboard modo kiosk funciona em `http://localhost:3000/simplified`
- [x] Alarmo arma/desarma corretamente via interface
- [x] Frigate mostra streams de câmeras em `http://localhost:5000`
- [x] Detecção de objetos funcionando (pessoa no frame → evento gerado)
- [x] Notificação push chega ao celular em < 5 s
- [x] Sensor Zigbee reporta abertura de porta no HA
- [x] Sirene aciona quando alarme dispara
- [x] VPN WireGuard permite acesso remoto ao HA
- [x] Logs de eventos registrados com timestamp correto
- [x] `curl http://localhost:8000/health` retorna `{"status":"ok"}`
- [x] `curl -H "X-API-Key: $DASHBOARD_API_KEY" http://localhost:8000/api/sensors` retorna lista de entidades

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
| `frontend-quality` | eslint + typecheck + vitest | Qualidade e testes do frontend |
| `backend-quality` | pytest | Testes backend do dashboard |
| `compliance-gates` | scripts + pytest | Auditorias de compliance + contratos de evidência |

Ver `.github/workflows/validate.yml` para implementação completa.
Ver `.github/workflows/compliance-gates.yml` para o gate de compliance.

## Status Atual de Cobertura Automatizada

Data de referência: **2026-02-24**

Execução local validada:

```bash
python3 -m venv .venv
.venv/bin/pip install -r src/dashboard/backend/requirements.txt pytest pytest-cov
.venv/bin/pytest -q tests/backend
```

Resultado mais recente:
- Backend: `155 passed in 1.00s`
- Frontend: `59 passed` com cobertura:
  - lines: `100%`
  - functions: `96.25%`
  - statements: `98.52%`
  - branches: `93.61%`

Notas:
- Esta cobertura refere-se à suíte automatizada do diretório `tests/backend`.
- Itens de validação física e operacional de campo continuam com evidência manual (checklists/runbooks).
- A suíte inclui contrato para persistência de dados críticos em manifests K8s
  (`tests/backend/test_k8s_security_context_contract.py`), validando montagem
  de PVCs em Mosquitto, Home Assistant, Zigbee2MQTT e Frigate.

### Cobertura de compliance operacional

O gate de compliance inclui também contratos de documentação operacional:
- `test_lgpd_operational_evidence_contract.py`
- `test_uav_regulatory_evidence_contract.py`
- `test_defense_legal_evidence_contract.py`
- `test_physical_hardening_operations_contract.py`
- `test_network_production_validation_contract.py`
- `test_integration_smoke_production_runbook_contract.py`
- `test_matter_thread_semester_review_contract.py`

**Cobertura mínima no CI:**
- Backend: `pytest-cov` com `--cov-fail-under=70` para `app/`
- Frontend: `vitest --coverage` com thresholds:
  - lines >= 90
  - functions >= 85
  - statements >= 85
  - branches >= 60

Atualização 2026-03-02 (Issue #723):
- Os caminhos críticos `src/pages/AssetsAdmin.jsx`, `src/components/OperationalMap.jsx` e `src/hooks/useWebSocket.js` voltaram ao cálculo de cobertura (remoção de exclusões no `vitest.config.js`).
- Foram adicionados testes cobrindo cenários de sucesso/erro em comandos e persistência do mapa operacional, além de reconexão e parsing no hook WebSocket.

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
