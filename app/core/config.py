"""Application configuration settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    environment: str = "development"
    log_level: str = "INFO"

    # OpenRouter API
    openrouter_api_key: str
    openrouter_app_name: str = "Botatouille"
    openrouter_site_url: str = ""

    # WhatsApp Cloud API
    whatsapp_verify_token: str
    whatsapp_access_token: str
    whatsapp_phone_number_id: str

    # Database (optional for now)
    database_url: str = "postgresql://user:password@host:5432/botatouille"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()
