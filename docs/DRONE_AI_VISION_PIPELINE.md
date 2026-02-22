# Pipeline de Visão Computacional dos Drones (T-035)

Data: 2026-02-22
Referência: Issue #90

## Escopo

Implementação de inferência real com backend selecionável:
- YOLOv8 (`ultralytics`)
- TensorFlow Lite (`tflite-runtime`)

Aplicado em:
- `src/drones/ugv/app/ugv_vision.py`
- `src/drones/uav/uav_vision.py`

## Classes mínimas detectadas

- `person`
- `car`
- `dog`

Também há suporte de bloqueio para `cat` no filtro de segurança.

## Tracking entre frames

Implementado rastreamento tipo SORT (centroide + associação por distância) com `track_id` persistente:
- classe `SortLikeTracker` em `src/drones/ugv/app/ugv_vision.py`
- parâmetros configuráveis de tolerância (`max_disappeared`, `max_distance`)

## Filtro de falsos positivos e segurança de defesa

Regra de bloqueio de disparo (`defense_blocked=true`):
- qualquer detecção de animal (`dog`/`cat`)
- pessoa com bbox pequena (`h/frame_h < 0.35`) tratada como possível criança/ambiguidade

Tópicos de saída:
- UGV: `ugv/vision/safety`
- UAV: `uav/vision/safety`

## Performance

- Processo alvo configurável por `VISION_PROCESS_FPS` (default 6 FPS).
- Métrica publicada em `ugv/vision/metrics` com `fps` e `meets_target` (`fps >= 5`).

### Baseline esperado (documentado)

| Plataforma | Backend | Resolução | FPS esperado |
|---|---|---|---|
| Raspberry Pi 4 | TFLite int8 | 640x384 | 5-8 FPS |
| Jetson Nano | YOLOv8n | 640x384 | 6-12 FPS |

## Precisão/Recall (metodologia)

Métricas a registrar com dataset de validação (anotações em COCO/YOLO):

- Precision = TP / (TP + FP)
- Recall = TP / (TP + FN)

Alvos operacionais do projeto:
- `person`: precision >= 0.80, recall >= 0.75
- `car`: precision >= 0.78, recall >= 0.70
- `dog`: precision >= 0.75, recall >= 0.70

Arquivo sugerido para evidências: `quality/vision_benchmark.md`.

## Recuperação de falhas de câmera

O pipeline inclui reopen automático da captura e publicação de estados:
- `camera_connected`
- `camera_recovered`
- `camera_unavailable`

Mantém o fix da issue #44 no fluxo operacional.
