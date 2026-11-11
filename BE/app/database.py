"""Kết nối PostgreSQL bất đồng bộ và phiên giao dịch.

1. Tạo Base chung cho ORM; dùng create_async_engine(Settings.DATABASE_URL).
2. Tạo async_sessionmaker(..., expire_on_commit=False) cấp AsyncSession theo request.
3. Viết async def get_db(): mở/đóng session bằng async with; không chia sẻ session giữa request.
4. Service await commit()/rollback() cho thao tác nhiều bước; kiểm tra SELECT 1 bằng await session.execute().
"""
