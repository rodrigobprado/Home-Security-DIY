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
        if "dashboard_user:password@" in value:
            raise ValueError("DATABASE_URL contains insecure default password.")
        return value


settings = Settings()
