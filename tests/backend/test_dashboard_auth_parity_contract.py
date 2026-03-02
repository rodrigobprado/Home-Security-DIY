from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
NGINX_CONF = ROOT / "src" / "dashboard" / "frontend" / "nginx.conf.template"
VITE_CONFIG = ROOT / "src" / "dashboard" / "frontend" / "vite.config.js"


def test_prod_nginx_does_not_inject_static_api_key():
    content = NGINX_CONF.read_text(encoding="utf-8")
    assert "proxy_set_header X-API-Key" not in content
    assert "proxy_set_header X-Admin-Key" not in content


def test_dev_vite_proxy_does_not_inject_auth_headers():
    content = VITE_CONFIG.read_text(encoding="utf-8")
    assert "'/api'" in content
    assert "'/ws'" in content
    assert "headers:" not in content
