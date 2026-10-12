from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    host_home: str = ""
    host_mount_prefix: str = "/host"
    oops_url: str = "http://localhost:8080/OOPS/rest"
    reasoner_timeout: int = 120
    server_host: str = "0.0.0.0"
    server_port: int = 8000


settings = Settings()
