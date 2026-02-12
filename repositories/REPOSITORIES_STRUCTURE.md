# Estrutura de Repositórios

> Comentário: Descreve como o projeto pode ser dividido em repositórios ou módulos.

## Repositório principal

- Contém:
  - Estrutura de documentação em `.md`
  - Configuração de agentes
  - Templates de PRD e tarefas

## Possíveis repositórios adicionais

- `backend/` – Código do backend do sistema de gestão de tarefas.
- `frontend/` – Interface do usuário.
- `automation/` – Scripts de orquestração e execução de agentes.

## Relações e dependências

- O repositório principal é a fonte de verdade para regras, normas e documentação.
- Repositórios de código devem referenciar este repositório para alinhamento de padrões.

> TODO: Adaptar para refletir a realidade da arquitetura final.

