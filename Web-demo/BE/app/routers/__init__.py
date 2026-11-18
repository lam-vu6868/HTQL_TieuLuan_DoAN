from fastapi import APIRouter

from app.routers import demo

api_router = APIRouter(prefix="/api")
api_router.include_router(demo.router)