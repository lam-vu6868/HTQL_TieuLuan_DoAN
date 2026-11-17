# Backend (BE)

Thư mục này dành cho API FastAPI **bất đồng bộ** của hệ thống Tiểu luận và Đồ án tốt nghiệp. Kết nối PostgreSQL, endpoint kiểm tra DB và model 14 bảng đã chạy; các API nghiệp vụ vẫn là bộ khung.

Phạm vi bản đầu: sinh viên tự đề xuất đề tài; với Đồ án, sinh viên chọn giảng viên nhận hồ sơ và khi giảng viên duyệt, hệ thống tự ghi nhận GVHD. Tiểu luận có một hạn nộp và chấm chung/riêng; GVHD đặt mốc Đồ án cho từng sinh viên được phân công rồi nhận xét, nhập điểm. Nộp trễ vẫn nhận, Quản lý duyệt công bố. Có email đặt lại mật khẩu; dùng `smtplib` của Python qua `asyncio.to_thread()` nên không thêm thư viện mail. Chưa quản lý hội đồng, lịch bảo vệ hoặc lời mời xác nhận nhóm.

Các repository đã có truy vấn ORM; router và service vẫn mô tả chức năng dự kiến, chưa có API nghiệp vụ.

## Luồng xử lý

`routers` dùng `async def` nhận HTTP và kiểm tra dữ liệu → `services` dùng `async def` xử lý nghiệp vụ, quyền và giao dịch → `repositories` dùng `AsyncSession` đọc/ghi qua `models`. Gọi truy vấn bằng `await`; mỗi request có session riêng. `schemas` định nghĩa dữ liệu API nhận và trả. Hai router `essay.py` và `thesis.py` cùng gọi service đăng ký; service kiểm tra quy tắc riêng theo loại hồ sơ.

## Thứ tự triển khai

1. Cài các gói trong `requirements.txt`; tạo `.env` từ `.env.example`, không đưa `.env` lên Git.
2. Chạy migration trong `BE/alembic/` để tạo 14 bảng.
3. Làm đăng nhập JWT và kiểm tra quyền, sau đó triển khai các chức năng lớp, nhóm, đăng ký, nộp bài và kết quả theo `03-ke-hoach-trien-khai.md` ở thư mục gốc.
4. Thêm kiểm thử cho các nhánh quan trọng trong `tests/`. Khi đã có mã chạy, ghi lệnh khởi động cụ thể tại đây.

File báo cáo nằm ở `storage/reports/`; database chỉ giữ đường dẫn và thông tin bài nộp. Khi viết API tải file, kiểm tra người dùng có quyền xem đúng hồ sơ trước khi trả nội dung.

## Cài thư viện trên Windows (PowerShell)

Chạy tại thư mục gốc dự án bằng Python 3.12:

```powershell
docker compose up -d postgres
py -3.12 -m venv BE\venv
.\BE\venv\Scripts\python.exe -m pip install -r BE\requirements.txt
if (-not (Test-Path BE\.env)) { Copy-Item BE\.env.example BE\.env }
```

Compose tạo database `httt07` trên cổng `5434` và giữ dữ liệu trong Docker volume. Mật khẩu mặc định `httt07_dev` chỉ dành cho máy phát triển; nếu đổi bằng biến môi trường `POSTGRES_PASSWORD`, hãy cập nhật mật khẩu trong `BE/.env` cho khớp trước khi chạy backend. Nếu `BE/venv` đã tồn tại, bỏ qua lệnh tạo môi trường và chạy lại lệnh cài requirements để nhận extra `SQLAlchemy[asyncio]` (bao gồm `greenlet`). Sửa `DATABASE_URL` và `JWT_SECRET` trong `BE/.env` cho máy của bạn. URL `postgresql+psycopg://...` dùng được với `create_async_engine()`; SQLAlchemy chọn bản async của psycopg. Nếu `py -3.12` không có, dùng `python -m venv BE\venv` khi `python --version` là 3.12. Cùng môi trường `BE/venv` này chạy Alembic trong `BE/alembic/`.

Tham khảo [SQLAlchemy asyncio](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html) khi viết session và repository.

## Kiểm tra kết nối PostgreSQL

Sau khi chạy `docker compose up -d postgres`, mở terminal trong `BE` và chạy:

```powershell
.\venv\Scripts\python.exe -m app.main
```

Truy cập `http://127.0.0.1:8000/health/db`; kết quả `{"status":"ok"}` xác nhận backend truy vấn được PostgreSQL. Để tạo 14 bảng trên database trống, chạy tại thư mục gốc dự án:

```powershell
.\BE\venv\Scripts\python.exe -m alembic -c BE\alembic.ini upgrade head
```
