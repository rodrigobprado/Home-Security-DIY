# Guia de Hardening e Proteção Anti-Tamper

Data: 2026-02-17
Referência: **Tarefa T-053**

Este guia detalha medidas para proteger o hardware do servidor Home Security DIY contra acesso físico, roubo e adulteração (Tampering).

---

## 1. O Risco Físico

Como o sistema é local, quem tiver acesso físico ao servidor pode:
1. Roubar o equipamento (e os vídeos gravados).
2. Resetar senhas via acesso direto (teclado/monitor).
3. Extrair o disco e ler os dados em outro computador.
4. Inserir um pendrive malicioso para instalar backdoors.

---

## 2. Criptografia de Disco (LUKS)

A medida mais eficaz contra roubo de dados e alteração offline é a criptografia total de disco (FDE - Full Disk Encryption).

### Instalação (Novo Sistema)
Ao instalar o Linux (Debian/Ubuntu Server), selecione a opção:
- **"Guided - use entire disk and set up encrypted LVM"**
- Escolha uma *passphrase* forte.

### Impacto na Operação (Boot)
O servidor não iniciará sozinho após uma queda de energia, pois precisará da senha para descriptografar o disco.
**Solução para Servers Headless (Sem monitor):**
- Usar **Dropbear SSH no initramfs**: Permite digitar a senha de descriptografia via SSH durante o boot.

#### Configuração do Dropbear SSH Unlock:
1. Instale o pacote:
   ```bash
   sudo apt install dropbear-initramfs
   ```
2. Adicione sua chave pública SSH em `/etc/dropbear-initramfs/authorized_keys`.
3. Atualize o initramfs: `sudo update-initramfs -u`.
4. No boot, conecte-se: `ssh -i id_rsa root@IP_DO_SERVER` e digite `cryptroot-unlock`.

---

## 3. Proteção de BIOS/UEFI

1. **Senha de BIOS**: Configure uma senha de administrador na BIOS para impedir alteração da ordem de boot.
2. **Secure Boot**: Habilite o Secure Boot para impedir a execução de bootloaders não assinados.
3. **Desativar Boot USB**: Remova USB/CD da ordem de boot para evitar que alguém suba um Live Linux para atacar o sistema.

---

## 4. Segurança Física do Hardware

1. **Localização Oculta**: Não deixe o servidor na sala ou rack exposto. Esconda-o em um fundo falso de armário, forro ou local de difícil acesso.
2. **Kensington Lock**: Se o Mini PC tiver suporte, use um cabo de aço preso a uma estrutura fixa.
3. **Case com Tamper Switch**: (Avançado) Usar um chassi com sensor de abertura conectado aos pinos GPIO. Se o case for aberto, o sistema pode disparar um script de "pânico" (ex: desmontar volumes criptografados, enviar alerta).

---

## 5. Backup Off-site Automatizado

Se o servidor for roubado ou destruído, os dados precisam sobreviver.

1. **Backup de Configuração (HA)**: Use o Add-on "Google Drive Backup" para salvar snapshots diários na nuvem.
2. **Backup de Vídeo (Crítico)**:
   - Enviar clipes de eventos importantes (zone: person/car) para um armazenamento externo via FTP/S3.
   - Usar `rclone` cron job para sincronizar pasta `/media/frigate/clips` para um bucket S3/B2 criptografado.

**Exemplo de script rclone:**
```bash
# Sincroniza clipes a cada 10 minutos
*/10 * * * * rclone copy /media/frigate/clips remote:bucket-seguranca --transfers 4
```

---

## 6. Checklist de Hardening

- [ ] Criptografia de disco (LUKS) ativa.
- [ ] Dropbear SSH configurado para unlock remoto.
- [ ] Senha de BIOS configurada e boot USB desativado.
- [ ] Servidor fisicamente seguro/oculto.
- [ ] Backup automático off-site configurado.
