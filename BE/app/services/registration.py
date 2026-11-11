"""Quy trình hồ sơ Tiểu luận và Đồ án.

1. Tạo RegistrationService.create_draft() và submit(): kiểm tra hạn, phạm vi đề tài và người gửi.
2. Viết edit_rejected() cho hồ sơ TU_CHOI; lựa chọn tạo hồ sơ mới dùng lại create_draft().
3. Viết review(): chỉ giảng viên đúng phạm vi duyệt/từ chối hồ sơ CHO_DUYET.
4. Chặn hồ sơ CHO_DUYET/DA_DUYET thứ hai của cùng người trong lớp hoặc đợt; dùng giao dịch.
"""
