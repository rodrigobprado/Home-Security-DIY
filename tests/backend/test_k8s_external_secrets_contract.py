from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROD_KUSTOMIZATION = ROOT / "k8s" / "overlays" / "production" / "kustomization.yaml"
PROD_EXTERNAL_SECRETS = ROOT / "k8s" / "overlays" / "production" / "external-secrets.yaml"
SECRETS_DOC = ROOT / "docs" / "K8S_SECRETS_MANAGEMENT.md"


def test_production_overlay_includes_external_secrets_manifest():
    content = PROD_KUSTOMIZATION.read_text(encoding="utf-8")

    assert "external-secrets.yaml" in content


def test_external_secrets_manifest_declares_required_resources():
    content = PROD_EXTERNAL_SECRETS.read_text(encoding="utf-8")

    assert "kind: SecretStore" in content
    assert "kind: ExternalSecret" in content
    assert "name: dashboard-credentials" in content
    assert "name: frigate-cameras" in content


def test_secrets_management_doc_sets_eso_as_production_standard():
    content = SECRETS_DOC.read_text(encoding="utf-8")

    assert "External Secrets Operator" in content
    assert "Produção" in content
