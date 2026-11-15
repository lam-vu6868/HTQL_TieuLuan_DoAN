<div align="center">

# 📚 HTTT07

### Hệ thống Quản lý Đề tài Tiểu luận và Đồ án tốt nghiệp

_Đưa việc đăng ký, nộp bài và chấm điểm về một nơi, thay cho bảng tính và tin nhắn rải rác._

![React](https://img.shields.io/badge/Frontend-ReactJS-61DAFB?logo=react&logoColor=white)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI_async-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Deploy-Docker-2496ED?logo=docker&logoColor=white)

</div>

---

## ✨ Giới thiệu

**HTTT07** là đồ án môn _Ứng dụng OOP_, hướng tới việc hỗ trợ quản lý tiểu luận và đồ án tốt nghiệp cho sinh viên ngành Công nghệ thông tin, Đại học Bình Dương.

Hệ thống phục vụ ba nhóm người dùng:

| Vai trò           | Có thể làm gì                                                                                  |
| ----------------- | ---------------------------------------------------------------------------------------------- |
| 🎓 **Sinh viên**  | Đăng ký đề tài (cá nhân hoặc theo nhóm), nộp file báo cáo theo tiến độ, xem nhận xét và điểm   |
| 👩‍🏫 **Giảng viên** | Duyệt đề tài và phản hồi, theo dõi tiến độ, chấm điểm và nhận xét                              |
| 🛠️ **Quản lý**    | Quản lý tài khoản sinh viên/giảng viên, học phần, gán giảng viên hướng dẫn, duyệt công bố điểm |

Hệ thống hỗ trợ hai quy trình: **Tiểu luận** (theo lớp học phần) và **Đồ án tốt nghiệp** (theo đợt, có giảng viên hướng dẫn).

## 🧰 Công nghệ

- **Frontend:** ReactJS
- **Backend:** FastAPI (async), thiết kế theo hướng **OOP**, truy cập dữ liệu bằng SQLAlchemy async
- **Cơ sở dữ liệu:** PostgreSQL
- **Xác thực:** JWT
- **Đóng gói:** Docker

File báo cáo được lưu trên máy chủ backend; PostgreSQL chỉ giữ thông tin bài nộp và đường dẫn nội bộ.

## 🗂️ Cấu trúc thư mục

```bash
HTTT07/
├── 📁 BE/                      # API, nghiệp vụ, truy cập dữ liệu, nơi lưu file báo cáo
├── 📁 DB/                      # Migration PostgreSQL và dữ liệu demo
├── 📁 Docs/                    # Tài liệu phân tích, thiết kế
│   ├── 📁 presentation-plans/  #Kế hoạch cho các bài thuyết trình
│   ├── 📝 01-phan-tich-nghiep-vu.md
│   ├── 📝 02-so-do-uml.md
│   ├── 📝 03-ke-hoach-trien-khai.md
│   ├── 📝 04-thiet-ke-co-so-du-lieu.md
│   └── 📝 05-huong-dan-lam-viec-voi-git.md
├── 📁 Web-test/                # Bản thực hành cho bài thuyết trình Chủ đề 9
│   ├── 📁 BACKEND/             # FastAPI async + PostgreSQL
│   ├── 📁 FRONTEND/            # Giao diện ReactJS
│   └── ⚙️ .gitignore
└── 📝 README.md
```

> 🚧 **Trạng thái:** dự án đang trong giai đoạn xây dựng; hiện mới có tài liệu và bộ khung ban đầu, bộ khung này chưa chắc đã chính xác nên tạm thời thử nghiệm trên thư mục Web-test. Thư mục `FE/` sẽ được bổ sung khi làm frontend chính.

## 📖 Tài liệu

1. [Phân tích nghiệp vụ](./Docs/01-phan-tich-nghiep-vu.md): vai trò và hai quy trình
2. [Sơ đồ UML](./Docs/02-so-do-uml.md): Use Case, Lớp, Tuần tự và Hoạt động
3. [Kế hoạch triển khai](./Docs/03-ke-hoach-trien-khai.md): thứ tự thực hiện từng chặng
4. [Thiết kế cơ sở dữ liệu](./Docs/04-thiet-ke-co-so-du-lieu.md): 14 bảng và ràng buộc
5. [Hướng dẫn làm việc với Git](./Docs/05-huong-dan-lam-viec-voi-git.md): quy trình làm việc nhóm

## 👥 Thành viên

| MSSV     | Họ và tên           | Vai trò          |
| -------- | ------------------- | ---------------- |
| 23050102 | **Lý Lâm Vũ**       | 👑 Sếp           |
| 23050118 | **Nguyễn Tuấn Anh** | 🏃 Chân chạy vặt |

## 🤖 AI hỗ trợ

Nhóm có tham khảo và nhờ các công cụ AI hỗ trợ trong quá trình phân tích, thiết kế và viết tài liệu:

**ChatGPT** · **Claude** · **Gemini** · **DeepSeek**

<div align="center">

### ✨ This file was made by Claude AI ✨

</div>
