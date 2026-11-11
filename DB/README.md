# Cơ sở dữ liệu (DB)

Thư mục này dành cho migration PostgreSQL và dữ liệu demo. Thiết kế 17 bảng và ràng buộc nằm trong [file 04](../04-thiet-ke-co-so-du-lieu.md). Hiện đây là **bộ khung**, chưa có migration hay dữ liệu mẫu chạy được.

## Quan hệ với BE

- Model ánh xạ bảng nằm trong `BE/app/models/`; chúng là nguồn cấu trúc cho Alembic.
- `migrations/env.py` sẽ nhập metadata từ các model và đọc `DATABASE_URL` từ cấu hình môi trường của BE.
- `migrations/versions/` giữ các bản thay đổi schema theo thứ tự. Không sửa migration đã áp dụng lên database có dữ liệu.
- `seeds/demo.sql` chỉ dành cho dữ liệu demo; không ghi mật khẩu thật vào file này.
- File báo cáo nằm ở `BE/storage/reports/`, không nằm trong PostgreSQL.

## Thứ tự làm khi triển khai

1. Tạo database PostgreSQL `httt07` trên máy phát triển.
2. Hoàn thiện model BE, `alembic.ini` và `migrations/env.py`; tạo migration đầu tiên cho 17 bảng.
3. Chạy migration trên database trống, kiểm tra khóa ngoại, chỉ mục duy nhất có điều kiện và các ràng buộc trong file 04.
4. Thêm dữ liệu mẫu rồi kiểm tra hai luồng qua API và FE. Ghi lệnh chạy chính xác tại đây sau khi chọn công cụ và phiên bản gói.
