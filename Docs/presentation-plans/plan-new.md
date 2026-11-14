# Kế hoạch thuyết trình Chủ đề 9: Async/Await & tích hợp API

> Chỉ làm **một lát cắt dọc** của đồ án, đủ chứa các ý thực hành của đề bài. Phần còn lại của kế hoạch full để sau. Lát cắt này chính là phần đầu của chặng 1 và 3 nên dùng lại được.

## 1. Đề bài và cách đáp ứng

| Đề bài                                 | Đáp ứng bằng                                                   |
| -------------------------------------- | -------------------------------------------------------------- |
| Đa luồng và bất đồng bộ trong OOP      | Báo cáo nặng: bản đồng bộ so với bản async/tác vụ nền (bước 5) |
| GUI bị "treo" và giải pháp async/await | React vẫn bấm được khi báo cáo chạy nền (bước 5, 7)            |
| REST API, JSON serialize/deserialize   | Pydantic schema và widget `httpx` (bước 3, 6)                  |
| Vẽ Use Case và Class thực tế           | UML của lát cắt (bước 2)                                       |
| Tích hợp ORM vào tầng DAL              | SQLAlchemy async trong lớp Repository (bước 2)                 |
| Báo cáo nặng dạng async để UI không đơ | Bước 5                                                         |
| Gọi API ngoài (tỷ giá, thời tiết)      | Widget ở dashboard (bước 6)                                    |

JWT và Docker không nằm trong đề bài, nên chỉ làm mức đủ dùng.

## 2. Phạm vi lát cắt

**Làm:** đăng nhập đơn giản, lớp học phần, hồ sơ đăng ký đề tài (xem danh sách, gửi hồ sơ), báo cáo thống kê hồ sơ theo lớp.

**Danh sách trong lát cắt là hồ sơ đăng ký đề tài** (`topic_registrations`), không phải danh sách sinh viên. Sinh viên, giảng viên, môn học chỉ là dữ liệu nền (seed sẵn), không làm API riêng.

**Hoãn lại (thuộc kế hoạch full):**

- Chặng 2: phân quyền chi tiết theo đối tượng, email đặt lại mật khẩu, gán GVHD.
- Chặng 3: nhóm, chuyển trưởng nhóm, duyệt hoặc từ chối, sửa và gửi lại, đồ án.
- Chặng 4: nộp file, mốc nộp, chấm điểm, công bố, thống kê đạt.
- Chặng 5: kiểm thử đầy đủ, README cho người khác chạy.

## 3. Quy ước đặt tên (chốt trước khi code)

Bảng `snake_case` số nhiều, lớp Python `PascalCase` số ít, giao diện vẫn hiển thị tiếng Việt. Áp dụng cho cả sơ đồ, CSDL và code, nếu không các phần sẽ lệch tên nhau.

| Tiếng Việt                         | Tiếng Anh                         |
| ---------------------------------- | --------------------------------- |
| `tai_khoan`                        | `accounts`                        |
| `sinh_vien`, `giang_vien`          | `students`, `lecturers`           |
| `mon_hoc`, `lop_hoc_phan`          | `courses`, `course_sections`      |
| `ho_so_dang_ky`                    | `topic_registrations`             |
| `nop_tre`                          | `is_late`                         |
| `CHO_DUYET`, `DA_DUYET`, `TU_CHOI` | `PENDING`, `APPROVED`, `REJECTED` |

Nếu có bạn trong nhóm đang dùng tài liệu tiếng Việt, cần báo bảng đối chiếu này.

## 4. Thứ tự thực hiện

Làm theo thứ tự, tick khi xong. Không đặt mốc thời gian; xem mục 8 để biết khi nào cắt.

- [x] **Bước 1. Khung dự án và DB.** Repo, FE/BE, `.env`, `.gitignore`. Chạy PostgreSQL bằng Docker Compose ngay từ đầu (chỉ service `db`, có volume), BE và FE vẫn chạy trực tiếp trên máy.
      _Xong khi:_ `docker compose up` lên DB và BE kết nối được.

