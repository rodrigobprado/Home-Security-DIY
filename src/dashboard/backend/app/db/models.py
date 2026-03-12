import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    Uuid,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Alert(Base):
    """Histórico de alertas e eventos do sistema de segurança."""

    __tablename__ = "alerts"
    __table_args__ = (
        Index("ix_dashboard_alerts_severity_timestamp", "severity", "timestamp"),
        {"schema": "dashboard"},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True
    )
    entity_id: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    event_type: Mapped[str] = mapped_column(String(100), nullable=False)
    old_state: Mapped[str | None] = mapped_column(String(200))
    new_state: Mapped[str | None] = mapped_column(String(200))
    severity: Mapped[str] = mapped_column(String(20), default="info")  # info|warning|critical
    message: Mapped[str | None] = mapped_column(Text)


class DevicePosition(Base):
    """Posição de cada dispositivo sobre a imagem do mapa operacional."""

    __tablename__ = "device_positions"
    __table_args__ = {"schema": "dashboard"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    entity_id: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    label: Mapped[str] = mapped_column(String(100), nullable=False)
    x: Mapped[float] = mapped_column(Float, default=50.0)  # % horizontal
    y: Mapped[float] = mapped_column(Float, default=50.0)  # % vertical
    device_type: Mapped[str] = mapped_column(
        String(50), default="sensor"
    )  # camera|sensor|siren|drone


class DashboardConfig(Base):
    """Configurações chave-valor do dashboard."""

    __tablename__ = "dashboard_config"
    __table_args__ = {"schema": "dashboard"}

    key: Mapped[str] = mapped_column(String(100), primary_key=True)
    value: Mapped[str | None] = mapped_column(Text)


class Asset(Base):
    """Catálogo de ativos do sistema de segurança (sensores, câmeras, UGV, UAV)."""

    __tablename__ = "assets"
    __table_args__ = (
        CheckConstraint(
            "asset_type IN ('sensor', 'camera', 'ugv', 'uav')",
            name="ck_assets_asset_type",
        ),
        CheckConstraint(
            "status IN ('active', 'inactive', 'offline', 'maintenance')",
            name="ck_assets_status",
        ),
        Index("ix_dashboard_assets_asset_type", "asset_type"),
        Index("ix_dashboard_assets_is_active", "is_active"),
        Index("ix_dashboard_assets_updated_at", "updated_at"),
        {"schema": "dashboard"},
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    asset_type: Mapped[str] = mapped_column(
        String(20), nullable=False
    )  # sensor|camera|ugv|uav
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    entity_id: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    status: Mapped[str] = mapped_column(
        String(20), default="active"
    )  # active|inactive|offline|maintenance
    location: Mapped[str | None] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text)
    config_json: Mapped[str | None] = mapped_column(Text)  # JSON com config por tipo
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    created_by: Mapped[str | None] = mapped_column(String(100))
    updated_by: Mapped[str | None] = mapped_column(String(100))


class AssetCredential(Base):
    """Referências de credenciais de ativos — armazenamento seguro sem exposição ao frontend."""

    __tablename__ = "asset_credentials"
    __table_args__ = {"schema": "dashboard"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    asset_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("dashboard.assets.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    credential_ref: Mapped[str] = mapped_column(
        String(500), nullable=False
    )  # alias/vault ref, nunca o valor real
    last_rotated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


class AssetAudit(Base):
    """Trilha de auditoria para todas as operações no catálogo de ativos."""

    __tablename__ = "asset_audit"
    __table_args__ = (
        CheckConstraint(
            "action IN ('create', 'update', 'delete', 'restore')",
            name="ck_asset_audit_action",
        ),
        Index("ix_dashboard_asset_audit_asset_id", "asset_id"),
        Index("ix_dashboard_asset_audit_created_at", "created_at"),
        Index("ix_dashboard_asset_audit_actor", "actor"),
        {"schema": "dashboard"},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    asset_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid(as_uuid=True), index=True
    )  # nullable para deleções permanentes
    action: Mapped[str] = mapped_column(
        String(20), nullable=False
    )  # create|update|delete|restore
    before_json: Mapped[str | None] = mapped_column(Text)  # estado anterior (JSON)
    after_json: Mapped[str | None] = mapped_column(Text)  # estado posterior (JSON)
    actor: Mapped[str | None] = mapped_column(String(100))  # usuário/sistema que executou
    actor_ip: Mapped[str | None] = mapped_column(String(45))  # IPv4 ou IPv6
    actor_ip_chain: Mapped[str | None] = mapped_column(Text)  # cadeia X-Forwarded-For normalizada
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )


class CameraAccessLog(Base):
    """LGPD/CFTV: Registro de acesso operacional às câmeras e eventos."""

    __tablename__ = "camera_access_logs"
    __table_args__ = (
        Index("ix_dashboard_camera_access_logs_camera_timestamp", "camera_name", "timestamp"),
        {"schema": "dashboard"},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True
    )
    camera_name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    action: Mapped[str] = mapped_column(String(50), nullable=False)  # snapshot|events|stream
    client_ip: Mapped[str] = mapped_column(String(45), nullable=False)
    actor: Mapped[str | None] = mapped_column(String(100))
