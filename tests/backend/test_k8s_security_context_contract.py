from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DASHBOARD_K8S = ROOT / "k8s" / "base" / "dashboard" / "dashboard.yaml"
MOSQUITTO_K8S = ROOT / "k8s" / "base" / "mosquitto" / "mosquitto.yaml"


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
