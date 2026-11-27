import asyncio
import sys
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

from app.core.config import settings as BackendSetting
from app.models.base import Base
from app import models  # noqa: F401  ← nạp toàn bộ model vào Base.metadata


# ---------------------------------------------------------------------------
# Windows fix: psycopg 3 async không chạy được trên ProactorEventLoop
# (mặc định của Windows từ Python 3.8+). Phải set policy TRƯỚC asyncio.run().
# Đoạn này no-op trên Linux/macOS nên an toàn khi deploy.
# ---------------------------------------------------------------------------
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


# Alembic Config object — truy cập giá trị trong alembic.ini
config = context.config

# Ký tự '%' trong URL bị configparser hiểu là nội suy → phải escape.
config.set_main_option("sqlalchemy.url", BackendSetting.DATABASE_URL)

# Thiết lập logging theo file alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata chứa toàn bộ bảng/cột do model khai báo — autogenerate đọc từ đây.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Chạy migration ở chế độ 'offline': chỉ in SQL ra stdout, không kết nối DB.

    Dùng khi muốn xem trước SQL, hoặc xuất script để DBA chạy tay.
    Không cần DBAPI, không cần driver.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Logic migration thực sự, chạy bên trong sync connection.

    Alembic không hỗ trợ async trực tiếp, nên ta "chuyển" connection
    async thành sync qua `connection.run_sync(...)` ở dưới.
    """
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Tạo async engine và chạy migration trên một connection."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,  # Alembic chạy 1 lần rồi thoát, không cần pool
    )

    async with connectable.connect() as connection:
        # run_sync: chạy hàm sync trong context async của SQLAlchemy
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()  # đóng connection, giải phóng tài nguyên


def run_migrations_online() -> None:
    """Entry point cho chế độ 'online': có kết nối DB thật."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()