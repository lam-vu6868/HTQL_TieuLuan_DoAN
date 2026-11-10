# HTTT07 — Sơ đồ UML

Tám sơ đồ PlantUML mô tả hai quy trình và các hoạt động của Quản lý trong HTTT07. Để xem một sơ đồ, sao chép cả khối từ dòng @startuml đến dòng @enduml vào trình xem PlantUML.

| Mục | Sơ đồ | Cách đọc |
| --- | --- | --- |
| 1 | Use Case | Nhìn theo vai trò và nhóm chức năng. |
| 2 | Lớp | Bắt đầu từ Hồ sơ đăng ký, sau đó xem từng nhánh. |
| 3.1–3.2 | Tuần tự | Đọc từ gửi hồ sơ đến quyết định của giảng viên. |
| 4.1–4.2 | Hoạt động | Tiểu luận và Đồ án từ đăng ký đến kết quả. |
| 4.3–4.4 | Hoạt động của Quản lý | Cấp tài khoản, thiết lập lớp, quản lý đợt và lịch bảo vệ. |

## 1. Use Case tổng thể

```plantuml
@startuml
title HTTT07 • Use Case tổng thể
left to right direction
!pragma layout smetana
skinparam shadowing false
skinparam DefaultFontName SansSerif
skinparam defaultFontColor #172B4D
skinparam ArrowColor #718198
skinparam ActorBorderColor #344C69
skinparam UsecaseBorderColor #587499
skinparam UsecaseBackgroundColor #FFFFFF
skinparam PackageBorderColor #CCD6E2
skinparam RectangleBorderColor #B4C4D5
skinparam packageStyle rectangle

actor "Sinh viên" as SV
actor "Nhóm trưởng" as NT
actor "Giảng viên" as GV
actor "Quản lý" as QL

rectangle "HỆ THỐNG HTTT07" {
  package "01  Truy cập" as AUTH #F3F5F8 {
    usecase "Đăng nhập" as LOGIN
    usecase "Tra cứu nhận xét\nvà kết quả" as RESULT
  }
  package "02  Tiểu luận" as ESSAY #EAF3FF {
    usecase "Lập nhóm" as TEAM
    usecase "Quản lý thành viên" as MEMBER
    usecase "Đăng ký đề tài\nvà nộp báo cáo" as TL
    usecase "Thiết lập kế hoạch\nvà giới hạn nhóm" as PLAN
    usecase "Xét duyệt đề tài" as TL_REVIEW
    usecase "Nhận xét, chấm điểm\nvà xem thống kê" as TL_MARK
  }
  package "03  Đồ án tốt nghiệp" as THESIS #E9F7F2 {
    usecase "Chọn người hướng dẫn,\nđăng ký và nộp báo cáo" as DA
    usecase "Xem lịch bảo vệ" as SCHED
    usecase "Xét duyệt đề tài\nvà nhận xét tiến độ" as DA_REVIEW
    usecase "Nhập điểm bảo vệ" as DEF_MARK
  }
  package "04  Quản trị" as ADMIN #FFF5E8 {
    usecase "Cấp tài khoản" as ACCOUNT
    usecase "Quản lý môn, lớp\nvà phân công giảng dạy" as CLASS
    usecase "Quản lý đợt, lịch bảo vệ\nvà phân công nhập điểm" as TERM
    usecase "Xem thống kê Đồ án" as STATS
  }
}

NT --|> SV
SV -- LOGIN
SV -- RESULT
SV -- TEAM
SV -- TL
NT -- MEMBER
NT -- TL
SV -- DA
SV -- SCHED

LOGIN -- GV
PLAN -- GV
TL_REVIEW -- GV
TL_MARK -- GV
DA_REVIEW -- GV
DEF_MARK -- GV

LOGIN -- QL
ACCOUNT -- QL
CLASS -- QL
TERM -- QL
STATS -- QL
@enduml
```

