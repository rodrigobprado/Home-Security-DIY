# PRD -- IA e Visao Computacional para Drones

> Sistema de Home Security -- Open Source / Open Hardware
>
> Modulo Reativo Avancado -- Inteligencia Artificial Embarcada
>
> Versao: 1.0 | Data: 2026-02-18 | Responsavel: Agente_Arquiteto_Drones

---

## 1. Visao geral

- **Nome do produto/funcionalidade**: Sistema de IA e Visao Computacional Embarcada para Drones
- **Responsavel**: Agente_Arquiteto_Drones
- **Data**: 2026-02-18
- **PRDs relacionados**: PRD_AUTONOMOUS_DRONES, PRD_DRONE_DEFENSE_MODULE, PRD_DRONE_FLEET_MANAGEMENT, PRD_DRONE_COMMUNICATION, PRD_VIDEO_SURVEILLANCE_AND_NVR

---

## 2. Problema e oportunidade

### 2.1 Problema

Drones de seguranca sem inteligencia embarcada sao essencialmente cameras moveis:

- **Sem deteccao**: transmitem video bruto que requer monitoramento humano constante
- **Sem classificacao**: nao distinguem entre moradores, visitantes, entregadores e intrusos
- **Sem rastreamento**: perdem alvos que saem do campo de visao
- **Sem decisao**: nao conseguem escalonar resposta conforme nivel de ameaca
- **Dependencia de rede**: processamento centralizado exige link estavel e de alta largura de banda
- **Falsos positivos**: animais, sombras e objetos em movimento geram alertas indevidos
- **Latencia critica**: enviar video ao servidor, processar e retornar decisao adiciona latencia inaceitavel para seguranca

### 2.2 Oportunidade

Implementar IA embarcada nos drones que:

- **Detecta em tempo real** pessoas, veiculos e animais com YOLOv8 executando localmente
- **Rastreia alvos** com DeepSORT/ByteTrack para manter identidade entre frames
- **Reconhece faces** de pessoas autorizadas (whitelist) para reduzir falsos positivos
- **Classifica comportamento** como normal, suspeito ou ameaca usando analise de pose e trajetoria
- **Toma decisoes autonomas** de escalonamento: ignorar, monitorar, alertar, seguir, acionar defesa
- **Processa localmente** na edge (Jetson/Hailo) sem depender de link de rede
- **Alimenta o modulo de defesa** com classificacao de alvo (incluindo deteccao de criancas/animais para bloqueio)

---

## 3. Publico-alvo

| Perfil | Descricao | Necessidades especificas |
|--------|-----------|--------------------------|
| **Proprietario rural** | Grandes propriedades | Deteccao em areas amplas, reducao de falsos positivos por animais |
| **Proprietario urbano** | Casas com vizinhos proximos | Reconhecimento facial para whitelist, privacidade de vizinhos |
| **Operador do sistema** | Monitoramento via dashboard | Alertas inteligentes classificados por severidade |
| **Desenvolvedor/ML Engineer** | Customizacao de modelos | Pipeline de treinamento documentado, modelos atualizaveis |

---

## 4. Requisitos funcionais

### 4.1 Deteccao de objetos

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-001 | Detectar pessoas em tempo real com YOLOv8n/s (>90% mAP) | Alta |
| RF-002 | Detectar veiculos (carros, motos, bicicletas) com YOLOv8 | Alta |
| RF-003 | Detectar animais domesticos (caes, gatos) para evitar falsos positivos e bloqueio de defesa | Alta |
| RF-004 | Detectar animais de grande porte (cavalos, bois) em cenarios rurais | Media |
| RF-005 | Classificar objetos abandonados ou fora de contexto | Baixa |
| RF-006 | Funcionar em condicoes de baixa luminosidade (camera IR + camera termica) | Alta |
| RF-007 | Funcionar com camera termica para deteccao noturna sem iluminacao | Media |
| RF-008 | Taxa de inferencia minima: 10 FPS em resolucao 640x480 | Alta |
| RF-009 | Deteccao multiclasse simultanea (pessoa + veiculo + animal no mesmo frame) | Alta |

