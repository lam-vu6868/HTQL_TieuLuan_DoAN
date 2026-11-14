# HTTT07 — Sơ đồ UML cho phạm vi bản đầu

Sáu sơ đồ PlantUML gồm Use Case, Lớp, hai sơ đồ Tuần tự duyệt đề tài và hai sơ đồ Hoạt động. Sao chép từng khối `@startuml` đến `@enduml` vào PlantUML để xem hình. Sơ đồ mô tả **nghiệp vụ bản đầu** trong [file 01](01-phan-tich-nghiep-vu.md); tên bảng và ràng buộc ở [file 04](04-thiet-ke-co-so-du-lieu.md).

## 1. Use Case tổng thể

```plantuml
@startuml
left to right direction
actor "Sinh viên" as SV
actor "Nhóm trưởng" as NT
actor "Giảng viên" as GV
actor "Quản lý" as QL
NT --|> SV
rectangle HTTT07 {
  usecase "Đăng nhập / đặt lại mật khẩu" as Login
  usecase "Tạo nhóm, thêm thành viên\nvà chuyển trưởng nhóm" as Group
  usecase "Đề xuất, sửa, gửi lại đề tài" as Register
  usecase "Duyệt hoặc từ chối\nkèm nhận xét" as Review
  usecase "Nộp hoặc thay file báo cáo" as Submit
  usecase "Nhận xét và nhập điểm" as Grade
  usecase "Xem điểm đã công bố" as View
  usecase "Tạo lớp và đợt" as Setup
  usecase "Đặt hạn nộp Tiểu luận\nvà mốc nộp Đồ án" as Deadlines
  usecase "Duyệt công bố điểm" as Publish
  usecase "Xem thống kê sinh viên đạt" as Stats
}
SV -- Login
SV -- Register
SV -- Submit
SV -- View
NT -- Group
GV -- Login
GV -- Review
GV -- Grade
GV -- Stats
GV -- Deadlines
QL -- Login
QL -- Setup
QL -- Publish
QL -- Stats
@enduml
```

Sinh viên tự đề xuất đề tài; không có chức năng chọn đề tài do giảng viên cung cấp trong bản đầu. Với Đồ án, sinh viên chọn giảng viên nhận đề xuất; khi giảng viên duyệt, hệ thống tự ghi nhận phân công GVHD. Trưởng nhóm Tiểu luận thêm sinh viên cùng lớp bằng mã; chỉ trưởng nhóm gửi hồ sơ và nộp bài thay nhóm.

## 2. Sơ đồ Lớp nghiệp vụ

```plantuml
@startuml
hide empty members
class LopHocPhan {
  +hanNop: datetime
  +cheDoCham: CHUNG | RIENG
  +kiemTraSiSo(nhom): bool
}
class DotDoAn {
  +dangMo(): bool
}
class PhanCongHuongDan {
  +sinhVienId: int
  +giangVienId: int
}
class NhomTieuLuan {
  +themThanhVien(maSV)
  +chuyenTruongNhom(sinhVien)
  +duDieuKienGui(): bool
}
class HoSoDangKy {
  +tenDeTai: str
  +giangVienDeXuatId: int
  +trangThai: str
  +gui()
  +duyet()
  +tuChoi(lyDo)
  +suaSauTuChoi()
}
class MocNop {
  +hanNop: datetime
  +laMocCuoi: bool
}
class BaiNop {
  +nopLuc: datetime
  +nopTre: bool
  +duongDanTep: str
  +thayFile()
  +ghiNhanXet()
}
class KetQua {
  +sinhVienId: int
  +diem: decimal
  +congBo()
  +dat(nguong): bool
}
class DichVuDuyetDeTai {
  +xetDuyet(hoSo, giangVien, quyetDinh)
}
LopHocPhan "1" -- "0..*" NhomTieuLuan
NhomTieuLuan "0..1" -- "0..*" HoSoDangKy
LopHocPhan "0..1" -- "0..*" HoSoDangKy
DotDoAn "0..1" -- "0..*" HoSoDangKy
DotDoAn "1" -- "0..*" PhanCongHuongDan
PhanCongHuongDan "0..1" -- "0..*" HoSoDangKy
PhanCongHuongDan "1" -- "0..*" MocNop
HoSoDangKy "1" -- "0..*" BaiNop
BaiNop "0..*" -- "0..1" MocNop
HoSoDangKy "1" -- "0..*" KetQua
DichVuDuyetDeTai ..> HoSoDangKy
@enduml
```

Hồ sơ Tiểu luận gắn lớp, có thể gắn nhóm; hồ sơ Đồ án gắn đợt và giảng viên được chọn. Khi giảng viên duyệt, hồ sơ mới gắn phân công GVHD. Tiểu luận lấy hạn từ lớp, Đồ án lấy hạn từ mốc do GVHD của phân công đó đặt. `BaiNop` giữ đường dẫn nội bộ; file thật lưu ở `BE/storage/reports/` và chỉ tải qua API có kiểm tra quyền. `KetQua` ứng với **một sinh viên trong một hồ sơ**; điểm chung ghi cùng giá trị cho các thành viên, điểm riêng ghi từng giá trị. Quản lý chỉ công bố khi hồ sơ đã đủ điểm.

## 3. Sơ đồ Tuần tự duyệt đề tài

### 3.1. Tiểu luận

