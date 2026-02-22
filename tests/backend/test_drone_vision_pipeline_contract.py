from pathlib import Path

UGV_VISION = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "drones"
    / "ugv"
    / "app"
    / "ugv_vision.py"
)

UAV_VISION = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "drones"
    / "uav"
    / "uav_vision.py"
)


def test_ugv_vision_uses_real_backends_not_random_mock():
    content = UGV_VISION.read_text(encoding="utf-8")

    assert "class YoloV8Backend" in content
    assert "class TFLiteBackend" in content
    assert "SortLikeTracker" in content
    assert "random.random()" not in content


def test_ugv_vision_has_safety_filter_for_animals_and_children():
    content = UGV_VISION.read_text(encoding="utf-8")

    assert "ANIMAL_CLASSES" in content
    assert "possible_child_or_uncertain_person" in content
    assert "defense_blocked" in content


def test_uav_vision_pipeline_exists_and_publishes_detections():
    content = UAV_VISION.read_text(encoding="utf-8")

    assert "uav/vision/detections" in content
    assert "uav/vision/safety" in content
    assert "SortLikeTracker" in content
