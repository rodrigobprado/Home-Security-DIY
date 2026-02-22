import base64
import hashlib
import hmac
import json
import logging
import struct
import time
from pathlib import Path


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class DefenseController:
    STATE_IDLE = "idle"
    STATE_WARNING = "warning"
    STATE_ARMED = "armed"
    STATE_ACTIVE = "active"
    STATE_BLOCKED = "blocked"

    MODE_DISABLED = "disabled"
    MODE_STANDBY = "standby"
    MODE_SEMI_AUTO = "semi_auto"

    def __init__(
        self,
        pin_code,
        totp_secret="",
        warning_seconds=5,
        cooldown_seconds=30,
        max_triggers_per_day=3,
        exclusion_zones=None,
        audit_log_path="/tmp/ugv_defense_audit.log",
    ):
        if not pin_code:
            raise ValueError("DefenseController requires a non-empty pin_code.")

        self.state = self.STATE_IDLE
        self.mode = self.MODE_STANDBY
        self.pin_code = str(pin_code)
        self.totp_secret = (totp_secret or "").strip()
        self.warning_seconds = max(1, int(warning_seconds))
        self.cooldown_seconds = max(1, int(cooldown_seconds))
        self.max_triggers_per_day = max(1, int(max_triggers_per_day))
        self.exclusion_zones = {str(z).strip() for z in (exclusion_zones or []) if str(z).strip()}

        self.last_arm_time = 0.0
        self.ARM_TIMEOUT = 60
        self.MAX_FAILED_ATTEMPTS = 3
        self.LOCKOUT_SECONDS = 300
        self.failed_attempts = 0
        self.locked_until = 0.0

        self.warning_started_at = 0.0
        self.last_trigger_time = 0.0
        self.trigger_events = []
        self.block_reason = ""

        self.audit_log_path = Path(audit_log_path)
        self.audit_head = self._load_last_hash()
        self._append_audit("controller_init", {"mode": self.mode, "state": self.state})

        logging.info("Defense Controller Initialized")

    def _load_last_hash(self):
        if not self.audit_log_path.exists():
            return "GENESIS"
        try:
            last = self.audit_log_path.read_text(encoding="utf-8").strip().splitlines()[-1]
            payload = json.loads(last)
            return payload.get("hash", "GENESIS")
        except Exception:
            return "GENESIS"

    def _append_audit(self, action, details):
        ts = int(time.time())
        entry = {
            "ts": ts,
            "action": action,
            "mode": self.mode,
            "state": self.state,
            "details": details,
            "prev_hash": self.audit_head,
        }
        canonical = json.dumps(entry, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        entry["hash"] = digest

        try:
            self.audit_log_path.parent.mkdir(parents=True, exist_ok=True)
            with self.audit_log_path.open("a", encoding="utf-8") as fp:
                fp.write(json.dumps(entry, ensure_ascii=True) + "\n")
            self.audit_head = digest
        except Exception as exc:
            logging.error("Audit log write failed: %s", exc)

    def _is_locked(self):
        return time.time() < self.locked_until

    def _is_totp_configured(self):
        return bool(self.totp_secret)

    def _verify_totp(self, code, window=1):
        if not self._is_totp_configured():
            return False
        if not isinstance(code, str) or not code.isdigit() or len(code) != 6:
            return False

        now = int(time.time())
        for offset in range(-window, window + 1):
            counter = (now // 30) + offset
            if self._totp_code(counter) == code:
                return True
        return False

    def _totp_code(self, counter):
        secret = self.totp_secret.replace(" ", "").upper()
        key = base64.b32decode(secret, casefold=True)
        msg = struct.pack(">Q", counter)
        digest = hmac.new(key, msg, hashlib.sha1).digest()
        offset = digest[-1] & 0x0F
        binary = struct.unpack(">I", digest[offset : offset + 4])[0] & 0x7FFFFFFF
        return f"{binary % 1_000_000:06d}"

    def _prune_daily_events(self):
        now = time.time()
        self.trigger_events = [ts for ts in self.trigger_events if (now - ts) <= 86400]

    def set_mode(self, mode):
        requested = str(mode).strip().lower()
        if requested == "automatic":
            self._append_audit("mode_rejected", {"requested": requested, "reason": "automatic_forbidden"})
            return False, "automatic_mode_forbidden"

        allowed = {self.MODE_DISABLED, self.MODE_STANDBY, self.MODE_SEMI_AUTO}
        if requested not in allowed:
            self._append_audit("mode_rejected", {"requested": requested, "reason": "invalid_mode"})
            return False, "invalid_mode"

        self.mode = requested
        if self.mode == self.MODE_DISABLED:
            self.disarm("Mode disabled")
        self._append_audit("mode_changed", {"mode": self.mode})
        return True, "mode_updated"

    def set_exclusion_zones(self, zones):
        parsed = {str(z).strip() for z in (zones or []) if str(z).strip()}
        self.exclusion_zones = parsed
        self._append_audit("exclusion_zones_updated", {"zones": sorted(self.exclusion_zones)})

    def get_status(self):
        now = time.time()
        if self.state == self.STATE_ARMED and (now - self.last_arm_time > self.ARM_TIMEOUT):
            self.disarm("arm_timeout")

        warning_remaining = 0
        if self.state == self.STATE_WARNING and self.warning_started_at > 0:
            warning_remaining = max(0, int(self.warning_seconds - (now - self.warning_started_at)))

        cooldown_remaining = max(0, int(self.cooldown_seconds - (now - self.last_trigger_time)))
        self._prune_daily_events()

        return {
            "mode": self.mode,
            "state": self.state,
            "block_reason": self.block_reason,
            "armed_time_remaining": max(0, int(self.ARM_TIMEOUT - (now - self.last_arm_time)))
            if self.state in {self.STATE_ARMED, self.STATE_WARNING}
            else 0,
            "warning_remaining": warning_remaining,
            "cooldown_remaining": cooldown_remaining,
            "failed_attempts": self.failed_attempts,
            "lockout_remaining": max(0, int(self.locked_until - now)),
            "triggers_last_24h": len(self.trigger_events),
            "max_triggers_last_24h": self.max_triggers_per_day,
            "totp_required": self._is_totp_configured(),
            "audit_hash_head": self.audit_head,
            "exclusion_zones": sorted(self.exclusion_zones),
        }

    def set_warning(self, level=1):
        if self.mode == self.MODE_DISABLED:
            self.block_reason = "defense_disabled"
            self.state = self.STATE_BLOCKED
            self._append_audit("warning_blocked", {"reason": self.block_reason})
            return False

        if self.state == self.STATE_ACTIVE:
            logging.warning("Cannot downgrade from Active to Warning directly. Disarm first.")
            return False

        self.state = self.STATE_WARNING
        self.warning_started_at = time.time()
        self._append_audit("warning_started", {"level": int(level), "warning_seconds": self.warning_seconds})
        return True

    def arm(self, pin, totp_code="", source_id="unknown"):
        if self.mode == self.MODE_DISABLED:
            self.block_reason = "defense_disabled"
            self.state = self.STATE_BLOCKED
            self._append_audit("arm_blocked", {"reason": self.block_reason, "source_id": source_id})
            return False, "defense_disabled"
        if self.mode != self.MODE_SEMI_AUTO:
            self._append_audit("arm_blocked", {"reason": "mode_not_semi_auto", "mode": self.mode})
            return False, "mode_not_semi_auto"
        if self._is_locked():
            self._append_audit("arm_blocked", {"reason": "locked", "source_id": source_id})
            return False, "locked"
        if str(pin) != self.pin_code:
            self.failed_attempts += 1
            if self.failed_attempts >= self.MAX_FAILED_ATTEMPTS:
                self.locked_until = time.time() + self.LOCKOUT_SECONDS
                self.failed_attempts = 0
                self._append_audit("arm_failed", {"reason": "too_many_invalid_pin", "source_id": source_id})
                return False, "too_many_invalid_pin"
            self._append_audit("arm_failed", {"reason": "invalid_pin", "source_id": source_id})
            return False, "invalid_pin"
        if not self._is_totp_configured():
            self._append_audit("arm_failed", {"reason": "totp_not_configured", "source_id": source_id})
            return False, "totp_not_configured"
        if not self._verify_totp(totp_code):
            self._append_audit("arm_failed", {"reason": "invalid_totp", "source_id": source_id})
            return False, "invalid_totp"

        self.state = self.STATE_ARMED
        self.last_arm_time = time.time()
        self.warning_started_at = 0.0
        self.block_reason = ""
        self.failed_attempts = 0
        self._append_audit("armed", {"source_id": source_id})
        return True, "armed"

    def disarm(self, reason="manual"):
        self.state = self.STATE_IDLE
        self.block_reason = ""
        self.warning_started_at = 0.0
        self._append_audit("disarmed", {"reason": reason})
        return True

    def request_fire(
        self,
        zone="",
        defense_blocked=False,
        block_reasons=None,
        source_id="unknown",
    ):
        zone_name = str(zone).strip().lower()
        reasons = [str(r) for r in (block_reasons or []) if str(r)]

        if self.mode != self.MODE_SEMI_AUTO:
            self._append_audit("fire_blocked", {"reason": "mode_not_semi_auto", "mode": self.mode})
            return False, "mode_not_semi_auto"
        if self.state not in {self.STATE_ARMED, self.STATE_WARNING}:
            self._append_audit("fire_blocked", {"reason": "not_armed", "state": self.state})
            return False, "not_armed"
        if defense_blocked:
            self.state = self.STATE_BLOCKED
            self.block_reason = "vision_blocked"
            self._append_audit(
                "fire_blocked",
                {"reason": self.block_reason, "vision_reasons": reasons, "source_id": source_id},
            )
            return False, "vision_blocked"
        if zone_name and zone_name in self.exclusion_zones:
            self.state = self.STATE_BLOCKED
            self.block_reason = f"exclusion_zone:{zone_name}"
            self._append_audit(
                "fire_blocked",
                {"reason": self.block_reason, "zone": zone_name, "source_id": source_id},
            )
            return False, "exclusion_zone"

        self._prune_daily_events()
        if len(self.trigger_events) >= self.max_triggers_per_day:
            self.state = self.STATE_BLOCKED
            self.block_reason = "daily_limit_reached"
            self._append_audit("fire_blocked", {"reason": self.block_reason, "source_id": source_id})
            return False, "daily_limit_reached"

        now = time.time()
        if now - self.last_trigger_time < self.cooldown_seconds:
            self._append_audit("fire_blocked", {"reason": "cooldown_active", "source_id": source_id})
            return False, "cooldown_active"

        if self.state != self.STATE_WARNING:
            self.state = self.STATE_WARNING
            self.warning_started_at = now
            self._append_audit("warning_started", {"warning_seconds": self.warning_seconds, "source_id": source_id})
            return False, "warning_started"

        if now - self.warning_started_at < self.warning_seconds:
            self._append_audit("fire_pending", {"reason": "warning_countdown", "source_id": source_id})
            return False, "warning_countdown"

        self.state = self.STATE_ACTIVE
        self.last_trigger_time = now
        self.trigger_events.append(now)
        self._append_audit("fired", {"zone": zone_name or None, "source_id": source_id})
        return True, "fired"

    def trigger(self):
        ok, _ = self.request_fire()
        return ok
