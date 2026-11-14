# HTTT07 — Quản lý đề tài Tiểu luận và Đồ án tốt nghiệp

Dự án dùng ReactJS (`FE`), FastAPI async theo OOP (`BE`) và PostgreSQL (`DB`). File báo cáo lưu trên máy chủ BE tại `BE/storage/reports/`; PostgreSQL chỉ giữ thông tin bài nộp và đường dẫn nội bộ. **Hiện mới có tài liệu và bộ khung BE/DB; chưa có ứng dụng hoặc migration chạy được.**

## Tài liệu

- [Phân tích nghiệp vụ](01-phan-tich-nghiep-vu.md): vai trò và hai quy trình.
- [Sơ đồ UML](02-so-do-uml.md): Use Case, Lớp, Tuần tự và Hoạt động.
- [Kế hoạch triển khai](03-ke-hoach-trien-khai.md): thứ tự thực hiện và tiêu chí hoàn thành từng chặng.
- [Thiết kế cơ sở dữ liệu](04-thiet-ke-co-so-du-lieu.md): 14 bảng và ràng buộc PostgreSQL dự kiến.
- [Hướng dẫn làm việc với Git](05-huong-dan-lam-viec-voi-git.md): cách tạo nhánh và ghép công việc của nhóm.

Phạm vi bản đầu: sinh viên tự đề xuất đề tài; với Đồ án, sinh viên chọn giảng viên nhận hồ sơ và khi giảng viên duyệt, hệ thống tự ghi nhận GVHD. GVHD đặt mốc và nhập điểm Đồ án; Tiểu luận chấm chung hoặc riêng từng sinh viên. Nộp trễ được đánh dấu, điểm cần Quản lý duyệt công bố. Hội đồng/lịch bảo vệ và kho đề tài gợi ý để sau.

## Cấu trúc

| Thư mục | Vai trò | Hướng dẫn |
| --- | --- | --- |
| `BE/` | API, nghiệp vụ, truy cập dữ liệu và nơi lưu file báo cáo | [BE/README.md](BE/README.md) |
| `DB/` | Migration PostgreSQL và dữ liệu demo | [DB/README.md](DB/README.md) |
| `FE/` | Giao diện ReactJS; chưa được khởi tạo | Sẽ bổ sung khi làm frontend |

Bước tiếp theo là hoàn thiện kết nối PostgreSQL, model và migration ở chặng 1; sau đó làm đăng nhập và phân quyền ở chặng 2. Khi ứng dụng chạy được, bổ sung lệnh cài đặt và khởi động tại đây.
