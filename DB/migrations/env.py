"""Chạy migration Alembic bằng SQLAlchemy AsyncEngine.

1. Nạp DATABASE_URL từ môi trường; nhập BE/app/models và gán Base.metadata cho target_metadata.
2. Viết do_run_migrations(connection) gọi Alembic context trên kết nối đồng bộ do run_sync cấp.
3. Viết async def run_async_migrations(): tạo async_engine_from_config(), async with connect(), await connection.run_sync(do_run_migrations), await dispose().
4. Viết run_migrations_online() gọi asyncio.run(run_async_migrations()); kiểm tra đường import BE từ thư mục gốc.
"""
