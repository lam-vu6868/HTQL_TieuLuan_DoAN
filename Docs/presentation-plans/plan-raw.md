# Kế hoạch rút gọn: chỉ làm một lát cắt dọc đủ chứa 4 ý thực hành, phần còn lại của kế hoạch full để sau.

**Thứ tự đề xuất**

| Bước                 | Việc                                                                                                                                                  | Lấy từ chặng nào của kế hoạch full |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------- |
| 1. Chốt lát cắt      | Chọn phạm vi nhỏ: đăng nhập đơn giản, lớp, hồ sơ đăng ký đề tài (xem danh sách, gửi hồ sơ), báo cáo thống kê hồ sơ theo lớp                           | Mới, rút từ chặng 2 và 3           |
| 2. UML cho lát cắt   | Use Case và sơ đồ lớp chỉ gồm các lớp của lát cắt (ví dụ `TaiKhoan`, `LopHocPhan`, `HoSoDangKy`, `HoSoRepository`, `HoSoService`)                     | Giai đoạn UML bạn đang làm         |
| 3. Nền tảng và ORM   | FastAPI async, PostgreSQL, SQLAlchemy async, khoảng 4 đến 5 bảng, tầng Repository (DAL). Có thể dùng `create_all` thay Alembic để tiết kiệm thời gian | Chặng 1 rút gọn                    |
| 4. Dữ liệu lớn       | Seed vài nghìn dòng hồ sơ để báo cáo "nặng" đủ chậm mà demo thấy rõ                                                                                   | Chặng 1 (dữ liệu demo)             |
| 5. Tác vụ nặng async | Làm endpoint xuất báo cáo bản **đồng bộ** (chặn) và bản **async/tác vụ nền**, React hiện trạng thái đang xử lý và vẫn bấm được                        | Mới, thay cho chặng 4              |
| 6. API ngoài         | Widget tỷ giá hoặc thời tiết bằng `httpx.AsyncClient` và Pydantic, đặt ở dashboard                                                                    | Mới, làm tạm cho thuyết trình      |
| 7. Slide và tập dượt | Lý thuyết ghép với demo, quay sẵn video dự phòng phòng khi demo lỗi                                                                                   | Mới                                |

**Phần bỏ hoặc hoãn so với kế hoạch full**

- Chặng 2: phân quyền chi tiết theo đối tượng, email đặt lại mật khẩu, gán GVHD.
- Chặng 3: nhóm, chuyển trưởng nhóm, duyệt hoặc từ chối, sửa và gửi lại, Đồ án.
- Chặng 4: nộp file, mốc nộp, chấm điểm, công bố, thống kê đạt.
- Chặng 5: kiểm thử đầy đủ, README cho người khác chạy.

Nếu sau này cần làm tiếp đồ án đầy đủ thì lát cắt này vẫn dùng lại được, vì nó chính là phần đầu của chặng 1 và 3.

## Kế hoạch ngắn hạn cho kịp thuyết trình

**1. Đổi sang tên tiếng Anh.** Quy ước gợi ý: bảng `snake_case` số nhiều, lớp Python `PascalCase` số ít, giao diện người dùng vẫn hiển thị tiếng Việt.

| Tiếng Việt (tài liệu bạn bạn)      | Tiếng Anh                         |
| ---------------------------------- | --------------------------------- |
| `tai_khoan`                        | `accounts`                        |
| `sinh_vien`, `giang_vien`          | `students`, `lecturers`           |
| `mon_hoc`, `lop_hoc_phan`          | `courses`, `course_sections`      |
| `ho_so_dang_ky`                    | `topic_registrations`             |
| `nop_tre`                          | `is_late`                         |
| `CHO_DUYET`, `DA_DUYET`, `TU_CHOI` | `PENDING`, `APPROVED`, `REJECTED` |

Lưu ý:

- Bộ tài liệu hiện tại viết bằng tiếng Việt, nên cần lập một bảng đối chiếu như trên. Nếu không, sơ đồ lớp, CSDL và code sẽ lệch tên nhau. Thay đổi áp dụng toàn bộ kể cả các sơ đồ.

## Thứ tự triển khai

| Bước | Việc                                                                                                                                                            | Xong khi                                    |
| ---- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------- |
| 1    | Khung dự án: repo, FE/BE/DB, `.env`, `.gitignore`. **Chạy PostgreSQL bằng Docker Compose ngay từ đầu** (chỉ service `db`), BE và FE vẫn chạy trực tiếp trên máy | `docker compose up` lên DB, BE kết nối được |
| 2    | Mô hình dữ liệu: model SQLAlchemy async, các bảng tiếng Anh, tạo bảng bằng `create_all` (hoặc Alembic nếu còn thời gian)                                        | Bảng được tạo trong DB                      |
| 3    | Tầng DAL: lớp Repository (`TopicRegistrationRepository`...) và lớp Service                                                                                      | Gọi được CRUD qua service                   |
| 4    | API của lát cắt: danh sách và tạo hồ sơ đăng ký, trả JSON qua Pydantic schema                                                                                   | Swagger thử được                            |
| 5    | **JWT** (xem bên dưới)                                                                                                                                          | Đăng nhập, gọi API có token                 |
| 6    | Dữ liệu lớn (vài nghìn dòng) và **báo cáo nặng**: bản đồng bộ chặn server, bản async/tác vụ nền                                                                 | Thấy rõ khác biệt khi demo                  |
| 7    | **API ngoài**: `httpx.AsyncClient`, Pydantic parse JSON, endpoint trung gian cho FE                                                                             | Widget hiển thị dữ liệu                     |
| 8    | Giao diện React: đăng nhập, danh sách hồ sơ, nút xuất báo cáo (trạng thái đang xử lý), widget                                                                   | Demo chạy trọn kịch bản                     |
| 9    | **Đóng gói Docker đầy đủ** (xem bên dưới)                                                                                                                       | Một lệnh dựng cả hệ thống                   |
| 10   | Viết báo cáo word, Slide, tập dượt                                                                                                                              | Có bản chạy thử trước ngày thuyết trình     |

