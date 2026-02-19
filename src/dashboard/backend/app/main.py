import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.session import init_db
from app.routers import alerts, cameras, sensors, services, ws
from app.services import ha_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

_ha_task: asyncio.Task | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _ha_task
    # Inicialização
    logger.info("Inicializando banco de dados (schema: dashboard)...")
    await init_db()

    logger.info("Iniciando cliente WebSocket do Home Assistant...")
    _ha_task = asyncio.create_task(ha_client.run_forever())

    yield

    # Encerramento
    if _ha_task:
        _ha_task.cancel()
        try:
            await _ha_task
        except asyncio.CancelledError:
            pass


app = FastAPI(
    title="Home Security Dashboard API",
    description="API de monitoramento em tempo real do sistema de segurança residencial.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restringir ao domínio do frontend em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(ws.router)
app.include_router(sensors.router)
app.include_router(cameras.router)
app.include_router(alerts.router)
app.include_router(services.router)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}
