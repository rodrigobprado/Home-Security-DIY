# Skills de Documentação

> Comentário: Skills focadas em criação e manutenção de documentação.

## Skills implementadas

### SKILL_DOC_001 — Elaborar PRD de subsistema
- **ID**: SKILL_DOC_001
- **Tipo**: Documentação
- **Descrição**: A partir de requisitos informais, gerar um PRD no formato de `prd/PRD_TEMPLATE.md`.
- **Entradas**: Descrição do subsistema, stakeholders, restrições técnicas
- **Saídas**: Arquivo PRD preenchido em `prd/`
- **Exemplos**: PRD_AUTONOMOUS_DRONES, PRD_DRONE_DEFENSE_MODULE

### SKILL_DOC_002 — Criar guia de montagem com BOM
- **ID**: SKILL_DOC_002
- **Tipo**: Documentação
- **Descrição**: Documentar passo a passo de montagem de hardware com Bill of Materials.
- **Entradas**: Especificação de hardware, fotos/diagramas
- **Saídas**: Guia em `docs/`, BOM com links de fornecedores nacionais
- **Exemplos**: `docs/GUIA_MONTAGEM_UGV.md`, `docs/ARQUITETURA_HARDWARE_UAV.md`

### SKILL_DOC_003 — Atualizar documentação técnica após mudança de código
- **ID**: SKILL_DOC_003
- **Tipo**: Documentação
- **Descrição**: Sincronizar docs/ com mudanças de implementação (API, segurança, arquitetura).
- **Entradas**: Diff de código ou PR, documentos existentes
- **Saídas**: Documentos atualizados com data de revisão

### SKILL_DOC_004 — Auditoria de TODOs e criação de issues
- **ID**: SKILL_DOC_004
- **Tipo**: Gestão + Documentação
- **Descrição**: Varrer o repositório por TODOs/FIXMEs e criar issues GitHub consolidadas.
- **Entradas**: Repositório git
- **Saídas**: Issues GitHub criadas, tasks locais atualizadas

