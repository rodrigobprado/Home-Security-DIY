# Plano de Manutenção e Ciclo de Vida – Sistema de Home Security

> Documento produzido durante revisão do projeto em 2026-02-12
>
> Categoria: Operação / Manutenção preventiva

---

## 1. Objetivo

Definir calendário de manutenção preventiva, ciclo de vida dos componentes e procedimentos de substituição para garantir o funcionamento contínuo do sistema de segurança.

---

## 2. Calendário de Manutenção Preventiva

### 2.1 Manutenção semanal

| Ação | Responsável | Ferramenta |
|------|-------------|------------|
| Verificar status de todos os sensores no dashboard | Morador | Home Assistant |
| Verificar se há alertas pendentes/não resolvidos | Morador | App HA |
| Verificar logs de acesso (acessos suspeitos) | Morador | Home Assistant |

### 2.2 Manutenção mensal

| Ação | Responsável | Ferramenta |
|------|-------------|------------|
| Verificar atualizações de firmware das câmeras | Admin | Interface web da câmera |
| Verificar atualizações do Home Assistant | Admin | HA Supervisor |
| Verificar atualizações do Frigate | Admin | Docker/Supervisor |
| Limpar lentes das câmeras externas | Morador | Pano de microfibra |
| Testar disparo do alarme (modo teste) | Morador | Alarmo |
| Verificar nível de bateria de todos os sensores Zigbee | Admin | HA → Zigbee2MQTT |
| Verificar integridade da gravação (reproduzir amostra) | Admin | Frigate |
| Verificar espaço livre em disco de gravações | Admin | HA ou SSH |

### 2.3 Manutenção trimestral

| Ação | Responsável | Ferramenta |
|------|-------------|------------|
| Teste completo do nobreak (simular queda de energia) | Admin | Desligar disjuntor por 5min |
| Verificar estado do HDD via S.M.A.R.T. | Admin | `smartctl` via SSH |
| Testar notificações por todos os canais (push, SMS, Telegram) | Morador | HA automação de teste |
| Verificar integridade da VPN (conectar remotamente) | Admin | WireGuard |
| Revisar regras de firewall | Admin | Roteador |
| Verificar se há dispositivos desconhecidos na rede | Admin | `nmap` ou router DHCP list |
| Testar backup de configuração (restaurar em ambiente de teste) | Admin | HA backup |

### 2.4 Manutenção semestral

| Ação | Responsável | Ferramenta |
|------|-------------|------------|
| Rotação de senhas de acesso ao HA e VPN | Admin | HA, WireGuard |
| Revisar ângulos de câmera (vegetação pode ter crescido) | Morador | Verificação visual |
| Verificar estado físico de câmeras externas (corrosão, umidade) | Morador | Inspeção visual |
| Verificar estado de cabos e conectores (PoE, energia) | Admin | Inspeção visual |
| Atualizar whitelist de pessoas autorizadas (se usar reconhecimento facial) | Morador | Frigate/HA |
| Verificar estado da cerca elétrica (se aplicável) | Técnico | Multímetro |

### 2.5 Manutenção anual

| Ação | Responsável | Ferramenta |
|------|-------------|------------|
| Auditoria completa de segurança (todas as camadas) | Admin/Técnico | Checklist |
| Revisar e atualizar plano de resposta a incidentes | Admin | Documentação |
| Verificar se fabricantes ainda fornecem atualizações para todos os dispositivos | Admin | Sites dos fabricantes |
| Testar todas as automações de segurança (cenário completo) | Admin | HA |
| Avaliar necessidade de upgrade de hardware | Admin | Monitoramento de recursos |
| Revisar estimativas de custo operacional | Admin | Planilha |
| Backup completo offsite (configuração + gravações importantes) | Admin | Disco externo |

---

## 3. Ciclo de Vida dos Componentes

### 3.1 Expectativa de vida útil

| Componente | Vida útil estimada | Indicadores de substituição | Custo de reposição estimado |
|-----------|-------------------|---------------------------|---------------------------|
| **Bateria sensor Zigbee (CR2032)** | 1-2 anos | Alerta de bateria baixa no HA (< 20%) | R$ 5-15 |
| **Bateria fechadura eletrônica** | 6-12 meses | Alerta de bateria baixa (1 semana antes) | R$ 20-50 (4x AA) |
| **Bateria nobreak** | 2-4 anos | Autonomia reduzida, alerta do UPS | R$ 150-400 |
| **HDD de gravações** | 3-5 anos | S.M.A.R.T. com erros, setores realocados | R$ 200-500 (2-4TB) |
| **SSD do sistema** | 5-7 anos | S.M.A.R.T., TBW próximo do limite | R$ 150-300 (256GB) |
| **Câmera IP externa** | 3-5 anos | Degradação de imagem, vedação comprometida | R$ 200-700 |
| **Câmera IP interna** | 5-7 anos | Degradação de imagem | R$ 150-500 |
| **Mini PC servidor** | 5-7 anos | Performance insuficiente, hardware falho | R$ 800-1.500 |
| **Sensor Zigbee** | 5-10 anos | Falha de comunicação frequente | R$ 50-150 |
| **Coordenador Zigbee** | 5-7 anos | Falha de comunicação com sensores | R$ 100-300 |
| **Switch PoE** | 5-10 anos | Portas falhando, superaquecimento | R$ 400-800 |
| **Roteador/Firewall** | 3-5 anos | Falta de atualizações de segurança | R$ 300-800 |
| **Sirene** | 5-10 anos | Redução de volume, falha no acionamento | R$ 100-200 |

