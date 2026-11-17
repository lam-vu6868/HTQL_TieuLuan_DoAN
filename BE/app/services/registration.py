"""Quy trình hồ sơ Tiểu luận và Đồ án.

1. Viết async def RegistrationService.create_draft()/submit(): nhận tên/mô tả tự đề xuất, kiểm tra hạn và người gửi.
2. Viết async def edit_rejected() cho TU_CHOI; tạo hồ sơ mới dùng lại create_draft().
3. Viết async def review(): Tiểu luận dùng GV lớp, Đồ án dùng giảng viên sinh viên chọn; chỉ xét CHO_DUYET. Khi duyệt Đồ án, tạo phân công GVHD và gắn hồ sơ trong cùng giao dịch.
4. Viết async def configure_class_rules(): chỉ GV phụ trách chỉnh cấu hình lớp; chặn đổi chế độ/ngưỡng sau khi có điểm/công bố.
5. Await repository, khóa và commit/rollback trong cùng giao dịch để chặn hồ sơ trùng.
"""
