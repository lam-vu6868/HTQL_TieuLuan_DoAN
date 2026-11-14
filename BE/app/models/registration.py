"""Nhóm Tiểu luận, thành viên và hồ sơ tự đề xuất đề tài.

1. Tạo NhomTieuLuan và ThanhVienNhom; trưởng nhóm thêm sinh viên cùng lớp bằng mã, không có trạng thái lời mời.
2. Tạo HoSoDangKy lưu ten_de_tai/mo_ta, loại, trạng thái, lần gửi, lý do từ chối; nguong_dat riêng cho Đồ án.
3. Hồ sơ Đồ án lưu giang_vien_de_xuat_id do sinh viên chọn; chỉ gắn PhanCongHuongDan sau khi giảng viên đó duyệt.
4. Thêm khóa/chỉ mục để chặn một sinh viên có hai hồ sơ đang xử lý cùng phạm vi.
5. Kiểm tra chi tiết ràng buộc qua nhiều bảng ở service và migration.
"""
