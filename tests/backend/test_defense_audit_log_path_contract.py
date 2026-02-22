from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFENSE_CONTROLLER = ROOT / "src" / "drones" / "common" / "defense_controller.py"
UGV_CONTROL = ROOT / "src" / "drones" / "ugv" / "app" / "ugv_control.py"
ENV_EXAMPLE = ROOT / "src" / ".env.example"


def test_defense_audit_default_path_is_not_tmp():
    controller = DEFENSE_CONTROLLER.read_text(encoding="utf-8")
    ugv = UGV_CONTROL.read_text(encoding="utf-8")
    env_example = ENV_EXAMPLE.read_text(encoding="utf-8")

    assert "/var/lib/home-security/audit/ugv_defense_audit.log" in controller
    assert "/var/lib/home-security/audit/ugv_defense_audit.log" in ugv
    assert "DEFENSE_AUDIT_LOG_PATH_UGV=/var/lib/home-security/audit/ugv_defense_audit.log" in env_example
    assert "/tmp/ugv_defense_audit.log" not in controller


def test_defense_audit_log_permission_is_restricted():
    controller = DEFENSE_CONTROLLER.read_text(encoding="utf-8")

    assert "os.chmod(self.audit_log_path, 0o600)" in controller
