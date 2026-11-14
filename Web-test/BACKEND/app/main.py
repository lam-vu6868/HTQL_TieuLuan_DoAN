# File hiện tại config để đảm bảo cấu trúc container db chạy ổn và BE có thể connect

from fastapi import FastAPI
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine


class Settings(BaseSettings):
    database_url: str
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

# Singleton
settings = Settings()
engine = create_async_engine(settings.database_url)
app = FastAPI()

@app.get("/health")
async def health():
    async with engine.connect() as connect:
        await connect.execute(text("SELECT 1"))
    return{
        "status":"OK",
        "db": "Connected"
    }

