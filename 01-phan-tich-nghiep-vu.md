# HTTT07 — Phân tích nghiệp vụ (phạm vi bản đầu)

## 1. Mục tiêu

Nhóm hai người triển khai luồng **đăng ký đề tài → giảng viên duyệt → nộp báo cáo → giảng viên nhận xét, chấm điểm → sinh viên xem kết quả**. Tiểu luận và Đồ án dùng chung phần đăng ký, bài nộp và kết quả; khác nhau ở người thực hiện và cách gán giảng viên. Bản đầu thu gọn phạm vi, đồng thời giữ quyết định của nhóm về nộp trễ, công bố điểm và hai cách chấm Tiểu luận.

Đề bài gốc yêu cầu nộp theo định kỳ, quản lý thời gian theo kế hoạch, thống kê số sinh viên đạt và bốn loại sơ đồ UML. Bản đầu giữ một hạn nộp cho Tiểu luận; Đồ án có nhiều mốc do GVHD thiết lập cho từng sinh viên được phân công.

| Quy trình | Người đăng ký | Người duyệt và chấm |
| --- | --- | --- |
| Tiểu luận | Sinh viên cá nhân hoặc trưởng nhóm trong lớp học phần | Giảng viên phụ trách lớp |
| Đồ án tốt nghiệp | Một sinh viên trong đợt đồ án | GVHD do Quản lý gán trước |

## 2. Vai trò

| Vai trò | Quyền trong bản đầu |
| --- | --- |
| Sinh viên | Xem lớp/đợt của mình, tự đề xuất đề tài, xem hồ sơ và nhận xét, nộp bài cá nhân, xem điểm đã công bố. |
| Nhóm trưởng | Tạo nhóm Tiểu luận, tìm sinh viên bằng mã trong cùng lớp rồi thêm vào nhóm, chuyển quyền trưởng nhóm cho thành viên, gửi hồ sơ và nộp bài cho nhóm. |
| Giảng viên | Duyệt/từ chối hồ sơ thuộc lớp mình hoặc được gán hướng dẫn; nhận xét, nhập điểm và xem thống kê trong phạm vi được phân công. Giảng viên lớp đặt hạn nộp Tiểu luận; GVHD đặt mốc nộp Đồ án cho sinh viên mình hướng dẫn. |
| Quản lý | Cấp tài khoản, tạo môn/lớp/đợt, xếp sinh viên vào lớp, gán giảng viên phụ trách và GVHD, duyệt công bố điểm. |

Nhóm trưởng là quyền của sinh viên trong một nhóm, không phải vai trò tài khoản riêng. Mọi API kiểm tra vai trò và quan hệ với lớp, nhóm hoặc đợt. Thành viên thường xem hồ sơ và bài nộp nhóm, nhưng chỉ xem điểm đã công bố của chính mình; chỉ trưởng nhóm hiện tại được gửi hồ sơ, nộp bài và chuyển quyền.

## 3. Tài khoản và phân công

Quản lý tạo tài khoản và hồ sơ sinh viên/giảng viên trước. Người dùng đăng nhập, Backend xác thực JWT. Quản lý tạo lớp học phần, gán giảng viên phụ trách, xếp sinh viên vào lớp. Với Đồ án, Quản lý tạo đợt và gán trước một GVHD cho từng sinh viên trong đợt. Chỉ GVHD đã được gán mới xét duyệt và chấm hồ sơ của sinh viên đó. Tên đăng nhập là email. Sinh viên có thể yêu cầu email đặt lại mật khẩu; liên kết chỉ dùng một lần và hết hạn.

## 4. Tiểu luận

