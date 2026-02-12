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

> TODO (humano/agente): Preencher com skills relevantes, usando o template de `SKILL_TEMPLATES.md`.

- [Exemplo] Gerar esqueleto de API REST.
- [Exemplo] Criar testes automatizados para módulo X.
- [Exemplo] Refatorar código para melhorar legibilidade.


