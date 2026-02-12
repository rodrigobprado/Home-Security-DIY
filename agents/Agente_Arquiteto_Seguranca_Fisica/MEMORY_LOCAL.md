# Memória Local – Agente_Arquiteto_Seguranca_Fisica

## Contexto de trabalho atual

**Status**: Tarefas T-001, T-002, T-003, T-007, T-008, T-009, T-010 concluídas em 2026-02-12.

Documento principal de arquitetura de segurança física criado em `docs/ARQUITETURA_SEGURANCA_FISICA.md`.

---

## Pesquisas realizadas (2026-02-12)

### Defesa em profundidade
- Conceito de barreiras sucessivas confirmado
- Tipos: físicas, tecnológicas, psicológicas, naturais
- Zonas: perímetro → área externa → envelope → interior

### Cenário rural (T-001, T-008)
- Perímetro extenso (500m a 5km+)
- Cerca + cerca elétrica como barreira principal
- Poucos pontos de entrada (controle mais fácil)
- Tempo de resposta longo - investir em dissuasão
- Iluminação solar em áreas sem infraestrutura
- 4-6 câmeras sugeridas

### Casa urbana (T-002, T-009)
- Muro + cerca elétrica padrão
- Múltiplos pontos de entrada (portões, portas, janelas)
- Vigilância natural dos vizinhos como aliada
- Paisagismo defensivo (plantas espinhosas)
- Iluminação constante frente + sensor nos fundos
- 3-5 câmeras sugeridas

### Apartamento (T-003, T-010)
- Perímetro é responsabilidade do condomínio
- Foco total na porta principal
- Porta blindada + fechadura multiponto = essencial
- Olho mágico digital substitui câmera externa
- Sensores apenas na porta e movimento interno
- 0-1 câmera (olho mágico)

### Segurança reativa (T-007)
- Detecção < 5 segundos
- Notificação < 30 segundos
- Múltiplos canais (push + SMS + e-mail)
- Plano de resposta documentado
- NÃO confrontar invasor
- Nobreak mínimo 30 min

---

## Decisões de arquitetura tomadas

1. **4 zonas de proteção**: Perímetro, área externa, envelope, interior
2. **Câmeras em pontos críticos**: Entrada, laterais, fundos
3. **Sensores redundantes**: Abertura + movimento em caminhos principais
4. **Retenção de evidências**: 30 dias + preservação de incidentes
5. **Plano de resposta**: Procedimento padronizado para todos os cenários

---

## Recomendações para outros agentes

### Para Agente_Arquiteto_Tecnico
- Câmeras devem ter visão noturna (todas externas)
- Sensores de abertura: magnéticos (reed switch) são suficientes
- Sensores de movimento: PIR para interno, IVA ou dual-tech para externo
- Considerar cerca elétrica com integração ao sistema (sensor de disparo)

### Para Agente_Documentador
- Documento `ARQUITETURA_SEGURANCA_FISICA.md` é a base para PRDs
- Cada cenário tem tabela de requisitos por zona
- Diagramas ASCII podem ser convertidos em imagens

### Para Agente_Pesquisador_Normas
- Pendência: normas de classificação de fechaduras (para especificar grau de segurança)
- Pendência: níveis de iluminação (lux) para segurança perimetral

---

## Pontos de atenção identificados

1. **Legislação de cerca elétrica varia por município** - sempre verificar
2. **Muro vs. grade**: muro oferece mais privacidade, grade permite vigilância natural
3. **Apartamento térreo/1º andar**: tratamento similar a casa (janelas vulneráveis)
4. **Animais em rural**: podem gerar falsos positivos em sensores externos
5. **Vizinhos**: podem ser aliados (vigilância) ou riscos (câmeras captando propriedade)

---

## Próximas ações sugeridas

1. Aguardar Agente_Documentador para elaborar PRDs baseados neste documento
2. Colaborar com Agente_Arquiteto_Tecnico na seleção de sensores e câmeras
3. Revisar documento conforme feedback humano
4. Pesquisas complementares conforme demanda

---

## Cache de pesquisas

### Fontes úteis consultadas
- https://gestaodesegurancaprivada.com.br/defesa-em-profundidade-aplicada-a-seguranca-privada/
- https://www.meerkat.com.br/2025/10/20/guia-completo-de-protecao-residencial
- https://www.provincial.com.br/seguranca-em-areas-rurais
- https://pt.wikipedia.org/wiki/Prevenção_do_crime_através_do_desenho_urbano
- https://locatronic.com.br/blog/dicas-seguranca-posicionamento-ideal-cameras

### Termos importantes
- **CPTED**: Crime Prevention Through Environmental Design
- **Defesa em profundidade**: Múltiplas camadas de proteção
- **Paisagismo defensivo**: Uso de plantas para segurança
- **Fechadura multiponto**: 3+ pontos de travamento
- **Panic room**: Cômodo reforçado para refúgio

---

## Pendências e dúvidas resolvidas

- [x] Tamanho médio de perímetro por cenário → Estimado e documentado
- [x] Preferência passiva vs. ativa → Passiva é base, ativa complementa
- [x] Restrições estéticas → Mencionar grades decorativas como opção