1. Giảng viên lớp đặt thời gian đăng ký, hạn nộp báo cáo, giới hạn nhóm và **chế độ chấm điểm**: điểm chung hoặc điểm riêng từng sinh viên. Chế độ này được chốt trước khi nhập điểm.
2. Sinh viên làm cá nhân hoặc trưởng nhóm tạo nhóm, tìm và thêm sinh viên cùng lớp bằng mã sinh viên. Hệ thống kiểm tra thành viên chưa thuộc nhóm khác trong lớp và không vượt giới hạn. Trưởng nhóm hiện tại có thể chuyển quyền cho một thành viên. Danh sách thành viên cố định sau khi gửi hồ sơ.
3. Người đăng ký tự nhập tên và mô tả đề tài. Hệ thống cho xem các đề tài đã đăng ký trong lớp để tự kiểm tra trùng, nhưng không bắt buộc tên đề tài duy nhất; giảng viên quyết định khi duyệt.
4. Giảng viên lớp duyệt hoặc từ chối kèm nhận xét. Sau khi từ chối, người gửi có thể sửa hồ sơ cũ rồi gửi lại hoặc tạo hồ sơ mới trong hạn đăng ký. Hồ sơ đã duyệt không sửa đề tài.
5. Sinh viên cá nhân hoặc trưởng nhóm nộp và có thể thay file. Giảng viên nhận xét và nhập điểm: ở chế độ điểm chung, mọi thành viên nhận cùng điểm; ở chế độ điểm riêng, giảng viên nhập điểm từng thành viên. Quản lý duyệt công bố trước khi sinh viên xem điểm. Thống kê đếm **sinh viên**, không đếm nhóm.

Tiểu luận chỉ có **một hạn nộp cố định**, không có chuỗi mốc trung gian.

## 5. Đồ án tốt nghiệp

1. Quản lý tạo đợt và gán GVHD cho từng sinh viên. GVHD thiết lập các mốc nộp cho sinh viên mình hướng dẫn; mốc cuối dùng để chấm điểm.
2. Sinh viên tự nhập tên và mô tả đề tài rồi gửi hồ sơ đến GVHD đã được gán. GVHD duyệt hoặc từ chối kèm nhận xét; hồ sơ bị từ chối được sửa rồi gửi lại hoặc tạo mới trong hạn.
3. Sinh viên nộp hoặc thay file theo mốc. GVHD nhận xét mốc trung gian và nhập điểm ở mốc cuối. Các thầy có thể thống nhất điểm bên ngoài hệ thống; trong bản đầu chỉ GVHD nhập điểm vào hệ thống.
4. Quản lý duyệt công bố, sau đó sinh viên xem kết quả. Hồ sơ chưa được nhập điểm là **chưa chấm**, không tự động thành không đạt.

Hội đồng, thành viên hội đồng, lịch bảo vệ và điểm từng giám khảo **chưa được quản lý trong bản đầu**. Nếu giảng viên môn học yêu cầu khi nộp, nhóm cần đưa trở lại phạm vi.

## 6. Quy tắc chung và phần để sau

- Hồ sơ có trạng thái `NHAP`, `CHO_DUYET`, `DA_DUYET`, `TU_CHOI`. Mỗi sinh viên/nhóm chỉ có một hồ sơ đang chờ hoặc đã duyệt trong cùng lớp/đợt; hồ sơ bị từ chối được giữ để xem lại.
- File báo cáo lưu trên máy chủ BE tại `BE/storage/reports/`; PostgreSQL chỉ lưu đường dẫn nội bộ và thông tin bài nộp. Sinh viên/giảng viên tải file qua API sau khi kiểm tra quyền với hồ sơ, không truy cập trực tiếp thư mục lưu trữ. Khi thay file, hệ thống giữ bản hiện hành và thời điểm nộp mới nhất. Nộp sau hạn vẫn được nhận và đánh dấu `nop_tre`.
- Điểm thang 10; ngưỡng đạt mặc định **4,0**. Giảng viên lớp có thể chỉnh ngưỡng Tiểu luận cho lớp; GVHD có thể chỉnh ngưỡng Đồ án cho hồ sơ mình phụ trách trước khi công bố. Chưa có điểm là chưa chấm. Sinh viên chỉ xem điểm của mình sau khi Quản lý công bố.
- Để sau: danh sách đề tài giảng viên cung cấp, lời mời/xác nhận tham gia nhóm, hội đồng và lịch bảo vệ trong hệ thống.

## 7. Công nghệ

Frontend ReactJS; Backend FastAPI async theo OOP, JWT và SQLAlchemy AsyncSession; PostgreSQL lưu dữ liệu nghiệp vụ và thông tin file, còn file báo cáo lưu trên ổ đĩa máy chủ BE. Router nhận HTTP và file tải lên, service kiểm tra nghiệp vụ/quyền và lưu file, repository truy cập CSDL. API kiểm tra quyền trước khi trả file cho người dùng. Các lớp/method thực tế cần khớp [sơ đồ UML](02-so-do-uml.md) và [thiết kế CSDL](04-thiet-ke-co-so-du-lieu.md).
