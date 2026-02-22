from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CAMERAS_ROUTER = ROOT / "src" / "dashboard" / "backend" / "app" / "routers" / "cameras.py"
FRIGATE_CONFIG = ROOT / "src" / "frigate" / "config.yml"
BACKEND_CONFIG = ROOT / "src" / "dashboard" / "backend" / "app" / "config.py"
LGPD_DOC = ROOT / "docs" / "LGPD_CAMERA_DATA_RETENTION_CHECKLIST.md"


def test_camera_access_logging_is_implemented():
    content = CAMERAS_ROUTER.read_text(encoding="utf-8")

    assert "event_type=\"camera_access\"" in content
    assert "async def _log_camera_access" in content
    assert "await _log_camera_access(" in content


def test_retention_baselines_are_defined():
    frigate = FRIGATE_CONFIG.read_text(encoding="utf-8")
    backend = BACKEND_CONFIG.read_text(encoding="utf-8")

    assert "days: 30" in frigate
    assert "alert_retention_days: int = 30" in backend


def test_lgpd_checklist_document_exists():
    content = LGPD_DOC.read_text(encoding="utf-8")

    assert "Checklist LGPD" in content
    assert "Issue #102" in content
    assert "camera_access" in content