- **Tiểu luận:** Sinh viên xem lớp mình đang học và tự đăng ký, nộp bài nếu làm cá nhân. Nhóm trưởng quản lý thành viên và thực hiện hai thao tác đó thay mặt nhóm.
- **Đồ án:** Sinh viên xem đợt đang mở, chọn giảng viên hướng dẫn và đăng ký cá nhân. Giảng viên được phân công nhập điểm sau khi hội đồng chấm.
- Ở cả hai luồng, người đăng ký có thể chọn đề tài có sẵn hoặc tự đề xuất.

## 2. Sơ đồ Lớp theo hướng đối tượng

Đọc từ lớp trung tâm **Hồ sơ đăng ký**. Tiểu luận và Đồ án cùng kế thừa thao tác gửi, duyệt và từ chối. Phần khác nhau nằm ở **cách tìm người duyệt** và **người thực hiện hồ sơ**.

```plantuml
@startuml
title HTTT07 • Sơ đồ Lớp nghiệp vụ
top to bottom direction
skinparam shadowing false
skinparam DefaultFontName SansSerif
skinparam defaultFontColor #172B4D
skinparam ArrowColor #718198
skinparam ClassBorderColor #587499
skinparam ClassBackgroundColor #FFFFFF
skinparam ClassAttributeIconSize 0
skinparam classFontStyle bold
skinparam nodesep 27
skinparam ranksep 39
skinparam linetype polyline
hide circle
hide empty members

class DichVuDuyetDeTai as "Dịch vụ duyệt đề tài" <<dịch vụ>> #F0F2FA {
  +xetDuyet(hoSo, giangVien, quyetDinh)
}

abstract class HoSoDangKy as "Hồ sơ đăng ký" #FFF4DC {
  -trangThai: TrangThaiHoSo
  +gui()
  +duyet()
  +tuChoi(lyDo)
}
class DeTai as "Đề tài" {
  -ten: str
}
class HoSoTieuLuan as "Hồ sơ Tiểu luận" #EAF3FF {
  +nguoiDuyet(): GiangVien
}
class HoSoDoAn as "Hồ sơ Đồ án" #E9F7F2 {
  -nguoiThucHien: SinhVien
  -giangVienDuocChon: GiangVien
  +nguoiDuyet(): GiangVien
}

class LopHocPhan as "Lớp học phần" #EAF3FF {
  -maLop: str
  -soThanhVienToiThieu: int
  -soThanhVienToiDa: int
  +kiemTraSoThanhVien(soNguoi): bool
}
class NhomTieuLuan as "Nhóm Tiểu luận" #EAF3FF {
  -truongNhom: SinhVien
  +themThanhVien(sv)
  +duDieuKienGui(): bool
}
class DotDoAn as "Đợt Đồ án" #E9F7F2 {
  -maDot: str
  +dangMo(): bool
}
class BuoiBaoVe as "Buổi bảo vệ" #E9F7F2 {
  -thoiGian: datetime
  -hoiDong: HoiDong
  +duocNhapDiem(gv): bool
}

class MocNop as "Mốc nộp" {
  -hanNop: datetime
}
class BaiNop as "Bài nộp" {
  -tepBaoCao: str
  -thoiDiemNop: datetime
  +ghiNhanXet(noiDung)
}
class KetQua as "Kết quả" {
  -diemCuoi: decimal
  +dat(nguong): bool
}

DichVuDuyetDeTai .down.> HoSoDangKy : xét duyệt
DeTai "1" -right- "0..*" HoSoDangKy
HoSoDangKy <|-- HoSoTieuLuan
HoSoDangKy <|-- HoSoDoAn
HoSoTieuLuan "0..*" -down- "1" LopHocPhan
HoSoTieuLuan "0..*" -down- "0..1" NhomTieuLuan
HoSoDoAn "0..*" -down- "1" DotDoAn
HoSoDoAn "0..*" -down- "0..1" BuoiBaoVe
HoSoDangKy "1" -right- "0..*" BaiNop
BaiNop "0..*" -down- "1" MocNop
HoSoDangKy "1" -down- "0..1" KetQua
LopHocPhan -[hidden]right- NhomTieuLuan
NhomTieuLuan -[hidden]right- DotDoAn
DotDoAn -[hidden]right- BuoiBaoVe
@enduml
```

