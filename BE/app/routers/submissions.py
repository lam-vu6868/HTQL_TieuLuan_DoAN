"""API nộp và đọc file báo cáo.

1. Viết async def submit_report()/replace_report(): nhận UploadFile, moc_nop_id, await SubmissionService.
2. Viết async def get_submission()/download_report(): await kiểm tra quyền trước khi trả metadata/file.
3. Giới hạn loại/kích thước file và không dùng tên file client làm đường dẫn lưu.
4. Không trả đường dẫn storage/reports cho FE.
"""
