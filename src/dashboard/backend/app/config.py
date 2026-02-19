from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Home Assistant
    ha_url: str = "http://homeassistant:8123"
    ha_token: str = ""

    # Frigate NVR
    frigate_url: str = "http://frigate:5000"

    # MQTT
    mqtt_broker: str = "mosquitto"
    mqtt_port: int = 1883

    # Dashboard API security
    dashboard_api_key: str = ""
    dashboard_allowed_origins: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    # PostgreSQL (schema: dashboard)
    database_url: str = "postgresql+asyncpg://UNCONFIGURED:UNCONFIGURED@localhost/UNCONFIGURED"

    # Entidades relevantes para alertas
    alert_entities: list[str] = [
        "alarm_control_panel.alarmo",
        "binary_sensor.porta_entrada",
        "binary_sensor.porta_fundos",
        "binary_sensor.janela_sala",
        "binary_sensor.pir_sala_occupancy",
        "binary_sensor.pir_corredor",
        "binary_sensor.ugv_online",
        "binary_sensor.uav_armed",
    ]
    alert_retention_days: int = 90

    # Câmeras disponíveis
    cameras: list[str] = [
        "cam_entrada",
        "cam_fundos",
        "cam_garagem",
        "cam_lateral",
    ]

    @field_validator("dashboard_allowed_origins", mode="before")
    @classmethod
    def parse_origins(cls, value):
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, value):
        upper_value = value.upper()
        if "dashboard_user:password@" in value:
            raise ValueError("DATABASE_URL contains insecure default password.")
        if "UNCONFIGURED" in upper_value or "CHANGE_ME" in upper_value:
            raise ValueError("DATABASE_URL contains placeholder credentials.")
        return value

    @field_validator("ha_token", "dashboard_api_key")
    @classmethod
    def validate_required_secrets(cls, value: str, info):
        secret = (value or "").strip()
        if not secret:
            raise ValueError(f"{info.field_name.upper()} must be configured.")
        upper_secret = secret.upper()
        if "CHANGE_ME" in upper_secret or "UNCONFIGURED" in upper_secret:
            raise ValueError(f"{info.field_name.upper()} contains insecure placeholder value.")
        return secret


settings = Settings()
