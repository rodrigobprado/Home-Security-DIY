import json

import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.config import settings

router = APIRouter(prefix="/api/drones", tags=["drones"])

_client: httpx.AsyncClient | None = None


class DroneCommandPayload(BaseModel):
    drone: str
    action: str
    route: str | None = None


def _resolve_command(payload: DroneCommandPayload) -> tuple[str, dict]:
    drone = payload.drone.strip().lower()
    action = payload.action.strip().lower()

    if drone == "ugv":
        topic = "ugv/command"
        if action == "start_patrol":
            return topic, {
                "cmd": "patrol",
                "route": (payload.route or "perimeter_day"),
                "source_id": "dashboard",
            }
        if action == "return_home":
            return topic, {"cmd": "return_home", "source_id": "dashboard"}
        if action == "emergency_stop":
            return topic, {"cmd": "stop", "source_id": "dashboard"}

    if drone == "uav":
        topic = "uav/command"
        if action == "start_patrol":
            return topic, {"cmd": "inspect_zone", "source_id": "dashboard"}
        if action == "return_home":
            return topic, {"cmd": "return_home", "source_id": "dashboard"}
        if action == "emergency_stop":
            return topic, {"cmd": "stop", "source_id": "dashboard"}

    raise HTTPException(status_code=400, detail="unsupported drone/action")


async def _get_client() -> httpx.AsyncClient:
    global _client
    if _client is None:
        _client = httpx.AsyncClient(
            timeout=5,
            limits=httpx.Limits(max_connections=10, max_keepalive_connections=5),
        )
    return _client


async def close() -> None:
    global _client
    if _client is not None:
        await _client.aclose()
        _client = None


@router.post("/command")
async def publish_drone_command(payload: DroneCommandPayload) -> dict:
    topic, body = _resolve_command(payload)
    client = await _get_client()
    resp = await client.post(
        f"{settings.ha_url}/api/services/mqtt/publish",
        headers={"Authorization": f"Bearer {settings.ha_token}"},
        json={
            "topic": topic,
            "payload": json.dumps(body, separators=(",", ":"), ensure_ascii=True),
            "qos": 0,
            "retain": False,
        },
    )
    if resp.status_code >= 300:
        raise HTTPException(
            status_code=502,
            detail=f"failed to publish mqtt command via HA service: {resp.status_code}",
        )
    return {"status": "accepted", "topic": topic, "command": body}
