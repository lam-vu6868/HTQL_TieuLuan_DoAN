"""Kết nối Alembic với model BE và PostgreSQL.

1. Nạp DATABASE_URL từ cấu hình môi trường, không ghi URL thật vào alembic.ini.
2. Nhập toàn bộ BE/app/models rồi gán Base.metadata cho target_metadata.
3. Viết run_migrations_online(); dùng kết nối và transaction của Alembic.
4. Kiểm tra đường import BE khi chạy Alembic từ thư mục gốc dự án.
"""