Sơ đồ Use Case và Class làm song song bước 2 đến 4, rồi chỉnh lại cho khớp code sau bước 4.

## JWT: làm tối thiểu trước

Phần này không phải nội dung chính của đề bài, nên đừng để nó ngốn thời gian.

- **Bản tối thiểu (bước 5):** endpoint đăng nhập, access token ngắn hạn (khoảng 15 phút), dependency kiểm tra token ở các API của lát cắt. Mật khẩu băm bằng bcrypt hoặc argon2. Bên FE lưu tạm localStoarge.
- **Bản nâng cấp:** refresh token lưu băm và hạn dùng trong bảng `refresh_tokens`, bản gốc đặt trong cookie `httpOnly`; access token giữ trong bộ nhớ React (không dùng localStorage), axios interceptor tự xin token mới khi hết hạn.
- Về HTTPS: trong Docker bạn không cần HTTPS thật. Cách đơn giản là để nginx phục vụ FE và chuyển tiếp `/api` sang BE, khi đó FE và API cùng một origin nên cookie đỡ rắc rối. Mình chưa chắc cookie `Secure` hoạt động ổn trên mọi trình duyệt khi chạy http://localhost, nên khi tới bước này cần thử thật.

## Docker: chia hai mức

- **Sớm (bước 1):** chỉ container PostgreSQL, kèm volume để giữ dữ liệu.
- **Cuối (bước 9):** thêm hai service. BE dùng Dockerfile (Python, `uvicorn`); FE build bằng nhiều giai đoạn rồi phục vụ bằng nginx. Compose có `healthcheck` cho DB để BE chờ DB sẵn sàng, và một lệnh seed dữ liệu demo.
- Nên thử `docker compose up` trên máy sạch (hoặc `down -v` rồi dựng lại) trước ngày thuyết trình.

## Quy tắc giữ kịp tiến độ

- Dừng thêm tính năng mới trước ngày thuyết trình khoảng 3 ngày; chỉ sửa lỗi và làm slide.
- Nếu trễ, thứ tự cắt giảm: refresh token trước, rồi Alembic, cuối cùng mới đến giao diện đẹp. Báo cáo async và API ngoài là phần đề bài yêu cầu nên không cắt.

Thứ tự thực hiện mình đề xuất, không kèm thời gian:

1. **Khung dự án và PostgreSQL bằng Docker** (bước bạn sẽ tìm hiểu ở chat khác).
2. **Model SQLAlchemy async và tầng Repository/Service theo OOP.** Làm trọn một lớp mẫu `TopicRegistration` rồi lặp lại cho các lớp còn lại. Vẽ Use Case đánh dấu, Class diagram và ERD song song ở bước này.
3. **API của lát cắt** (danh sách và tạo hồ sơ, Pydantic schema), rồi **JWT bản tối thiểu**. Phần này bạn đã quen tay.
4. **Thí nghiệm nhỏ về async** (hai endpoint `time.sleep` và `asyncio.sleep`, gọi song song). Đọc lý thuyết event loop, I/O-bound và CPU-bound ngay lúc này, vì đây là chỗ bạn chưa tiếp cận.
5. **Seed dữ liệu và báo cáo nặng**: bản đồng bộ, bản async/tác vụ nền, đo thời gian. Vẽ Sequence và Activity cho luồng xuất báo cáo.
6. **API ngoài** (`httpx.AsyncClient` và Pydantic) cùng Sequence tương ứng.
7. **Giao diện React**: đăng nhập, danh sách hồ sơ, nút xuất báo cáo có trạng thái đang xử lý, widget.
8. **Đóng gói Docker đầy đủ**, thử dựng lại trên máy sạch.
9. **Hoàn thiện Word, slide, tập dượt, quay video dự phòng.**

Trong suốt quá trình, mỗi phần chạy được thì viết luôn phần Word tương ứng. Riêng đoạn lý thuyết đa luồng (so sánh thread, async, process) viết sau bước 4, khi bạn đã tự thấy khác biệt.

Mình đã ghi lại các điểm chốt trong chat này vào bộ nhớ của dự án, nên khi sang chat khác bạn có thể tiếp tục từ bước 1.
