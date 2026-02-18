# PRD – [Nome do Subsistema/Funcionalidade]

> Sistema de Home Security – Open Source / Open Hardware
>
> Versão: X.X | Data: YYYY-MM-DD | Responsável: [Agente/Humano]

---

## 1. Visão geral

- **Nome do produto/funcionalidade**: [Nome descritivo]
- **Responsável**: [Quem especifica e quem documenta]
- **Data**: [Data de criação]
- **PRDs relacionados**: [Lista de PRDs que se integram com este]

> Exemplo preenchido:
> - **Nome**: Plataforma de Sensores e Alarmes
> - **Responsável**: Agente_Arquiteto_Tecnico (especificação), Agente_Documentador (documentação)
> - **Data**: 2026-02-12
> - **PRDs relacionados**: PRD_MONITORING_DASHBOARD, PRD_NETWORK_SECURITY

---

## 2. Problema e oportunidade

### 2.1 Problema

> Descreva o problema que será resolvido. Seja específico sobre o cenário atual e suas limitações.

### 2.2 Oportunidade

> Descreva como a solução proposta resolve o problema. Destaque diferencias em relação a alternativas comerciais.

---

## 3. Público-alvo

| Perfil | Descrição | Necessidades específicas |
|--------|-----------|--------------------------|
| **[Perfil 1]** | [Descrição do perfil] | [O que precisa] |
| **[Perfil 2]** | [Descrição do perfil] | [O que precisa] |

> Exemplo:
> | **Proprietário rural** | Fazendas e sítios | Cobertura de perímetros extensos |
> | **Morador de apartamento** | Apartamentos em condomínios | Integração simples |

---

## 4. Requisitos funcionais

### 4.1 [Categoria de requisitos]

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-001 | [Descrição clara e testável] | Alta/Média/Baixa |
| RF-002 | [Descrição clara e testável] | Alta/Média/Baixa |

> **Dicas**:
> - Use verbos no infinitivo: "Suportar...", "Permitir...", "Registrar..."
> - Cada requisito deve ser verificável (testável)
> - Prioridade Alta = essencial para MVP; Média = importante; Baixa = desejável

### 4.2 [Outra categoria]

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-010 | [Descrição] | [Prioridade] |

---

## 5. Requisitos não funcionais

### 5.1 Performance

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-001 | [Aspecto de performance] | [Valor mensurável] |

### 5.2 Segurança

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-010 | [Aspecto de segurança] | [Especificação] |

### 5.3 Confiabilidade

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-020 | [Aspecto de confiabilidade] | [Especificação] |

### 5.4 Conformidade com normas

| ID | Requisito | Norma/Regra |
|----|-----------|-------------|
| RNF-030 | [Requisito de conformidade] | [Referência à regra] |

> Referência: `rules/RULES_COMPLIANCE_AND_STANDARDS.md`

---

## 6. Arquitetura técnica

### 6.1 Diagrama de componentes

```
[Diagrama ASCII ou Mermaid mostrando os componentes e suas conexões]
```

### 6.2 Fluxo de dados

```
[Diagrama de fluxo mostrando como os dados transitam pelo sistema]
```

### 6.3 Integração com outros subsistemas

| Subsistema | Tipo de integração | Protocolo |
|------------|--------------------|-----------|
| [Subsistema] | [Tipo] | [MQTT/REST/RTSP] |

---

## 7. Produtos e componentes recomendados

### 7.1 [Categoria de componente]

| Tipo | Modelo | Preço estimado | Compatibilidade |
|------|--------|----------------|-----------------|
| [Tipo] | [Modelo específico] | R$ XX-XX | [Compatibilidade verificada] |

> **Dicas**:
> - Incluir modelos disponíveis no mercado brasileiro
> - Preços estimados em R$ (faixa)
> - Verificar compatibilidade em zigbee2mqtt.io ou docs do Frigate

---

## 8. Estimativa por cenário

### 8.1 Cenário rural

| Componente | Quantidade | Subtotal |
|------------|------------|----------|
| [Componente] | X | R$ XX |
| **Total** | | **R$ XX** |

### 8.2 Cenário casa urbana

| Componente | Quantidade | Subtotal |
|------------|------------|----------|
| [Componente] | X | R$ XX |

### 8.3 Cenário apartamento

| Componente | Quantidade | Subtotal |
|------------|------------|----------|
| [Componente] | X | R$ XX |

---

## 9. Critérios de aceitação

| ID | Critério | Método de verificação |
|----|----------|----------------------|
| CA-001 | [Condição testável de aceite] | [Como verificar] |
| CA-002 | [Condição testável de aceite] | [Como verificar] |

---

## 10. Métricas de sucesso

| Métrica | Alvo | Medição |
|---------|------|---------|
| [Nome da métrica] | [Valor alvo] | [Como medir] |

---

## 11. Riscos e dependências

### 11.1 Riscos

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| [Descrição do risco] | Alta/Média/Baixa | Alto/Médio/Baixo | [Estratégia] |

### 11.2 Dependências

| Dependência | Tipo | PRD relacionado |
|-------------|------|-----------------|
| [O que depende] | [Infraestrutura/Software/Hardware] | [PRD_XXX] |

---

## 12. Referências

### Documentos do projeto
- `docs/ARQUITETURA_TECNICA.md` - [Seções relevantes]
- `rules/RULES_COMPLIANCE_AND_STANDARDS.md` - [Regras aplicáveis]

### Externos
- [Link para documentação oficial]
- [Link para guia de compatibilidade]

---

> **Status**: Rascunho vX.X
>
> **Próxima revisão**: [Quando/por quem]
