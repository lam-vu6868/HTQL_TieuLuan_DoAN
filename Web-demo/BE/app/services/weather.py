import time
from datetime import datetime

import httpx

from app.schemas.weather import OpenMeteoResponse, WeatherRead

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

# key -> (tên hiển thị, vĩ độ, kinh độ)
CITIES = {
    "ho-chi-minh": ("TP. Hồ Chí Minh", 10.82, 106.63),
    "binh-duong": ("Bình Dương", 10.99, 106.65),
    "ha-noi": ("Hà Nội", 21.03, 105.85),
    "da-nang": ("Đà Nẵng", 16.05, 108.20),
}


def describe(code: int) -> str:
    """Mã thời tiết WMO -> mô tả tiếng Việt (gộp nhóm cho gọn)."""
    if code == 0:
        return "Trời quang"
    if code in (1, 2, 3):
        return "Có mây"
    if code in (45, 48):
        return "Sương mù"
    if 51 <= code <= 57:
        return "Mưa phùn"
    if 61 <= code <= 67 or 80 <= code <= 82:
        return "Mưa"
    if 71 <= code <= 77:
        return "Tuyết"
    if code >= 95:
        return "Dông"
    return "Không xác định"


def _mock(name: str, reason: str, start: float) -> WeatherRead:
    return WeatherRead(
        city=name,
        temperature_c=30.0,
        humidity_percent=70,
        wind_kmh=10.0,
        description="Có mây (dữ liệu giả lập)",
        observed_at=datetime.now(),
        source="mock",
        fallback_reason=reason,
        elapsed_ms=int((time.perf_counter() - start) * 1000),
    )


async def fetch_weather(city_key: str, force_mock: bool = False) -> WeatherRead:
    name, lat, lon = CITIES[city_key]
    start = time.perf_counter()

    if force_mock:
        return _mock(name, "Bật chế độ giả lập", start)

    try:
        # await: trong lúc chờ mạng, event loop rảnh để phục vụ request khác
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(
                OPEN_METEO_URL,
                params={
                    "latitude": lat,
                    "longitude": lon,
                    "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
                    "timezone": "auto",
                },
            )
            resp.raise_for_status()

        data = OpenMeteoResponse.model_validate(resp.json())  # JSON -> object
        cur = data.current
        return WeatherRead(
            city=name,
            temperature_c=cur.temperature_2m,
            humidity_percent=cur.relative_humidity_2m,
            wind_kmh=cur.wind_speed_10m,
            description=describe(cur.weather_code),
            observed_at=cur.time,
            source="open-meteo",
            elapsed_ms=int((time.perf_counter() - start) * 1000),
        )
    except httpx.TimeoutException:          # phải đặt trước HTTPError (lớp cha)
        reason = "Quá thời gian chờ (5s)"
    except httpx.HTTPError as e:
        reason = f"Lỗi mạng/HTTP: {type(e).__name__}"
    except ValueError:                      # JSON hỏng hoặc Pydantic báo sai định dạng
        reason = "Dữ liệu trả về sai định dạng"

    return _mock(name, reason, start)