- [ ] **Bước 2. Model, ORM, tầng DAL theo OOP.** Model SQLAlchemy async với tên tiếng Anh, 4 đến 5 bảng, tạo bằng `create_all` (Alembic nếu còn thời gian). Viết lớp Repository và lớp Service, inject bằng `Depends`. Làm trọn một lớp mẫu `TopicRegistration` rồi lặp lại cho các lớp còn lại.
      _Xong khi:_ gọi được CRUD qua Service.
      _Song song:_ vẽ UML (mục 5).

- [ ] **Bước 3. API của lát cắt và JWT tối thiểu.**
  - `GET /api/registrations`: danh sách hồ sơ, trả mảng JSON.
  - `POST /api/registrations`: gửi hồ sơ mới, trả hồ sơ vừa tạo.
  - Pydantic schema tách hai lớp: `TopicRegistrationCreate` (dữ liệu vào) và `TopicRegistrationRead` (dữ liệu ra, `from_attributes=True`). Đây là chỗ minh họa JSON Deserialization và Serialization.
  - JWT bản tối thiểu (mục 7).
    _Xong khi:_ thử được trên Swagger, đăng nhập rồi gọi API có token.

- [ ] **Bước 4. Thí nghiệm async nhỏ (học trước khi làm báo cáo).** Viết hai endpoint thử: một dùng `time.sleep`, một dùng `asyncio.sleep`, rồi gọi song song nhiều request để thấy server đứng hay không. Đọc lý thuyết đúng lúc này: I/O-bound và CPU-bound, event loop làm gì khi gặp `await`, `BackgroundTasks`, `asyncio.to_thread`.
      _Xong khi:_ giải thích được vì sao có bản "async" mà server vẫn đơ.

- [ ] **Bước 5. Dữ liệu lớn và báo cáo nặng.**
  - Seed vài nghìn dòng hồ sơ (dùng `faker` hoặc vòng lặp random, không cần dữ liệu đẹp). Đo và tăng số dòng, hoặc thêm tính toán, cho tới khi báo cáo mất khoảng 3 đến 5 giây. Nếu vẫn chưa đủ chậm thì mới thêm bước chờ giả lập.
  - **Bản đồng bộ:** server xử lý xong mới trả; trong lúc đó các request khác (ví dụ `/health`) bị treo.
  - **Bản async/tác vụ nền:** trả ngay `202` kèm `job_id`, việc nặng chạy nền, có endpoint hỏi trạng thái (`PENDING`, `RUNNING`, `DONE`), xong thì tải kết quả. Dùng `BackgroundTasks` và dict trong bộ nhớ lưu trạng thái là đủ cho demo.
  - Lưu ý: `async def` chỉ giúp khi **chờ I/O**. Phần tính toán nặng chạy thẳng trong `async def` vẫn chặn event loop, cần đẩy sang thread hoặc tác vụ nền.
  - Ghi lại bảng thời gian đo được, dùng cho Word và slide.
    _Xong khi:_ demo thấy rõ khác biệt giữa hai bản.

- [ ] **Bước 6. API ngoài.** `httpx.AsyncClient` gọi tỷ giá hoặc thời tiết, Pydantic parse JSON, endpoint trung gian cho FE.
      _Xong khi:_ widget hiển thị được dữ liệu.

- [ ] **Bước 7. Giao diện React.** Đăng nhập, danh sách hồ sơ, nút xuất báo cáo (hiện trạng thái đang xử lý, hỏi trạng thái định kỳ, các nút khác vẫn bấm được), widget.
      _Xong khi:_ chạy trọn kịch bản demo.

- [ ] **Bước 8. Đóng gói Docker đầy đủ.** Thêm hai service: BE (Dockerfile, `uvicorn`) và FE (build nhiều giai đoạn, nginx, chuyển tiếp `/api` sang BE). Compose có `healthcheck` cho DB và một lệnh seed. Thử `docker compose down -v` rồi dựng lại, tốt nhất trên máy sạch.
      _Xong khi:_ một lệnh dựng cả hệ thống.

- [ ] **Bước 9. Hoàn thiện Word, slide, tập dượt.** Quay sẵn video demo dự phòng phòng khi demo lỗi.
      _Xong khi:_ có bản chạy thử trọn vẹn trước ngày thuyết trình.

## 5. UML cho lát cắt

