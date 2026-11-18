# 🎯 Kế hoạch thuyết trình — Chủ đề 9: Async/Await & Tích hợp API

> 💡 Phạm vi thu gọn: phần thực hành dừng ở **ORM → tầng DAL → tích hợp REST API (JSON serialize/deserialize)**, cộng với **demo UI bị treo** và **gọi API ngoài**. Chưa đụng nghiệp vụ, chưa có đăng nhập. Phần còn lại thuộc kế hoạch full (`03-ke-hoach-trien-khai.md`).
> Cơ sở lý thuyết và thiết kế demo chi tiết: `suy_luan.md` (bản chốt của nhóm).

---

## 1. 📋 Đề bài và cách đáp ứng

|  #  | Đề bài                                 | Đáp ứng bằng                                                                    |
| :-: | :------------------------------------- | :------------------------------------------------------------------------------ |
|  1  | Đa luồng và bất đồng bộ trong OOP      | Thí nghiệm async (bước 5) và tác vụ nặng sync so với `BackgroundTasks` (bước 7) |
|  2  | GUI bị "treo" và giải pháp async/await | Demo 1 và Demo 2 trên React (bước 6, 7)                                         |
|  3  | REST API, JSON serialize/deserialize   | Schema Pydantic `Read` cho các GET (bước 4), parse JSON API ngoài (bước 5)      |
|  4  | Vẽ Use Case và Class thực tế           | Sơ đồ có sẵn của nhóm, đổi tên sang tiếng Anh (mục 5)                           |
|  5  | Tích hợp ORM vào tầng DAL              | SQLAlchemy async + `BaseRepository` generic (bước 2, 3)                         |
|  6  | Tác vụ nặng dạng async để UI không đơ  | Bước 7                                                                          |
|  7  | Gọi API ngoài                          | Open-Meteo bằng `httpx.AsyncClient` (bước 5, 6)                                 |

---

## 2. 🎬 Phạm vi

### ✅ Làm

- Model ORM cho **đủ 14 bảng** của `04-thiet-ke-co-so-du-lieu.md`.
- Tầng DAL cho tất cả bảng: một `BaseRepository` generic, mỗi bảng kế thừa.
- Schema Pydantic `Read` và API **GET đơn giản** (danh sách có phân trang, xem theo id), không cần token.
- API thời tiết (Open-Meteo) qua `httpx.AsyncClient`, có mock fallback.
- Các endpoint phục vụ demo UI treo (`slow-1s/2s/3s`, tác vụ nặng).
- React: trang demo.

### ❌ Không làm (để sau)

| Hạng mục                                      | Ghi chú                                                               |
| :-------------------------------------------- | :-------------------------------------------------------------------- |
| Đăng nhập, JWT, phân quyền                    | Các GET demo để mở, không cần token                                   |
| Nghiệp vụ (duyệt đề tài, nhóm, nộp bài, chấm) | Thuộc chặng 2 đến 4 của kế hoạch full                                 |
| POST, PUT, DELETE                             | Chỉ GET, nên chưa cần schema `Create`                                 |
| Lớp Service có nghiệp vụ                      | Nếu muốn đủ kiến trúc trong slide thì chỉ giữ lớp mỏng gọi Repository |
| Sơ đồ vẽ mới                                  | Chỉ đổi tên sơ đồ có sẵn                                              |

---

## 3. 🏷️ Quy ước đặt tên

> 📏 Bảng `snake_case` số nhiều, lớp Python `PascalCase` số ít, cột `snake_case`, enum `UPPER_SNAKE_CASE`, giao diện vẫn hiển thị tiếng Việt.

Bảng đối chiếu đầy đủ cho **14 bảng, lớp Python, enum và cột hay gặp** nằm ở **mục 0 của `04-thiet-ke-co-so-du-lieu.md`**. Dùng đúng bảng đó cho sơ đồ, CSDL và code để các phần không lệch tên nhau. Có bạn trong nhóm đang dùng tài liệu tiếng Việt nên cần báo bảng đối chiếu này.

---

## 4. 🪜 Thứ tự thực hiện

> 🧭 Làm theo thứ tự, tick khi xong. Không đặt mốc thời gian; xem mục 8 để biết khi nào cắt. Làm đến đâu tạo đến đó, không tạo sẵn file hàng loạt.

### ✅ Bước 1 — Khung dự án và DB

- [x] Repo, FE/BE, `.env`, `.gitignore`. PostgreSQL chạy bằng Docker Compose (service `db`, có volume), BE và FE chạy trực tiếp trên máy.
- [x] BE `/health` trả JSON báo kết nối DB thành công.

### ⬜ Bước 2 — Model ORM cho đủ 14 bảng