| Nhìn vào | Cách hiểu |
| --- | --- |
| Dòng có dấu trừ | Thuộc tính nội bộ. Ví dụ, lớp học phần giữ giới hạn số thành viên. |
| Dòng có dấu cộng | Phương thức có thể gọi từ bên ngoài. Ví dụ, hàm kiểm tra sĩ số trả về đúng hoặc sai. |
| Mũi tên tam giác rỗng | Kế thừa. Hai loại hồ sơ dùng chung các thao tác của Hồ sơ đăng ký. |
| Số ở đầu đường nối | Số lượng. Ví dụ, một hồ sơ có từ 0 đến nhiều bài nộp và từ 0 đến 1 kết quả. |

Hồ sơ Tiểu luận lấy người duyệt từ giảng viên phụ trách lớp. Hồ sơ có một người làm cá nhân hoặc một nhóm. Hồ sơ Đồ án lấy người duyệt từ giảng viên được sinh viên chọn. Mỗi mốc nộp thuộc một lớp học phần hoặc một đợt đồ án.

Bản tổng quan tập trung vào các lớp trực tiếp xử lý hai quy trình. Tài khoản, Sinh viên, Giảng viên, Môn học, Hội đồng và Dịch vụ đăng ký là các lớp hỗ trợ trong thiết kế chi tiết. Số bảng và các khóa PostgreSQL được xác định trong ERD.

## 3. Sơ đồ Tuần tự duyệt đề tài

Người gửi và người duyệt đã đăng nhập. FastAPI xác thực JWT và kiểm tra quyền theo phạm vi của hồ sơ. Thao tác gửi và thao tác xét duyệt có thể diễn ra ở hai thời điểm khác nhau.

### 3.1. Tiểu luận

```plantuml
@startuml
title HTTT07 • Tuần tự duyệt Tiểu luận
hide footbox
skinparam shadowing false
skinparam DefaultFontName SansSerif
skinparam defaultFontColor #172B4D
skinparam ArrowColor #526C91
skinparam ParticipantBackgroundColor #EAF3FF
skinparam ParticipantBorderColor #6586AB
skinparam SequenceDividerBackgroundColor #EAF3FF
skinparam SequenceGroupBorderColor #B7C9DD

actor "Sinh viên hoặc\nNhóm trưởng" as SV
participant "ReactJS" as UI
participant "FastAPI" as API
database "PostgreSQL" as DB
actor "Giảng viên\nphụ trách lớp" as GV

== 01  Gửi đăng ký ==
SV -> UI: Chọn lớp, chọn hoặc đề xuất đề tài rồi gửi
UI -> API: Gửi đăng ký Tiểu luận
API -> DB: Đọc lớp, thành viên và đề tài nếu có
DB --> API: Trả dữ liệu kiểm tra
API -> API: Kiểm tra thời hạn, người gửi,\nsĩ số và phạm vi đề tài
break Hồ sơ chưa hợp lệ
  API --> UI: Báo lý do để điều chỉnh
end
API -> DB: Lưu hồ sơ CHỜ DUYỆT theo lớp
API --> UI: Trả mã hồ sơ và trạng thái

== 02  Giảng viên xét duyệt ==
GV -> UI: Mở hồ sơ chờ duyệt của lớp
UI -> API: Yêu cầu chi tiết hồ sơ
API -> DB: Đọc hồ sơ theo lớp được phân công
API --> UI: Trả chi tiết hồ sơ
GV -> UI: Chọn duyệt hoặc từ chối
UI -> API: Gửi quyết định xét duyệt
API -> DB: Đọc hồ sơ và phân công lớp
DB --> API: Trả hồ sơ và giảng viên phụ trách
break Sai người duyệt hoặc hồ sơ đã được xử lý
  API --> UI: Báo lý do từ chối thao tác
end
alt Đồng ý
  API -> DB: Ghi ĐÃ DUYỆT
else Từ chối
  API -> DB: Ghi TỪ CHỐI và lý do
end
API --> UI: Trả kết quả xét duyệt
@enduml
```

