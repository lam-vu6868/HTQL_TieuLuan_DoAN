# HTTT07 — Kế hoạch triển khai

Triển khai theo 5 chặng. Mỗi chặng có kết quả có thể chạy hoặc kiểm tra trước khi chuyển tiếp. Frontend dùng **ReactJS**, backend dùng **FastAPI theo OOP** và **JWT**. Cơ sở dữ liệu dùng **PostgreSQL đã cài trên máy phát triển**.

Tài liệu đối chiếu gồm [phân tích nghiệp vụ](01-phan-tich-nghiep-vu.md) và [sáu sơ đồ UML](02-so-do-uml.md).

| Chặng | Việc chính | Đầu ra |
| --- | --- | --- |
| 1 | Thiết lập môi trường và thiết kế dữ liệu | React gọi được FastAPI. FastAPI kết nối được PostgreSQL. Có ERD và migration nền. |
| 2 | Tài khoản, phân quyền và dữ liệu lớp | Quản lý cấp tài khoản, gán giảng viên và xếp sinh viên vào lớp. |
| 3 | Tiểu luận | Demo đăng ký, duyệt, nộp báo cáo theo mốc và chấm Tiểu luận. |
| 4 | Đồ án tốt nghiệp | Demo chọn người hướng dẫn, duyệt, nộp báo cáo, ghi lịch bảo vệ và nhập điểm hội đồng. |
| 5 | Kiểm thử và chuẩn bị nộp | Hai luồng chạy qua giao diện. README có đủ bước để người khác tự chạy demo. |

## Chặng 1 — Môi trường và thiết kế dữ liệu

- [ ] Khởi tạo thư mục `backend/` và `frontend/`. Tạo môi trường Python và dự án ReactJS. Tạo cơ sở dữ liệu phát triển `httt07` trên PostgreSQL local và cấu hình kết nối qua biến môi trường.
- [ ] Vẽ ERD từ nghiệp vụ. Chốt bảng, khóa chính, khóa ngoại và ràng buộc cho tài khoản, lớp học phần, nhóm, hồ sơ, mốc nộp, bài nộp, bảo vệ và kết quả. Xác định cách lưu hai loại hồ sơ trước khi viết migration.
- [ ] Tạo migration nền và một API kiểm tra chạy thử. Kết nối một màn hình React với API để kiểm tra đường đi từ trình duyệt đến backend. Kiểm tra kết nối cơ sở dữ liệu riêng.
- [ ] Tổ chức backend sao cho route nhận yêu cầu, lớp nghiệp vụ kiểm tra quy tắc, và lớp truy cập dữ liệu đọc hoặc ghi PostgreSQL. Đối chiếu với trách nhiệm của các lớp trong sơ đồ UML.

**Đạt chặng khi** migration chạy được trên database trống, FastAPI đọc được PostgreSQL và React hiển thị phản hồi từ API.

## Chặng 2 — Tài khoản, phân quyền và lớp học phần

- [ ] Tạo dữ liệu demo cho Quản lý, Giảng viên và Sinh viên. Làm chức năng Quản lý cấp tài khoản và API đăng nhập bằng JWT.
- [ ] Làm chức năng quản lý môn, lớp học phần, giảng viên phụ trách và danh sách sinh viên. Màn hình Sinh viên hiển thị lớp đang học. Màn hình Giảng viên hiển thị lớp được phân công.
- [ ] Kiểm tra quyền ở API theo vai trò và theo từng đối tượng. Quyền Nhóm trưởng được xác định theo nhóm, cùng với tư cách tài khoản Sinh viên.

**Đạt chặng khi** ba vai trò đăng nhập được và thấy đúng dữ liệu. Sinh viên ngoài lớp và giảng viên ngoài phạm vi phân công bị chặn khi truy cập API của lớp.

## Chặng 3 — Tiểu luận theo lớp học phần

