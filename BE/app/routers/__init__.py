"""Gói router HTTP.

1. Mỗi module tạo APIRouter và dùng async def cho endpoint gọi DB/service.
2. main.py gọi include_router() cho từng module; không để endpoint ở đây.
"""