```plantuml
@startuml
actor "Sinh viên/Trưởng nhóm" as SV
participant "React" as FE
participant "FastAPI" as API
database "PostgreSQL" as DB
actor "Giảng viên lớp" as GV
SV -> FE: Nhập tên, mô tả đề tài
FE -> API: Gửi hồ sơ Tiểu luận
API -> DB: Kiểm tra lớp, hạn, người gửi, nhóm
DB --> API: Dữ liệu kiểm tra
alt Hợp lệ
  API -> DB: Lưu CHO_DUYET
  API --> FE: Mã hồ sơ
else Không hợp lệ
  API --> FE: Lý do từ chối thao tác
end
GV -> FE: Mở hồ sơ chờ của lớp
FE -> API: Gửi quyết định và nhận xét
API -> DB: Kiểm tra GV phụ trách, trạng thái hồ sơ
alt Duyệt
  API -> DB: Ghi DA_DUYET
else Từ chối
  API -> DB: Ghi TU_CHOI và lý do
end
API --> FE: Trạng thái mới
note over SV,FE: Nếu bị từ chối: trong hạn, sửa hồ sơ cũ\nhoặc tạo hồ sơ mới rồi gửi lại.
@enduml
```

### 3.2. Đồ án tốt nghiệp

```plantuml
@startuml
actor "Sinh viên" as SV
participant "React" as FE
participant "FastAPI" as API
database "PostgreSQL" as DB
actor "Giảng viên được chọn" as GV
SV -> FE: Chọn đợt, giảng viên, nhập tên và mô tả đề tài
FE -> API: Gửi hồ sơ đề xuất Đồ án
API -> DB: Kiểm tra đợt, hạn và hồ sơ đang xử lý của SV
DB --> API: Dữ liệu kiểm tra
alt Còn hạn và chưa có hồ sơ đang xử lý
  API -> DB: Lưu CHO_DUYET gắn giảng viên được chọn
  API --> FE: Mã hồ sơ
else Không hợp lệ
  API --> FE: Lý do từ chối thao tác
end
GV -> FE: Mở hồ sơ gửi đến mình
FE -> API: Gửi quyết định và nhận xét
API -> DB: Kiểm tra đúng giảng viên được chọn, trạng thái hồ sơ và sinh viên chưa có GVHD
alt Đồng ý hướng dẫn và duyệt đề tài
  API -> DB: Tạo phân công GVHD, gắn hồ sơ và ghi DA_DUYET trong một giao dịch
else Từ chối
  API -> DB: Ghi TU_CHOI và lý do
end
API --> FE: Trạng thái mới
note over SV,FE: Nếu bị từ chối: trong hạn, sửa hồ sơ cũ\nhoặc tạo hồ sơ mới và có thể chọn giảng viên khác.
@enduml
```

## 4. Sơ đồ Hoạt động

### 4.1. Tiểu luận

```plantuml
@startuml
start
:Quản lý tạo lớp và xếp sinh viên;
:Giảng viên đặt hạn, giới hạn nhóm và chế độ chấm;
:Sinh viên làm cá nhân hoặc trưởng nhóm thêm thành viên cùng lớp;
:Sinh viên/Trưởng nhóm tự đề xuất đề tài và gửi;
if (Giảng viên duyệt?) then (Có)
  :Hồ sơ DA_DUYET;
else (Không)
  :Ghi lý do TU_CHOI;
  :Trong hạn, sửa hồ sơ cũ hoặc tạo mới;
  stop
endif
:Nộp hoặc thay file, đánh dấu trễ nếu quá hạn;
:Giảng viên nhận xét và nhập điểm chung hoặc riêng;
if (Đủ điểm cho mọi thành viên?) then (Có)
  :Quản lý duyệt công bố;
  :Mỗi sinh viên xem điểm của mình;
else (Chưa)
  :Giữ chưa chấm/chưa công bố;
endif
:Thống kê đạt theo từng sinh viên;
stop
@enduml
```

### 4.2. Đồ án tốt nghiệp

```plantuml
@startuml
start
:Quản lý tạo đợt;
:Sinh viên chọn giảng viên và gửi đề xuất đề tài;
if (Giảng viên đồng ý?) then (Có)
  :Tự tạo phân công GVHD và duyệt hồ sơ;
  :GVHD đặt các mốc nộp cho sinh viên;
else (Không)
  :Ghi lý do TU_CHOI;
  :Trong hạn, sửa hồ sơ cũ hoặc tạo mới và có thể chọn giảng viên khác;
  stop
endif
:Sinh viên nộp hoặc thay file theo mốc;
:Đánh dấu trễ nếu quá hạn;
:GVHD nhận xét mốc trung gian, nhập điểm mốc cuối;
if (Đã có điểm?) then (Có)
  :Quản lý duyệt công bố;
  :Sinh viên xem điểm;
else (Chưa)
  :Giữ trạng thái chưa chấm;
endif
:Thống kê sinh viên đạt trong đợt;
stop
@enduml
```

## Phạm vi chưa triển khai

Sơ đồ không có kho đề tài gợi ý, lời mời xác nhận nhóm, hội đồng, lịch bảo vệ hoặc điểm từng giám khảo. Email đặt lại mật khẩu thuộc chức năng tài khoản; nộp trễ và Quản lý duyệt công bố thuộc bản đầu.