- [ ] Giảng viên cấu hình thời gian đăng ký, giới hạn thành viên tối thiểu và tối đa, đề tài có sẵn và mốc nộp. Sinh viên chọn đề tài có sẵn hoặc tự đề xuất.
- [ ] Hỗ trợ đăng ký cá nhân và đăng ký nhóm theo cấu hình. Kiểm tra thành viên cùng lớp, mỗi sinh viên tham gia tối đa một nhóm trong lớp và nhóm trưởng được tính vào sĩ số. Chỉ nhóm trưởng gửi hồ sơ và nộp bài thay mặt nhóm.
- [ ] Lưu hồ sơ chờ duyệt và chuyển đến giảng viên phụ trách lớp. Hỗ trợ duyệt hoặc từ chối kèm lý do. Khi được duyệt, hồ sơ có thể nộp file báo cáo theo từng mốc.
- [ ] Giảng viên xem file, ghi nhận xét, nhập điểm cuối và xem thống kê đạt, không đạt, chưa chấm theo số sinh viên. Kết nối màn hình React cho các bước này với API.

**Đạt chặng khi** sinh viên làm cá nhân và nhóm hợp lệ đều đi được từ đăng ký đến kết quả trên React. Nhóm thiếu người, hồ sơ chưa duyệt và giảng viên ngoài lớp bị chặn ở thao tác tương ứng.

## Chặng 4 — Đồ án tốt nghiệp cá nhân

- [ ] Quản lý tạo đợt đồ án và kế hoạch nộp. Sinh viên chọn đợt, giảng viên hướng dẫn và đề tài có sẵn hoặc tự đề xuất. Mỗi hồ sơ đứng tên một sinh viên.
- [ ] Chuyển hồ sơ đến giảng viên được chọn. Khi duyệt, ghi nhận người hướng dẫn. Dùng lại phần xử lý file và mốc nộp, đồng thời kiểm tra quyền riêng của luồng Đồ án.
- [ ] Sinh viên nộp báo cáo theo mốc và báo cáo cuối. Giảng viên hướng dẫn nhận xét tiến độ. Quản lý ghi lịch, hội đồng và phân công người nhập điểm bảo vệ.
- [ ] Người được phân công nhập điểm tổng hợp của hội đồng. Sinh viên xem kết quả và Quản lý xem thống kê theo đợt. Kết nối các màn hình React với API.

**Đạt chặng khi** một sinh viên đi được từ chọn giảng viên hướng dẫn đến xem điểm bảo vệ. API từ chối xét duyệt bởi giảng viên khác và từ chối nhập điểm khi người dùng chưa được phân công.

## Chặng 5 — Kiểm thử và chuẩn bị nộp

- [ ] Chạy lại hai luồng qua giao diện với dữ liệu demo mới. Kiểm tra các nhánh từ chối hồ sơ, vượt sĩ số, sai người duyệt, nộp sai mốc và nhập điểm sai quyền. Kiểm tra các ca nộp trễ và điểm sát ngưỡng theo quy định đã chốt.
- [ ] Đối chiếu thống kê với danh sách sinh viên. Nếu áp dụng điểm chung, nhóm 4 người đạt được tính là 4 sinh viên đạt.
- [ ] Cập nhật README với các bước chuẩn bị PostgreSQL local, cấu hình môi trường, chạy migration, tạo dữ liệu demo và khởi động backend, frontend.
- [ ] Đối chiếu bốn loại sơ đồ bắt buộc với nghiệp vụ đã triển khai. Chuẩn bị một kịch bản demo Tiểu luận theo nhóm và một kịch bản demo Đồ án cá nhân.

**Đạt chặng khi** người khác có thể làm theo README để chạy hệ thống, đăng nhập và demo cả hai luồng với dữ liệu mẫu.

## Quyết định cần xác nhận

| Quyết định | Mốc cần xác nhận |
| --- | --- |
| Ngưỡng đạt và cách xử lý nộp trễ của từng luồng | Trước khi triển khai nộp bài và thống kê |
| Tiểu luận nhóm dùng điểm chung hay có điểm riêng từng thành viên | Trước khi chốt cách lưu kết quả trong ERD. Phương án hiện tại là điểm chung. |
| Ai được phân công nhập điểm bảo vệ | Trước khi triển khai phần bảo vệ. Phương án hiện tại là Quản lý chỉ định giảng viên nhập điểm tổng hợp của hội đồng. |
| Có thêm nhánh yêu cầu chỉnh sửa đề tài và gửi lại hay không | Sau khi luồng duyệt hoặc từ chối đã chạy ổn định |
