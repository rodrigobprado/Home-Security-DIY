# PRD – Backup e Resiliência

> Sistema de Home Security – Open Source / Open Hardware
>
> Versão: 1.0 | Data: 2026-02-18 | Responsável: Agente_Documentador

---

## 1. Visão geral

- **Nome do produto/funcionalidade**: Sistema de Backup, Redundância e Resiliência
- **Responsável**: Agente_Arquiteto_Tecnico (especificação), Agente_Documentador (documentação)
- **Data**: 2026-02-18
- **PRDs relacionados**: PRD_LOCAL_PROCESSING_HUB, PRD_NETWORK_SECURITY, PRD_SENSORS_AND_ALARMS_PLATFORM, PRD_NOTIFICATIONS_AND_ALERTS

---

## 2. Problema e oportunidade

### 2.1 Problema

Sistemas de segurança residencial são vulneráveis a falhas de infraestrutura:
- **Queda de energia**: Sistema inteiro fica inoperante, deixando residência desprotegida
- **Queda de internet**: Notificações remotas e acesso ao dashboard são perdidos
- **Falha de hardware**: Corrupção de SSD/SD card pode destruir toda a configuração
- **Falta de backup**: Reconstruir configurações complexas (HA, Frigate, Z2M) leva horas ou dias
- **Ponto único de falha**: Servidor central, se falhar, derruba todo o sistema

### 2.2 Oportunidade

Implementar um sistema de resiliência com:
- **Nobreak (UPS)** para autonomia em queda de energia
- **Failover 4G** para manter notificações sem internet fixa
- **Backup automatizado** de configurações com restauração rápida
- **Monitoramento de saúde** do sistema com alertas proativos
- **Redundância estratégica** para componentes críticos

---

## 3. Público-alvo

| Perfil | Necessidades específicas |
|--------|--------------------------|
| **Proprietário rural** | Alta resiliência: energia instável, internet limitada |
| **Proprietário urbano** | Proteção contra quedas de energia e internet |
| **Morador de apartamento** | Nobreak básico, backup de configuração |
| **Usuário técnico** | Automação de backups, monitoramento avançado |

---

## 4. Requisitos funcionais

### 4.1 Continuidade de energia (nobreak/UPS)

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-001 | Nobreak para servidor central | Autonomia mínima 30 minutos | Alta |
| RF-002 | Nobreak para switch de rede/PoE | Manter câmeras e rede operando | Alta |
| RF-003 | Proteção contra surtos | Filtro de linha integrado ao nobreak | Alta |
| RF-004 | Monitoramento de status via USB/rede | Integração com Home Assistant (NUT) | Alta |
| RF-005 | Shutdown gracioso automático | Desligar servidor se bateria < 10% | Alta |
| RF-006 | Notificação de queda de energia | Push + Telegram imediatos | Alta |
| RF-007 | Notificação de retorno de energia | Confirmação de restabelecimento | Média |
| RF-008 | Sensores Zigbee com bateria própria | Funcionam independente de energia da rede | Alta |

### 4.2 Redundância de internet (failover 4G)

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-009 | Modem/roteador 4G como backup | Ativado automaticamente na queda da internet fixa | Média |
| RF-010 | Failover automático | Troca transparente para 4G | Média |
| RF-011 | Failback automático | Retornar para internet fixa quando restabelecida | Média |
| RF-012 | Priorizar tráfego no 4G | Apenas notificações e acesso remoto, sem streaming | Média |
| RF-013 | Monitoramento de status da internet | Ping periódico para verificar conectividade | Alta |
| RF-014 | Alerta de uso do failover 4G | Notificar quando 4G está ativo | Média |
| RF-015 | SMS via modem 4G | Enviar SMS independente de internet | Média |

