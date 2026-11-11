"""Quy trình nộp và thay file báo cáo.

1. Viết async def SubmissionService.submit_or_replace(): kiểm tra hồ sơ đã duyệt và người nộp; Tiểu luận một hạn, Đồ án theo mốc.
2. So thời điểm nhận file với han_nop của lớp hoặc mốc để ghi nop_tre; quá hạn vẫn nhận.
3. Đọc UploadFile theo từng khối; ghi/xóa file local qua asyncio.to_thread() để không chặn event loop.
4. Lưu bằng tên do server tạo, await repository cập nhật bài hiện hành theo (ho_so_id, moc_nop_id).
5. Nếu ghi DB lỗi, dọn file mới; chỉ xóa file cũ sau khi thay thành công.
"""
