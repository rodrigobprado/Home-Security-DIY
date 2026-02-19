from fastapi import APIRouter, HTTPException

from app.services import ha_client

router = APIRouter(prefix="/api/sensors", tags=["sensors"])


@router.get("")
async def list_sensors() -> dict:
    """Retorna o estado atual de todas as entidades HA."""
    return {"states": ha_client.get_all_states()}


@router.get("/{entity_id:path}")
async def get_sensor(entity_id: str) -> dict:
    """Retorna o estado de uma entidade específica."""
    state = ha_client.get_state(entity_id)
    if state is None:
        raise HTTPException(status_code=404, detail=f"Entidade '{entity_id}' não encontrada.")
    return state
