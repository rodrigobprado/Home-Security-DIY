# Templates de Skills

> Comentário: Use este modelo para definir cada skill que agentes poderão executar.

## Modelo de definição de skill

```markdown
## Nome da Skill
- ID: SKILL_XXX
- Tipo: [Documentação | Desenvolvimento | Pesquisa | Gestão | Outro]
- Descrição: [Descrição curta e clara da skill]
- Entradas:
  - [Entrada 1]
  - [Entrada 2]
- Saídas:
  - [Saída 1]
  - [Saída 2]
- Restrições:
  - [Restrições ou limites]
- Exemplos de uso:
  - [Exemplo 1]
  - [Exemplo 2]

## Exemplo (genérico, substituir depois):
## Gerar PRD básico
- ID: SKILL_PRD_BASIC
- Tipo: Documentação
- Descrição: A partir de uma descrição de produto, gerar um PRD no formato do arquivo `prd/PRD_TEMPLATE.md`.
- Entradas:
  - Descrição do produto
  - Lista de requisitos iniciais
- Saídas:
  - Arquivo PRD preenchido
- Restrições:
  - Não incluir dados sensíveis
- Exemplos de uso:
  - Criar PRD para “Módulo de cadastro de usuários”.

***

### `skills/SKILLS_DEV.md`

```markdown
# Skills de Desenvolvimento

> Comentário: Liste aqui skills relacionadas a código, testes e infraestrutura.

## Skills propostas

> **Implementado em 2026-02** — ver `skills/SKILLS_DEV.md` para as skills completas (SKILL_DEV_001 a SKILL_DEV_004).

- SKILL_DEV_001: Gerar esqueleto de serviço FastAPI com autenticação e testes
- SKILL_DEV_002: Criar suite de testes unitários e de integração (pytest/vitest)
- SKILL_DEV_003: Gerar manifesto Kubernetes / Docker Compose com hardening
- SKILL_DEV_004: Auditar e refatorar código para segurança (OWASP Top 10)


