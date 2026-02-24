from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DRONES_ARCH_DOC = ROOT / "docs" / "ARQUITETURA_DRONES_AUTONOMOS.md"


def test_drone_task_status_table_exists_for_t031_to_t045():
    content = DRONES_ARCH_DOC.read_text(encoding="utf-8")

    assert "Status de execução das tasks (T-031 a T-045)" in content
    assert "T-031" in content
    assert "T-045" in content


def test_drone_task_artifacts_exist():
    required_paths = [
        ROOT / "docs" / "ARQUITETURA_HARDWARE_UGV.md",
        ROOT / "docs" / "ARQUITETURA_HARDWARE_UAV.md",
        ROOT / "src" / "drones" / "ugv" / "app" / "ugv_control.py",
        ROOT / "docs" / "UGV_ROS2_NAVIGATION.md",
        ROOT / "docs" / "DRONE_AI_VISION_PIPELINE.md",
        ROOT / "docs" / "DRONE_COMMUNICATION_REDUNDANCY.md",
        ROOT / "docs" / "DRONE_DEFENSE_IMPLEMENTATION.md",
        ROOT / "docs" / "DRONE_HOMEASSISTANT_MQTT_INTEGRATION.md",
        ROOT / "src" / "dashboard" / "frontend" / "src" / "components" / "DroneStatus.jsx",
        ROOT / "prd" / "PRD_DRONE_DEFENSE_MODULE.md",
        ROOT / "prd" / "PRD_DRONE_COMMUNICATION.md",
        ROOT / "docs" / "GUIA_MONTAGEM_UGV.md",
        ROOT / "docs" / "GUIA_MONTAGEM_UAV.md",
    ]

    for path in required_paths:
        assert path.exists(), f"Artifact missing: {path}"
