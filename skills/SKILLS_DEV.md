# Skills de Desenvolvimento

> Comentário: Skills relacionadas a código, testes e infraestrutura do projeto Home-Security-DIY.

> **Última atualização**: 2026-02-22 por Agente_Documentador

---

## Skills implementadas

### SKILL_DEV_001 — Gerar esqueleto de serviço FastAPI

- **ID**: SKILL_DEV_001
- **Tipo**: Desenvolvimento
- **Descrição**: A partir de uma especificação de endpoints, gerar código base de serviço FastAPI com autenticação por API Key, modelos Pydantic e testes unitários iniciais.
- **Entradas**:
  - Especificação dos endpoints (paths, métodos HTTP, parâmetros)
  - Esquema do banco de dados (se aplicável)
  - Requisitos de autenticação
- **Saídas**:
  - Arquivo `main.py` com rotas FastAPI
  - Modelos Pydantic em `models.py`
  - Testes em `tests/test_*.py`
  - `Dockerfile` e `requirements.txt`
- **Restrições**:
  - Não incluir segredos hardcoded (usar variáveis de ambiente)
  - Autenticação obrigatória em todos os endpoints exceto `/health`
  - `runAsNonRoot: true` no Dockerfile
- **Exemplos de uso**:
  - Backend da Dashboard API (`src/dashboard-backend/`)
  - Serviço de telemetria dos drones (futuro)

---

### SKILL_DEV_002 — Criar testes unitários e de integração

- **ID**: SKILL_DEV_002
- **Tipo**: Desenvolvimento
- **Descrição**: A partir de um módulo ou serviço existente, criar suite de testes com cobertura mínima exigida (70% backend Python / 60% frontend TypeScript).
- **Entradas**:
  - Código-fonte do módulo a testar
  - Especificação de comportamento esperado (contratos de entrada/saída)
  - Dependências externas (banco, MQTT, APIs)
- **Saídas**:
  - Arquivos `tests/test_*.py` (pytest) ou `*.test.tsx` (vitest)
  - Fixtures e mocks para dependências externas
  - Configuração de cobertura (`pytest.ini` / `vitest.config.ts`)
- **Restrições**:
  - Testar contratos externos, não implementações internas
  - Mocks obrigatórios para MQTT e chamadas de rede
  - Não criar testes que dependam de estado externo (banco real, broker real)
- **Exemplos de uso**:
  - Testes do firmware UGV (`src/drone-ugv/tests/`) — heartbeat, HMAC, patrulha
  - Testes do dashboard backend (`src/dashboard-backend/tests/`) — auth, endpoints, WebSocket

---

### SKILL_DEV_003 — Gerar manifesto Kubernetes / Docker Compose

- **ID**: SKILL_DEV_003
- **Tipo**: Desenvolvimento / Infraestrutura
- **Descrição**: A partir da especificação de um serviço, gerar manifesto Kubernetes (Deployment + Service + ConfigMap) ou serviço Docker Compose com configurações de segurança aplicadas.
- **Entradas**:
  - Nome e versão da imagem Docker
  - Variáveis de ambiente necessárias (separar segredos de configuração)
  - Requisitos de volume e persistência
  - Requisitos de rede (portas, políticas de acesso)
- **Saídas**:
  - Manifesto em `k8s/base/<servico>/` (Deployment, Service, ConfigMap)
  - Entrada em `src/docker-compose.yml`
  - Atualização de `scripts/generate-k8s-secrets.sh` se novos segredos forem adicionados
- **Restrições**:
  - `privileged: false` obrigatório
  - `runAsNonRoot: true` + `readOnlyRootFilesystem: true` sempre que possível
  - Segredos nunca em ConfigMap — sempre em Secret do K8s ou variável de ambiente
  - StorageClass padrão: `local-path` (K3s)
- **Exemplos de uso**:
  - Manifesto K8s para `drone-ugv` com service account restrito (Issue #87)
  - Serviço Docker Compose para novo sensor MQTT periférico

---

### SKILL_DEV_004 — Auditar e refatorar código para segurança

- **ID**: SKILL_DEV_004
- **Tipo**: Desenvolvimento / Segurança
- **Descrição**: Identificar e corrigir vulnerabilidades de segurança em código existente (OWASP Top 10, injeção de comandos, segredos hardcoded, autenticação fraca, anti-replay).
- **Entradas**:
  - Código-fonte a auditar
  - Contexto de execução (serviço web, firmware embarcado, script de infraestrutura)
- **Saídas**:
  - Código corrigido com comentários explicando cada mudança de segurança
  - Relatório resumido das vulnerabilidades encontradas e resolvidas
  - Testes que cobrem os vetores de ataque corrigidos
- **Restrições**:
  - Não alterar lógica de negócio — apenas segurança
  - Preservar testes existentes (ou atualizar se necessário)
  - Abrir issue GitHub para cada classe de vulnerabilidade identificada
- **Exemplos de uso**:
  - Auditoria red team do dashboard backend (Issues #7–#29, PR #78)
  - Hardening do firmware UGV contra command injection e replay de comandos MQTT