- [x] 5 bảng đầu: `accounts`, `students`, `lecturers`, `course_sections`, `topic_registrations`; `enums.py`; `database.py` (async engine/session).
- [ ] Đối chiếu 5 model đã code với `04` mới (tên cột, tên enum); sai lệch thì sửa theo `04`.
- [ ] 9 bảng còn lại: `courses`, `section_students`, `project_periods`, `supervisor_assignments`, `essay_groups`, `group_members`, `milestones`, `submissions`, `results`.
- [ ] Setup Alembic, tạo migration đầu tiên, `upgrade head`. (Nếu vướng thì dùng `create_all`, Alembic làm sau.)
- 🎯 _Xong khi:_ migration chạy ra đủ 14 bảng, kiểm tra được trong pgAdmin.

### ⬜ Bước 3 — Tầng DAL theo OOP

- [ ] `BaseRepository[T]` generic: `get_by_id`, `list` (có `limit/offset`), `count`, và các thao tác CRUD cơ bản.
- [ ] Mỗi bảng một Repository kế thừa; chỉ thêm truy vấn riêng khi cần.
- [ ] Inject Repository bằng `Depends`.
- 🎯 _Xong khi:_ gọi được Repository của từng bảng và lấy dữ liệu đúng.

### ⬜ Bước 4 — Pydantic và API GET

- [ ] Schema `Read` cho các bảng (`from_attributes=True`). Đây là chỗ minh họa **JSON Serialization**.
- [ ] GET danh sách (có phân trang) và GET theo id cho các bảng chính; bảng phụ làm thêm nếu còn thời gian.
- [ ] Seed ít dữ liệu theo thứ tự khóa ngoại (đủ để các danh sách GET không rỗng, có một bảng khoảng vài trăm đến vài nghìn dòng để thử phân trang).
- 🎯 _Xong khi:_ thử được các GET trên Swagger.

### ⬜ Bước 5 — Thí nghiệm async + API ngoài

- [ ] Thí nghiệm nhỏ: endpoint dùng `time.sleep` và endpoint dùng `asyncio.sleep`; `async def` chứa code blocking và `def` thường; gọi song song nhiều request để thấy server đứng hay không. Đọc lý thuyết đúng lúc này (xem `suy_luan.md`, mục 2).
- [ ] Endpoint `/api/demo/slow-1s`, `slow-2s`, `slow-3s` (dùng `asyncio.sleep`).
- [ ] `httpx.AsyncClient` gọi Open-Meteo, Pydantic parse JSON (**JSON Deserialization**), endpoint trung gian cho FE, mock fallback khi mất mạng.
- 🎯 _Xong khi:_ giải thích được vì sao có bản "async" mà server vẫn đơ, và gọi được endpoint thời tiết.

### ⬜ Bước 6 — Giao diện React

- [ ] **Demo 1:** 3 widget fetch độc lập (1s/2s/3s), trạng thái `loading → success/error`, nút "Mở modal" vẫn bấm được.
- [ ] Widget thời tiết.
- [ ] Trang demo 2 (khung): phần dưới là các tab gọi GET nhẹ ở bước 4; phần trên chừa chỗ cho nút tác vụ nặng.
- 🎯 _Xong khi:_ chạy trọn Demo 1 và tab GET trên React.

### ⬜ Bước 7 — Tác vụ nặng ở BE (Demo 2) — làm sau cùng được

- [ ] Hàm mô phỏng CPU nặng, không cần dữ liệu DB, có tham số điều chỉnh để chạy khoảng 2 đến 3 giây (vòng lặp tính toán, đếm số nguyên tố, băm lặp nhiều vòng, tuỳ bạn chọn). Đo thử để đủ chậm.
- [ ] **Bản sync:** viết là `async def` chứa tính toán blocking, nên chặn event loop. Lưu ý: nếu viết `def` thường thì FastAPI đẩy vào thread pool và `/health` sẽ không đứng, demo mất tác dụng.
- [ ] **Bản `BackgroundTasks`:** hàm tính toán là `def` (sync), trả `202` kèm `job_id`, dict trong bộ nhớ lưu trạng thái (`PENDING`, `RUNNING`, `DONE`), có endpoint hỏi trạng thái.
- [ ] Chạy `uvicorn --workers 1`.
- [ ] Kiểm tra BE bằng vòng lặp `curl /health` mỗi 0,5 giây: bản sync im lặng, bản background vẫn in đều. Quay video.
- [ ] React: nút xuất báo cáo (trạng thái, polling), tab GET phía dưới vẫn bấm được ở bản background và treo ở bản sync.
- [ ] Ghi lại bảng thời gian đo được cho Word và slide.
- [ ] _(Tùy chọn)_ Demo 3: tab riêng, busy-wait **có thời hạn**, tuyệt đối không dùng `while(true)`, có video dự phòng.
- 🎯 _Xong khi:_ cùng một FE, đổi BE thì trải nghiệm khác hẳn.

