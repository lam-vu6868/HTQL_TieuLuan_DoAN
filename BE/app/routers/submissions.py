"""API nộp và đọc file báo cáo.

1. Viết submit_report() và replace_report(): nhận file, moc_nop_id và gọi SubmissionService.
2. Viết get_submission() trả metadata; download_report() kiểm tra quyền rồi trả file.
3. Giới hạn loại/kích thước file và không dùng tên file client làm đường dẫn lưu.
4. Không trả đường dẫn storage/reports cho FE.
"""
