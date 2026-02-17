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

---

## Código de Conduta

Ao participar deste projeto, você concorda em manter uma comunidade respeitosa e inclusiva. Assédio, discriminação ou comportamento abusivo não serão tolerados.

---

Obrigado por ajudar a tornar o Home Security DIY melhor! 🚀
