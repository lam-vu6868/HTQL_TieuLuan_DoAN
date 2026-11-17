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
SV -- Register
SV -- Submit
SV -- View
NT -- Group
GV -- Review
GV -- Grade
GV -- Stats
GV -- Deadlines
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
title Tiểu luận — Gửi và duyệt đề tài
skinparam defaultFontSize 30
actor "Sinh viên /\nTrưởng nhóm" as SV
participant "Giao diện\nReact" as FE
participant "API\nFastAPI" as API
database "PostgreSQL" as DB
actor "Giảng viên\nphụ trách lớp" as GV

== Gửi hồ sơ ==
SV -> FE: Nhập tên và mô tả đề tài
FE -> API: Gửi hồ sơ Tiểu luận
API -> DB: Kiểm tra lớp, hạn đăng ký,\nngười gửi và nhóm
DB --> API: Kết quả kiểm tra
alt Hợp lệ
  API -> DB: Lưu hồ sơ CHO_DUYET
  API --> FE: Mã hồ sơ
else Không hợp lệ
  API --> FE: Lý do không nhận hồ sơ
end

== Giảng viên duyệt ==
GV -> FE: Mở hồ sơ chờ duyệt
FE -> API: Gửi quyết định và nhận xét
API -> DB: Kiểm tra giảng viên phụ trách\nvà trạng thái hồ sơ
alt Duyệt
  API -> DB: Cập nhật DA_DUYET
else Từ chối
  API -> DB: Cập nhật TU_CHOI và lý do
end
API --> FE: Trạng thái hồ sơ mới
note over SV,FE
  Nếu bị từ chối, trong hạn đăng ký
  có thể sửa hồ sơ cũ hoặc tạo hồ sơ mới để gửi lại.
end note
@enduml
```

### 3.2. Đồ án tốt nghiệp

```plantuml
@startuml
title Đồ án tốt nghiệp — Gửi và duyệt đề tài
skinparam defaultFontSize 18
actor "Sinh viên" as SV
participant "Giao diện\nReact" as FE
participant "API\nFastAPI" as API
database "PostgreSQL" as DB
actor "Giảng viên\nđược chọn" as GV

== Gửi đề xuất ==
SV -> FE: Chọn đợt và giảng viên,\nnhập tên và mô tả đề tài
FE -> API: Gửi hồ sơ Đồ án
API -> DB: Kiểm tra đợt, hạn đăng ký\nvà hồ sơ đang xử lý của sinh viên
DB --> API: Kết quả kiểm tra
alt Hợp lệ
  API -> DB: Lưu CHO_DUYET cùng\ngiảng viên được chọn
  API --> FE: Mã hồ sơ
else Không hợp lệ
  API --> FE: Lý do không nhận hồ sơ
end

== Giảng viên xét duyệt ==
GV -> FE: Mở hồ sơ gửi đến mình
FE -> API: Gửi quyết định và nhận xét
API -> DB: Kiểm tra đúng giảng viên, trạng thái\nvà sinh viên chưa có GVHD
alt Đồng ý hướng dẫn
  API -> DB: Tạo phân công GVHD, gắn hồ sơ\nvà ghi DA_DUYET trong một giao dịch
else Từ chối
  API -> DB: Cập nhật TU_CHOI và lý do
end
API --> FE: Trạng thái hồ sơ mới
note over SV,FE
  Nếu bị từ chối, trong hạn đăng ký
  có thể sửa hồ sơ cũ hoặc tạo hồ sơ mới,
  rồi chọn giảng viên khác để gửi lại.
end note
@enduml
```

## 4. Sơ đồ Hoạt động

### 4.1. Tiểu luận

```plantuml
@startuml
title Tiểu luận — Từ đề xuất đến kết quả
skinparam defaultFontSize 18
start
:Quản lý tạo lớp và xếp sinh viên;
:Giảng viên đặt hạn đăng ký, hạn nộp,\ngiới hạn nhóm và chế độ chấm;
:Sinh viên làm cá nhân hoặc trưởng nhóm\nthêm thành viên cùng lớp;
:Sinh viên hoặc trưởng nhóm\nđề xuất đề tài và gửi hồ sơ;
if (Giảng viên duyệt?) then (Có)
  :Hồ sơ DA_DUYET;
else (Không)
  :Ghi lý do TU_CHOI;
  :Trong hạn đăng ký, sửa hồ sơ cũ\nhoặc tạo hồ sơ mới;
  stop
endif
:Nộp hoặc thay file báo cáo,\nđánh dấu trễ nếu quá hạn;
:Giảng viên nhận xét và nhập điểm\nchung hoặc riêng từng sinh viên;
if (Đủ điểm cho mọi thành viên?) then (Có)
  :Quản lý duyệt công bố;
  :Mỗi sinh viên xem điểm của mình;
else (Chưa)
  :Giữ trạng thái chưa chấm\nvà chưa công bố;
endif
:Thống kê số sinh viên đạt;
stop
@enduml
```

### 4.2. Đồ án tốt nghiệp

```plantuml
@startuml
title Đồ án tốt nghiệp — Từ đề xuất đến kết quả
skinparam defaultFontSize 18
start
:Quản lý tạo đợt;
:Sinh viên chọn giảng viên,\nnhập đề tài và gửi hồ sơ;
if (Giảng viên đồng ý?) then (Có)
  :Hệ thống tạo phân công GVHD\nvà duyệt hồ sơ;
  :GVHD đặt các mốc nộp;
else (Không)
  :Ghi TU_CHOI và lý do;
  :Trong hạn đăng ký, sinh viên sửa\nhoặc tạo hồ sơ mới, có thể đổi giảng viên;
  stop
endif
:Sinh viên nộp hoặc thay file\ntheo từng mốc;
:Đánh dấu trễ nếu quá hạn;
:GVHD nhận xét mốc trung gian\nvà nhập điểm ở mốc cuối;
if (Đã có điểm?) then (Có)
  :Quản lý duyệt công bố;
  :Sinh viên xem điểm;
else (Chưa)
  :Giữ trạng thái chưa chấm;
endif
:Thống kê số sinh viên đạt\ntrong đợt;
stop
@enduml
```

## Phạm vi chưa triển khai

Sơ đồ không có kho đề tài gợi ý, lời mời xác nhận nhóm, hội đồng, lịch bảo vệ hoặc điểm từng giám khảo. Email đặt lại mật khẩu thuộc chức năng tài khoản; nộp trễ và Quản lý duyệt công bố thuộc bản đầu.
