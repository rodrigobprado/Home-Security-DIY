from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SECURITY = ROOT / "src" / "dashboard" / "backend" / "app" / "security.py"


def test_ws_auth_does_not_accept_query_params():
    content = SECURITY.read_text(encoding="utf-8")

    assert 'websocket.headers.get("x-api-key")' in content
    assert "query_params.get(\"api_key\")" not in content
    assert "query_params.get(\"token\")" not in content
