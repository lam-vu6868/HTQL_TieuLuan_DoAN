"""Quy trình nhận xét, điểm và công bố.

1. Viết async def ResultService.add_comment()/enter_score(): kiểm tra giảng viên đúng quyền.
2. Viết async def confirm_absence(): chỉ Quản lý đánh dấu vắng bảo vệ sau lịch.
3. Viết async def publish(): chỉ Quản lý công bố kết quả đã có điểm hoặc xác nhận vắng.
4. Viết async def statistics(): thiếu điểm/chưa xác nhận vắng là CHUA_CHAM, vắng là KHONG_DAT.
"""
