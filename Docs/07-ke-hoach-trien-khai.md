## Danh sách module (theo thứ tự phụ thuộc)

| #   | Module            | Nội dung chính                                                                              | Phụ thuộc | Cỡ  |
| --- | ----------------- | ------------------------------------------------------------------------------------------- | --------- | --- |
| M0  | Nền móng          | Chốt quy ước tên tiếng Anh, models 14 bảng, repository, Alembic, seed dữ liệu mẫu           | không     | L   |
| M1  | Xác thực          | login, me, refresh, logout, phân quyền theo vai trò; FE: trang đăng nhập, axios interceptor | M0        | M   |
| M2  | Quản lý học vụ    | Tạo tài khoản, môn, lớp, phân công GV, ghi danh SV, đợt Đồ án                               | M1        | M   |
| M3  | Đăng ký Tiểu luận | Nhóm (thêm thành viên, chuyển trưởng nhóm), hồ sơ đề tài, duyệt, cấu hình lớp               | M2        | L   |
| M4  | Đăng ký Đồ án     | Đợt mở, chọn GV, duyệt và tạo phân công GVHD (dùng lại `RegistrationService` của M3)        | M3        | M   |
| M5  | Nộp bài và mốc    | Đặt mốc Đồ án, nộp/thay file, cờ nộp trễ, tải file                                          | M3, M4    | L   |
| M6  | Nhận xét và điểm  | Nhận xét, nhập điểm (chung/riêng), công bố, thống kê, ngưỡng đạt                            | M5        | L   |
| M7  | Quên mật khẩu     | Token reset, gửi email SMTP                                                                 | M1        | S   |
| M8  | Hoàn thiện        | Docker, test chính, README tổng, demo                                                       | tất cả    | M   |

## Chi tiết M0 và M1

**M0 – Nền móng**

- [x] Chốt bảng đối chiếu tên cũ → mới (`han_nop`→`due_date`, `che_do_cham`→`grading_mode`, `CHO_DUYET`→`PENDING`...), dùng cho cả code lẫn tài liệu 01–04
- [x] Bê ORM models + repository của bạn nhóm vào thư mục mới, đổi tên theo bảng đối chiếu
- [x] Alembic migration đầu tiên, chạy được trên PostgreSQL trong Docker
- [x] Script seed: 1 admin, 2 giảng viên, vài sinh viên, 1 lớp
- [x] `/health/db` vẫn chạy

**M1 – Xác thực**

- [x] Bảng `refresh_tokens` (lưu hash, hạn, `revoked`), tách khỏi bảng reset mật khẩu
- [ ] `security.py`: hash mật khẩu, tạo/giải mã access token
- [ ] `POST /auth/login`: trả access token trong body, đặt refresh token vào cookie httpOnly
- [ ] `POST /auth/refresh`, `POST /auth/logout`, `GET /auth/me`
- [ ] Dependency `require_role(...)` dùng cho các router sau
- [ ] FE: `AuthContext` (access token trong `useState`), axios interceptor tự gọi refresh khi nhận 401
