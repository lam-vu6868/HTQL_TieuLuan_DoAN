from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# BE/app/core/config.py → parents[2] = BE/
_ENV_FILE = Path(__file__).resolve().parents[2] / ".env"


class Settings(BaseSettings):
    DATABASE_URL: str
    FE_URL: str
    
    JWT_SECRET: str
    ACCESS_EXPIRE_MINUTES: int = 15
    REFRESH_EXPIRE_DAYS: int = 3

    model_config = SettingsConfigDict(
        env_file=_ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False
    )


# Fail-fast: app không khởi động được nếu .env thiếu biến bắt buộc.
settings = Settings()