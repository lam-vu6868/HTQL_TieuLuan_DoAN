"""Nghiệp vụ Quản lý chuẩn bị tài khoản, lớp và đợt.

1. Viết async def AdminService.create_account(): băm mật khẩu rồi gắn hồ sơ sinh viên/giảng viên.
2. Viết async def create_class()/assign_teacher()/enroll_student(): kiểm tra mã và quan hệ không trùng.
3. Viết async def create_thesis_term(): tạo đợt Đồ án; phân công GVHD được tạo khi giảng viên duyệt đề xuất.
4. Await AcademicRepository; commit một lần cho mỗi nghiệp vụ, rollback khi lỗi.
"""
