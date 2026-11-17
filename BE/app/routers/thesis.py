"""API Đồ án tốt nghiệp cá nhân.

1. Viết async def list_open_terms()/get_my_supervisor()/list_registered_topics().
2. Viết async def create_registration()/submit_registration()/edit_rejected()/review_registration()/create_milestone().
3. Await RegistrationService với loại DO_AN; sinh viên chọn giảng viên khi gửi đề xuất, chỉ giảng viên đó xét duyệt.
4. create_milestone() gọi SubmissionService; chỉ GVHD của phân công được đặt mốc, mỗi phân công có đúng một mốc cuối trước khi nộp.
5. Sinh viên chỉ thấy hồ sơ/phân công của mình; giảng viên chỉ thấy đề xuất gửi đến mình và mốc thuộc phân công đã duyệt.
"""
