# Engenharia Social e Ameaças Internas

**Data**: 2026-02-17
**Referência**: T-054 (TASKS_BACKLOG)

---

## 1. Visão Geral

A segurança mais forte de hardware e software pode ser anulada por falhas humanas. Este documento descreve vetores de ataque baseados em psicologia (Engenharia Social) e riscos originados de pessoas com acesso legítimo (Insider Threats).

---

## 2. Vetores de Engenharia Social

### 2.1 Pretexting (O "Técnico da Net")
**Cenário**: Um indivíduo uniformizado chega ao portão alegando ser técnico da operadora de internet/energia para "reparo urgente".
**Risco**: Acesso físico ao roteador, switch ou instalação de keyloggers.
**Contramedida (SOP)**:
- NUNCA permitir entrada sem solicitação prévia confirmada pelo morador.
- Verificar ordem de serviço ligando para a central oficial (não usar o número dado pelo técnico).

### 2.2 Phishing Direcionado (Spear Phishing)
**Cenário**: E-mail ou SMS parecendo vir do sistema de alarme ("Alarmo: Senha expirada, clique para resetar").
**Risco**: Roubo de credenciais do Home Assistant.
**Contramedida**:
- O Home Security DIY é **100% Local**. Ele NUNCA envia e-mails pedindo senha.
- Treinamento dos moradores para reconhecer URLs falsas.

### 2.3 Duress (Coação)
**Cenário**: Criminoso aborda o morador na entrada e o obriga a desarmar o alarme.
**Risco**: Desarmamento legítimo sob ameaça.
**Contramedida**:
- **Código de Pânico (Duress Code)**: Configurar um código especial no Alarmo (ex: `9999`) que visualmente desarma o sistema (para satisfazer o atacante) mas silenciosamente envia alerta crítico para contatos de emergência e Telegram.

---

## 3. Ameaças Internas (Insider Threats)

### 3.1 Funcionários Domésticos e Prestadores
**Risco**: Acesso legítimo à casa pode ser usado para reconhecimento ou sabotagem.
**Contramedidas**:
- **Contas de Convidados**: Criar usuários no Home Assistant com permissão apenas de visualização (não admin).
- **Wi-Fi Guest**: NUNCA dar a senha da rede principal. Usar VLAN Guest isolada que não acessa o servidor.
- **Revogação**: Desativar credenciais/códigos imediatamente após o fim do contrato/serviço.

### 3.2 O "Inimigo Íntimo"
**Risco**: Ex-cônjuges ou moradores expulsos que ainda possuem chaves ou senhas.
**Contramedidas**:
- Rotação de credenciais Wi-Fi e HA após mudanças na composição familiar.
- Troca física de segredos das fechaduras (ou reprogramação de tags RFID).

---

## 4. Procedimentos Operacionais Padrão (SOP)

1. **Entregas**: Não abrir o portão principal. Usar passa-volumes ou receber na calçada com portão fechado.
2. **Wi-Fi**: Não colar a senha do Wi-Fi na geladeira. Uso de QR Code para rede de visitas.
3. **Descarte**: Destruir etiquetas de encomendas (nome/endereço) e documentos sensíveis antes de jogar no lixo (Lixo é fonte de reconhecimento).

---

## 5. Conclusão

"A confiança é a vulnerabilidade". O sistema técnico deve operar sob o princípio de **Zero Trust**, mesmo para pessoas conhecidas, limitando privilégios ao mínimo necessário.
