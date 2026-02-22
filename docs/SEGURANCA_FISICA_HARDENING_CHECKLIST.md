# Checklist de Segurança Física e Hardening da Infraestrutura (Issue #105)

Data: 2026-02-22

## 1. Perímetro e barreiras físicas (validação de campo)

- [ ] Perímetro fechado e em bom estado
- [ ] Cerca elétrica instalada e sinalizada (2,20m + placa a cada 10m)
- [ ] Portões com fechadura adequada
- [ ] Portas reforçadas com fechadura multiponto
- [ ] Janelas térreas protegidas (grade/laminado)
- [ ] Batentes fixados com parafusos longos
- [ ] Protetor de cilindro em portas de entrada

Evidência requerida: fotos com data + responsável da inspeção.

## 2. Iluminação e visibilidade (validação de campo)

- [ ] Iluminação externa funcional
- [ ] Sem pontos cegos (mín. 50 lux em entradas)
- [ ] Sem ofuscamento em câmeras
- [ ] Sem exposição de objetos de valor
- [ ] Paisagismo sem pontos de ocultação

Evidência requerida: fotos noturnas + medição de lux.

## 3. Hardening do servidor (técnico + físico)

- [ ] Criptografia de disco ativa (LUKS)
- [ ] Dropbear para unlock remoto configurado (quando aplicável)
- [ ] Senha de BIOS ativa e boot USB desabilitado
- [ ] Servidor fisicamente protegido/oculto
- [ ] Nobreak testado com autonomia mínima de 30 min
- [ ] Backup automático off-site testado

Evidência técnica: relatório de `scripts/physical_hardening_audit.sh`.
Evidência física: foto/localização do servidor e nobreak.

## 4. Conformidade elétrica (NBR 5410)

- [ ] DPS instalado no quadro
- [ ] Aterramento de todos os equipamentos do sistema

Evidência requerida: laudo/foto da instalação por profissional habilitado.

## 5. Execução recomendada

1. Rodar auditoria técnica local:
   - `bash scripts/physical_hardening_audit.sh`
2. Coletar evidências físicas em campo.
3. Consolidar relatório final com data/responsável e anexar na issue.