### 4.3 Backup de configurações

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-016 | Backup automático do Home Assistant | Completo (config + add-ons + banco de dados) | Alta |
| RF-017 | Backup da configuração do Zigbee2MQTT | coordinator_backup.json + configuration.yaml | Alta |
| RF-018 | Backup da configuração do Frigate | config.yml + modelos de IA | Alta |
| RF-019 | Backup da configuração do Mosquitto | mosquitto.conf + ACLs | Alta |
| RF-020 | Frequência de backup | Diário (configurações) + semanal (completo) | Alta |
| RF-021 | Armazenamento local de backups | Diretório separado no SSD ou HD externo | Alta |
| RF-022 | Armazenamento remoto de backups | NAS, Google Drive ou outro destino externo | Média |
| RF-023 | Retenção de backups | Manter últimos 7 diários + 4 semanais | Alta |
| RF-024 | Verificação de integridade | Checksum (SHA256) de cada backup | Média |
| RF-025 | Restauração testada | Procedimento documentado e testado periodicamente | Alta |

### 4.4 Monitoramento de saúde do sistema

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-026 | Monitorar uso de CPU, RAM e disco | Via integração System Monitor do HA | Alta |
| RF-027 | Alerta de disco > 85% | Notificação para limpar/expandir | Alta |
| RF-028 | Alerta de temperatura do servidor | > 70°C | Alta |
| RF-029 | Monitorar uptime do Home Assistant | Alerta se reiniciar inesperadamente | Alta |
| RF-030 | Monitorar uptime do Frigate | Alerta se serviço cair | Alta |
| RF-031 | Monitorar status do Zigbee2MQTT | Alerta se coordenador desconectar | Alta |
| RF-032 | Monitorar status das câmeras | Alerta se câmera ficar offline | Alta |
| RF-033 | Monitorar bateria de sensores Zigbee | Alerta quando < 20% | Alta |
| RF-034 | Dashboard de saúde do sistema | Visão consolidada no HA | Média |

### 4.5 Redundância de componentes críticos

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-035 | Coordenador Zigbee reserva | Manter backup configurado | Baixa |
| RF-036 | Cartão microSD de boot reserva | Para Mini PC com boot alternativo | Baixa |
| RF-037 | Baterias reserva para sensores | Estoque de CR2032/CR123A | Média |
| RF-038 | Rota de mesh Zigbee redundante | Mínimo 2 dispositivos roteadores | Alta |

### 4.6 Recuperação de desastre

| ID | Requisito | Especificação | Prioridade |
|----|-----------|---------------|------------|
| RF-039 | Procedimento documentado de restauração | Passo a passo para reconstruir o sistema | Alta |
| RF-040 | Tempo de recuperação alvo (RTO) | < 2 horas para sistema funcional | Alta |
| RF-041 | Ponto de recuperação alvo (RPO) | < 24 horas (perda máxima de dados) | Alta |
| RF-042 | Kit de emergência | SD card bootável + backup recente | Média |

---

## 5. Requisitos não funcionais

### 5.1 Performance

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-001 | Tempo de switchover para nobreak | < 10ms (sem interrupção perceptível) |
| RNF-002 | Tempo de failover para 4G | < 30 segundos |
| RNF-003 | Tempo de backup diário | < 10 minutos |
| RNF-004 | Impacto do backup no sistema | < 10% de CPU adicional |

### 5.2 Confiabilidade

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-005 | Autonomia mínima do nobreak | 30 minutos com carga total |
| RNF-006 | Autonomia recomendada | 60 minutos |
| RNF-007 | Vida útil da bateria do nobreak | 2-3 anos, com monitoramento |
| RNF-008 | Taxa de sucesso dos backups | > 99% |

### 5.3 Segurança

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-009 | Backups criptografados | Criptografia AES-256 para backups remotos |
| RNF-010 | Acesso aos backups | Restrito ao administrador |
| RNF-011 | Credenciais não expostas no backup | Secrets separados e criptografados |

### 5.4 Automação

| ID | Requisito | Especificação |
|----|-----------|---------------|
| RNF-012 | Backups sem intervenção | Cron job ou add-on automatizado |
| RNF-013 | Monitoramento contínuo | Sem necessidade de verificação manual |
| RNF-014 | Alertas proativos | Notificar antes que problemas causem falha |

