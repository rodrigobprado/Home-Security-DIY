# Guia de Onboarding para Novos Contribuidores

> Bem-vindo ao projeto Home Security DIY!

---

## 1. O que e este projeto?

Sistema de seguranca residencial **100% local** (sem nuvem), **open source** e **open hardware**. Cobre tres cenarios: propriedade rural, casa urbana e apartamento.

**Stack principal**: Home Assistant + Frigate + Zigbee2MQTT + Mosquitto

Para uma visao completa, leia:
- `README.md` — Visao geral e quick start
- `PROJECT_OVERVIEW.md` — Descricao detalhada do projeto

---

## 2. Estrutura do repositorio

```
Home-Security-DIY/
├── src/                  # Docker Compose stack (desenvolvimento)
│   ├── docker-compose.yml
│   ├── .env.example
│   ├── mosquitto/        # Config do MQTT broker
│   ├── zigbee2mqtt/      # Config do bridge Zigbee
│   ├── frigate/          # Config do NVR + IA
│   └── homeassistant/    # Config do Home Assistant
│
├── k8s/                  # Kubernetes/K3s stack (producao)
│   ├── base/             # Manifests base
│   └── overlays/         # Staging e production
│
├── docs/                 # Documentacao tecnica
│   ├── ARCHITECTURE.md   # Arquitetura do sistema (diagramas)
│   ├── ARQUITETURA_TECNICA.md  # Detalhamento tecnico
│   ├── API_DOCS.md       # APIs e endpoints
│   ├── THREAT_MODEL.md   # Modelo de ameacas
│   └── adr/              # Architecture Decision Records
│
├── prd/                  # Product Requirements Documents
│   ├── PRD_INDEX.md      # Indice de todos os PRDs
│   └── PRD_*.md          # PRDs individuais
│
├── tasks/                # Gestao de tarefas (Kanban em Markdown)
├── quality/              # Debitos tecnicos, melhorias, pendencias
├── rules/                # Regras do projeto (tecnicas, compliance)
├── standards/            # Normas pesquisadas e aplicadas
├── scripts/              # Scripts de automacao (deploy, validacao)
└── .github/workflows/    # CI/CD com GitHub Actions
```

---

## 3. Primeiros passos

### 3.1 Prerequisitos

- Git
- Docker e Docker Compose
- Editor de texto (VS Code recomendado)

### 3.2 Clonar e explorar

```bash
git clone https://github.com/rodrigobprado/Home-Security-DIY.git
cd Home-Security-DIY
```

### 3.3 Ambiente de desenvolvimento

```bash
cd src
cp .env.example .env
# Editar .env com suas configuracoes
docker compose up -d
```

> **Nota**: Alguns servicos requerem hardware especifico (dongle Zigbee, cameras IP). Sem hardware, voce pode trabalhar na documentacao e configuracao.

### 3.4 Validar configuracoes

```bash
./scripts/validate-configs.sh
```

### 3.5 Executar testes automatizados backend (recomendado)

```bash
python3 -m venv .venv
.venv/bin/pip install -r src/dashboard/backend/requirements.txt pytest pytest-cov
.venv/bin/pytest -q tests/backend
```

---

## 4. Como contribuir

### 4.1 Areas de contribuicao

| Area | Descricao | Habilidades |
|------|-----------|-------------|
| **Documentacao** | PRDs, guias, traducoes | Escrita tecnica |
| **Configuracao** | Docker, K8s, YAML | DevOps, infra |
| **Automacoes** | Home Assistant, Node-RED | Automacao, YAML |
| **Seguranca** | Threat modeling, hardening | Seguranca da informacao |
| **Hardware** | Selecao de sensores, cameras | IoT, eletronica |
| **Drones** | ROS2, firmware, IA | Robotica, visao computacional |

### 4.2 Encontrar tarefas

1. Veja `tasks/TASKS_BACKLOG.md` para tarefas pendentes
2. Veja `quality/IMPROVEMENTS.md` para melhorias abertas
3. Veja `quality/TECH_DEBT.md` para debitos tecnicos
4. Procure issues no GitHub com tag `good first issue`

### 4.3 Fluxo de trabalho

1. Fork do repositorio
2. Criar branch: `git checkout -b feature/descricao-curta`
3. Fazer alteracoes seguindo os padroes
4. Validar: `./scripts/validate-configs.sh`
5. Commit (Conventional Commits): `feat: adiciona suporte a sensor X`
6. Push e abrir Pull Request

---

## 5. Padroes do projeto

### 5.1 Documentacao

- Linguagem: Portugues (pt-BR)
- Formato: Markdown padrao (CommonMark)
- IDs de tarefas: `T-XXX` (ex: T-001)
- IDs de requisitos: `RF-XXX`, `RNF-XXX`, `CA-XXX`
- Referencia completa: `rules/RULES_GENERAL.md`

### 5.2 Commits

Usamos [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: nova funcionalidade
fix: correcao de bug
docs: alteracao de documentacao
chore: manutencao, dependencias
refactor: refatoracao sem mudanca funcional
```

### 5.3 Nomenclatura de dispositivos

- Sensores: `sensor_{tipo}_{local}` (ex: `sensor_porta_entrada`)
- Cameras: `cam_{local}` (ex: `cam_entrada`)
- Sirenes: `sirene_{tipo}` (ex: `sirene_interna`)
- Referencia completa: `rules/RULES_TECHNICAL.md`

---

## 6. Documentos essenciais para ler

| Prioridade | Documento | O que aprende |
|------------|-----------|---------------|
| 1 | `README.md` | Visao geral, quick start |
| 2 | `docs/ARCHITECTURE.md` | Arquitetura do sistema |
| 3 | `docs/ARQUITETURA_TECNICA.md` | Stack tecnologico completo |
| 4 | `rules/RULES_COMPLIANCE_AND_STANDARDS.md` | Normas e regras |
| 5 | `prd/PRD_INDEX.md` | Indice de requisitos |
| 6 | `CONTRIBUTING.md` | Regras de contribuicao |

---

## 7. Perguntas frequentes

**P: Preciso de hardware para contribuir?**
R: Nao. Voce pode contribuir com documentacao, configuracao, revisao de codigo e testes sem hardware.

**P: Posso usar outro protocolo alem do Zigbee?**
R: O projeto prioriza Zigbee 3.0 (ADR-003), mas contribuicoes para Z-Wave ou Matter sao bem-vindas como modulos opcionais.

**P: O sistema funciona sem internet?**
R: Sim! O processamento e 100% local. Internet e necessaria apenas para notificacoes externas (push, Telegram) e acesso remoto (VPN).

**P: Quanto custa montar o sistema?**
R: De ~R$ 2.500 (apartamento) a ~R$ 6.000 (rural). Ver `docs/ARQUITETURA_TECNICA.md` Secao 10.

---

## 8. Contato e comunidade

- **Issues**: [GitHub Issues](https://github.com/rodrigobprado/Home-Security-DIY/issues)
- **Discussoes**: GitHub Discussions (quando habilitado)
- **Seguranca**: Reportar vulnerabilidades conforme `SECURITY.md`

---

> Obrigado por contribuir para tornar residencias mais seguras com tecnologia aberta!
