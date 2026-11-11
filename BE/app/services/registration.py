"""Quy trình hồ sơ Tiểu luận và Đồ án.

1. Viết async def RegistrationService.create_draft()/submit(): kiểm tra hạn, đề tài và người gửi.
2. Viết async def edit_rejected() cho TU_CHOI; tạo hồ sơ mới dùng lại create_draft().
3. Viết async def review(): chỉ giảng viên đúng phạm vi duyệt/từ chối CHO_DUYET.
4. Await repository, khóa và commit/rollback trong cùng giao dịch để chặn hồ sơ trùng.
"""