### 4.2 Rastreamento de objetos (tracking)

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-010 | Rastreamento de objetos entre frames com DeepSORT ou ByteTrack | Alta |
| RF-011 | Manter identidade (ID) unica por alvo rastreado | Alta |
| RF-012 | Re-identificacao de alvo apos oclusao temporaria | Media |
| RF-013 | Rastreamento de multiplos alvos simultaneos (minimo 10) | Alta |
| RF-014 | Calcular trajetoria e velocidade estimada de cada alvo | Alta |
| RF-015 | Predizer posicao futura do alvo para navegacao preditiva | Media |
| RF-016 | Gerar trilha de movimento (heatmap) por alvo rastreado | Baixa |

### 4.3 Reconhecimento facial (whitelist)

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-017 | Reconhecimento facial para identificar pessoas autorizadas (whitelist) | Media |
| RF-018 | Modelo de reconhecimento: FaceNet ou ArcFace | Media |
| RF-019 | Banco de dados de faces armazenado localmente (LGPD) | Alta |
| RF-020 | Cadastro de faces via interface web no Home Assistant | Media |
| RF-021 | Precisao de reconhecimento: > 95% em condicoes de boa iluminacao | Media |
| RF-022 | Fallback para "desconhecido" quando confianca < threshold configuravel | Alta |
| RF-023 | Nao transmitir dados faciais pela rede (processamento exclusivamente local) | Alta |
| RF-024 | Whitelist configuravel via MQTT com sincronizacao entre drones | Media |

### 4.4 Classificacao de comportamento

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-025 | Estimativa de pose humana com MoveNet ou MediaPipe | Media |
| RF-026 | Classificar comportamento: caminhando, correndo, agachado, escalando, parado | Media |
| RF-027 | Detectar comportamento suspeito: tentar abrir portas/janelas, escalar muros, rondar o perimetro | Media |
| RF-028 | Classificar nivel de ameaca: baixo, medio, alto | Alta |
| RF-029 | Analisar trajetoria: pessoa se aproximando vs. passando vs. rondando | Media |
| RF-030 | Considerar contexto temporal: horario, zona, historico de alertas | Media |
| RF-031 | Detectar grupamento de pessoas (possivel acao coordenada) | Baixa |

### 4.5 Deteccao de criancas e classificacao etaria (REGRA-DRONE-24)

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-032 | Classificacao etaria por proporcoes corporais (cabeca/corpo, comprimento de membros) | Alta |
| RF-033 | Classificacao complementar por pose (MoveNet) e altura estimada | Alta |
| RF-034 | Threshold conservador: em caso de duvida, classificar como crianca | Alta |
| RF-035 | Resultado da classificacao alimenta diretamente o bloqueio do modulo de defesa | Alta |
| RF-036 | Modelo treinado com dataset diverso (etnias, angulos, roupas) | Alta |
| RF-037 | Funcionar em condicoes de baixa luminosidade (IR) | Media |

### 4.6 Arvore de decisao autonoma

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-038 | Implementar arvore de decisao conforme docs/ARQUITETURA_DRONES_AUTONOMOS.md secao 6.3 | Alta |
| RF-039 | Pessoa detectada -> verificar whitelist -> conhecido: log / desconhecido: seguir e alertar | Alta |
| RF-040 | Desconhecido com comportamento normal -> monitorar passivamente | Alta |
| RF-041 | Desconhecido com comportamento suspeito -> escalar alerta + avisos sonoros/visuais | Alta |
| RF-042 | Invasao confirmada -> solicitar autorizacao de defesa ao operador humano | Alta |
| RF-043 | Decisao de escalonamento publicada via MQTT para fleet manager e Home Assistant | Alta |
| RF-044 | Cada decisao registrada em log com justificativa (deteccao, classificacao, confianca) | Alta |

### 4.7 Processamento embarcado

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-045 | Processamento de inferencia executado localmente no drone (edge computing) | Alta |
| RF-046 | Suporte a NVIDIA Jetson Orin Nano como plataforma principal | Alta |
| RF-047 | Suporte a Raspberry Pi 5 + Hailo-8L como plataforma alternativa | Alta |
| RF-048 | Suporte a Raspberry Pi 5 com ONNX Runtime como plataforma minima | Media |
| RF-049 | Modelos otimizados: TensorRT (Jetson), Hailo Model Zoo, ONNX | Alta |
| RF-050 | Pipeline de visao containerizado (Docker) para facilitar atualizacao | Alta |
| RF-051 | Modelos atualizaveis via OTA (Over-The-Air) quando drone na base | Media |
| RF-052 | Fallback para modo degradado se GPU indisponivel (CPU-only com menor FPS) | Media |