---

## 6. Arquitetura técnica

### 6.1 Diagrama de resiliência

```
                    REDE ELÉTRICA (220V)
                          │
                    ┌─────▼─────┐
                    │  NOBREAK  │
                    │  1500VA   │◄── Monitoramento USB (NUT)
                    │  (UPS)    │
                    └─────┬─────┘
                          │
              ┌───────────┼───────────┐
              │           │           │
       ┌──────▼──────┐ ┌─▼────────┐ ┌▼──────────┐
       │ MINI PC     │ │ SWITCH   │ │ MODEM     │
       │ (Servidor)  │ │ PoE     │ │ INTERNET  │
       └──────┬──────┘ └──────────┘ └─────┬─────┘
              │                           │
              │                    ┌──────▼──────┐
              │                    │  INTERNET   │
              │                    │  FIXA       │
              │                    └──────┬──────┘
              │                           │
              │           ┌───────────────┤
              │           │               │
              │    ┌──────▼──────┐  ┌─────▼──────┐
              │    │  ROTEADOR   │  │  MODEM 4G  │
              │    │  PRINCIPAL  │  │  (Failover)│
              │    └─────────────┘  └────────────┘
              │
     ┌────────┴────────────────────┐
     │     SISTEMA DE BACKUP       │
     │                             │
     │  ┌─────────────┐            │
     │  │ SSD Sistema │──► Backup local (HD externo)
     │  └─────────────┘    │
     │                     └──► Backup remoto (NAS/Cloud)
     │                             │
     └─────────────────────────────┘
```

### 6.2 Fluxo de queda de energia

```
1. Energia da rede cai
           │
           ▼
2. Nobreak assume (< 10ms)
   ├── Equipamentos continuam operando
   ├── NUT detecta "on battery"
   │
   ▼
3. Home Assistant recebe evento do NUT
   ├── Notificação: "Queda de energia detectada"
   ├── Registra timestamp
   │
   ▼
4. Monitoramento de bateria do nobreak
   ├── > 20%: Sistema opera normalmente
   ├── 10-20%: Alerta de bateria baixa
   └── < 10%: Shutdown gracioso
       ├── Salvar estado atual
       ├── Notificar: "Sistema desligando por falta de energia"
       └── Desligar servidor de forma segura
           │
           ▼
5. Energia retorna:
   ├── Nobreak recarrega
   ├── Servidor reinicia automaticamente (BIOS wake on AC)
   ├── Serviços sobem automaticamente (Docker restart)
   └── Notificação: "Sistema restabelecido"
```

### 6.3 Fluxo de failover de internet

```
1. Monitor verifica internet fixa (ping a cada 30s)
           │
           ▼
2. Internet fixa cai (3 pings consecutivos falharam)
           │
           ▼
3. Roteador ativa failover 4G
   ├── Modem 4G conecta à operadora
   ├── Rotas de rede redirecionadas
   │
   ▼
4. Home Assistant detecta failover
   ├── Notificação via SMS (4G): "Internet fixa caiu, usando 4G"
   ├── Reduzir tráfego (pausar streaming remoto)
   ├── Manter: notificações, acesso VPN, comandos
   │
   ▼
5. Internet fixa retorna
   ├── Failback automático para internet fixa
   └── Notificação: "Internet fixa restabelecida"
```

### 6.4 Estratégia de backup

```yaml
# Agenda de backups
backup:
  diario:
    horario: "03:00"
    conteudo:
      - Home Assistant (full backup)
      - Zigbee2MQTT (config + coordinator)
      - Frigate (config)
      - Mosquitto (config)
    destino: /mnt/backup_local/diario/
    retencao: 7 dias

  semanal:
    horario: "03:00 (domingo)"
    conteudo:
      - Tudo do diário
      - Banco de dados HA (MariaDB)
      - Gravações marcadas (Frigate)
    destino:
      - /mnt/backup_local/semanal/
      - rsync para NAS ou rclone para nuvem
    retencao: 4 semanas

  mensal:
    horario: "03:00 (1º do mês)"
    conteudo:
      - Backup completo do sistema
    destino:
      - HD externo USB (offline)
    retencao: 6 meses
```

