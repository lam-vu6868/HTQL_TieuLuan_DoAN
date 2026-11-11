"""Quy trình nhận xét, điểm và công bố.

1. Viết async def ResultService.add_comment()/enter_score(): Tiểu luận GV lớp, Đồ án GVHD được gán.
2. Với CHUNG, ghi cùng điểm vào từng sinh viên; với RIENG, ghi điểm riêng từng thành viên trong một giao dịch.
3. Viết async def publish(): chỉ Quản lý công bố khi mọi sinh viên của hồ sơ đều đã có điểm.
4. Viết async def statistics(): đếm theo sinh viên, thiếu điểm là CHUA_CHAM; dùng ngưỡng lớp/hồ sơ Đồ án.
5. Chỉ GV lớp chỉnh ngưỡng lớp, GVHD chỉnh ngưỡng hồ sơ Đồ án trước khi công bố.
"""
