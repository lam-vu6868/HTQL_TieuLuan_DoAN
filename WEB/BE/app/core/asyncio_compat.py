"""
Fix tương thích event loop cho psycopg async trên Windows.

Windows mặc định dùng ProactorEventLoop, nhưng psycopg (async driver
cho PostgreSQL) chỉ hoạt động với SelectorEventLoop. Phải gọi
apply_windows_selector_loop() TRƯỚC khi:
  - bất kỳ kết nối DB nào được mở
  - asyncio.run() / uvicorn.run() được gọi

Trên Linux/macOS hàm này là no-op (đã mặc định là SelectorEventLoop).
"""
import asyncio
import sys


def apply_windows_selector_loop() -> None:
    """Buộc asyncio dùng SelectorEventLoop trên Windows."""
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())