### 4.8 Integracao com Frigate e Home Assistant

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RF-053 | Publicar deteccoes via MQTT em formato compativel com Frigate | Alta |
| RF-054 | Snapshots de deteccoes enviados ao Home Assistant | Alta |
| RF-055 | Eventos de deteccao acionam automacoes no Home Assistant | Alta |
| RF-056 | Dashboard com feed de deteccoes em tempo real (bounding boxes) | Media |
| RF-057 | Historico de deteccoes pesquisavel por tipo, data, drone | Media |

---

## 5. Requisitos nao funcionais

### 5.1 Performance de inferencia

| ID | Requisito | Especificacao |
|----|-----------|---------------|
| RNF-001 | Taxa de inferencia (Jetson Orin Nano) | >= 15 FPS com YOLOv8n |
| RNF-002 | Taxa de inferencia (RPi 5 + Hailo-8L) | >= 10 FPS com YOLOv8n |
| RNF-003 | Taxa de inferencia (RPi 5, CPU-only) | >= 3 FPS com YOLOv8n (modo degradado) |
| RNF-004 | Latencia de deteccao (captura a resultado) | < 100ms (Jetson), < 200ms (Hailo) |
| RNF-005 | Latencia de decisao (deteccao a acao) | < 500ms |
| RNF-006 | Uso de memoria GPU | < 2GB (para manter margem para outros processos) |
| RNF-007 | Consumo de energia do pipeline de IA | < 15W (Jetson), < 8W (Hailo) |

### 5.2 Acuracia

| ID | Requisito | Especificacao |
|----|-----------|---------------|
| RNF-008 | Precisao de deteccao de pessoas (mAP@0.5) | > 90% |
| RNF-009 | Precisao de deteccao de veiculos | > 85% |
| RNF-010 | Precisao de deteccao de animais | > 85% |
| RNF-011 | Precisao de reconhecimento facial (whitelist) | > 95% em boa iluminacao, > 80% em IR |
| RNF-012 | Taxa de falsos positivos de "comportamento suspeito" | < 10% |
| RNF-013 | Taxa de falsos negativos de deteccao de criancas | < 2% (prioridade maxima) |
| RNF-014 | Funcionamento em baixa luminosidade (< 1 lux com IR) | Degradacao de acuracia < 15% |

### 5.3 Privacidade e conformidade

| ID | Requisito | Especificacao |
|----|-----------|---------------|
| RNF-015 | Processamento de faces exclusivamente local | Zero transmissao de dados faciais |
| RNF-016 | Armazenamento de embeddings faciais criptografado | AES-256 em repouso |
| RNF-017 | Video nao transmitido para nuvem | LGPD - processamento local |
| RNF-018 | Retencao de snapshots de deteccao | 30 dias com rotacao automatica |
| RNF-019 | Camera nao deve captar propriedade de vizinhos | Mascaras de privacidade configuraveis |

### 5.4 Robustez

| ID | Requisito | Especificacao |
|----|-----------|---------------|
| RNF-020 | Operacao em chuva/neblina | Degradacao graceful, alertar operador |
| RNF-021 | Operacao com contra-luz (sol direto) | HDR ou exposicao adaptativa |
| RNF-022 | Temperatura de operacao do acelerador de IA | Throttling automatico acima de 80C |
| RNF-023 | Recuperacao de crash do pipeline de IA | Restart automatico em < 5 segundos |

---

## 6. Arquitetura tecnica

### 6.1 Pipeline de visao computacional

