# Regras Gerais do Projeto

> Comentário: Este arquivo define regras de comportamento, prioridades e estilo para humanos e agentes.

## Princípios gerais

- Priorizar clareza sobre concisão na escrita de documentação.
- Registrar decisões importantes na memória compartilhada.
- Evitar alterações destrutivas em arquivos sem registrar o motivo.

> Exemplo: Antes de reescrever uma seção inteira, adicionar uma entrada em `MEMORY_EVOLUTION_LOG.md` explicando o motivo.

## Linguagem e estilo

- Linguagem principal: Português (pt-BR), exceto quando requisitos exigirem o contrário.
- Usar Markdown padrão, evitando sintaxes proprietárias.
- Manter títulos e seções consistentes entre arquivos.

## Colaboração humano–IA

- Humanos têm prioridade em decisões de negócio.
- Agentes podem propor alterações, mas devem sempre registrar recomendações antes de aplicar grandes mudanças.
- Qualquer alteração automática em arquivos críticos deve ser acompanhada de resumo na memória compartilhada.

## Regras de edição

- Ler sempre o arquivo completo antes de editar.
- Respeitar seções marcadas como `> TODO` e não apagá-las; apenas substituí-las por conteúdo final.
- Evitar criar arquivos fora da estrutura definida, a menos que seja acordado em `MEMORY_SHARED.md`.

> TODO: Adicionar regras específicas da organização (ex.: horários, revisões, aprovações).

