"""Entrypoint chạy seed data.

Usage:
    python seed.py
"""
import asyncio

from app.core.asyncio_compat import apply_windows_selector_loop

# Phải gọi TRƯỚC khi import app.core.database (engine) và TRƯỚC asyncio.run().
apply_windows_selector_loop()

from app.core.database import AsyncSessionLocal 
from app.seed import run_seed 


async def _main() -> None:
    async with AsyncSessionLocal() as db:
        await run_seed(db)


if __name__ == "__main__":
    asyncio.run(_main())