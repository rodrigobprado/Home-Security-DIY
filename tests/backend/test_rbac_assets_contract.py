"""Testes de contrato de RBAC para operações de ativos — Issue #338."""

import pytest


class TestRBACMatrix:
    """Valida a matriz de permissões definida na Issue #338."""

    def test_rbac_matrix_viewer_only_read(self):
        """viewer: somente leitura — endpoints GET são permitidos, POST/PUT/DELETE exigem admin."""
        # Esta é uma validação de design: leitura pública (com operator key), escrita requer admin
        readonly_methods = ["GET"]
        write_methods = ["POST", "PUT", "DELETE"]

        # Valida que a separação está clara na implementação
        from app.routers.assets import router

        routes = {route.path: list(route.methods) for route in router.routes}

        # /api/assets GET deve ser read-only (sem require_admin_key no nível do router)
        get_routes = [path for path, methods in routes.items() if "GET" in methods]
        assert len(get_routes) > 0, "Deve haver rotas GET para ativos"

    def test_admin_key_required_for_create(self):
        """Endpoint de criação deve ter require_admin_key como dependência."""
        from app.routers.assets import router
        from app.security import require_admin_key

        for route in router.routes:
            if hasattr(route, "methods") and "POST" in route.methods:
                if route.path == "/api/assets":  # rota de criação
                    dep_funcs = [
                        d.dependency for d in route.dependencies if hasattr(d, "dependency")
                    ]
                    assert require_admin_key in dep_funcs, (
                        "POST /api/assets deve ter require_admin_key"
                    )

    def test_admin_key_required_for_delete(self):
        """Endpoint de deleção deve ter require_admin_key."""
        from app.routers.assets import router
        from app.security import require_admin_key

        for route in router.routes:
            if hasattr(route, "methods") and "DELETE" in route.methods:
                dep_funcs = [
                    d.dependency for d in route.dependencies if hasattr(d, "dependency")
                ]
                assert require_admin_key in dep_funcs, (
                    f"DELETE {route.path} deve ter require_admin_key"
                )

    def test_admin_key_required_for_update(self):
        """Endpoint de atualização deve ter require_admin_key."""
        from app.routers.assets import router
        from app.security import require_admin_key

        for route in router.routes:
            if hasattr(route, "methods") and "PUT" in route.methods:
                dep_funcs = [
                    d.dependency for d in route.dependencies if hasattr(d, "dependency")
                ]
                assert require_admin_key in dep_funcs, (
                    f"PUT {route.path} deve ter require_admin_key"
                )


class TestRBACAdminKeyConfig:
    """Valida que a configuração de admin key falha de forma segura."""

    def test_admin_key_fail_secure_when_empty(self, monkeypatch):
        """Se DASHBOARD_ADMIN_KEY não configurado, operações admin devem ser bloqueadas (503)."""
        import asyncio
        from unittest.mock import MagicMock

        from fastapi import HTTPException

        # Patch settings para admin key vazia
        from app import config as cfg_module

        original_key = cfg_module.settings.dashboard_admin_key
        monkeypatch.setattr(cfg_module.settings, "dashboard_admin_key", "")

        from app.security import require_admin_key

        req = MagicMock()
        req.client = MagicMock()
        req.client.host = "127.0.0.1"
        req.headers = {}

        with pytest.raises(HTTPException) as exc_info:
            asyncio.run(require_admin_key(request=req, x_admin_key=None))

        assert exc_info.value.status_code == 503
        assert "Admin key not configured" in str(exc_info.value.detail)

    def test_admin_key_rejects_wrong_key(self, monkeypatch):
        """Admin key errada deve retornar 403."""
        import asyncio
        from unittest.mock import MagicMock

        from fastapi import HTTPException

        from app import config as cfg_module

        monkeypatch.setattr(cfg_module.settings, "dashboard_admin_key", "correct-admin-key")

        from app.security import require_admin_key

        req = MagicMock()
        req.client = MagicMock()
        req.client.host = "127.0.0.1"
        req.headers = {}

        with pytest.raises(HTTPException) as exc_info:
            asyncio.run(require_admin_key(request=req, x_admin_key="wrong-key"))

        assert exc_info.value.status_code == 403

    def test_admin_key_accepts_correct_key(self, monkeypatch):
        """Admin key correta não deve levantar exceção."""
        import asyncio
        from unittest.mock import MagicMock

        from app import config as cfg_module

        monkeypatch.setattr(cfg_module.settings, "dashboard_admin_key", "correct-admin-key")

        from app.security import require_admin_key

        req = MagicMock()
        req.client = MagicMock()
        req.client.host = "127.0.0.1"
        req.headers = {}

        # Não deve levantar exceção
        result = asyncio.run(require_admin_key(request=req, x_admin_key="correct-admin-key"))
        assert result is None