### 3.2. Đồ án tốt nghiệp

```plantuml
@startuml
title HTTT07 • Tuần tự duyệt Đồ án tốt nghiệp
hide footbox
skinparam shadowing false
skinparam DefaultFontName SansSerif
skinparam defaultFontColor #172B4D
skinparam ArrowColor #477C70
skinparam ParticipantBackgroundColor #E9F7F2
skinparam ParticipantBorderColor #6B9A8C
skinparam SequenceDividerBackgroundColor #E9F7F2
skinparam SequenceGroupBorderColor #AECFC4

actor "Sinh viên" as SV
participant "ReactJS" as UI
participant "FastAPI" as API
database "PostgreSQL" as DB
actor "Giảng viên\nđược chọn" as GV

== 01  Gửi đăng ký cá nhân ==
SV -> UI: Chọn đợt, giảng viên và đề tài
UI -> API: Gửi đăng ký Đồ án
API -> DB: Đọc đợt, giảng viên và đề tài nếu có
DB --> API: Trả dữ liệu kiểm tra
API -> API: Kiểm tra đợt đang mở và phạm vi đề tài
break Hồ sơ chưa hợp lệ
  API --> UI: Báo lý do để điều chỉnh
end
API -> DB: Lưu hồ sơ CHỜ DUYỆT với giảng viên được chọn
API --> UI: Trả mã hồ sơ và trạng thái

== 02  Giảng viên xét duyệt ==
GV -> UI: Mở hồ sơ gửi đến mình
UI -> API: Yêu cầu chi tiết hồ sơ
API -> DB: Đọc hồ sơ theo giảng viên được chọn
API --> UI: Trả chi tiết hồ sơ
GV -> UI: Chọn nhận hướng dẫn hoặc từ chối
UI -> API: Gửi quyết định xét duyệt
API -> DB: Đọc hồ sơ và người được chọn hướng dẫn
DB --> API: Trả hồ sơ và thông tin người duyệt
break Sai người duyệt hoặc hồ sơ đã được xử lý
  API --> UI: Báo lý do từ chối thao tác
end
alt Nhận hướng dẫn
  API -> DB: Ghi ĐÃ DUYỆT và xác nhận người hướng dẫn
else Từ chối
  API -> DB: Ghi TỪ CHỐI và lý do
end
API --> UI: Trả kết quả xét duyệt
@enduml
```

## 4. Sơ đồ Hoạt động

### 4.1. Tiểu luận theo lớp học phần

```plantuml
@startuml
title HTTT07 • Hoạt động Tiểu luận
skinparam shadowing false
skinparam DefaultFontName SansSerif
skinparam defaultFontColor #172B4D
skinparam ArrowColor #587499
skinparam ActivityBorderColor #6586AB
skinparam ActivityBackgroundColor #FFFFFF
skinparam ActivityDiamondBackgroundColor #FFF4DC
skinparam ActivityDiamondBorderColor #A48347
skinparam PartitionBorderColor #C8D8EB

start
partition #EAF3FF "01  Chuẩn bị và đăng ký" {
  :Giảng viên đặt hạn và giới hạn nhóm;
  :Sinh viên chọn lớp mình đang học;
  if (Làm nhóm?) then (Có)
    :Nhóm trưởng thêm thành viên cùng lớp;
  else (Cá nhân)
    :Sinh viên chuẩn bị hồ sơ cá nhân;
  endif
  :Chọn đề tài có sẵn hoặc tự đề xuất rồi gửi;
  if (Hồ sơ hợp lệ?) then (Có)
    :Hệ thống ghi chờ duyệt theo lớp;
  else (Không)
    :Hiển thị lý do để điều chỉnh và gửi lại;
    stop
  endif
}

partition #F3F5F8 "02  Xét duyệt" {
  :Giảng viên phụ trách lớp xem hồ sơ;
  if (Duyệt đề tài?) then (Duyệt)
    :Hệ thống ghi đã duyệt;
  else (Từ chối)
    :Hệ thống ghi từ chối và lý do;
    stop
  endif
}

partition #E9F7F2 "03  Nộp bài và kết quả" {
  :Sinh viên hoặc nhóm trưởng nộp báo cáo theo mốc;
  :Hệ thống ghi file, mốc và thời điểm nộp;
  :Giảng viên nhận xét và nhập điểm cuối;
  :Hệ thống thống kê theo số sinh viên trong lớp;
}
stop
@enduml
```

