# 🚀 Quick Start – Home Security DIY

Guia rápido para subir o stack de segurança residencial com Docker Compose.

---

## Pré-requisitos

| Componente | Mínimo | Recomendado |
|------------|--------|-------------|
| **Hardware** | Qualquer PC x86_64 | Mini PC Intel N100, 8GB RAM |
| **SO** | Linux (Ubuntu 22.04+, Debian 12+) | Ubuntu Server 24.04 LTS |
| **Docker** | 24.0+ | Última versão estável |
| **Docker Compose** | v2.20+ | Última versão estável |
| **Armazenamento** | 50GB (sistema) | SSD 256GB + HDD 2TB (gravações) |
| **Coordenador Zigbee** | Sonoff ZBDongle-P | SLZB-06 (PoE) |

### Instalar Docker (se necessário)

```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
# Faça logout e login novamente
```

---

## 1. Clonar o repositório

```bash
git clone https://github.com/rodrigobprado/Home-Security-DIY.git
cd Home-Security-DIY/src
```

## 2. Configurar variáveis de ambiente

```bash
cp .env.example .env
nano .env
```

**Edite pelo menos:**

| Variável | O que alterar |
|----------|---------------|
| `MQTT_PASSWORD` | Defina uma senha forte |
| `ZIGBEE_DEVICE` | Caminho do coordenador Zigbee (`ls /dev/serial/by-id/`) |
| `FRIGATE_CAM_*_URL` | URLs RTSP das suas câmeras |
| `TZ` | Seu fuso horário |

> **Dica:** Para encontrar o device do Zigbee:
> ```bash
> ls -la /dev/serial/by-id/
> # Ex: /dev/serial/by-id/usb-ITead_Sonoff_Zigbee_3.0_USB_Dongle_Plus_xxx-if00-port0
> ```

## 3. Criar arquivo de senhas do MQTT

```bash
# Criar diretório de dados
mkdir -p mosquitto/config

# Criar arquivo de senha
docker run --rm -v $(pwd)/mosquitto/config:/mosquitto/config \
  eclipse-mosquitto:2 \
  mosquitto_passwd -b /mosquitto/config/password_file homeassistant SUA_SENHA_AQUI

# Adicionar usuários extras (Zigbee2MQTT e Frigate usam o mesmo user por padrão)
```

## 4. Criar diretórios necessários

```bash
mkdir -p frigate/media
mkdir -p homeassistant/www/snapshots
mkdir -p homeassistant/themes
```

## 5. Subir o stack

```bash
docker compose up -d
```

Aguarde ~2 minutos para todos os serviços inicializarem.

## 6. Verificar status

```bash
docker compose ps
docker compose logs -f  # Ctrl+C para sair
```

Todos os containers devem estar `healthy` ou `running`.

---

## Primeiros passos

### Acessar o Home Assistant

1. Abra **http://SEU_IP:8123** no navegador
2. Crie sua conta de administrador
3. Siga o wizard de configuração (país, timezone, etc.)

### Instalar Alarmo (HACS)

1. Instale o [HACS](https://hacs.xyz/docs/use/) no Home Assistant
2. No HACS, busque e instale **Alarmo**
3. Configure as zonas de alarme conforme seu cenário:

| Zona | Sensores | Comportamento |
|------|----------|---------------|
| Perímetro | Cerca elétrica, sensores externos | Alerta imediato |
| Entrada | Porta principal, PIR entrada | Delay de entrada |
| Portas/Janelas | Sensores de abertura | Alerta imediato |
| Interior | PIR internos | Apenas armado total |

### Verificar Zigbee2MQTT

1. Acesse **http://localhost:8080** (bind local por segurança)
2. Verifique que o coordenador está conectado
3. Coloque sensores em modo de pareamento e adicione-os

### Verificar Frigate

1. Acesse **http://localhost:5000** (bind local por segurança)
2. Verifique que as câmeras aparecem com stream ativo
3. Ajuste zonas de detecção conforme necessário

### Instalar cards do dashboard (HACS)

No HACS, instale:
- **alarmo-card** — controle do alarme
- **frigate-card** — visualização de câmeras
- **mushroom-cards** — cards modernos
- **button-card** — botões customizados

---

## Portas utilizadas

| Porta | Serviço | Protocolo |
|-------|---------|-----------|
| 8123 | Home Assistant | HTTP |
| 1883 | Mosquitto MQTT | TCP (loopback) |
| 8883 | Mosquitto MQTT (produção) | TLS |
| 9001 | Mosquitto WebSocket | TCP (loopback) |
| 8080 | Zigbee2MQTT Frontend | HTTP (loopback) |
| 5000 | Frigate Web UI | HTTP (loopback) |
| 8554 | Frigate RTSP Restream | TCP (loopback) |
| 8555 | Frigate WebRTC | TCP/UDP (loopback) |

> Nota: Dashboard API roda com `uvicorn --workers 1` por restrição arquitetural atual
> do cliente Home Assistant (`ha_client.py` usa estado em memória por processo).

## Produção: baseline MQTT TLS-only

Para produção, use `src/mosquitto/config/mosquitto.prod.conf` (listener 8883, sem 1883).

---

## Arquitetura

```
┌─────────────────────────────────────────────────────┐
│                   Docker Host                        │
│                                                      │
│  ┌────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ Mosquitto  │◄─┤ Zigbee2MQTT  │  │   Frigate    │ │
│  │   :1883    │  │    :8080     │  │    :5000     │ │
│  └─────┬──────┘  └──────────────┘  └──────┬───────┘ │
│        │              │                    │         │
│        └──────────────┼────────────────────┘         │
│                       │ MQTT                          │
│              ┌────────▼─────────┐                    │
│              │  Home Assistant  │                    │
│              │     :8123        │                    │
│              │   + Alarmo       │                    │
│              └──────────────────┘                    │
└─────────────────────────────────────────────────────┘
         │                    │
    ┌────▼────┐          ┌────▼────┐
    │ Zigbee  │          │ Câmeras │
    │ Sensors │          │   IP    │
    └─────────┘          └─────────┘
```

---

## Troubleshooting

### Container não inicia

```bash
docker compose logs <service_name>
# Ex: docker compose logs mosquitto
```

### Zigbee2MQTT não encontra o coordenador

```bash
# Verificar dispositivo USB
ls -la /dev/serial/by-id/
# Atualizar ZIGBEE_DEVICE no .env com o caminho correto
```

### Câmera não aparece no Frigate

1. Teste a URL RTSP diretamente: `ffplay rtsp://user:pass@IP:554/stream`
2. Verifique a VLAN — câmera e Frigate devem estar acessíveis
3. Revise os logs: `docker compose logs frigate`

### Home Assistant não conecta ao MQTT

1. Verifique se o Mosquitto está running: `docker compose ps mosquitto`
2. Teste a conexão: `mosquitto_sub -h localhost -t '#' -u USER -P PASS`
3. Verifique as credenciais no arquivo de senha do Mosquitto

---

## Próximos passos

- [ ] Configurar VLANs para isolar câmeras e IoT ([docs/ARQUITETURA_TECNICA.md](../../docs/ARQUITETURA_TECNICA.md))
- [ ] Configurar VPN WireGuard para acesso remoto
- [ ] Configurar notificações Telegram
- [ ] Ajustar zonas de detecção do Frigate
- [ ] Instalar e configurar nobreak com monitoramento
- [ ] Criar backup automático das configurações

---

> **Documentação completa**: Consulte os PRDs em `prd/` para requisitos detalhados de cada subsistema.
