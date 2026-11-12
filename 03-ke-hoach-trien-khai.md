# HTTT07 — Kế hoạch triển khai bản đầu

Nhóm hai người làm luồng chạy được trước: **đăng ký → duyệt → nộp → chấm → Quản lý công bố → sinh viên xem**. Frontend ReactJS; Backend FastAPI async theo OOP và JWT; PostgreSQL. Đối chiếu [nghiệp vụ](01-phan-tich-nghiep-vu.md), [UML](02-so-do-uml.md) và [CSDL 14 bảng](04-thiet-ke-co-so-du-lieu.md).

## Chặng 1 — Nền tảng và CSDL

- [ ] Tạo ứng dụng React, FastAPI async, PostgreSQL local; cấu hình `DATABASE_URL` và JWT qua `.env`.
- [ ] Viết model của 14 bảng và migration Alembic. Kiểm tra `AsyncSession` đọc được dữ liệu; Alembic dùng `AsyncEngine` với `run_sync()`.
- [ ] Tạo dữ liệu demo: tài khoản Quản lý/Giảng viên/Sinh viên, lớp, đợt, phân công GVHD.

**Đạt khi:** migration chạy trên CSDL trống và một trang React đọc được API kết nối PostgreSQL.

## Chặng 2 — Đăng nhập, lớp và phân công

- [ ] Quản lý cấp tài khoản, tạo môn/lớp/đợt, gán giảng viên lớp, xếp sinh viên vào lớp và gán GVHD theo sinh viên/đợt.
- [ ] Làm đăng nhập JWT và email đặt lại mật khẩu một lần, có hạn dùng; kiểm tra quyền theo vai trò và đối tượng. Sinh viên xem lớp/đợt của mình; giảng viên xem lớp và phân công của mình.

**Đạt khi:** cả ba vai trò đăng nhập và chỉ xem được lớp, đợt hoặc phân công thuộc quyền của mình.

## Chặng 3 — Đăng ký và duyệt đề tài

- [ ] Tiểu luận: cấu hình hạn đăng ký, hạn nộp, giới hạn nhóm và chế độ chấm `CHUNG`/`RIENG`; cho làm cá nhân hoặc tạo nhóm, thêm sinh viên cùng lớp bằng mã, chuyển trưởng nhóm.
- [ ] Đồ án: Quản lý gán GVHD trước; sinh viên tự nhập tên/mô tả đề tài và gửi đúng GVHD. Không làm kho đề tài gợi ý.
- [ ] Hai luồng: giảng viên duyệt hoặc từ chối kèm lý do; cho sửa hồ sơ cũ hoặc tạo hồ sơ mới trong hạn. Xem đề tài đã đăng ký để tự kiểm tra trùng, không ép tên duy nhất.

**Đạt khi:** hồ sơ hai luồng đi từ gửi đến duyệt/từ chối; gửi sai quyền, quá hạn đăng ký, nhóm vượt sĩ số hoặc sai GVHD bị chặn; giảng viên khác lớp hoặc khác phân công GVHD không thể xét hồ sơ.

## Chặng 4 — Nộp, chấm và công bố

- [ ] Tiểu luận có một hạn nộp; GVHD đặt mốc trung gian và mốc cuối cho từng sinh viên được phân công. Cho nộp/thay file vào `BE/storage/reports/`, chỉ lưu đường dẫn nội bộ trong PostgreSQL; nhận cả nộp trễ và đánh dấu `nop_tre`.
- [ ] Giảng viên nhận xét. Tiểu luận chấm chung hoặc chấm riêng theo cấu hình lớp; lưu một dòng điểm cho mỗi sinh viên. GVHD nhập điểm Đồ án ở mốc cuối.
- [ ] Quản lý công bố khi hồ sơ đủ điểm; sinh viên chỉ xem điểm của mình đã công bố. Tính thống kê đạt/không đạt/chưa chấm theo sinh viên, ngưỡng mặc định 4,0; GV lớp chỉnh ngưỡng lớp, GVHD chỉnh ngưỡng hồ sơ Đồ án trước công bố.

**Đạt khi:** hai luồng chạy qua giao diện từ đăng ký đến kết quả; chỉ người có quyền với hồ sơ tải được file và điểm chưa công bố không lộ ra API sinh viên.

## Chặng 5 — Kiểm tra và nộp bài

- [ ] Kiểm tra cá nhân/nhóm, thêm thành viên sai lớp, chuyển trưởng nhóm sai quyền, sửa/tạo mới sau từ chối, nộp trễ, thay file và quyền xem điểm.
- [ ] Kiểm tra cả `CHUNG` và `RIENG`: nhóm bốn người có bốn dòng điểm; thống kê đếm bốn sinh viên. Kiểm tra điểm dưới/trên ngưỡng và trường hợp chưa chấm.
- [ ] Đối chiếu bốn loại UML với code đã viết. Viết lệnh chạy BE, FE, migration và dữ liệu demo trong README.

**Đạt khi:** người khác làm theo README chạy được và demo cả hai luồng.

## Chưa làm trong bản đầu

Kho đề tài gợi ý của giảng viên, quy trình mời/xác nhận nhóm, hội đồng và lịch bảo vệ trong hệ thống. Các thầy có thể thống nhất điểm Đồ án bên ngoài; GVHD được gán là người nhập điểm. Nếu giảng viên môn học xác nhận hội đồng/lịch là bắt buộc, phải bổ sung trước khi nộp.
