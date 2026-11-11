"""Gói truy vấn PostgreSQL.

1. Mỗi repository nhận AsyncSession từ service; viết async def cho truy vấn DB và await execute()/get().
2. Không commit riêng trong repository khi service đang xử lý một giao dịch nhiều bước.
3. Khi cần quan hệ ORM, nạp trước bằng selectinload() trong truy vấn; tránh lazy load ngầm ngoài await.
"""