### 4.2. Đồ án tốt nghiệp cá nhân

```plantuml
@startuml
title HTTT07 • Hoạt động Đồ án tốt nghiệp
skinparam shadowing false
skinparam DefaultFontName SansSerif
skinparam defaultFontColor #172B4D
skinparam ArrowColor #587499
skinparam ActivityBorderColor #6586AB
skinparam ActivityBackgroundColor #FFFFFF
skinparam ActivityDiamondBackgroundColor #FFF4DC
skinparam ActivityDiamondBorderColor #A48347
skinparam PartitionBorderColor #C8D8EB

start
partition #EAF3FF "01  Đăng ký cá nhân" {
  :Sinh viên chọn đợt và giảng viên hướng dẫn;
  :Chọn đề tài có sẵn hoặc tự đề xuất rồi gửi;
  if (Hồ sơ hợp lệ?) then (Có)
    :Hệ thống ghi chờ duyệt cho giảng viên đã chọn;
  else (Không)
    :Hiển thị lý do để điều chỉnh và gửi lại;
    stop
  endif
}

partition #F3F5F8 "02  Xét duyệt và theo dõi" {
  :Giảng viên được chọn xem hồ sơ;
  if (Nhận hướng dẫn?) then (Đồng ý)
    :Hệ thống ghi đã duyệt và xác nhận người hướng dẫn;
  else (Từ chối)
    :Hệ thống ghi từ chối và lý do;
    stop
  endif
  :Sinh viên nộp báo cáo theo mốc và báo cáo cuối;
  :Giảng viên hướng dẫn nhận xét tiến độ;
}

partition #E9F7F2 "03  Bảo vệ và kết quả" {
  :Quản lý ghi lịch, hội đồng và người nhập điểm;
  :Sinh viên bảo vệ, hội đồng chấm điểm;
  :Người được phân công nhập điểm tổng hợp;
  :Hệ thống lưu điểm và thống kê theo đợt;
}
stop
@enduml
```

### 4.3. Quản lý cấp tài khoản và thiết lập lớp học phần

Quản lý đã đăng nhập. Đây là luồng chuẩn bị dữ liệu trước khi sinh viên và giảng viên bắt đầu sử dụng các chức năng Tiểu luận. Có thể dùng lại tài khoản và môn học đã có.

