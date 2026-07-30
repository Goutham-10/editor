from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # OpenRouter — text + vision LLM calls (edit planning, revision, QC).
    # Left blank-able so the app can boot before a key exists; llm/openrouter.py
    # validates presence at call time, not at startup.
    openrouter_api_key: str = ""
    openrouter_model: str = ""
    openrouter_fallback_model: str = ""

    # Supabase Postgres connection string, e.g.
    # postgresql+psycopg://postgres:<password>@<host>:5432/postgres
    database_url: str = ""

    storage_root: Path = PROJECT_ROOT / "storage"
    brands_dir: Path = PROJECT_ROOT / "brands"
    assets_dir: Path = PROJECT_ROOT / "assets"

    whisper_model_size: str = "small"
    log_level: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    return Settings()
