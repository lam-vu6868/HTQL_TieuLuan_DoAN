# HTTT07 — Phân tích nghiệp vụ

## 1. Mục tiêu và phạm vi

Hệ thống hỗ trợ sinh viên và giảng viên đăng ký đề tài, duyệt đề tài, nộp báo cáo theo kế hoạch, nhận xét, chấm điểm và thống kê số sinh viên đạt. Hệ thống có hai quy trình riêng.

| Quy trình        | Đăng ký theo                                                                           | Người duyệt                       | Người chấm                        |
| ---------------- | -------------------------------------------------------------------------------------- | --------------------------------- | --------------------------------- |
| Tiểu luận        | Lớp học phần sinh viên đang học. Làm cá nhân hoặc theo nhóm tùy giới hạn của lớp.      | Giảng viên phụ trách lớp học phần | Giảng viên phụ trách lớp học phần |
| Đồ án tốt nghiệp | Đợt đồ án và giảng viên hướng dẫn do sinh viên chọn. Mỗi hồ sơ đứng tên một sinh viên. | Giảng viên được chọn hướng dẫn    | Hội đồng bảo vệ                   |

Cả hai quy trình cho phép chọn đề tài có sẵn hoặc tự đề xuất. Bài nộp gồm các sơ đồ Use Case, Lớp, Tuần tự và Hoạt động, RESTful API có xác thực và frontend kết nối với API. Sơ đồ Tuần tự tập trung vào quy trình duyệt đề tài của từng luồng.

## 2. Vai trò và quyền

| Vai trò nghiệp vụ | Quyền và phạm vi                                                                                                                                                                                                                                        |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Sinh viên         | Xem lớp mình đang học và đợt đồ án đang mở. Đăng ký, xác nhận lời mời vào nhóm, nộp báo cáo và xem kết quả đã công bố của hồ sơ cá nhân. Với hồ sơ nhóm, xem đề tài, bài nộp, nhận xét và kết quả đã công bố của nhóm mình.                             |
| Nhóm trưởng       | Có các quyền của Sinh viên. Trong nhóm mình phụ trách, mời thành viên, chuyển quyền trưởng nhóm cho thành viên đã xác nhận, gửi đăng ký và nộp báo cáo thay mặt nhóm.                                                                                   |
| Giảng viên        | Trong lớp được phân công, cấu hình giới hạn nhóm và các mốc nộp, duyệt đề tài, nhận xét, chấm và xem thống kê Tiểu luận. Trong đợt Đồ án tốt nghiệp, xét hồ sơ gửi đến mình và nhận xét hồ sơ đã nhận hướng dẫn. Quyền nhập điểm bảo vệ theo phân công. |
| Quản lý           | Cấp tài khoản, quản lý môn học và lớp học phần, gán giảng viên phụ trách, xếp sinh viên vào lớp, quản lý đợt đồ án, phân công người nhập điểm bảo vệ, xác nhận vắng bảo vệ và duyệt công bố điểm.                                                       |

Tài khoản có ba vai trò là Sinh viên, Giảng viên và Quản lý. Nhóm trưởng là quyền trong từng nhóm. Cùng một sinh viên có thể là nhóm trưởng ở lớp này và là thành viên ở lớp khác. API kiểm tra vai trò và quan hệ với đối tượng đang xử lý.

## 3. Cấp tài khoản, đăng nhập và phân công

1. Quản lý cấp tài khoản sẵn và liên kết với hồ sơ sinh viên hoặc giảng viên tương ứng. Trang công khai có chức năng đăng nhập.
2. Quản lý tạo lớp học phần cho từng môn, gán giảng viên phụ trách và đưa sinh viên vào lớp.
3. Người dùng đăng nhập bằng tài khoản được cấp. Backend xác thực và cấp JWT. Frontend mở trang theo vai trò. Sinh viên thấy lớp mình đang học, còn giảng viên thấy lớp mình phụ trách.
4. Khi gửi đăng ký Tiểu luận, hệ thống lấy giảng viên duyệt từ lớp học phần. Khi gửi đăng ký Đồ án tốt nghiệp, hệ thống lấy người duyệt từ lựa chọn giảng viên hướng dẫn của sinh viên.

Ví dụ, nếu môn Lập trình Web có hai lớp WEB01 và WEB02 do hai giảng viên khác nhau phụ trách, hồ sơ của sinh viên WEB01 chuyển cho giảng viên của WEB01.

## 4. Quy trình Tiểu luận(vd)

1. Giảng viên phụ trách đặt số thành viên tối thiểu và tối đa, thời gian đăng ký và hạn nộp của từng mốc.
2. Sinh viên chọn lớp học phần đang học. Nếu làm nhóm, nhóm trưởng lập nhóm và mời thành viên cùng lớp; người được mời phải xác nhận mới được tính vào nhóm. Mỗi sinh viên tham gia tối đa một nhóm trong cùng lớp học phần. Chỉ nhóm trưởng hiện tại được chuyển quyền trưởng nhóm cho thành viên đã xác nhận.
3. Sinh viên làm cá nhân hoặc nhóm trưởng chọn đề tài có sẵn của lớp hay tự đề xuất, rồi gửi đăng ký. Hệ thống kiểm tra tư cách tham gia lớp và số thành viên trước khi nhận hồ sơ.
4. Giảng viên phụ trách duyệt hoặc từ chối đăng ký. Nếu bị từ chối, người gửi có thể sửa hồ sơ cũ rồi gửi lại hoặc tạo hồ sơ mới trong thời gian đăng ký. Nếu hồ sơ được duyệt, sinh viên hoặc nhóm trưởng nộp file báo cáo theo từng mốc.
5. Giảng viên xem báo cáo, ghi nhận xét và nhập điểm Tiểu luận. Quản lý duyệt công bố điểm trước khi sinh viên xem kết quả. Hệ thống thống kê theo số sinh viên trong lớp, kể cả khi bài được nộp theo nhóm.

