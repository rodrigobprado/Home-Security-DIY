from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SECURITY = ROOT / "src" / "dashboard" / "backend" / "app" / "security.py"


def test_security_module_has_auth_rate_limit_controls():
    content = SECURITY.read_text(encoding="utf-8")

    assert "_is_rate_limited" in content
    assert "get_redis" in content
    assert "_AUTH_MAX_FAILURES_PER_WINDOW" in content
    assert "_WS_AUTH_MAX_ATTEMPTS_PER_WINDOW" in content
    assert "HTTP_429_TOO_MANY_REQUESTS" in content
    assert "Too many auth failures." in content
