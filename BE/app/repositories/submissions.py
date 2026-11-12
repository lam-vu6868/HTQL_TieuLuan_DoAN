"""Truy vấn mốc nộp và metadata file.

1. Viết async def get_milestone()/save_milestone()/get_class_deadline()/get_current_submission() trên AsyncSession; mốc gắn phan_cong_id.
2. Viết async def upsert_submission() cho một bài hiện hành mỗi hồ sơ Tiểu luận hoặc hồ sơ/mốc Đồ án.
3. Ghi nop_luc, nop_tre và đường dẫn do server tạo; không lưu nội dung file trong DB.
"""
