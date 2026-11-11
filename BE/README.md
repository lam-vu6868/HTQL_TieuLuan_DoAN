# Backend (BE)

Thư mục này dành cho API FastAPI **bất đồng bộ** của hệ thống Tiểu luận và Đồ án tốt nghiệp. Hiện đây là **bộ khung**, các file Python chỉ mô tả trách nhiệm, chưa có API chạy được.

Mở đầu mỗi file Python là danh sách lớp/hàm dự kiến và các bước cần làm trong chính file đó. Đây là hướng dẫn triển khai, chưa phải mã chức năng.

## Luồng xử lý

`routers` dùng `async def` nhận HTTP và kiểm tra dữ liệu → `services` dùng `async def` xử lý nghiệp vụ, quyền và giao dịch → `repositories` dùng `AsyncSession` đọc/ghi qua `models`. Gọi truy vấn bằng `await`; mỗi request có session riêng. `schemas` định nghĩa dữ liệu API nhận và trả. Hai router `essay.py` và `thesis.py` cùng gọi service đăng ký; service kiểm tra quy tắc riêng theo loại hồ sơ.

## Thứ tự triển khai

1. Cài các gói trong `requirements.txt`; tạo `.env` từ `.env.example`, không đưa `.env` lên Git.
2. Hoàn thiện `config.py`, `database.py`, `models/` rồi tạo migration trong `DB/migrations/`.
3. Làm đăng nhập JWT và kiểm tra quyền, sau đó triển khai các chức năng lớp, nhóm, đăng ký, nộp bài và kết quả theo `03-ke-hoach-trien-khai.md` ở thư mục gốc.
4. Thêm kiểm thử cho các nhánh quan trọng trong `tests/`. Khi đã có mã chạy, ghi lệnh khởi động cụ thể tại đây.

File báo cáo nằm ở `storage/reports/`; database chỉ giữ đường dẫn và thông tin bài nộp. Khi viết API tải file, kiểm tra người dùng có quyền xem đúng hồ sơ trước khi trả nội dung.

## Cài thư viện trên Windows (PowerShell)

Chạy tại thư mục gốc dự án bằng Python 3.12:

```powershell
py -3.12 -m venv BE\venv
.\BE\venv\Scripts\python.exe -m pip install -r BE\requirements.txt
Copy-Item BE\.env.example BE\.env
```

Nếu `BE/venv` đã tồn tại, bỏ qua lệnh tạo môi trường và chạy lại lệnh cài requirements để nhận extra `SQLAlchemy[asyncio]` (bao gồm `greenlet`). Sửa `DATABASE_URL` và `JWT_SECRET` trong `BE/.env` cho máy của bạn. URL `postgresql+psycopg://...` dùng được với `create_async_engine()`; SQLAlchemy chọn bản async của psycopg. Nếu `py -3.12` không có, dùng `python -m venv BE\venv` khi `python --version` là 3.12. Cùng môi trường `BE/venv` này sẽ chạy Alembic của thư mục `DB` sau khi migration được viết.

Tham khảo [SQLAlchemy asyncio](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html) khi viết session và repository.
