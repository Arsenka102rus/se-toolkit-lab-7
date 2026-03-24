"""Configuration management for the LMS bot.

Loads settings from environment variables, typically from .env.bot.secret.
Uses pydantic-settings for validation and type safety.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class BotSettings(BaseSettings):
    """Bot configuration settings."""

    model_config = SettingsConfigDict(
        env_file=".env.bot.secret",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Telegram bot token
    bot_token: str = ""

    # LMS API connection
    lms_api_base_url: str = ""
    lms_api_key: str = ""

    # LLM API connection
    llm_api_base_url: str = ""
    llm_api_key: str = ""
    llm_api_model: str = "coder-model"


# Global settings instance
settings = BotSettings()
