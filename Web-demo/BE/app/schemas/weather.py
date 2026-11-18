from datetime import datetime
from typing import Literal

from pydantic import BaseModel


# Chiều NHẬN: khớp JSON của Open-Meteo (trường thừa tự bị bỏ qua)
class OpenMeteoCurrent(BaseModel):
    time: datetime
    temperature_2m: float
    relative_humidity_2m: int
    wind_speed_10m: float
    weather_code: int


class OpenMeteoResponse(BaseModel):
    latitude: float
    longitude: float
    current: OpenMeteoCurrent


# Chiều GỬI: JSON trả cho FE
class WeatherRead(BaseModel):
    city: str
    temperature_c: float
    humidity_percent: int
    wind_kmh: float
    description: str
    observed_at: datetime
    source: Literal["open-meteo", "mock"]
    fallback_reason: str | None = None
    elapsed_ms: int