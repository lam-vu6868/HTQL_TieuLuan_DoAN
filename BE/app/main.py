"""Điểm khởi động API và kiểm tra kết nối database."""

from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import engine, get_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()


app = FastAPI(title="HTTT07", lifespan=lifespan)


@app.get("/health/db")
async def db_health(session: AsyncSession = Depends(get_db)) -> dict[str, str]:
    await session.execute(text("SELECT 1"))
    return {"status": "ok"}


if __name__ == "__main__":
    import asyncio

    import uvicorn

    # Psycopg async requires a selector event loop on Windows.
    server = uvicorn.Server(uvicorn.Config(app, host="127.0.0.1", port=8000))
    asyncio.run(server.serve(), loop_factory=asyncio.SelectorEventLoop)
