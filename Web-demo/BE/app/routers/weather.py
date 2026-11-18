from fastapi import APIRouter, HTTPException, Query

from app.schemas.weather import WeatherRead
from app.services.weather import CITIES, fetch_weather

router = APIRouter(prefix="/api/weather", tags=["weather"])


@router.get("/current", response_model=WeatherRead)
async def current_weather(
    city: str = Query("ho-chi-minh"),
    force_mock: bool = False,
):
    if city not in CITIES:
        raise HTTPException(status_code=404, detail=f"Không có thành phố '{city}'")
    return await fetch_weather(city, force_mock)