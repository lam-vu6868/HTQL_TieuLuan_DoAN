"""Kết nối PostgreSQL và phiên giao dịch.

1. Tạo Base chung cho ORM, engine từ Settings.DATABASE_URL và một session factory.
2. Tạo get_db() cấp session cho router rồi đóng session sau request.
3. Service quyết định commit/rollback cho thao tác nhiều bước; kiểm tra SELECT 1 ở chặng 1.
"""
