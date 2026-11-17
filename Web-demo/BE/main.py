from fastapi import FastAPI

from app.routers import api_router
from app.routers.health import router as health_router

app = FastAPI(title="HTTT07 - Demo Async")

app.include_router(health_router)   # /health
app.include_router(api_router)      # /api/...