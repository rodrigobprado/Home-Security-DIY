# 2. Adoção do Frigate NVR

Data: 2026-02-17

## Status

Aceito

## Contexto

O sistema requer um NVR (Network Video Recorder) capaz de:
1. Gravar 24/7 múltiplos streams de vídeo (câmeras IP).
2. Realizar detecção de objetos (pessoas, veículos) em tempo real para reduzir falsos positivos de alarmes baseados apenas em pixel-change.
3. Integrar-se via MQTT com o Home Assistant.
4. Processar IA localmente para manter a privacidade.

As alternativas consideradas foram:
- Frigate
- ZoneMinder
- Blue Iris (Windows, pago)
- Shinobi
- MotionEye

## Decisão

Escolhemos o **Frigate** como solução de NVR e detecção de objetos.

## Consequências

### Positivas
- **IA nativa**: Projetado desde o início para usar detectores de objetos (Coral, OpenVINO, TensorRT), eliminando falsos positivos de "movimento de árvores".
- **Integração profunda**: Expõe sensores binários via MQTT para cada objeto/zona, permitindo automações instantâneas no HA.
- **Eficiência**: Usa detectores de hardware para baixo uso de CPU.
- **WebRTC**: Streaming de baixíssima latência para visualização ao vivo.

### Negativas
- **Desprezo por gravação contínua histórica**: O foco é em eventos; a navegação na timeline de 24/7 é menos fluida que em NVRs tradicionais (embora tenha melhorado na v14+).
- **Dependência de hardware**: Requer acelerador (Google Coral ou Intel iGPU/OpenVINO) para performance aceitável com múltiplas câmeras.
- **Configuração**: Baseada inteiramente em arquivo YAML, sem GUI para setups iniciais.

## Mitigação
- Utilizar **Intel OpenVINO** para aproveitar iGPUs de Mini PCs (N100), evitando a escassez/custo do Google Coral.
- Configurar retenção diferenciada (mínima para contínuo, longa para eventos) para otimizar storage.