```
+-----------------------------------------------------------------------+
|                 PIPELINE DE VISAO COMPUTACIONAL                       |
+-----------------------------------------------------------------------+
|                                                                       |
|  +----------+    +----------+    +-------------+    +-----------+     |
|  | CAPTURA  |--->| PRE-PROC |--->| INFERENCIA  |--->| POS-PROC  |     |
|  | Camera   |    | Resize   |    | YOLOv8      |    | NMS       |     |
|  | 30 FPS   |    | Normalize|    | (TensorRT/  |    | Threshold |     |
|  | 640x480  |    | Crop     |    |  Hailo/ONNX)|    | Filter    |     |
|  +----------+    +----------+    +-------------+    +-----+-----+     |
|                                                           |           |
|       +---------------------------------------------------+           |
|       |                                                               |
|       v                                                               |
|  +----------+    +----------+    +-------------+    +-----------+     |
|  | TRACKING |--->| FACE ID  |--->| POSE/       |--->| DECISAO   |     |
|  | DeepSORT |    | ArcFace  |    | COMPORTAM.  |    | Arvore de |     |
|  | ByteTrack|    | (se face |    | MoveNet     |    | decisao   |     |
|  | (IDs)    |    |  visivel)|    | (suspeito?) |    | autonoma  |     |
|  +----------+    +----------+    +-------------+    +-----+-----+     |
|                                                           |           |
|       +---------------------------------------------------+           |
|       |                                                               |
|       v                                                               |
|  +----------+    +----------+    +-------------+                      |
|  | PUBLISH  |    | DEFENSE  |    | LOG/AUDIT   |                      |
|  | MQTT +   |    | GATE     |    | Registro    |                      |
|  | ROS2     |    | Bloqueio |    | completo    |                      |
|  | Eventos  |    | crianca/ |    | de cada     |                      |
|  |          |    | animal   |    | decisao     |                      |
|  +----------+    +----------+    +-------------+                      |
|                                                                       |
|  Latencia alvo: < 100ms (deteccao), < 500ms (decisao completa)       |
+-----------------------------------------------------------------------+
```

### 6.2 Modelos de IA utilizados

| Modelo | Framework | Funcao | Plataforma | Tamanho |
|--------|-----------|--------|------------|---------|
| **YOLOv8n** | Ultralytics | Deteccao de objetos (pessoas, veiculos, animais) | Jetson (TensorRT), Hailo, ONNX | ~6MB |
| **YOLOv8s** | Ultralytics | Deteccao com maior acuracia (modo performance) | Jetson (TensorRT) | ~22MB |
| **DeepSORT** | Custom | Rastreamento multi-objeto | CPU/GPU | ~60MB (encoder) |
| **ByteTrack** | Custom | Rastreamento leve (alternativa) | CPU | ~1MB |
| **ArcFace/FaceNet** | ONNX/TRT | Reconhecimento facial | Jetson/Hailo | ~100MB |
| **MoveNet Lightning** | TFLite | Estimativa de pose (17 keypoints) | CPU/GPU | ~3MB |
| **MediaPipe Pose** | MediaPipe | Estimativa de pose (alternativa) | CPU/GPU | ~5MB |
| **MiDaS v2.1 Small** | ONNX | Estimativa de profundidade monocular | Jetson | ~25MB |
| **Classificador etario** | Custom (PyTorch) | Deteccao de criancas (REGRA-DRONE-24) | Jetson/Hailo | ~10MB |

### 6.3 Arquitetura de nos ROS2

```
+-----------------------------------------------------------------------+
|                      SISTEMA ROS2 - IA EMBARCADA                      |
+-----------------------------------------------------------------------+
|                                                                       |
|  +-----------------+                                                  |
|  | /camera_node    |---> /camera/image_raw (sensor_msgs/Image)        |
|  | (driver camera) |---> /camera/thermal (sensor_msgs/Image)          |
|  +-----------------+                                                  |
|          |                                                            |
|          v                                                            |
|  +-----------------+                                                  |
|  | /detector_node  |---> /perception/detections                       |
|  | (YOLOv8)        |     (vision_msgs/Detection2DArray)               |
|  +-----------------+                                                  |
|          |                                                            |
|          v                                                            |
|  +-----------------+                                                  |
|  | /tracker_node   |---> /perception/tracks                           |
|  | (DeepSORT)      |     (custom_msgs/TrackedObjects)                 |
|  +-----------------+                                                  |
|          |                                                            |
|     +----+----+                                                       |
|     |         |                                                       |
|     v         v                                                       |
|  +--------+ +------------------+                                      |
|  | /face  | | /behavior_node   |                                      |
|  | _recog | | (MoveNet + regras)|                                     |
|  | _node  | +--------+---------+                                      |
|  +---+----+          |                                                |
|      |               |                                                |
|      v               v                                                |
|  +-----------------+--------+                                         |
|  | /decision_maker          |---> /decision/action                    |
|  | (arvore de decisao)      |     (custom_msgs/SecurityAction)        |
|  +---------+----------------+---> /defense/target_classification      |
|            |                      (custom_msgs/TargetClass)            |
|            v                                                          |
|  +-----------------+                                                  |
|  | /mqtt_bridge    |---> drone/{id}/ai/detections                     |
|  | (ROS2 <-> MQTT) |---> drone/{id}/ai/decision                      |
|  +-----------------+---> drone/{id}/ai/tracks                         |
|                                                                       |
+-----------------------------------------------------------------------+
```

