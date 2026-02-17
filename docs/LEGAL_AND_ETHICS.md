# Aspectos Legais e Éticos - Drones e Defesa Ativa

Data: 2026-02-17
Referencia-se às Tarefas: **T-050, T-058**

---

## ⚠️ AVISO CRÍTICO

Este documento não constitui aconselhamento jurídico. O usuário é inteiramente responsável por verificar a legislação local antes de implementar qualquer componente deste projeto.

---

## 1. Drones e Operação Autônoma (T-050)

### O Conflito: VLOS vs. Autonomia

A legislação brasileira (ANAC RBAC-E nº 94) e a maioria das regulações internacionais exigem, para operação recreativa ou não-tripulada padrão, que o voo seja **VLOS (Visual Line of Sight)** — ou seja, o piloto deve manter contato visual direto com a aeronave o tempo todo.

**O Problema**: A proposta do Home Security DIY inclui drones autônomos que decolam sem intervenção humana para verificar alarmes, o que configura operação **BVLOS (Beyond Visual Line of Sight)** se o operador não estiver olhando para o drone, ou se o drone operar totalmente sem piloto humano no comando.

### Restrições da ANAC (Brasil)
1. **Voo Autônomo É PROIBIDO**: A ANAC proíbe aeronaves totalmente autônomas (onde não há intervenção humana possível). O que é permitido é a aeronave **automatizada** (voa sozinha, mas um piloto humano pode assumir o controle a qualquer momento).
2. **BVLOS Requer Autorização Especial**: Voar além da visada visual exige certificação da aeronave e autorização específica de voo do DECEA (SARPAS), o que é inviável para uma resposta de alarme automática residencial.

### Solução de Conformidade (Compliance)

Para manter o projeto legal para uso residencial sem certificações complexas:

1. **Apenas Drones Terrestres (UGVs)**: Drones terrestres (rovers) não são regulados pela ANAC. Eles podem operar autonomamente dentro de propriedade privada fechada sem restrições de espaço aéreo.
2. **Drones Aéreos (UAVs) no Modo "Assistido"**:
   - O drone **NÃO** decola sozinho.
   - O sistema envia um alerta ao operador: "Invasião detectada. Iniciar patrulha aérea?".
   - O operador confirma e **mantém contato visual** com o drone enquanto ele executa a rota (Operação VLOS Automatizada).
   - O drone nunca sai dos limites verticais da propriedade (ex: voo baixo, abaixo da altura do muro/telhado, embora a legislação de espaço aéreo se aplique a partir do solo, áreas confinadas podem ter interpretações diferentes, mas o risco legal permanece).

**Decisão do Projeto**: O módulo de drones aéreos será marcado como **Experimental/Risco Legal**. O foco principal para automação total será em **Drones Terrestres**.

---

## 2. Defesa Ativa e Não-Letal (T-058)

### O Risco da Autonomia em Defesa

A ideia de um drone ou torre disparar spray de pimenta (OC) ou balas de borracha ou tinta (paintball) de forma **autônoma** contra um intruso é **eticamente inaceitável e legalmente catastrófica**.

1. **Falsos Positivos**: Uma criança pulando o muro para pegar uma bola, um entregador no lugar errado, ou um animal não podem ser alvos de agressão automatizada.
2. **Responsabilidade Civil e Criminal**: O proprietário do sistema responderá por lesão corporal dolosa. "Foi o robô que fez" não é defesa válida; é negligência grave ou dolo eventual.
3. **Legítima Defesa**: A lei exige que a resposta seja proporcional e atual de uma agressão injusta. Um sistema automático não tem discernimento jurídico para avaliar "injusta agressão".

### Diretriz de Design: Human-in-the-Loop (HITL) Obrigatório

Nenhum mecanismo de defesa ativa (sirenes ensurdecedoras, luzes estroboscópicas incapacitantes, dispersores de gás/fumaça) poderá ser acionado sem **confirmação humana expressa**.

**Implementação Segura:**
1. **Detecção**: Sistema detecta intruso.
2. **Verificação**: Sistema envia vídeo ao dono.
3. **Armar**: Dono confirma "É um invasor".
4. **Engajamento**: Dono aperta e SEGURA um botão no app ("Dead man's switch") para ativar contramedidas não-letais (ex: disparar fumaça ou strobo). Se soltar o botão, para imediatamente.

### Dispositivos Proibidos no Projeto
O projeto **Home Security DIY** não fornecerá código, esquemas ou suporte para:
- Armas de fogo automatizadas (obviamente).
- Dispositivos que causem dano físico permanente.
- Armadilhas ("booby traps") que funcionem sem discriminação.

---

## 3. Resumo

| Recurso | Status Legal/Ético | Abordagem do Projeto |
|---------|--------------------|----------------------|
| Drone Terrestre Autônomo | ✅ Verde | Permitido em propriedade privada. |
| Drone Aéreo Autônomo | 🔴 Vermelho | Proibido (requer piloto pronto para intervir e VLOS). Implementar apenas como "Assistente de Piloto". |
| Vigilância de Rua | 🟡 Amarelo | Câmeras não podem focar propriedade vizinha ou via pública (máscaras de privacidade obrigatórias). |
| Defesa Ativa Autônoma | 🔴 Vermelho | **PROIBIDA**. Apenas Human-in-the-Loop. |

Esta política será incorporada na arquitetura (ADRs) e no código (travas de software).