### ⬜ Bước 8 — Đóng gói Docker đầy đủ

- [ ] Thêm hai service: BE (Dockerfile, `uvicorn --workers 1`) và FE (build nhiều giai đoạn, nginx, chuyển tiếp `/api` sang BE).
- [ ] Compose có `healthcheck` cho DB và một lệnh seed.
- [ ] Thử `docker compose down -v` rồi dựng lại, tốt nhất trên máy sạch.
- 🎯 _Xong khi:_ một lệnh dựng cả hệ thống.

### ⬜ Bước 9 — Hoàn thiện Word, slide, tập dượt

- [ ] Quay video demo dự phòng.
- [ ] Học thuộc câu chốt trên slide (`suy_luan.md`, mục 5) và câu trả lời cho _"Sao không demo browser freeze thật?"_.
- 🎯 _Xong khi:_ có bản chạy thử trọn vẹn trước ngày thuyết trình.

---

## 5. 🗺️ Sơ đồ: chỉ dùng lại và đổi tên

> ✏️ Không vẽ mới. Dùng bộ sơ đồ của nhóm (`02-so-do-uml.md`, ERD trong `04`), chỉ đổi tên cho khớp code.

| Sơ đồ                    | Việc cần làm                                                                                                            |
| :----------------------- | :---------------------------------------------------------------------------------------------------------------------- |
| Use Case tổng quát       | Giữ nguyên nội dung, đổi tên nếu có định danh kỹ thuật                                                                  |
| Class diagram            | Đổi tên lớp và thuộc tính theo mục 0 của `04` (ví dụ `NhomTieuLuan` → `EssayGroup`, `HoSoDangKy` → `TopicRegistration`) |
| ERD (3 sơ đồ trong `04`) | Đã đổi tên trong bản `04` mới                                                                                           |
| 2 Tuần tự, 2 Hoạt động   | Chỉ đổi tên định danh nếu có                                                                                            |

> 🧩 Sơ đồ so sánh sync/async không vẽ; trong Word dùng bảng thời gian đo được và kết quả `curl /health` thay thế.

---

## 6. 📝 Cấu trúc Word: lý thuyết đi cùng thực hành

> 🔁 Mỗi nội dung theo vòng: **lý thuyết → sơ đồ → đoạn code chính → kết quả demo**. Viết từng phần ngay khi phần code tương ứng chạy được.

| 📚 Phần               | 🧠 Lý thuyết                                                                                                | 🛠️ Thực hành tương ứng                          |
| :-------------------- | :---------------------------------------------------------------------------------------------------------- | :---------------------------------------------- |
| **ORM, tầng DAL**     | Repository, tách tầng trong OOP, generic                                                                    | `BaseRepository` với SQLAlchemy async, 14 model |
| **API ngoài, JSON**   | HTTP client bất đồng bộ, serialize/deserialize, validate bằng Pydantic                                      | schema `Read`, widget `httpx.AsyncClient`       |
| **Đa luồng và async** | thread, async, process; event loop; I/O-bound và CPU-bound; vì sao UI treo; GIL; đơ kỹ thuật và đơ cảm nhận | Demo 1, Demo 2, bảng thời gian đo được          |
| **Docker**            | image, container, compose                                                                                   | một lệnh dựng cả hệ thống                       |

> ✍️ Đoạn lý thuyết đa luồng nên viết sau bước 5, khi đã tự thấy khác biệt. Hệ thống thật thường dùng hàng đợi như Celery hoặc RQ, chỉ cần nhắc tới.

---

## 7. 🐳 Docker: làm vừa đủ

| Giai đoạn         | Nội dung                                        |
| :---------------- | :---------------------------------------------- |
| **Sớm (bước 1)**  | Chỉ container PostgreSQL kèm volume.            |
| **Cuối (bước 8)** | Thêm BE và FE, `healthcheck` cho DB, lệnh seed. |

---

## 8. ✂️ Quy tắc cắt giảm

- Dừng thêm tính năng khoảng **3 ngày** trước thuyết trình để tập dượt.
- Nếu trễ, cắt theo thứ tự: **Demo 3 → Alembic (dùng `create_all`) → giao diện đẹp**.
- Nếu trễ ở khâu "đủ 14 bảng": giữ ORM và Repository cho tất cả bảng, bỏ GET endpoint của bảng phụ.
- **Không cắt:** thí nghiệm async, Demo 1, Demo 2 (tác vụ nặng) và API ngoài.
