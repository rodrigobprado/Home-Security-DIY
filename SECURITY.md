# Política de Segurança

O projeto **Home Security DIY** leva a segurança a sério. Como um sistema projetado para proteger lares e privacidade, nossa prioridade é garantir que o software seja seguro, resiliente e confiável.

Este documento delineia nossa política de segurança e explica como reportar vulnerabilidades.

## Versões suportadas

Apenas a versão mais recente (`main` branch) e as releases marcadas como `stable` recebem atualizações de segurança.

| Versão | Suportada | Notas |
|--------|-----------|-------|
| `main` | ✅ Sim | Desenvolvimento ativo |
| `stable` (latest tag) | ✅ Sim | Versão estável recomendada |
| Versões antigas (< 1.0) | ❌ Não | Não suportadas |

## Reportando uma Vulnerabilidade

Nós encorajamos a divulgação responsável de vulnerabilidades de segurança. Se você acredita ter encontrado uma vulnerabilidade no Home Security DIY, por favor, siga os passos abaixo:

### O que reportar

- Falhas que permitam acesso não autorizado ao sistema (bypass de autenticação).
- Exposição inadvertida de dados sensíveis (vídeo, credenciais, tokens).
- Vulnerabilidades nos scripts de deploy ou configurações padrão que deixem o sistema inseguro.
- Cross-Site Scripting (XSS), Cross-Site Request Forgery (CSRF) ou Injection no dashboard.

### Como reportar

> **NÃO abra uma issue pública no GitHub para reportar uma vulnerabilidade de segurança.**

Use o canal privado de Security Advisory do projeto:

- **GitHub Private Vulnerability Reporting**: https://github.com/rodrigobprado/Home-Security-DIY/security/advisories/new

Inclua no report:

1. Tipo de vulnerabilidade.
2. Passo a passo para reproduzir o problema.
3. Impacto potencial.
4. (Opcional) Código para correção ou mitigação.

Nós nos comprometemos a responder em até 48 horas.

## Processo de Resposta

1. **Triagem**: Analisaremos o report para confirmar a vulnerabilidade e determinar sua severidade.
2. **Correção**: Desenvolveremos um patch de correção em um branch privado.
3. **Validação**: Testaremos a correção para garantir que não introduza regressões.
4. **Divulgação**: Publicaremos a correção e um Security Advisory detalhando o problema (após a mitigação estar disponível).

## Boas Práticas de Segurança para Usuários

Para manter seu sistema seguro, recomendamos:

- **Nunca exponha o Home Assistant ou Frigate diretamente à internet** (port forwarding). Use sempre VPN (WireGuard/Tailscale) ou Cloudflare Tunnel.
- Mantenha o sistema base (Linux/Docker/K3s) e os containers atualizados.
- Isole a rede de câmeras e dispositivos IoT em VLANs separadas sem acesso à internet.
- Use senhas fortes e únicas para todos os serviços (MQTT, HA, Frigate).
- Habilite autenticação multifator (MFA) no Home Assistant.

## Ameaças Conhecidas (Out of Scope)

- **Acesso físico**: Se um atacante tiver acesso físico ao servidor, a segurança do software pode ser comprometida. Proteja fisicamente seu hardware.
- **Jamming de RF**: Dispositivos sem fio (Zigbee/Wi-Fi) são suscetíveis a interferência intencional. Considere sensores cabeados para ambientes críticos.

---

Obrigado por ajudar a manter o Home Security DIY seguro para todos!
