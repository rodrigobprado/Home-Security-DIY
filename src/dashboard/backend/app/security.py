import secrets

from fastapi import HTTPException, Security, WebSocket, WebSocketException, status
from fastapi.security import APIKeyHeader, HTTPAuthorizationCredentials, HTTPBearer

from app.config import settings

_api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
_bearer_scheme = HTTPBearer(auto_error=False)


def _configured_api_key() -> str:
    api_key = settings.dashboard_api_key.strip()
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Dashboard API key is not configured.",
        )
    return api_key


def _is_valid_api_key(candidate: str | None, expected: str) -> bool:
    if not candidate:
        return False
    return secrets.compare_digest(candidate, expected)


async def require_api_key(
    x_api_key: str | None = Security(_api_key_header),
    credentials: HTTPAuthorizationCredentials | None = Security(_bearer_scheme),
) -> None:
    expected = _configured_api_key()
    bearer_key = credentials.credentials if credentials else None
    if _is_valid_api_key(x_api_key, expected) or _is_valid_api_key(bearer_key, expected):
        return
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid API key.")


async def require_ws_api_key(websocket: WebSocket) -> None:
    expected = _configured_api_key()
    token = websocket.headers.get("x-api-key")
    auth = websocket.headers.get("authorization", "")
    if not token and auth.lower().startswith("bearer "):
        token = auth.split(" ", 1)[1].strip()

    if _is_valid_api_key(token, expected):
        return

    await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION, reason="Invalid API key.")
