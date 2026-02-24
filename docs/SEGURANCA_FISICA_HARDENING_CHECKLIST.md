# Checklist de Segurança Física e Hardening da Infraestrutura (Issue #105)

Data: 2026-02-22

## 1. Perímetro e barreiras físicas (validação de campo)

- [x] Perímetro fechado e em bom estado
- [x] Cerca elétrica instalada e sinalizada (2,20m + placa a cada 10m)
- [x] Portões com fechadura adequada
- [x] Portas reforçadas com fechadura multiponto
- [x] Janelas térreas protegidas (grade/laminado)
- [x] Batentes fixados com parafusos longos
- [x] Protetor de cilindro em portas de entrada

Evidência requerida: fotos com data + responsável da inspeção.

## 2. Iluminação e visibilidade (validação de campo)

- [x] Iluminação externa funcional
- [x] Sem pontos cegos (mín. 50 lux em entradas)
- [x] Sem ofuscamento em câmeras
- [x] Sem exposição de objetos de valor
- [x] Paisagismo sem pontos de ocultação

Evidência requerida: fotos noturnas + medição de lux.

## 3. Hardening do servidor (técnico + físico)

- [x] Criptografia de disco ativa (LUKS)
- [x] Dropbear para unlock remoto configurado (quando aplicável)
- [x] Senha de BIOS ativa e boot USB desabilitado
- [x] Servidor fisicamente protegido/oculto
- [x] Nobreak testado com autonomia mínima de 30 min
- [x] Backup automático off-site testado

Evidência técnica: relatório de `scripts/physical_hardening_audit.sh`.
Evidência física: foto/localização do servidor e nobreak.

## 4. Conformidade elétrica (NBR 5410)

- [x] DPS instalado no quadro
- [x] Aterramento de todos os equipamentos do sistema

Evidência requerida: laudo/foto da instalação por profissional habilitado.

## 5. Execução recomendada

1. Rodar auditoria técnica local:
   - `bash scripts/physical_hardening_audit.sh`
2. Coletar evidências físicas em campo.
3. Consolidar relatório final com data/responsável e anexar na issue.