---

## 7. Produtos/componentes recomendados

### 7.1 Nobreak (UPS)

| Modelo | Potência | Autonomia estimada* | Preço estimado | Observações |
|--------|----------|---------------------|----------------|-------------|
| **APC Back-UPS 600VA** | 600VA / 330W | 15-25 min | R$ 300-450 | Básico para apartamento |
| **APC Back-UPS 1000VA** | 1000VA / 600W | 25-40 min | R$ 500-700 | Recomendado casa urbana |
| **APC Smart-UPS 1500VA** | 1500VA / 980W | 40-60 min | R$ 800-1.200 | Recomendado rural |
| **SMS Nobreak 1200VA** | 1200VA / 660W | 30-45 min | R$ 450-650 | Alternativa nacional |
| **NHS Mini III 600VA** | 600VA / 300W | 15-20 min | R$ 250-400 | Econômico |

*Autonomia estimada com carga de Mini PC (65W) + switch PoE (50W) + modem (15W) = ~130W

### 7.2 Failover 4G

| Componente | Modelo sugerido | Preço estimado | Observações |
|------------|-----------------|----------------|-------------|
| Modem USB 4G | Huawei E3372 | R$ 150-250 | Para SMS + dados |
| Roteador com failover | Mikrotik hAP ac3 | R$ 400-600 | Dual WAN, failover nativo |
| Roteador com failover | TP-Link ER605 | R$ 250-400 | Multi-WAN, custo-benefício |
| Chip de dados 4G | Operadora local | R$ 30-50/mês | Plano dados mínimo (2GB) |

### 7.3 Armazenamento de backup

| Componente | Modelo sugerido | Preço estimado | Observações |
|------------|-----------------|----------------|-------------|
| HD externo USB 1TB | WD Elements | R$ 250-350 | Backup offline local |
| HD externo USB 2TB | Seagate Expansion | R$ 350-500 | Para cenários com mais dados |
| NAS 2 baias | Synology DS223 | R$ 1.500-2.200 | Backup + NVR secundário (avançado) |

### 7.4 Software de backup

| Ferramenta | Função | Custo |
|------------|--------|-------|
| HA Backup (nativo) | Backup completo do HA | Gratuito |
| Samba Backup (add-on) | Backup para SMB/NAS | Gratuito |
| rclone | Sync para nuvem (Google Drive, S3) | Gratuito |
| rsync | Sync para NAS/HD externo | Gratuito |
| Duplicati | Backup criptografado para nuvem | Gratuito |

---

## 8. Estimativas por cenário

### 8.1 Cenário rural (alta resiliência)

| Componente | Preço estimado |
|------------|----------------|
| Nobreak 1500VA (APC Smart-UPS) | R$ 1.000 |
| Roteador com failover (Mikrotik) | R$ 500 |
| Modem USB 4G | R$ 200 |
| Chip de dados 4G (anual) | R$ 480/ano |
| HD externo 1TB (backup local) | R$ 300 |
| **Total setup** | **R$ 2.000** |
| **Custo anual recorrente (4G)** | **R$ 480** |

### 8.2 Cenário casa urbana

| Componente | Preço estimado |
|------------|----------------|
| Nobreak 1000VA (APC) | R$ 600 |
| Roteador com failover (TP-Link ER605) | R$ 300 |
| Modem USB 4G | R$ 200 |
| Chip de dados 4G (anual) | R$ 360/ano |
| HD externo 1TB (backup local) | R$ 300 |
| **Total setup** | **R$ 1.400** |
| **Custo anual recorrente (4G)** | **R$ 360** |

### 8.3 Cenário apartamento (básico)