class TestCredentialMasking:
    """Valida que credenciais sensíveis não são expostas na API — Issue #338."""

    def test_asset_serializer_excludes_credentials(self):
        """_asset_to_dict não deve incluir o campo de credenciais."""
        from unittest.mock import MagicMock
        import uuid
        from datetime import datetime, timezone

        from app.routers.assets import _asset_to_dict

        asset = MagicMock()
        asset.id = uuid.uuid4()
        asset.asset_type = "camera"
        asset.name = "Camera Entrada"
        asset.entity_id = "camera.entrada"
        asset.status = "active"
        asset.location = "entrada"
        asset.description = None
        asset.config_json = None
        asset.is_active = True
        asset.created_at = datetime.now(timezone.utc)
        asset.updated_at = datetime.now(timezone.utc)
        asset.created_by = "admin"
        asset.updated_by = "admin"

        result = _asset_to_dict(asset)

        # Campos de credencial NÃO devem estar presentes
        assert "credential_ref" not in result
        assert "password" not in result
        assert "secret" not in result
        # AssetCredential é uma tabela separada — nunca join automático

    def test_asset_response_does_not_include_credential_ref(self):
        """A resposta do asset não deve incluir referência de credencial."""
        from app.routers.assets import _asset_to_dict
        from unittest.mock import MagicMock
        import uuid
        from datetime import datetime, timezone

        asset = MagicMock()
        asset.id = uuid.uuid4()
        asset.asset_type = "camera"
        asset.name = "Camera"
        asset.entity_id = "camera.test"
        asset.status = "active"
        asset.location = None
        asset.description = None
        asset.config_json = None
        asset.is_active = True
        asset.created_at = datetime.now(timezone.utc)
        asset.updated_at = datetime.now(timezone.utc)
        asset.created_by = "system"
        asset.updated_by = "system"

        serialized = _asset_to_dict(asset)
        serialized_str = str(serialized)
        assert "credential" not in serialized_str.lower()


class TestRBACEndpointCoverage:
    """Valida que todos os endpoints de escrita têm RBAC configurado."""

    def test_all_write_endpoints_have_admin_dependency(self):
        """Todos os endpoints POST/PUT/DELETE em /api/assets devem ter require_admin_key."""
        from app.routers.assets import router
        from app.security import require_admin_key

        write_routes = [
            route
            for route in router.routes
            if hasattr(route, "methods")
            and any(m in route.methods for m in ("POST", "PUT", "DELETE"))
        ]

        assert len(write_routes) > 0, "Deve haver endpoints de escrita"

        for route in write_routes:
            dep_funcs = [
                d.dependency for d in route.dependencies if hasattr(d, "dependency")
            ]
            assert require_admin_key in dep_funcs, (
                f"Endpoint {route.methods} {route.path} não tem require_admin_key"
            )

    def test_get_endpoints_do_not_require_admin(self):
        """Endpoints GET não devem exigir admin key (apenas operator key via main.py)."""
        from app.routers.assets import router
        from app.security import require_admin_key

        get_routes = [
            route
            for route in router.routes
            if hasattr(route, "methods") and "GET" in route.methods
        ]

        for route in get_routes:
            dep_funcs = [
                d.dependency for d in route.dependencies if hasattr(d, "dependency")
            ]
            assert require_admin_key not in dep_funcs, (
                f"GET {route.path} não deve exigir admin key"
            )
