# Sơ đồ Class cốt lõi cho slide

Sơ đồ chọn 7 lớp ORM đang có trong `BE/app/models` để thể hiện luồng đăng ký → nộp bài → kết quả. Chỉ hiện thuộc tính và quan hệ chính để đọc được trên slide; các bảng còn lại nằm trong [thiết kế CSDL](04-thiet-ke-co-so-du-lieu.md). Chưa vẽ phương thức nghiệp vụ vì các phương thức đó chưa được triển khai trong model.

```plantuml
@startuml
title Class cốt lõi — Đăng ký, nộp bài và kết quả
left to right direction
skinparam defaultFontSize 20
skinparam nodesep 90
skinparam ranksep 110
skinparam linetype polyline

class SinhVien {
  +id: bigint
  +ma_sinh_vien: text
}

class GiangVien {
  +id: bigint
  +ma_giang_vien: text
}

class LopHocPhan {
  +id: bigint
  +ma_lop: text
  +han_nop: timestamptz?
}

class PhanCongHuongDan {
  +id: bigint
  +sinh_vien_id: bigint
  +giang_vien_id: bigint
}

class HoSoDangKy {
  +id: bigint
  +ten_de_tai: text
  +loai: text
  +trang_thai: text
}

class BaiNop {
  +id: bigint
  +nop_luc: timestamptz
  +nop_tre: bool
}

class KetQua {
  +ho_so_id: bigint
  +sinh_vien_id: bigint
  +diem: numeric(4,2)
}

GiangVien "1" -- "0..*" LopHocPhan : phụ trách
GiangVien "1" -- "0..*" PhanCongHuongDan : GVHD
SinhVien "1" -- "0..*" PhanCongHuongDan : được phân công
SinhVien "1" -- "0..*" HoSoDangKy : gửi
LopHocPhan "0..1" -- "0..*" HoSoDangKy : Tiểu luận
PhanCongHuongDan "0..1" -- "0..*" HoSoDangKy : Đồ án
HoSoDangKy "1" -- "0..*" BaiNop : nộp
HoSoDangKy "1" -- "0..*" KetQua : chấm
SinhVien "1" -- "0..*" KetQua : nhận điểm
@enduml
```

**Ghi chú thuyết trình:** Giảng viên phụ trách lớp và có thể làm GVHD; sinh viên gửi hồ sơ. Hồ sơ Tiểu luận gắn lớp, còn hồ sơ Đồ án đã duyệt gắn phân công GVHD. Một hồ sơ có thể có nhiều bài nộp và có một dòng `KetQua` cho mỗi sinh viên được chấm.
