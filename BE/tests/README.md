# Kiểm thử backend

Thư mục này sẽ chứa kiểm thử khi bắt đầu viết logic. Ưu tiên các ca có rủi ro nghiệp vụ:

- Sinh viên ngoài lớp hoặc giảng viên không được phân công bị chặn.
- Chỉ giảng viên sinh viên chọn được xét đề xuất Đồ án; duyệt tạo đúng một phân công GVHD, từ chối không tạo phân công.
- Chỉ GVHD được phân công đặt mốc Đồ án cho sinh viên đó; bài nộp không dùng mốc của phân công khác.
- Thêm thành viên phải cùng lớp, chưa thuộc nhóm khác; chỉ trưởng nhóm hiện tại được chuyển quyền.
- Hồ sơ bị từ chối được sửa/gửi lại hoặc tạo mới; không có hai hồ sơ đang xử lý cùng phạm vi.
- Thay file cập nhật thời điểm nộp và trạng thái trễ.
- Điểm CHUNG ghi cho cả nhóm, điểm RIENG ghi từng người; thiếu điểm là chưa chấm, Quản lý chỉ công bố khi đủ điểm.
- Email đặt lại mật khẩu không tiết lộ tài khoản, token hết hạn và chỉ dùng một lần.

Chưa có file test chạy được vì bộ khung chưa có logic để kiểm tra.
Khi thêm test API và service, dùng client/fixture hỗ trợ async và kiểm tra cả commit/rollback với AsyncSession.