Giới hạn hợp lệ có số tối thiểu từ 1 trở lên và tối đa bằng hoặc lớn hơn tối thiểu. Nhóm trưởng được tính vào tổng số thành viên.

| Cấu hình tối thiểu–tối đa | Hình thức được gửi đăng ký  |
| ------------------------- | --------------------------- |
| 1–1                       | Cá nhân                     |
| 1–4                       | Cá nhân hoặc nhóm 2–4 người |
| 2–4                       | Nhóm 2–4 người              |

Nhóm có thể lưu nháp khi thiếu thành viên. Lời mời chưa được xác nhận không tính vào sĩ số. Hệ thống chặn thêm người khi đã đủ tối đa và kiểm tra lại toàn bộ điều kiện lúc gửi. Sau khi gửi hồ sơ, danh sách thành viên được giữ cố định để điểm gắn đúng người.

## 5. Quy trình Đồ án tốt nghiệp

1. Sinh viên chọn đợt đồ án đang mở và chọn giảng viên hướng dẫn. Sinh viên chọn đề tài có sẵn của giảng viên đó hoặc tự đề xuất.
2. Giảng viên được chọn xét hồ sơ. Khi duyệt, giảng viên xác nhận nhận hướng dẫn đề tài. Nếu bị từ chối, sinh viên có thể sửa hồ sơ cũ rồi gửi lại hoặc tạo hồ sơ mới trong thời gian đăng ký.
3. Sinh viên nộp báo cáo theo từng mốc của đợt. Sinh viên được thay file đã nộp; bài nộp sau hạn mang trạng thái trễ. Giảng viên hướng dẫn theo dõi và nhận xét tiến độ.
4. Sinh viên nộp báo cáo cuối và bảo vệ trước hội đồng. Hệ thống ghi lịch và hội đồng của buổi bảo vệ.
5. Hội đồng chấm. Người được phân quyền nhập điểm tổng hợp của hội đồng. Quản lý duyệt công bố điểm trước khi sinh viên xem kết quả. Nếu sinh viên vắng bảo vệ, Quản lý xác nhận vắng và kết quả là không đạt. Chưa nhập điểm hoặc chưa xác nhận vắng vẫn là chưa chấm.

Cả hai luồng cho phép thay file đã nộp, ghi nhận thời điểm nộp mới nhất và gắn bài nộp với đúng hồ sơ và mốc báo cáo. Bài nộp sau hạn được nhận và đánh dấu **trễ**. Thống kê tách ba nhóm là **đạt**, **không đạt** và **chưa chấm**; điểm chưa được Quản lý công bố không hiển thị cho sinh viên.

## 6. Công nghệ và thiết kế hướng đối tượng

- **Frontend** dùng ReactJS cho web trên trình duyệt.
- **Backend** dùng FastAPI và Python để xây dựng RESTful API. Xác thực bằng JWT.
- **Cơ sở dữ liệu** dùng PostgreSQL đã cài trên máy phát triển.
- **Yêu cầu môn học** là tổ chức backend theo lập trình hướng đối tượng (OOP).

Phương án tổ chức backend là để route FastAPI tiếp nhận yêu cầu HTTP và gọi các lớp xử lý nghiệp vụ. Những quy tắc như kiểm tra nhóm, chuyển trạng thái hồ sơ và phân quyền duyệt nằm trong các lớp có trách nhiệm rõ ràng.

| Lớp minh họa       | Trách nhiệm dự kiến                                                                                               |
| ------------------ | ----------------------------------------------------------------------------------------------------------------- |
| `NhomTieuLuan`     | Quản lý thành viên, xác định nhóm trưởng và kiểm tra giới hạn số người khi gửi đăng ký.                           |
| `HoSoDangKy`       | Quản lý dữ liệu và các chuyển đổi trạng thái của hồ sơ, như gửi, duyệt hoặc từ chối.                              |
| `DichVuDuyetDeTai` | Xác định người được quyền duyệt theo lớp học phần hoặc theo giảng viên được chọn, rồi thực hiện việc duyệt hồ sơ. |

Ví dụ, khi trưởng nhóm gửi đăng ký Tiểu luận, route gọi lớp xử lý đăng ký. Lớp này lấy dữ liệu lớp học phần và yêu cầu đối tượng `NhomTieuLuan` kiểm tra số thành viên trước khi chuyển hồ sơ sang trạng thái chờ duyệt. Sơ đồ Lớp sẽ thể hiện thuộc tính, phương thức và mối quan hệ của các lớp thực sự dùng trong backend.

## 7. Các quyết định cần xác nhận khi triển khai

| Nội dung                 | Phương án đề xuất                                                                                |
| ------------------------ | ------------------------------------------------------------------------------------------------ |
| Điểm Tiểu luận theo nhóm | Một điểm chung cho cả nhóm. Khi thống kê, nhóm 4 người đạt được tính là 4 sinh viên đạt.         |
| Nhập điểm bảo vệ         | Quản lý phân công thư ký hoặc giảng viên được phép nhập một điểm tổng hợp của hội đồng.          |
| Ngưỡng đạt và thang điểm | Xác nhận theo yêu cầu của môn trước khi tính kết quả. Bài nộp trễ vẫn được nhận và đánh dấu trễ. |
| Chức năng bổ sung        | Giảng viên yêu cầu chỉnh sửa đề tài trước khi ra quyết định duyệt hoặc từ chối.                  |
