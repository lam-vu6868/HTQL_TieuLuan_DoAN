"""Điểm khởi động API.

1. Tạo biến app = FastAPI(...); cấu hình CORS cho địa chỉ FE khi cần.
2. Gắn các router auth, admin, essay, thesis, submissions, results.
3. Viết async def cho endpoint kiểm tra API/DB ở chặng 1; await truy vấn PostgreSQL.
4. Đóng AsyncEngine khi ứng dụng dừng; không đặt nghiệp vụ ở đây.
"""
