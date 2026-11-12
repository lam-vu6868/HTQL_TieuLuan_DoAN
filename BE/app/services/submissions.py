"""Quy trình nộp và thay file báo cáo.

1. Viết async def SubmissionService.create_milestone(): chỉ GVHD của phân công đặt mốc Đồ án; kiểm tra thứ tự và đúng một mốc cuối trước khi nộp.
2. Viết async def submit_or_replace(): kiểm tra hồ sơ đã duyệt và người nộp; mốc Đồ án phải thuộc đúng phân công của hồ sơ.
3. So thời điểm nhận file với han_nop của lớp hoặc mốc để ghi nop_tre; quá hạn vẫn nhận.
4. Đọc UploadFile theo từng khối; ghi/xóa file local qua asyncio.to_thread() để không chặn event loop.
5. Lưu bằng tên do server tạo, await repository cập nhật bài hiện hành theo (ho_so_id, moc_nop_id).
6. Nếu ghi DB lỗi, dọn file mới; chỉ xóa file cũ sau khi thay thành công.
"""
