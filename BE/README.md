# Backend (BE)

Thư mục này dành cho API FastAPI của hệ thống Tiểu luận và Đồ án tốt nghiệp. Hiện đây là **bộ khung**, các file Python chỉ mô tả trách nhiệm, chưa có API chạy được.

Mở đầu mỗi file Python là danh sách lớp/hàm dự kiến và các bước cần làm trong chính file đó. Đây là hướng dẫn triển khai, chưa phải mã chức năng.

## Luồng xử lý

`routers` nhận yêu cầu HTTP và kiểm tra dữ liệu → `services` xử lý nghiệp vụ, quyền và giao dịch → `repositories` đọc/ghi qua `models`. `schemas` định nghĩa dữ liệu API nhận và trả. Hai router `essay.py` và `thesis.py` cùng gọi service đăng ký; service kiểm tra quy tắc riêng theo loại hồ sơ.

## Thứ tự triển khai

1. Điền các gói thực sự dùng vào `requirements.txt`; tạo `.env` từ `.env.example`, không đưa `.env` lên Git.
2. Hoàn thiện `config.py`, `database.py`, `models/` rồi tạo migration trong `DB/migrations/`.
3. Làm đăng nhập JWT và kiểm tra quyền, sau đó triển khai các chức năng lớp, nhóm, đăng ký, nộp bài và kết quả theo `03-ke-hoach-trien-khai.md` ở thư mục gốc.
4. Thêm kiểm thử cho các nhánh quan trọng trong `tests/`. Khi đã có mã chạy, ghi lệnh cài đặt và khởi động cụ thể tại đây.

File báo cáo nằm ở `storage/reports/`; database chỉ giữ đường dẫn và thông tin bài nộp. Khi viết API tải file, kiểm tra người dùng có quyền xem đúng hồ sơ trước khi trả nội dung.
