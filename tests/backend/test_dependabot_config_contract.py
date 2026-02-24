from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEPENDABOT_CONFIG = ROOT / ".github" / "dependabot.yml"


def test_dependabot_config_covers_required_ecosystems_and_paths():
    content = DEPENDABOT_CONFIG.read_text(encoding="utf-8")

    expected_pairs = [
        ('package-ecosystem: "github-actions"', 'directory: "/"'),
        ('package-ecosystem: "docker"', 'directory: "/src"'),
        ('package-ecosystem: "pip"', 'directory: "/src/dashboard/backend"'),
        ('package-ecosystem: "pip"', 'directory: "/src/drones/common"'),
        ('package-ecosystem: "pip"', 'directory: "/src/drones/ugv/app"'),
        ('package-ecosystem: "pip"', 'directory: "/src/drones/uav"'),
        ('package-ecosystem: "npm"', 'directory: "/src/dashboard/frontend"'),
    ]

    for ecosystem, directory in expected_pairs:
        assert ecosystem in content
        assert directory in content


def test_dependabot_config_enforces_main_branch_weekly_schedule_and_labels():
    content = DEPENDABOT_CONFIG.read_text(encoding="utf-8")

    assert 'target-branch: "main"' in content
    assert 'interval: "weekly"' in content
    assert 'timezone: "America/Sao_Paulo"' in content
    assert 'labels:' in content
