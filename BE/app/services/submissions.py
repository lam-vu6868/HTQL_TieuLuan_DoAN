"""Quy trình nộp và thay file báo cáo.

1. Tạo SubmissionService.submit_or_replace(): kiểm tra hồ sơ đã duyệt, mốc đúng phạm vi và người nộp.
2. So thời điểm nhận file với han_nop để ghi nop_tre; quá hạn vẫn nhận.
3. Lưu file bằng tên do server tạo, cập nhật bài hiện hành theo (ho_so_id, moc_nop_id).
4. Nếu ghi DB lỗi, dọn file mới; chỉ xóa file cũ sau khi thay thành công.
"""