### 6.4 Topicos MQTT de IA

| Topico | Direcao | Descricao |
|--------|---------|-----------|
| `drone/{id}/ai/detections` | Drone -> Base | Lista de deteccoes (classe, confianca, bbox) |
| `drone/{id}/ai/tracks` | Drone -> Base | Objetos rastreados (ID, trajetoria, velocidade) |
| `drone/{id}/ai/decision` | Drone -> Base | Decisao autonoma (acao, justificativa, confianca) |
| `drone/{id}/ai/face_match` | Drone -> Base | Resultado de reconhecimento facial (conhecido/desconhecido) |
| `drone/{id}/ai/behavior` | Drone -> Base | Classificacao de comportamento (normal/suspeito/ameaca) |
| `drone/{id}/ai/child_detected` | Drone -> Base | Alerta de deteccao de crianca (bloqueio de defesa) |
| `drone/{id}/ai/snapshot` | Drone -> Base | Imagem com anotacoes de deteccao |
| `drone/{id}/ai/model_status` | Drone -> Base | Status dos modelos carregados e metricas |

### 6.5 Formato de dados de deteccao (JSON via MQTT)

```json
{
  "drone_id": "ugv-01",
  "timestamp": "2026-02-18T14:30:00.123Z",
  "frame_id": 12345,
  "detections": [
    {
      "class": "person",
      "confidence": 0.92,
      "bbox": [120, 80, 340, 480],
      "track_id": 7,
      "face_match": "unknown",
      "behavior": "suspicious",
      "is_child": false,
      "threat_level": "medium"
    },
    {
      "class": "dog",
      "confidence": 0.88,
      "bbox": [400, 300, 520, 420],
      "track_id": 12,
      "defense_block": true
    }
  ],
  "decision": {
    "action": "follow_and_alert",
    "target_track_id": 7,
    "confidence": 0.85,
    "reason": "unknown_person_suspicious_behavior"
  }
}
```

---

## 7. Hardware e componentes recomendados

### 7.1 Plataformas de processamento de IA

| Componente | Modelo | Preco estimado (R$) | Performance | Consumo |
|------------|--------|---------------------|-------------|---------|
| **Opcao A (Premium)** | NVIDIA Jetson Orin Nano 8GB | R$ 2.000-3.000 | 40 TOPS, TensorRT | 7-15W |
| **Opcao B (Custo-beneficio)** | Raspberry Pi 5 8GB + Hailo-8L M.2 | R$ 700-1.000 + R$ 400-600 | 13 TOPS (Hailo) | 5-8W |
| **Opcao C (Minima)** | Raspberry Pi 5 8GB (CPU/ONNX) | R$ 700-1.000 | ~3 FPS YOLOv8n | 5-8W |
| **Opcao D (UAV leve)** | Raspberry Pi Zero 2 W + acelerador coral | R$ 150-250 + R$ 300-500 | 4 TOPS (Coral) | 2-3W |

### 7.2 Cameras

| Componente | Modelo | Preco estimado (R$) | Especificacao |
|------------|--------|---------------------|---------------|
| Camera principal (dia) | Raspberry Pi Camera V3 Wide | R$ 200-300 | 12MP, 120 FOV, autofoco |
| Camera principal (alt.) | IMX477 HQ Camera | R$ 250-350 | 12.3MP, lentes intercambiaveis |
| Camera com IA integrada | Luxonis OAK-D Lite | R$ 500-800 | Stereo depth + IA on-chip |
| Camera noturna (IR) | Pi NoIR Camera V3 | R$ 200-300 | 12MP, sem filtro IR |
| Camera termica | FLIR Lepton 3.5 (modulo) | R$ 600-1.200 | 160x120, LWIR |
| Camera termica (alt.) | MLX90640 | R$ 300-500 | 32x24, I2C |
| Iluminador IR | Array LED IR 850nm | R$ 50-100 | Para visao noturna |

