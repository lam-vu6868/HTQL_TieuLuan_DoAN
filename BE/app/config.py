"""Cấu hình môi trường của BE.

1. Tạo lớp Settings chứa DATABASE_URL, JWT_SECRET và cấu hình SMTP/địa chỉ FE cho email đặt lại mật khẩu.
2. Tạo get_settings() để các phần khác dùng cùng một cấu hình.
3. URL postgresql+psycopg:// dùng với create_async_engine() sẽ chọn driver async.
4. Đọc .env khi chạy local; kiểm tra giá trị bắt buộc và không ghi mật khẩu hoặc khóa thật vào mã nguồn.
"""