### 3.2 Alertas automáticos recomendados

| Alerta | Condição | Canal |
|--------|----------|-------|
| Bateria de sensor baixa | < 20% | Push notification |
| Bateria de fechadura baixa | < 30% (1 semana antes de morrer) | Push + SMS |
| HDD com erros S.M.A.R.T. | Qualquer erro preditivo | Push + Email |
| Disco quase cheio | > 85% de uso | Push notification |
| Nobreak em bateria | Queda de energia detectada | Push imediato |
| Nobreak com bateria fraca | Autonomia < 50% do nominal | Push mensal |
| Firmware desatualizado | > 30 dias sem verificar | Push mensal |
| Sensor offline | > 1 hora sem comunicação | Push notification |
| Câmera offline | > 5 minutos sem stream | Push notification |

---

## 4. Gestão de End-of-Life (EOL)

### 4.1 Política quando fabricante para de atualizar firmware

| Dispositivo | Ação recomendada | Alternativa |
|------------|-----------------|-------------|
| **Câmera IP** sem updates | Isolar na VLAN, monitorar tráfego anômalo, planejar substituição | Firmware alternativo: OpenIPC (para câmeras HiSilicon/Ingenic) |
| **Sensor Zigbee** sem updates | Manter se funcional (protocolo padronizado), não depende de firmware | Substituir por modelo suportado |
| **Roteador** sem updates | Substituir IMEDIATAMENTE (risco de segurança crítico) | OpenWrt se compatível |
| **Switch PoE** sem updates | Manter se funcional (managed switches são mais seguros) | Substituir por modelo gerenciável |
| **Mini PC** sem updates | Manter Linux atualizado (não depende do fabricante) | - |

### 4.2 Casos conhecidos de descontinuação

| Componente | Status | Impacto | Mitigação |
|-----------|--------|---------|-----------|
| **Google Coral (TPU)** | Descontinuado | Aceleração IA para Frigate | Migrar para Intel OpenVINO (incluso no N100) |
| **Zigbee2MQTT com dongle CC2531** | Dongle obsoleto | Performance ruim com muitos dispositivos | Migrar para CC2652P (Sonoff ZBDongle-P) |

---

## 5. Custo de Manutenção Anual Estimado

| Item | Rural (R$/ano) | Urbano (R$/ano) | Apartamento (R$/ano) |
|------|---------------|----------------|---------------------|
| Baterias de sensores Zigbee (troca) | R$ 60-120 | R$ 40-80 | R$ 15-30 |
| Baterias de fechadura eletrônica | R$ 80-100 | R$ 80-100 | R$ 80-100 |
| HDD de gravações (amortizado 4 anos) | R$ 100 | R$ 100 | R$ 50 |
| Nobreak bateria (amortizado 3 anos) | R$ 100-130 | R$ 100-130 | R$ 75-100 |
| Internet (dedicada para segurança)* | - | - | - |
| Plano 4G backup (1GB/mês) | R$ 240-360 | R$ 240-360 | R$ 0 (opcional) |
| Energia elétrica (sistema 24/7)** | R$ 360-600 | R$ 300-480 | R$ 120-240 |
| **Total estimado** | **R$ 940-1.310** | **R$ 860-1.150** | **R$ 340-520** |

*Internet não contabilizada pois geralmente já existe na residência.

**Estimativa de energia: Mini PC (~15W) + Switch PoE (~40W) + Câmeras (~5W×N) = 75-120W × 24h × 365d × R$0.85/kWh

---

## 6. Checklist de Manutenção (modelo imprimível)

```
MANUTENÇÃO MENSAL – Data: ___/___/______

[ ] Verificar atualizações de firmware (câmeras, HA, Frigate)
[ ] Limpar lentes das câmeras externas
[ ] Testar alarme em modo teste
[ ] Verificar bateria dos sensores (< 20% = trocar)
[ ] Verificar espaço em disco de gravações
[ ] Reproduzir gravação para verificar qualidade

Observações: _________________________________
Responsável: _________________________________
```

---

## Referências

- [Home Assistant Backup Guide](https://www.home-assistant.io/common-tasks/os/#backups)
- [Frigate Storage Recommendations](https://docs.frigate.video/configuration/record)
- [Zigbee2MQTT FAQ - Battery life](https://www.zigbee2mqtt.io/guide/faq/)
- [smartmontools - S.M.A.R.T. monitoring](https://www.smartmontools.org/)

---

> Próximos passos: Criar automações no Home Assistant para alertas automáticos de manutenção.
