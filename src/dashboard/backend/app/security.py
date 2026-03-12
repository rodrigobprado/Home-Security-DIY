import secrets
import time
from ipaddress import ip_address

from fastapi import HTTPException, Request, Security, WebSocket, WebSocketException, status
from fastapi.security import APIKeyHeader, HTTPAuthorizationCredentials, HTTPBearer

from app.config import settings
from app.db.redis import get_redis

_api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
_admin_key_header = APIKeyHeader(name="X-Admin-Key", auto_error=False)
_bearer_scheme = HTTPBearer(auto_error=False)

_AUTH_WINDOW_SECONDS = 60
_AUTH_MAX_FAILURES_PER_WINDOW = 20
_WS_AUTH_WINDOW_SECONDS = 60
_WS_AUTH_MAX_ATTEMPTS_PER_WINDOW = 60

# Rate limit para operações admin (menor tolerância)
_ADMIN_AUTH_WINDOW_SECONDS = 60
_ADMIN_AUTH_MAX_FAILURES_PER_WINDOW = 10


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


def _normalize_ip(value: str | None) -> str | None:
    if value is None:
        return None
    candidate = value.strip()
    if not candidate:
        return None
    try:
        return str(ip_address(candidate))
    except ValueError:
        return None


def _trusted_proxies() -> set[str]:
    return {ip for ip in (_normalize_ip(raw) for raw in settings.trusted_proxy_ips) if ip}


def _get_request_ip(request: Request) -> str:
    direct_ip = _normalize_ip(request.client.host if request.client else None) or "unknown"
    forwarded = request.headers.get("X-Forwarded-For")
    if not forwarded or direct_ip not in _trusted_proxies():
        return direct_ip
    
    ips = [ip.strip() for ip in forwarded.split(",")]
    return ips[0] if ips else direct_ip


def _get_authenticated_actor(request: Request) -> str:
    """
    Determina o actor da requisição de forma segura.
    Só confia no header X-Actor se a requisição vier de um proxy confiável.
    """
    direct_ip = _normalize_ip(request.client.host if request.client else None) or "unknown"
    actor_header = request.headers.get("X-Actor")
    
    if actor_header and direct_ip in _trusted_proxies():
        return actor_header
    
    return "api-client"


async def _is_rate_limited(
    category: str,
    key: str,
    *,
    window_seconds: int,
    max_events: int,
) -> bool:
    """
    Verifica rate limit usando Redis (Sliding Window via List).
    Retorna True se estiver limitado, False se permitido.
    """
    redis = get_redis()
    redis_key = f"ratelimit:{category}:{key}"
    now = time.time()
    cutoff = now - window_seconds

    async with redis.pipeline(transaction=True) as pipe:
        # 1. Remove timestamps fora da janela
        await pipe.zremrangebyscore(redis_key, 0, cutoff)
        # 2. Adiciona o timestamp atual
        await pipe.zadd(redis_key, {str(now): now})
        # 3. Conta quantos eventos existem na janela
        await pipe.zcard(redis_key)
        # 4. Define expiração para limpeza automática
        await pipe.expire(redis_key, window_seconds + 10)
        
        results = await pipe.execute()
        event_count = results[2]
        
    return event_count > max_events


async def require_api_key(
    request: Request,
    x_api_key: str | None = Security(_api_key_header),
    credentials: HTTPAuthorizationCredentials | None = Security(_bearer_scheme),
) -> str:
    expected = _configured_api_key()
    bearer_key = credentials.credentials if credentials else None
    if _is_valid_api_key(x_api_key, expected) or _is_valid_api_key(bearer_key, expected):
        return _get_authenticated_actor(request)
    
    ip = _get_request_ip(request)
    if await _is_rate_limited(
        "api_auth_failures",
        ip,
        window_seconds=_AUTH_WINDOW_SECONDS,
        max_events=_AUTH_MAX_FAILURES_PER_WINDOW,
    ):
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Too many auth failures.")
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid API key.")


async def require_admin_key(
    request: Request,
    x_admin_key: str | None = Security(_admin_key_header),
) -> str:
    """Exige chave de nível admin (DASHBOARD_ADMIN_KEY) para operações CRUD de ativos.

    Se DASHBOARD_ADMIN_KEY não estiver configurado, todas as operações admin são bloqueadas.
    Retorna o actor autenticado.
    """
    admin_key = (settings.dashboard_admin_key or "").strip()
    if not admin_key:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Admin key not configured. Set DASHBOARD_ADMIN_KEY to enable asset management.",
        )

    ip = _get_request_ip(request)
    if _is_valid_api_key(x_admin_key, admin_key):
        return _get_authenticated_actor(request)

    if await _is_rate_limited(
        "admin_auth_failures",
        ip,
        window_seconds=_ADMIN_AUTH_WINDOW_SECONDS,
        max_events=_ADMIN_AUTH_MAX_FAILURES_PER_WINDOW,
    ):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many admin auth failures.",
        )
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid admin key. Use X-Admin-Key header.",
    )


async def require_ws_api_key(websocket: WebSocket) -> None:
    ip = _client_ip(websocket.client.host if websocket.client else None)
    if await _is_rate_limited(
        "ws_auth_attempts",
        ip,
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
    if not token:
        token = websocket.query_params.get("token")
    if not token:
        token = websocket.query_params.get("api_key")

    if _is_valid_api_key(token, expected):
        return

    await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION, reason="Invalid API key.")
