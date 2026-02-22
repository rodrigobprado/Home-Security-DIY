import secrets
import time
from collections import defaultdict, deque
from collections.abc import MutableMapping

from fastapi import HTTPException, Request, Security, WebSocket, WebSocketException, status
from fastapi.security import APIKeyHeader, HTTPAuthorizationCredentials, HTTPBearer

from app.config import settings

_api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
_bearer_scheme = HTTPBearer(auto_error=False)
_api_auth_failures: MutableMapping[str, deque[float]] = defaultdict(deque)
_ws_auth_attempts: MutableMapping[str, deque[float]] = defaultdict(deque)
_AUTH_WINDOW_SECONDS = 60
_AUTH_MAX_FAILURES_PER_WINDOW = 20
_WS_AUTH_WINDOW_SECONDS = 60
_WS_AUTH_MAX_ATTEMPTS_PER_WINDOW = 60


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


def _client_ip(value: str | None) -> str:
    return (value or "unknown").strip() or "unknown"


def _register_rate_event(
    store: MutableMapping[str, deque[float]],
    key: str,
    *,
    now: float,
    window_seconds: int,
    max_events: int,
) -> bool:
    queue = store[key]
    cutoff = now - window_seconds
    while queue and queue[0] < cutoff:
        queue.popleft()
    queue.append(now)
    return len(queue) <= max_events


async def require_api_key(
    request: Request,
    x_api_key: str | None = Security(_api_key_header),
    credentials: HTTPAuthorizationCredentials | None = Security(_bearer_scheme),
) -> None:
    expected = _configured_api_key()
    bearer_key = credentials.credentials if credentials else None
    if _is_valid_api_key(x_api_key, expected) or _is_valid_api_key(bearer_key, expected):
        return
    ip = _client_ip(request.client.host if request.client else None)
    if not _register_rate_event(
        _api_auth_failures,
        ip,
        now=time.time(),
        window_seconds=_AUTH_WINDOW_SECONDS,
        max_events=_AUTH_MAX_FAILURES_PER_WINDOW,
    ):
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Too many auth failures.")
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid API key.")


async def require_ws_api_key(websocket: WebSocket) -> None:
    ip = _client_ip(websocket.client.host if websocket.client else None)
    if not _register_rate_event(
        _ws_auth_attempts,
        ip,
        now=time.time(),
        window_seconds=_WS_AUTH_WINDOW_SECONDS,
        max_events=_WS_AUTH_MAX_ATTEMPTS_PER_WINDOW,
    ):
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION, reason="Too many auth attempts.")

    expected = _configured_api_key()
    token = websocket.headers.get("x-api-key")
    auth = websocket.headers.get("authorization", "")
    if not token and auth.lower().startswith("bearer "):
        token = auth.split(" ", 1)[1].strip()

    if _is_valid_api_key(token, expected):
        return

    await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION, reason="Invalid API key.")