```plantuml
@startuml
title HTTT07 • Quản lý cấp tài khoản và thiết lập lớp
skinparam shadowing false
skinparam DefaultFontName SansSerif
skinparam defaultFontColor #172B4D
skinparam ArrowColor #587499
skinparam ActivityBorderColor #6586AB
skinparam ActivityBackgroundColor #FFFFFF
skinparam ActivityDiamondBackgroundColor #FFF4DC
skinparam ActivityDiamondBorderColor #A48347
skinparam PartitionBorderColor #C8D8EB

start
partition #FFF5E8 "01  Chuẩn bị tài khoản" {
  if (Cần cấp tài khoản mới?) then (Có)
    :Quản lý nhập thông tin và chọn vai trò;
    if (Thông tin và định danh hợp lệ?) then (Có)
      :Hệ thống lưu tài khoản và hồ sơ tương ứng;
    else (Không)
      :Báo lỗi để Quản lý điều chỉnh;
      stop
    endif
  else (Không)
    :Dùng tài khoản đã có;
  endif
}

partition #EAF3FF "02  Thiết lập lớp học phần" {
  :Quản lý chọn hoặc tạo môn học;
  :Tạo lớp theo học kỳ và năm học;
  :Gán giảng viên phụ trách;
  :Đưa sinh viên vào lớp;
  if (Thông tin lớp và phân công hợp lệ?) then (Có)
    :Hệ thống lưu lớp, giảng viên và danh sách lớp;
  else (Không)
    :Báo lỗi để Quản lý điều chỉnh;
    stop
  endif
}

partition #E9F7F2 "03  Dữ liệu sẵn sàng sử dụng" {
  :Giảng viên thấy lớp mình phụ trách;
  :Sinh viên thấy lớp mình đang học;
}
stop
@enduml
```

### 4.4. Quản lý đợt Đồ án và lịch bảo vệ

Quản lý thực hiện hai việc ở hai thời điểm. Đợt được thiết lập trước khi sinh viên đăng ký. Lịch bảo vệ được xếp sau khi có hồ sơ đủ điều kiện.

```plantuml
@startuml
title HTTT07 • Quản lý đợt Đồ án và lịch bảo vệ
skinparam shadowing false
skinparam DefaultFontName SansSerif
skinparam defaultFontColor #172B4D
skinparam ArrowColor #587499
skinparam ActivityBorderColor #6586AB
skinparam ActivityBackgroundColor #FFFFFF
skinparam ActivityDiamondBackgroundColor #FFF4DC
skinparam ActivityDiamondBorderColor #A48347
skinparam PartitionBorderColor #C8D8EB

start
partition #FFF5E8 "01  Thiết lập đợt Đồ án" {
  :Quản lý tạo đợt Đồ án;
  :Đặt thời gian đăng ký và các mốc nộp;
  if (Kế hoạch hợp lệ?) then (Có)
    :Hệ thống lưu đợt và kế hoạch;
  else (Không)
    :Báo lỗi để Quản lý điều chỉnh;
    stop
  endif
}

partition #F3F5F8 "02  Khi có hồ sơ để xếp lịch" {
  :Quản lý chọn hồ sơ thuộc đợt;
  if (Hồ sơ đã duyệt và đủ điều kiện bảo vệ?) then (Có)
    :Tạo hoặc chọn hội đồng và thành viên;
    :Chọn thời gian và địa điểm;
    :Phân công giảng viên nhập điểm hội đồng;
    :Hệ thống lưu lịch và phân công;
  else (Không)
    :Hiển thị lý do hồ sơ chưa được xếp lịch;
    stop
  endif
}

partition #E9F7F2 "03  Sử dụng lịch đã lưu" {
  :Sinh viên xem lịch bảo vệ;
  :Giảng viên được phân công có thể nhập điểm sau khi hội đồng chấm;
}
stop
@enduml
```

Quản lý có thể xem thống kê theo đợt ở bất kỳ thời điểm nào. Khi chưa có điểm, hồ sơ đã duyệt được tính vào nhóm chưa chấm theo phương án ERD hiện tại. Điều kiện cụ thể để hồ sơ đủ điều kiện bảo vệ cần chốt trước khi triển khai tính năng xếp lịch.

## Ghi chú nghiệp vụ

- Tiểu luận kiểm tra người gửi, tư cách thuộc lớp, thời gian đăng ký và số thành viên. Nhóm trưởng được tính vào sĩ số.
- Bản thiết kế dùng phương án một điểm chung cho nhóm Tiểu luận và một điểm tổng hợp của hội đồng cho mỗi hồ sơ Đồ án. Thống kê đếm theo sinh viên.
- Ngưỡng đạt và cách xử lý nộp trễ cần xác nhận theo quy định của môn hoặc đợt. Nhánh yêu cầu chỉnh sửa đề tài là chức năng bổ sung.

