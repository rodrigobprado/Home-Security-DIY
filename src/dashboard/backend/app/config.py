from pydantic_settings import BaseSettings, SettingsConfigDict


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

    # PostgreSQL (schema: dashboard)
    database_url: str = (
        "postgresql+asyncpg://dashboard_user:password"
        "@postgres:5432/homedb?options=-csearch_path%3Ddashboard"
    )

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


settings = Settings()
