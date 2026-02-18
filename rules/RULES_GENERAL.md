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

## Convenções de identificadores

### Formato de IDs de tarefas

- Prefixo: `T-` seguido de número sequencial com 3 dígitos
- Exemplo: `T-001`, `T-042`, `T-068`
- IDs são únicos e nunca reutilizados (mesmo após conclusão)

### Formato de IDs de PRDs

- Prefixo: `PRD_` seguido de nome descritivo em UPPER_SNAKE_CASE
- Exemplo: `PRD_SENSORS_AND_ALARMS_PLATFORM.md`
- Sufixo `.md` obrigatório

### Formato de IDs de requisitos

- Requisitos funcionais: `RF-XXX` (ex: `RF-001`)
- Requisitos não funcionais: `RNF-XXX` (ex: `RNF-001`)
- Critérios de aceitação: `CA-XXX` (ex: `CA-001`)
- Numeração reinicia por PRD (cada PRD tem seu próprio RF-001)

### Outros IDs

- Débitos técnicos: `TD-XXX` (ex: `TD-001`)
- Melhorias: `IMP-XXX` (ex: `IMP-001`)
- ADRs: `ADR-XXX` (ex: `ADR-001`)
- Regras: `REGRA-{CATEGORIA}-XX` (ex: `REGRA-IOT-01`, `REGRA-DRONE-17`)

---

## Política de backup de documentação

### Arquivos Markdown

- **Versionamento**: Todo arquivo `.md` é versionado no Git (fonte primária de backup)
- **Branches**: Branch `main` é protegida; alterações via Pull Request
- **Tags**: Criar tag Git a cada milestone relevante (ex: `v1.0-docs`)
- **Backup offsite**: Repositório espelhado no GitHub (push automático)

### Boas práticas

- Não armazenar dados sensíveis em arquivos `.md` (senhas, tokens, IPs reais)
- Manter o `.gitignore` atualizado para excluir arquivos temporários
- Realizar `git push` regularmente para manter o backup atualizado

