from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Alert(Base):
    """Histórico de alertas e eventos do sistema de segurança."""

    __tablename__ = "alerts"
    __table_args__ = {"schema": "dashboard"}

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
