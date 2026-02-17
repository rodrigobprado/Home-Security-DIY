# Gestão de Falsos Positivos e Fadiga de Alerta

**Data**: 2026-02-17
**Referência**: T-055 (TASKS_BACKLOG)

---

## 1. O Problema da Fadiga de Alerta

A "Fadiga de Alerta" ocorre quando um sistema gera tantas notificações irrelevantes (falsos positivos) que o operador (morador) passa a ignorá-las ou até mesmo desativa o sistema. Para um sistema de segurança residencial DIY, isso é a falha crítica número 1.

### 1.1 Metas de Performance
- **Falsos Alarmes (Sirene)**: < 1 por ano.
- **Notificações de Movimento (Push)**: Apenas eventos com pessoas/veículos confirmados.
- **Erros de Identificação (IA)**: < 5% em condições adversas.

---

## 2. Estratégias de Mitigação

### 2.1 Confirmação Multi-Sensor ("Double Knock")

NUNCA disparar a sirene baseada em um único sensor PIR interno, pois insetos, correntes de ar quente ou animais podem ativá-lo.

**Lógica Recomendada**:
- **Alarme Confirmado**: Disparar APENAS se:
    - Sensor A (PIR Sala) aciona E Sensor B (Porta Frente) aciona em < 30s.
    - OU Sensor A aciona 2x em < 60s.
- **Pré-Alarme**: Se apenas 1 sensor aciona:
    - Tocar "Ding-dong" suave.
    - Enviar notificação de "Atividade Suspeita" (sem sirene).

### 2.2 Cross-Zoning (Físico + Visual)

Utilizar a IA do Frigate para confirmar disparos de sensores físicos.

**Fluxo**:
1. Sensor de Muro (Laser/IV) detecta intrusão.
2. Sistema agenda disparo em 10 segundos.
3. Câmera que cobre o setor verifica se há "Person" com confiabilidade > 70%.
    - **Se SIM**: Disparo imediato da Sirene.
    - **Se NÃO**: Notificação silenciosa "Sensor de muro ativado (sem confirmação visual)".

### 2.3 Ajuste de Sensibilidade e Mascaramento

#### Câmeras (Frigate)
- **Min Score**: Subir de 0.5 para 0.7 em áreas com muitas sombras/árvores.
- **Masks**: Mascarar árvores que balançam com vento e áreas de rua movimentada.
- **Object Size**: Definir tamanho mínimo/máximo (ex: evitar que gato seja detectado como pessoa).

#### Sensores PIR
- **Pet Immunity**: Usar sensores com lentes específicas para ignorar animais < 20kg.
- **Posicionamento**: Não apontar para janelas (sol direto) ou saídas de ar condicionado.

---

## 3. Implementação no Home Assistant

Exemplo de automação segura (YAML) para evitar falsos disparos.

```yaml
alias: "Segurança - Alarme Confirmado (Double Knock)"
trigger:
  - platform: state
    entity_id: group.sensores_internos
    to: "on"
condition:
  - condition: state
    entity_id: alarm_control_panel.alarmo
    state: "armed_away"
action:
  - wait_for_trigger:
      - platform: state
        entity_id: group.sensores_internos
        to: "on"
        from: "off"
    timeout: "00:00:30"
    continue_on_timeout: false
  
  # Se chegou aqui, um segundo sensor disparou em < 30s
  - service: alarm_control_panel.alarm_trigger
    target:
      entity_id: alarm_control_panel.alarmo
```

---

## 4. Manutenção Contínua (Tuning)

A calibração do sistema não termina na instalação.

1. **Modo Silencioso (1ª Semana)**: Operar o sistema registrando eventos mas SEM tocar sirene. Analisar logs para identificar sensores problemáticos.
2. **Review de Gravações**: Sempre que houver um falso positivo do Frigate, salvar a imagem ("False Positive") e treinar/ajustar a config.
3. **Limpeza**: Teias de aranha em câmeras infravermelho são a maior causa de falso movimento à noite. Limpeza mensal obrigatória.

---

## 5. Conclusão

Um sistema que dispara à toa é pior que nenhum sistema. A confiabilidade deve ser priorizada sobre a sensibilidade extrema. É preferível perder uma detecção precoce de perímetro (mas pegar na porta) do que acordar os vizinhos com alarme falso e perder a credibilidade.
