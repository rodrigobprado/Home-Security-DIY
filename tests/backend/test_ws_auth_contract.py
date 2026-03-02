from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SECURITY = ROOT / "src" / "dashboard" / "backend" / "app" / "security.py"


def test_ws_auth_accepts_browser_query_token():
    content = SECURITY.read_text(encoding="utf-8")

    assert 'websocket.headers.get("x-api-key")' in content
    assert 'query_params.get("token")' in content
