# 3. Adoção do Zigbee como Protocolo de Sensores

Data: 2026-02-17

## Status

Aceito

## Contexto

O sistema necessita de uma rede de sensores sem fio (wireless) de baixo consumo, baixo custo e alta confiabilidade para detecção de abertura de portas/janelas, movimento e fumaça. Wi-Fi é inadequado devido ao alto consumo de energia (baterias duram pouco) e congestionamento da rede 2.4GHz.

As alternativas consideradas foram:
- Zigbee
- Z-Wave
- Wi-Fi (Shellies, Tuya)
- 433MHz (RF simples)
- Thread/Matter (emergente)

## Decisão

Escolhemos o **Zigbee 3.0** como protocolo principal para sensores.

## Consequências

### Positivas
- **Custo**: Sensores custam 30-50% menos que equivalentes Z-Wave.
- **Disponibilidade**: Ampla oferta no mercado brasileiro (Sonoff, Aqara, Tuya).
- **Consumo**: Baterias CR2032 duram 1-2 anos.
- **Mesh**: Dispositivos alimentados na tomada (lâmpadas, tomadas) funcionam como repetidores, estendendo o alcance.
- **Compatibilidade**: Zigbee2MQTT suporta milhares de dispositivos de centenas de marcas.

### Negativas
- **Interferência**: Opera na frequência 2.4GHz, competindo com Wi-Fi.
- **Padrão fragmentado**: Alguns fabricantes fogem do padrão (ex: Aqara antigo), exigindo "quirks" no software.

## Mitigação
- Configurar canal Zigbee 20 ou 25 para evitar sobreposição com canais Wi-Fi 1, 6 e 11.
- Usar coordenador de alta qualidade (Sonoff Dongle-P ou SLZB-06).
- Adicionar repetidores (tomadas inteligentes) estrategicamente para fortalecer a malha.
