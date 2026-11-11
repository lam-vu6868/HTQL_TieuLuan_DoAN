"""Cấu hình môi trường của BE.

1. Tạo lớp Settings chứa DATABASE_URL và JWT_SECRET; kiểm tra giá trị bắt buộc.
2. Tạo get_settings() để các phần khác dùng cùng một cấu hình.
3. Đọc .env khi chạy local; không ghi mật khẩu hoặc khóa thật vào mã nguồn.
"""