Không vẽ lại từ đầu, chỉ lọc từ cái đã có rồi bổ sung. Vẽ song song bước 2 đến 3, rồi chỉnh lại cho khớp code.

**Dùng lại:**

- **Use Case tổng quát:** giữ nguyên, tô đậm hoặc viền đậm use case thuộc lát cắt (Đăng nhập, Xem danh sách hồ sơ, Gửi hồ sơ đăng ký, Xuất báo cáo thống kê), để xám phần chưa làm, thêm ô chú thích "đậm = phạm vi demo, xám = để sau". Có thể vẽ thêm một Use Case nhỏ chỉ gồm 4 use case này cho slide. `Có thể vẽ mới riêng nếu cần.`
- **Activity đầy đủ:** chỉ lấy luồng gửi hồ sơ đăng ký.

**Vẽ mới:**

- Activity cho luồng xuất báo cáo.
- Class diagram của lát cắt: `Account`, `CourseSection`, `TopicRegistration`, Repository, Service (tên tiếng Anh).
- ERD cho 4 đến 5 bảng.
- Sequence (quan trọng nhất): báo cáo đồng bộ so với async (client, API, tác vụ nền, DB), và luồng gọi API ngoài bằng `httpx`.
- Deployment (nginx, BE, DB trong Docker Compose), nếu muốn có hình cho phần Docker.

**Mức tối thiểu nếu thiếu thời gian:** Use Case đánh dấu, Class, ERD, hai Sequence và một Activity cho xuất báo cáo.

## 6. Cấu trúc Word: lý thuyết đi cùng thực hành

Mỗi nội dung theo vòng: **lý thuyết, sơ đồ, đoạn code chính, kết quả demo**. Viết từng phần ngay khi phần code tương ứng chạy được, để có số liệu thật. Phần UML và mô tả lát cắt đặt ngắn ở đầu, làm bối cảnh.

| Phần              | Lý thuyết                                                                                                                 | Thực hành tương ứng                                      |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| Đa luồng và async | thread, async, process; vì sao FastAPI chọn async cho việc chờ I/O; event loop; I/O-bound và CPU-bound; vì sao UI bị treo | báo cáo đồng bộ so với async, kèm bảng thời gian đo được |
| API ngoài, JSON   | HTTP client bất đồng bộ, serialize/deserialize, validate bằng Pydantic                                                    | widget `httpx.AsyncClient` và schema Pydantic            |
| ORM, tầng DAL     | Repository, Service, tách tầng trong OOP                                                                                  | lớp Repository với SQLAlchemy async                      |
| JWT               | cấu trúc token, xác thực không trạng thái                                                                                 | đăng nhập, dependency kiểm tra token                     |
| Docker            | image, container, compose                                                                                                 | một lệnh dựng cả hệ thống                                |

Đoạn lý thuyết đa luồng nên viết sau bước 4, khi đã tự thấy khác biệt. Hệ thống thật thường dùng hàng đợi như Celery hoặc RQ, chỉ cần nhắc tới trong lý thuyết.

## 7. JWT và Docker: làm vừa đủ

**JWT** không phải nội dung chính, đừng để nó ngốn thời gian.

- **Bản tối thiểu (bước 3):** endpoint đăng nhập, access token ngắn hạn (khoảng 15 phút), dependency kiểm tra token, mật khẩu băm bằng bcrypt hoặc argon2. FE tạm lưu bằng `localStorage`.
- **Bản nâng cấp (chỉ khi dư thời gian):** refresh token lưu băm và hạn dùng trong bảng `refresh_tokens`, bản gốc nằm trong cookie `httpOnly`; access token giữ trong bộ nhớ React; axios interceptor tự xin token mới khi hết hạn.
- Trong Docker không cần HTTPS thật. Để nginx phục vụ FE và chuyển tiếp `/api` sang BE, khi đó FE và API cùng origin nên cookie đỡ rắc rối. Chưa chắc cookie `Secure` chạy ổn trên mọi trình duyệt khi dùng `http://localhost`, cần thử thật khi tới bước này.

**Docker** chia hai mức:

- **Sớm (bước 1):** chỉ container PostgreSQL kèm volume.
- **Cuối (bước 8):** thêm BE và FE, `healthcheck` cho DB, lệnh seed.
