from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DASHBOARD_K8S = ROOT / "k8s" / "base" / "dashboard" / "dashboard.yaml"
MOSQUITTO_K8S = ROOT / "k8s" / "base" / "mosquitto" / "mosquitto.yaml"
Z2M_K8S = ROOT / "k8s" / "base" / "zigbee2mqtt" / "zigbee2mqtt.yaml"


def test_dashboard_manifests_include_baseline_container_hardening():
    content = DASHBOARD_K8S.read_text(encoding="utf-8")

    assert "runAsNonRoot: true" in content
    assert "allowPrivilegeEscalation: false" in content
    assert "readOnlyRootFilesystem: true" in content
    assert "seccompProfile:" in content
    assert "type: RuntimeDefault" in content
    assert "drop:" in content
    assert "- ALL" in content


def test_mosquitto_manifest_includes_baseline_container_hardening():
    content = MOSQUITTO_K8S.read_text(encoding="utf-8")

    assert "runAsUser: 1883" in content
    assert "runAsNonRoot: true" in content
    assert "allowPrivilegeEscalation: false" in content
    assert "readOnlyRootFilesystem: true" in content
    assert "seccompProfile:" in content
    assert "type: RuntimeDefault" in content


def test_zigbee2mqtt_manifest_drops_privileged_and_has_baseline_hardening():
    content = Z2M_K8S.read_text(encoding="utf-8")

    assert "privileged: true" not in content
    assert "runAsNonRoot: true" in content
    assert "allowPrivilegeEscalation: false" in content
    assert "readOnlyRootFilesystem: true" in content
    assert "seccompProfile:" in content
    assert "type: RuntimeDefault" in content
    assert "drop:" in content
    assert "- ALL" in content
