from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DASHBOARD_K8S = ROOT / "k8s" / "base" / "dashboard" / "dashboard.yaml"
MOSQUITTO_K8S = ROOT / "k8s" / "base" / "mosquitto" / "mosquitto.yaml"
Z2M_K8S = ROOT / "k8s" / "base" / "zigbee2mqtt" / "zigbee2mqtt.yaml"
FRIGATE_K8S = ROOT / "k8s" / "base" / "frigate" / "frigate.yaml"
HOMEASSISTANT_K8S = ROOT / "k8s" / "base" / "homeassistant" / "homeassistant.yaml"
RUN_AS_NON_ROOT = "runAsNonRoot: true"
ALLOW_PRIV_ESC_FALSE = "allowPrivilegeEscalation: false"
READ_ONLY_FS_TRUE = "readOnlyRootFilesystem: true"
SECCOMP_PROFILE = "seccompProfile:"
RUNTIME_DEFAULT = "type: RuntimeDefault"


def test_dashboard_manifests_include_baseline_container_hardening():
    content = DASHBOARD_K8S.read_text(encoding="utf-8")

    assert RUN_AS_NON_ROOT in content
    assert ALLOW_PRIV_ESC_FALSE in content
    assert READ_ONLY_FS_TRUE in content
    assert SECCOMP_PROFILE in content
    assert RUNTIME_DEFAULT in content
    assert "drop:" in content
    assert "- ALL" in content


def test_mosquitto_manifest_includes_baseline_container_hardening():
    content = MOSQUITTO_K8S.read_text(encoding="utf-8")

    assert "runAsUser: 1883" in content
    assert RUN_AS_NON_ROOT in content
    assert ALLOW_PRIV_ESC_FALSE in content
    assert READ_ONLY_FS_TRUE in content
    assert SECCOMP_PROFILE in content
    assert RUNTIME_DEFAULT in content


def test_zigbee2mqtt_manifest_drops_privileged_and_has_baseline_hardening():
    content = Z2M_K8S.read_text(encoding="utf-8")

    assert "privileged: true" not in content
    assert RUN_AS_NON_ROOT in content
    assert ALLOW_PRIV_ESC_FALSE in content
    assert READ_ONLY_FS_TRUE in content
    assert SECCOMP_PROFILE in content
    assert RUNTIME_DEFAULT in content
    assert "drop:" in content
    assert "- ALL" in content


def test_critical_services_mount_persistent_data_volumes():
    z2m_content = Z2M_K8S.read_text(encoding="utf-8")
    frigate_content = FRIGATE_K8S.read_text(encoding="utf-8")
    ha_content = HOMEASSISTANT_K8S.read_text(encoding="utf-8")
    mosquitto_content = MOSQUITTO_K8S.read_text(encoding="utf-8")

    assert "claimName: zigbee2mqtt-data" in z2m_content
    assert "mountPath: /app/data" in z2m_content

    assert "claimName: frigate-config" in frigate_content
    assert "claimName: frigate-media" in frigate_content
    assert "mountPath: /config" in frigate_content
    assert "mountPath: /media" in frigate_content

    assert "claimName: homeassistant-config" in ha_content
    assert "mountPath: /config" in ha_content

    assert "claimName: mosquitto-data" in mosquitto_content
    assert "mountPath: /mosquitto/data" in mosquitto_content