### 7.3 Aceleradores de IA (complementares)

| Componente | Modelo | Preco estimado (R$) | Especificacao |
|------------|--------|---------------------|---------------|
| Hailo-8L M.2 | Hailo-8L | R$ 400-600 | 13 TOPS, M.2 Key B+M |
| Google Coral USB | Coral USB Accelerator | R$ 300-500 | 4 TOPS, USB 3.0 |
| Google Coral M.2 | Coral M.2 Accelerator | R$ 250-400 | 4 TOPS, M.2 Key A+E |

### 7.4 Estimativa de custo por configuracao

| Configuracao | Plataforma | Camera | Custo estimado |
|--------------|------------|--------|----------------|
| **UGV MVP (minima)** | RPi 5 8GB (ONNX) | Pi Camera V3 Wide | R$ 900-1.300 |
| **UGV recomendada** | RPi 5 + Hailo-8L | Pi Camera V3 Wide + NoIR | R$ 1.300-2.000 |
| **UGV premium** | Jetson Orin Nano | OAK-D Lite + FLIR Lepton | R$ 3.100-5.000 |
| **UAV (leve)** | RPi Zero 2 W + Coral | Pi Camera V3 | R$ 650-1.050 |
| **UAV (completa)** | Jetson Orin Nano | IMX477 + gimbal | R$ 2.750-4.350 |

---

## 8. Criterios de aceitacao

| ID | Criterio | Metodo de verificacao |
|----|----------|----------------------|
| CA-001 | YOLOv8 detecta pessoas com >90% mAP em condicoes diurnas | Teste com dataset de validacao |
| CA-002 | Taxa de inferencia >= 10 FPS na plataforma escolhida | Benchmark de performance |
| CA-003 | Tracking mantem ID unico por alvo entre frames | Teste com multiplos alvos |
| CA-004 | Reconhecimento facial identifica >95% das faces cadastradas em boa iluminacao | Teste com whitelist de 10+ pessoas |
| CA-005 | Deteccao de criancas funciona com >95% de acuracia (REGRA-DRONE-24) | Teste com manequins e imagens de referencia |
| CA-006 | Bloqueio de defesa e ativado quando crianca/animal detectado | Teste funcional integrado com modulo de defesa |
| CA-007 | Classificacao de comportamento suspeito funciona (escalar muro, forcar porta) | Teste com cenarios simulados |
| CA-008 | Arvore de decisao escala corretamente: monitorar -> alertar -> seguir -> defesa | Teste de escalonamento end-to-end |
| CA-009 | Pipeline funciona em modo noturno com camera IR | Teste em condicoes de baixa luminosidade |
| CA-010 | Deteccoes publicadas via MQTT em formato compativel com HA/Frigate | Teste de integracao |
| CA-011 | Processamento 100% local, nenhum dado enviado para nuvem | Auditoria de trafego de rede |
| CA-012 | Pipeline reinicia automaticamente apos crash | Teste de kill + recovery |
| CA-013 | Modelos atualizaveis via OTA quando drone na base | Teste de atualizacao |

---

## 9. Metricas de sucesso

| Metrica | Alvo | Medicao |
|---------|------|---------|
| **Precisao de deteccao de pessoas** | > 90% mAP@0.5 | Validacao com dataset anotado |
| **Taxa de falsos positivos** | < 5% de alertas indevidos por dia | Contagem diaria de alertas falsos |
| **Taxa de falsos negativos de criancas** | < 2% | Testes periodicos com cenarios |
| **Tempo medio de deteccao a decisao** | < 500ms | Analise de logs de pipeline |
| **Disponibilidade do pipeline de IA** | > 99% | Monitoramento continuo |
| **FPS medio em operacao** | >= 10 FPS (Hailo), >= 15 FPS (Jetson) | Metricas de telemetria |
| **Reducao de falsos positivos vs. camera burra** | > 80% de reducao | Comparacao com baseline |
| **Acuracia de reconhecimento facial** | > 95% (dia), > 80% (noite/IR) | Testes periodicos com whitelist |

