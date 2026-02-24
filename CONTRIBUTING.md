# Guia de Contribuição

Obrigado pelo interesse em contribuir para o **Home Security DIY**! 🎉

Este projeto é open source e construído pela comunidade. Todas as contribuições são bem-vindas, seja corrigindo bugs, adicionando novas funcionalidades, melhorando a documentação ou sugerindo novas ideias.

## Como posso contribuir?

### 1. Reportando Bugs

Se você encontrou um bug, por favor abra uma [Issue](https://github.com/rodrigobprado/Home-Security-DIY/issues) descrevendo:
- Passos para reproduzir o problema.
- Comportamento esperado vs. comportamento real.
- Logs relevantes (remova senhas/tokens!).
- Seu ambiente (OS, versão do Docker/K3s, Hardware).

### 2. Sugerindo Melhorias

Tem uma ideia para melhorar o projeto?
- Abra uma Issue com a tag `enhancement`.
- Descreva sua proposta e o valor que ela agrega.
- Se possível, inclua exemplos ou mockups.

### 3. Enviando Código (Pull Requests)

1. Faça um **Fork** do repositório.
2. Crie um branch para sua feature (`git checkout -b feature/minha-melhoria`).
3. Faça suas alterações seguindo o padrão de código existente.
4. Teste suas mudanças localmente.
5. Faça o commit (`git commit -m "Adiciona funcionalidade X"`).
6. Faça o push para seu fork (`git push origin feature/minha-melhoria`).
7. Abra um **Pull Request** para o branch `main` do repositório original.

### Fluxo padrão de issue -> PR -> merge

Para padronizar revisão e fechamento automático de issues, use o script:

```bash
./scripts/pr_flow.sh \
  --title "fix: resumo da correção" \
  --issues "123 124"
```

Opcionalmente, inclua um resumo customizado:

```bash
./scripts/pr_flow.sh \
  --title "fix: resumo da correção" \
  --issues "123 124" \
  --summary-file /tmp/pr-summary.md
```

O script cria o PR com checklist de validação/operação e adiciona `Closes #...` para cada issue.

## Critérios de aceite para Pull Request

Antes de solicitar merge, confirme:

- O PR referencia a issue (`Closes #<id>` ou equivalente).
- Testes automatizados relevantes foram executados e estão passando.
- Mudanças de comportamento incluem testes novos/atualizados.
- Documentação impactada foi atualizada (`docs/`, wiki, runbooks, ADR quando aplicável).
- Mudanças de segurança foram avaliadas (segredos, autenticação, exposição de portas e permissões).
- Existe plano de rollback para mudanças com impacto operacional.

Checklist sugerido para descrição do PR:

```md
## Resumo
- ...

## Testes
- [ ] Backend: `.venv/bin/pytest tests/backend -q`
- [ ] Frontend: `npm test -- --run`
- [ ] Outros: ...

## Operação
- [ ] Sem impacto de downtime
- [ ] Rollback documentado

## Segurança
- [ ] Sem segredos em código/log
- [ ] Permissões mínimas preservadas
```

## Padrões de Projeto

### Estrutura de Diretórios
- `src/`: Stack Docker Compose (desenvolvimento).
- `k8s/`: Manifests Kubernetes (produção).
- `docs/`: Documentação técnica.
- `prd/`: Requisitos de produto.

### Padrão de Commits
Recomendamos o uso de [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:` Nova funcionalidade.
- `fix:` Correção de bug.
- `docs:` Alteração apenas na documentação.
- `chore:` Tarefas de manutenção, dependências.

Exemplo: `feat: adiciona suporte a sensor de vazamento Zigbee`

## Desenvolvimento Local

Siga o guia [src/docs/QUICK_START.md](src/docs/QUICK_START.md) para configurar seu ambiente de desenvolvimento com Docker Compose.
Para onboarding completo de novos contribuidores, consulte também [docs/ONBOARDING.md](docs/ONBOARDING.md).

### Rodando testes do Dashboard Backend

```bash
python3 -m venv .venv
.venv/bin/pip install -r src/dashboard/backend/requirements.txt pytest pytest-cov
.venv/bin/pytest -q tests/backend
```

### Rodando testes do Dashboard Frontend

```bash
cd src/dashboard/frontend
npm test -- --run
```

### Cobertura mínima (CI)

- Backend (`pytest-cov`): mínimo de **70%** em `app/`
- Frontend (`vitest --coverage`): mínimo de **60%** em linhas/funções/statements e **50%** em branches

---

## Código de Conduta

Ao participar deste projeto, você concorda em manter uma comunidade respeitosa e inclusiva. Assédio, discriminação ou comportamento abusivo não serão tolerados.

---

Obrigado por ajudar a tornar o Home Security DIY melhor! 🚀
