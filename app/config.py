from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración cargada desde variables de entorno / archivo .env."""

    model_config = SettingsConfigDict(
        env_file=".env",env_file_encoding="utf-8", env_ignore_empty=True, extra="ignore"
    )

    app_name: str = "Estimador CAG"
    llm_provider: Literal["openai", "anthropic"] = "anthropic"

    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"

    anthropic_api_key: str = ""
    anthropic_model: str = "claude-haiku-4-5"

    max_tokens: int = 4096
    temperature: float = 0.3

    @property
    def active_model(self) -> str:
        return self.openai_model if self.llm_provider == "openai" else self.anthropic_model


@lru_cache
def get_settings() -> Settings:
    return Settings()