---

## 10. Riscos e dependencias

### 10.1 Riscos

| Risco | Probabilidade | Impacto | Mitigacao |
|-------|---------------|---------|-----------|
| Falso negativo de deteccao de crianca causa disparo indevido | Baixa | Critico | Threshold conservador + confirmacao humana obrigatoria (REGRA-DRONE-23) |
| Acuracia degrada em condicoes adversas (chuva, neblina, contraluz) | Alta | Medio | Camera termica como fallback + modo degradado com alerta ao operador |
| Modelo de IA desatualizado perde acuracia com o tempo | Media | Medio | Pipeline de re-treinamento documentado + atualizacao OTA |
| Consumo de energia excessivo reduz autonomia do drone | Media | Alto | Modelos otimizados (quantizacao INT8) + duty cycle de inferencia |
| Bias do modelo em deteccao de criancas de diferentes etnias | Media | Critico | Dataset diverso + validacao com representatividade |
| Reconhecimento facial gera falso positivo (confundir intruso com morador) | Baixa | Alto | Threshold alto de confianca + multiplas verificacoes |
| Superaquecimento do acelerador de IA em operacao continua | Media | Medio | Dissipador de calor adequado + throttling automatico |
| Privacidade: camera capta propriedade de vizinhos | Media | Alto | Mascaras de privacidade configuraveis + LGPD compliance |

### 10.2 Dependencias

| Dependencia | Tipo | PRD relacionado |
|-------------|------|-----------------|
| Hardware do drone (camera, computador de bordo) | Infraestrutura | PRD_AUTONOMOUS_DRONES |
| Modulo de defesa (consumidor das classificacoes) | Funcional | PRD_DRONE_DEFENSE_MODULE |
| Comunicacao para transmissao de eventos | Infraestrutura | PRD_DRONE_COMMUNICATION |
| Fleet manager (consumidor de decisoes) | Funcional | PRD_DRONE_FLEET_MANAGEMENT |
| Frigate (integracao de eventos de IA) | Integracao | PRD_VIDEO_SURVEILLANCE_AND_NVR |
| Home Assistant (dashboard e automacoes) | Interface | PRD_MONITORING_DASHBOARD |

---

## 11. Referencias

### Documentos do projeto

- `docs/ARQUITETURA_DRONES_AUTONOMOS.md` -- Secao 6 (IA Embarcada)
- `docs/ARQUITETURA_HARDWARE_UGV.md` -- Secao 3.3 (Sensores de visao)
- `docs/ARQUITETURA_HARDWARE_UAV.md` -- Secao 3.3 (Computador de bordo)
- `rules/RULES_COMPLIANCE_AND_STANDARDS.md` -- REGRA-DRONE-24 (bloqueio criancas/animais)
- `prd/PRD_AUTONOMOUS_DRONES.md` -- Secao 4.4 (Inteligencia artificial)

### Modelos e frameworks

- [YOLOv8 - Ultralytics](https://docs.ultralytics.com/)
- [DeepSORT](https://github.com/nwojke/deep_sort)
- [ByteTrack](https://github.com/ifzhang/ByteTrack)
- [ArcFace](https://github.com/deepinsight/insightface)
- [MoveNet - TensorFlow](https://www.tensorflow.org/hub/tutorials/movenet)
- [MediaPipe Pose](https://mediapipe.dev/)
- [ONNX Runtime](https://onnxruntime.ai/)

### Hardware de IA

- [NVIDIA Jetson Orin Nano](https://developer.nvidia.com/embedded/jetson-orin-nano)
- [Hailo-8L AI Processor](https://hailo.ai/products/ai-accelerators/hailo-8l/)
- [Google Coral](https://coral.ai/)
- [Luxonis OAK-D](https://docs.luxonis.com/)

### Datasets de referencia

- [COCO Dataset](https://cocodataset.org/) -- Deteccao de objetos
- [WIDER Face](http://shuoyang1213.me/WIDERFACE/) -- Deteccao facial
- [LFW (Labeled Faces in the Wild)](http://vis-www.cs.umass.edu/lfw/) -- Reconhecimento facial

---

> **Status**: Rascunho v1.0
>
> **Proxima revisao**: Apos benchmarks de performance com hardware real
