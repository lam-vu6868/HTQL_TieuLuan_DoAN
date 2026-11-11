"""Quy trình nhóm Tiểu luận.

1. Viết async def GroupService.add_member(ma_sinh_vien): chỉ trưởng nhóm thêm sinh viên cùng lớp chưa thuộc nhóm khác.
2. Viết async def transfer_leader(): chỉ trưởng nhóm hiện tại chuyển cho thành viên đang ở trong nhóm.
3. Await repository; kiểm tra giới hạn sĩ số, giữ danh sách nhóm sau khi gửi hồ sơ.
4. Thêm thành viên và chuyển quyền trong một giao dịch để không có hai trưởng nhóm.
"""
