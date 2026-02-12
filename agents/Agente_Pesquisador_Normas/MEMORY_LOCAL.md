# Memória Local – Agente_Pesquisador_Normas

## Contexto de trabalho atual

**Status**: Todas as tarefas concluídas em 2026-02-12.

- T-018 a T-021: Pesquisas iniciais (LGPD, segurança física, CFTV, instalações elétricas)
- T-028 a T-030: Pesquisas complementares (fechaduras, fechaduras eletrônicas, iluminação)

---

## Pesquisas realizadas

### Pesquisas iniciais (T-018 a T-021)

#### T-019: LGPD e proteção de dados ✅
- Exceção Art. 4º, I para uso pessoal/doméstico
- Câmeras que captam via pública devem seguir LGPD integralmente
- Retenção recomendada: 30 dias

#### T-018: Segurança física residencial ✅
- Lei 13.477/2017 + NBR 15.401: Cercas elétricas (altura mín. 2,20m)
- NBR 10821, NBR 7199, NBR 15575: Esquadrias e vidros

#### T-020: Videovigilância (CFTV) ✅
- Retenção residencial: 30 dias
- Resolução: 1080p para identificação
- Visão noturna obrigatória para externas

#### T-021: Instalações elétricas ✅
- NBR 5410: DPS obrigatório
- NBR 5419: Proteção contra descargas atmosféricas
- Nobreak: autonomia mínima 30 minutos

#### OWASP IoT e ETSI EN 303 645 ✅
- Senhas padrão = principal vulnerabilidade
- VLANs separadas para IoT/câmeras
- Firmware updates mensais

---

### Pesquisas complementares (T-028 a T-030)

#### T-028: Classificação de fechaduras ✅

**NBR 14913 - Fechadura de embutir**:
- Classificação por: utilização, segurança, resistência à corrosão
- Graus de segurança: leve a máximo
- Normas relacionadas: NBR 13051, NBR 16833

**EN 1303 - Cilindros (padrão europeu)**:
- Sistema de 8 dígitos de classificação
- Segurança de chave: graus 1 a 6
- Resistência a ataque: graus 0 a D
- Recomendado: grau de chave 5-6, resistência A ou B

#### T-029: Fechaduras eletrônicas ✅

**Certificações aplicáveis**:
- IP65/IP66 para externas
- Criptografia AES-128 mínimo
- FCC/CE para radiofrequência

**Requisitos de segurança**:
- Chave física de backup obrigatória
- Log de acessos com timestamp
- Alerta de bateria baixa
- Protocolo preferencial: Zigbee ou Z-Wave

#### T-030: Níveis de iluminação ✅

**Normas**: NBR 8995-1 (substituiu NBR 5413), IES Lighting Handbook

**Níveis recomendados**:
| Área | Lux mínimo |
|------|------------|
| Identificação facial | 20 |
| Entradas | 50-100 |
| Corredores | 100 |
| Perímetro | 10-30 |

**Conversão**: 10 lux ≈ 1 foot-candle

---

## Regras derivadas criadas

### Fechaduras (REGRA-FECHADURA-01 a 11)
- Grau de segurança médio ou superior
- Multiponto para entradas
- Cilindro EN 1303 grau 5-6
- Protetor de cilindro obrigatório
- Fechaduras eletrônicas: IP65, AES-128, backup físico

### Iluminação (REGRA-ILUM-01 a 10)
- Entradas: mínimo 50 lux
- Uniformidade obrigatória
- Sem ofuscamento em câmeras
- Iluminação constante em entradas principais
- Solar para perímetros rurais

---

## Cache de pesquisas

### Links úteis (fechaduras)
- https://www.normas.com.br/visualizar/abnt-nbr-nm/22471/abnt-nbr14913
- https://lockwiki.com/index.php/EN_1303
- https://www.carlislebrass.com/media/simplepage/standards/bsen1303.pdf

### Links úteis (iluminação)
- https://www.luxatec.com.br/blog/norma-nbr-8995-o-que-ela-diz-sobre-iluminao
- https://inlucce.com.br/lux-norma-brasileira-abnt-nbr/
- https://rclite.com/blog/recommended-outdoor-lighting-levels/

---

## Pendências e dúvidas resolvidas

- [x] Classificação de fechaduras → NBR 14913 + EN 1303
- [x] Fechaduras eletrônicas → IP65, AES-128, Zigbee/Z-Wave
- [x] Níveis de iluminação → NBR 8995-1, IES; 50-100 lux entradas

---

## Status final

✅ **Todas as 7 tarefas concluídas** (T-018 a T-021, T-028 a T-030)

Documentação atualizada em:
- `standards/STANDARDS_TO_RESEARCH.md`
- `rules/RULES_COMPLIANCE_AND_STANDARDS.md`

---

> Última atualização: 2026-02-12