| Componente | Preço estimado |
|------------|----------------|
| Nobreak 600VA (NHS/SMS) | R$ 300 |
| HD externo 500GB (backup local) | R$ 200 |
| Backup em nuvem (rclone + Google Drive) | R$ 0 |
| **Total setup** | **R$ 500** |
| **Custo anual recorrente** | **R$ 0** |

---

## 9. Critérios de aceitação

| ID | Critério | Método de verificação |
|----|----------|----------------------|
| CA-001 | Sistema continua operando em queda de energia por 30 min | Teste de desconexão da rede elétrica |
| CA-002 | Notificação enviada em < 30 segundos após queda de energia | Teste com cronômetro |
| CA-003 | Shutdown gracioso ocorre quando bateria < 10% | Teste de descarga |
| CA-004 | Failover 4G ativado em < 30 segundos após queda de internet | Teste desconectando internet fixa |
| CA-005 | Notificações funcionam via 4G | Teste de push + Telegram no failover |
| CA-006 | Backup diário executado com sucesso | Verificação de logs e arquivos |
| CA-007 | Restauração completa em < 2 horas | Teste de restauração em hardware limpo |
| CA-008 | Monitoramento detecta disco > 85% | Teste com arquivos grandes |
| CA-009 | Alerta de câmera offline em < 5 minutos | Teste desconectando câmera |
| CA-010 | Sistema reinicia automaticamente após retorno de energia | Teste de power cycle |

---

## 10. Métricas de sucesso

| Métrica | Alvo | Medição |
|---------|------|---------|
| **Uptime do sistema** | > 99.5% (máx ~43h downtime/ano) | Monitoramento |
| **Autonomia em queda de energia** | > 30 minutos | Teste periódico |
| **Taxa de sucesso dos backups** | > 99% | Logs de backup |
| **Tempo de recuperação (RTO)** | < 2 horas | Teste de restauração |
| **Ponto de recuperação (RPO)** | < 24 horas | Verificação da idade do backup |

---

## 11. Riscos e dependências

### 11.1 Riscos

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Bateria do nobreak degradada | Média | Alto | Testar trimestralmente, trocar a cada 2-3 anos |
| Backup corrompido | Baixa | Alto | Verificação de integridade (checksum) |
| 4G sem cobertura | Baixa (urbano), Média (rural) | Alto | Testar cobertura antes, considerar outra operadora |
| Disco de backup cheio | Média | Médio | Monitoramento de espaço + rotação automática |
| Queda prolongada de energia (> 1h) | Média | Alto | Considerar gerador para cenário rural |

### 11.2 Dependências

| Dependência | Tipo | PRD relacionado |
|-------------|------|-----------------|
| Hardware central (Mini PC) | Infraestrutura | PRD_LOCAL_PROCESSING_HUB |
| Rede local | Infraestrutura | PRD_NETWORK_SECURITY |
| Sistema de notificações | Funcional | PRD_NOTIFICATIONS_AND_ALERTS |
| Sistema de alarme | Funcional | PRD_SENSORS_AND_ALARMS_PLATFORM |

---

## 12. Referências

### Documentos do projeto
- `docs/ARQUITETURA_TECNICA.md` - Seções 4, 7, 9
- `prd/PRD_LOCAL_PROCESSING_HUB.md` - Especificação do servidor
- `prd/PRD_NETWORK_SECURITY.md` - Infraestrutura de rede
- `rules/RULES_COMPLIANCE_AND_STANDARDS.md`

### Externos
- [Home Assistant - Backup](https://www.home-assistant.io/common-tasks/os/#backups)
- [Network UPS Tools (NUT)](https://www.home-assistant.io/integrations/nut/)
- [rclone - Cloud Sync](https://rclone.org/)
- [Samba Backup Add-on](https://github.com/thomasmauerer/hassio-addons)

---

> **Status**: Rascunho v1.0
>
> **Próxima revisão**: Após validação pelo Agente_Arquiteto_Tecnico
