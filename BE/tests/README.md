# Kiểm thử backend

Thư mục này sẽ chứa kiểm thử khi bắt đầu viết logic. Ưu tiên các ca có rủi ro nghiệp vụ:

- Sinh viên ngoài lớp hoặc giảng viên không được phân công bị chặn.
- Thành viên phải xác nhận lời mời; chỉ trưởng nhóm hiện tại được chuyển quyền.
- Hồ sơ bị từ chối được sửa/gửi lại hoặc tạo mới; không có hai hồ sơ đang xử lý cùng phạm vi.
- Thay file cập nhật thời điểm nộp và trạng thái trễ.
- Chưa có điểm là chưa chấm; Quản lý xác nhận vắng và duyệt công bố trước khi sinh viên xem điểm.

Chưa có file test chạy được vì bộ khung chưa có logic để kiểm tra.
Khi thêm test API và service, dùng client/fixture hỗ trợ async và kiểm tra cả commit/rollback với AsyncSession.
