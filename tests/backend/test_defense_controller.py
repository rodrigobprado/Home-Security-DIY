import base64
import hashlib
import hmac
import importlib.util
import json
import struct
import time
from pathlib import Path


MODULE_PATH = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "drones"
    / "common"
    / "defense_controller.py"
)


def _load_controller_class():
    spec = importlib.util.spec_from_file_location("defense_controller", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module.DefenseController


def _totp(secret, timestamp=None):
    now = int(timestamp or time.time())
    counter = now // 30
    key = base64.b32decode(secret, casefold=True)
    msg = struct.pack(">Q", counter)
    digest = hmac.new(key, msg, hashlib.sha1).digest()
    offset = digest[-1] & 0x0F
    binary = struct.unpack(">I", digest[offset : offset + 4])[0] & 0x7FFFFFFF
    return f"{binary % 1_000_000:06d}"


def test_arm_requires_pin_and_totp(tmp_path):
    DefenseController = _load_controller_class()
    secret = "JBSWY3DPEHPK3PXP"
    ctrl = DefenseController(
        pin_code="123456",
        totp_secret=secret,
        audit_log_path=str(tmp_path / "audit.log"),
    )
    ok, detail = ctrl.set_mode("semi_auto")
    assert ok and detail == "mode_updated"

    ok, detail = ctrl.arm("123456", "000000", source_id="test")
    assert not ok
    assert detail == "invalid_totp"

    ok, detail = ctrl.arm("123456", _totp(secret), source_id="test")
    assert ok
    assert detail == "armed"
    assert ctrl.get_status()["state"] == "armed"


def test_automatic_mode_is_forbidden(tmp_path):
    DefenseController = _load_controller_class()
    ctrl = DefenseController(
        pin_code="123456",
        totp_secret="JBSWY3DPEHPK3PXP",
        audit_log_path=str(tmp_path / "audit.log"),
    )
    ok, detail = ctrl.set_mode("automatic")
    assert not ok
    assert detail == "automatic_mode_forbidden"


def test_fire_flow_enforces_warning_zone_and_daily_limit(tmp_path):
    DefenseController = _load_controller_class()
    secret = "JBSWY3DPEHPK3PXP"
    ctrl = DefenseController(
        pin_code="123456",
        totp_secret=secret,
        warning_seconds=5,
        cooldown_seconds=1,
        max_triggers_per_day=1,
        exclusion_zones=["sidewalk"],
        audit_log_path=str(tmp_path / "audit.log"),
    )
    ctrl.set_mode("semi_auto")
    ok, detail = ctrl.arm("123456", _totp(secret), source_id="test")
    assert ok and detail == "armed"

    ok, detail = ctrl.request_fire(zone="sidewalk", source_id="test")
    assert not ok
    assert detail == "exclusion_zone"

    ctrl.disarm("reset")
    ctrl.set_mode("semi_auto")
    ctrl.arm("123456", _totp(secret), source_id="test")

    ok, detail = ctrl.request_fire(zone="yard", source_id="test")
    assert not ok
    assert detail == "warning_started"

    ctrl.warning_started_at -= 10
    ok, detail = ctrl.request_fire(zone="yard", source_id="test")
    assert ok
    assert detail == "fired"

    ctrl.disarm("reset2")
    ctrl.set_mode("semi_auto")
    ctrl.arm("123456", _totp(secret), source_id="test")
    ok, detail = ctrl.request_fire(zone="yard", source_id="test")
    assert not ok
    assert detail == "daily_limit_reached"


def test_audit_log_keeps_hash_chain(tmp_path):
    DefenseController = _load_controller_class()
    secret = "JBSWY3DPEHPK3PXP"
    log_file = tmp_path / "audit.log"
    ctrl = DefenseController(
        pin_code="123456",
        totp_secret=secret,
        audit_log_path=str(log_file),
    )
    ctrl.set_mode("semi_auto")
    ctrl.arm("123456", _totp(secret), source_id="test")
    ctrl.disarm("done")

    lines = log_file.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) >= 3

    previous_hash = "GENESIS"
    for line in lines:
        record = json.loads(line)
        assert "hash" in record
        assert record["prev_hash"] == previous_hash
        previous_hash = record["hash"]
