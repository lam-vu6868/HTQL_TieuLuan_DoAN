# HTTT07 — Quản lý đề tài Tiểu luận và Đồ án tốt nghiệp

Dự án dùng ReactJS (`FE`), FastAPI theo OOP (`BE`) và PostgreSQL (`DB`). **Hiện mới có tài liệu và bộ khung BE/DB; chưa có ứng dụng hoặc migration chạy được.**

## Tài liệu

- [Phân tích nghiệp vụ](01-phan-tich-nghiep-vu.md): vai trò và hai quy trình.
- [Sơ đồ UML](02-so-do-uml(1).md): Use Case, Lớp, Tuần tự và Hoạt động.
- [Kế hoạch triển khai](03-ke-hoach-trien-khai.md): thứ tự thực hiện và tiêu chí hoàn thành từng chặng.
- [Thiết kế cơ sở dữ liệu](04-thiet-ke-co-so-du-lieu.md): 17 bảng và ràng buộc PostgreSQL dự kiến.

## Cấu trúc

| Thư mục | Vai trò | Hướng dẫn |
| --- | --- | --- |
| `BE/` | API, nghiệp vụ, truy cập dữ liệu và nơi lưu file báo cáo | [BE/README.md](BE/README.md) |
| `DB/` | Migration PostgreSQL và dữ liệu demo | [DB/README.md](DB/README.md) |
| `FE/` | Giao diện ReactJS; chưa được khởi tạo | Sẽ bổ sung khi làm frontend |

Bước tiếp theo là hoàn thiện kết nối PostgreSQL, model và migration ở chặng 1; sau đó làm đăng nhập và phân quyền ở chặng 2. Khi ứng dụng chạy được, bổ sung lệnh cài đặt và khởi động tại đây.
