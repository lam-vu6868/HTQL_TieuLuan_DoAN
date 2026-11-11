"""Gói truy vấn PostgreSQL.

1. Mỗi repository nhận session từ service và trả dữ liệu cần thiết.
2. Không commit riêng trong repository khi service đang xử lý một giao dịch nhiều bước.
"""
