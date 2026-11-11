# Cơ sở dữ liệu (DB)

Thư mục này dành cho migration PostgreSQL và dữ liệu demo. Thiết kế 17 bảng và ràng buộc nằm trong [file 04](../04-thiet-ke-co-so-du-lieu.md). Hiện đây là **bộ khung**, chưa có migration hay dữ liệu mẫu chạy được.

## Quan hệ với BE

- Model ánh xạ bảng nằm trong `BE/app/models/`; chúng là nguồn cấu trúc cho Alembic.
- `migrations/env.py` sẽ nhập metadata từ các model, đọc `DATABASE_URL` của BE và chạy migration qua AsyncEngine cùng `connection.run_sync()`.
- `migrations/versions/` giữ các bản thay đổi schema theo thứ tự. Không sửa migration đã áp dụng lên database có dữ liệu.
- `seeds/demo.sql` chỉ dành cho dữ liệu demo; không ghi mật khẩu thật vào file này.
- File báo cáo nằm ở `BE/storage/reports/`, không nằm trong PostgreSQL.

## Cài thư viện

DB dùng chung môi trường Python và [requirements.txt của BE](../BE/requirements.txt). Từ thư mục gốc dự án, chạy lệnh cài trong [BE/README.md](../BE/README.md); không cần cài một bộ thư viện Python thứ hai. `psycopg[binary]` hỗ trợ kết nối async với SQLAlchemy; Alembic dùng AsyncEngine và cầu nối `run_sync()` để chạy migration. PostgreSQL **server** là phần mềm cài riêng trên máy, không được cài qua pip.

Tham khảo [Alembic async cookbook](https://alembic.sqlalchemy.org/en/latest/cookbook.html#using-asyncio-with-alembic) khi hoàn thiện `migrations/env.py`.

## Thứ tự làm khi triển khai

1. Tạo database PostgreSQL `httt07` trên máy phát triển.
2. Hoàn thiện model BE, `alembic.ini` và `migrations/env.py`; tạo migration đầu tiên cho 17 bảng.
3. Chạy migration trên database trống, kiểm tra khóa ngoại, chỉ mục duy nhất có điều kiện và các ràng buộc trong file 04.
4. Thêm dữ liệu mẫu rồi kiểm tra hai luồng qua API và FE. Ghi lệnh chạy migration và nạp dữ liệu tại đây sau khi các file đó hoàn chỉnh.
