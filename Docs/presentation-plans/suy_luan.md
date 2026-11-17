# 📝 Chủ đề 9 — Async/Await & Tích hợp API

## Ghi chú lý thuyết và thiết kế demo (bản chốt của nhóm)

---

## 1. Đề bài và phạm vi

**Lý thuyết:**

- Đa luồng (Multithreading) và bất đồng bộ (Asynchronous Programming) trong OOP.
- Tại sao ứng dụng GUI bị "treo" (Freezing UI) và giải pháp với `async/await`.
- Tích hợp REST API (`HttpClient` / JSON serialize–deserialize) vào ứng dụng hướng đối tượng.

**Thực hành:**

- Vẽ Use Case và Class diagram thực tế.
- Tích hợp ORM vào tầng DAL.
- Viết chức năng tải dữ liệu / báo cáo nặng dạng async để UI không bị đơ.
- Gọi API bên ngoài (thời tiết) để hiển thị.

**Ghi chú phạm vi:**

- API thời tiết **chỉ để minh họa kỹ thuật** (REST + JSON), **không thuộc nghiệp vụ full** của dự án.

---

## 2. Lý thuyết — những gì nhóm đã thống nhất

### 2.1. Gốc rễ: Event Loop và "đơ"

Cả **FastAPI (server)** và **React (trình duyệt)** đều chạy trên một **event loop** — một vòng lặp trên **một thread duy nhất**, liên tục nhận việc và trả kết quả. Khi một tác vụ **chiếm giữ thread đó quá lâu**, event loop không thể quay lại phục vụ việc khác → **"đơ"**.

> 🔑 **Câu chốt của nhóm:** `async/await` **không làm code chạy nhanh hơn**. Nó chỉ cho event loop **tạm rời đi làm việc khác trong lúc chờ**. Nếu tác vụ là tính toán CPU (không có gì để "chờ"), `await` cũng vô dụng.

### 2.2. Hai loại tác vụ quyết định mọi thứ

|                        | **I/O-bound**                                                           | **CPU-bound**                                                                                    |
| ---------------------- | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| Bản chất               | Dành phần lớn thời gian **chờ** thứ bên ngoài: mạng, đĩa, DB, API ngoài | Dành phần lớn thời gian **tính toán** trên CPU                                                   |
| Ví dụ trong dự án      | Gọi API thời tiết, query PostgreSQL                                     | Tính thống kê trên vài nghìn hồ sơ                                                               |
| `async/await` có giúp? | ✅ **Có**                                                               | ❌ **Không** — không có `await` nào để nhường quyền                                              |
| Giải pháp              | Thư viện async (`httpx.AsyncClient`, SQLAlchemy async)                  | **Đẩy sang thread/process khác** (`asyncio.to_thread`, `BackgroundTasks`, `ProcessPoolExecutor`) |

> 🔑 **Câu chốt thứ hai:** `async/await` là cơ chế **hợp tác** (cooperative) — chỉ chuyển quyền tại điểm `await`. CPU-bound **không có điểm `await`** bên trong vòng lặp tính toán, nên phải **đẩy ra khỏi event loop** chứ không thể "async hóa" bản thân phép tính.

### 2.3. Ba kịch bản endpoint của FastAPI

Đây là chỗ dễ hiểu lầm nhất. "Req nặng chiếm thread, req sau đợi" **chỉ đúng một trường hợp**:

| Endpoint     | Bên trong                                  | Chuyện gì xảy ra                                                                |
| ------------ | ------------------------------------------ | ------------------------------------------------------------------------------- |
| `async def`  | Toàn code blocking (sync query, tính toán) | **Chặn event loop** — mọi req khác đợi                                          |
| `async def`  | Có `await` thật (async lib)                | Event loop rảnh trong lúc chờ → req khác chạy                                   |
| `def` (sync) | Bất kỳ                                     | FastAPI đẩy vào **thread pool** (mặc định 40 thread) → event loop không bị chặn |

> ⚠️ Nghịch lý: đôi khi viết `def` lại an toàn hơn `async def`. Với code blocking, khai báo `def` để FastAPI tự lo "đi luồng" — đừng viết `async def` mà bên trong toàn code sync.

### 2.4. `await` khác `BackgroundTasks` — đừng gộp hai cơ chế

|                     | **`await`**                                                          | **`BackgroundTasks`**                         |
| ------------------- | -------------------------------------------------------------------- | --------------------------------------------- |
| Bản chất            | Coroutine tạm dừng, event loop chạy task khác; I/O xong thì tiếp tục | Trả response **ngay**, việc nặng chạy **sau** |
| Client              | Vẫn **chờ response** (server không bị chặn)                          | Nhận `202` + `job_id` ngay, phải polling      |
| Dùng khi            | Chờ ngắn (200ms–2s)                                                  | Việc nặng (3s+)                               |
| Ví dụ trong lát cắt | Gọi API thời tiết                                                    | Báo cáo nặng                                  |

### 2.5. Vì sao CPU-bound phải dùng process (Python)

`Nội dung liên quan chuyên sâu hơn đến phần xử lý tác vụ nặng dành cho Python`

- **Thread pool**: giúp event loop không bị chặn, nhưng **không làm nhanh hơn** — do **GIL** (Global Interpreter Lock), tại một thời điểm chỉ một thread chạy bytecode Python.
- **Process pool**: mỗi process có GIL riêng và bộ nhớ riêng → **chạy song song thật** trên nhiều core. Nhưng phức tạp hơn, khó demo trong thời gian ngắn.
- **Kết luận thực dụng cho lát cắt:** dùng `BackgroundTasks` với hàm `def` (sync) cho báo cáo nặng. Đủ để event loop không bị chặn, đủ để demo.

### 2.6. Desktop freeze vs Web "đơ" — phân biệt rạch ròi

Đây là kết luận quan trọng nhất của nhóm sau khi mổ xẻ vấn đề:

|                         | **Desktop (WinForms, WPF, PyQt)**                   | **Web (React + FastAPI)**                            |
| ----------------------- | --------------------------------------------------- | ---------------------------------------------------- |
| Ai vẽ UI?               | **Main thread của app** — vừa xử lý sự kiện, vừa vẽ | **Browser thread** — tách biệt với server            |
| Tác vụ nặng chạy ở đâu? | Cùng main thread → **freeze thật**                  | Server (event loop riêng) → **browser không freeze** |
| Giải pháp               | Đẩy sang thread khác, marshal kết quả về UI thread  | Đẩy sang `BackgroundTasks`, FE polling               |
| "Đơ" mà người dùng thấy | **Đơ kỹ thuật** (browser/app freeze)                | **Đơ cảm nhận** (BE không trả lời → tab không load)  |

> 🔑 **Kết luận của nhóm:** Trên web, `fetch` **luôn async sẵn**, nên browser thread gần như không bao giờ freeze vì chờ API. Cái "đơ" mà người dùng web trải nghiệm **chính là "đơ cảm nhận"** — do BE bị block, mọi request khác đều treo. **Đây mới là thứ demo cần chứng minh**, không phải browser freeze.

---

## 3. Thiết kế demo thực hành

### 3.1. Cấu trúc tổng thể — ba demo độc lập

| #     | Demo                                    | Test ở đâu     | Minh họa điều gì                                                                            |
| ----- | --------------------------------------- | -------------- | ------------------------------------------------------------------------------------------- |
| **1** | 3 widget fetch độc lập, delay khác nhau | FE             | I/O-bound không block UI; kết quả hiện dần theo thứ tự hoàn thành                           |
| **2** | Báo cáo nặng: sync vs `BackgroundTasks` | **Cả BE + FE** | CPU-bound trên server: `async` không cứu được, phải đẩy sang thread/background; UI vẫn sống |
| **3** | Technical freeze (tùy chọn)             | FE — tab riêng | Minh họa **browser thread freeze thật** bằng vòng lặp JS nặng                               |

### 3.2. Demo 1 — I/O-bound không block UI (FE)

**Mục đích:** Chứng minh `fetch` async giúp UI vẫn sống trong lúc chờ mạng.

**Thiết kế:**

- 3 widget độc lập: `/api/demo/slow-1s`, `/api/demo/slow-2s`, `/api/demo/slow-3s`.
- Mỗi widget hiện trạng thái `loading → success/error` (có status fetch, hiện lỗi màu đỏ nếu fail).
- Widget 1s hiện trước, 3s hiện sau → minh họa kết quả hiện dần.
- Trong lúc chờ, nút "Mở modal" vẫn bấm được → UI sống nhăn răng.

**Kết quả mong đợi:** Cả 3 widget đều hiện đúng thứ tự, không widget nào block widget nào, UI luôn phản hồi.

### 3.3. Demo 2 — Báo cáo nặng: sync vs `BackgroundTasks`

**Đây là demo "đinh" — quan trọng nhất.**

**Thiết kế page (theo đúng ý nhóm):**

```

┌─────────────────────────────────────────────┐
│ PHẦN TRÊN: Nút "Xuất báo cáo" (API nặng) │
│ → Loading → PENDING/RUNNING/DONE │
├─────────────────────────────────────────────┤
│ PHẦN DƯỚI: Các tab gọi API nhẹ │
│ [Tab A] [Tab B] [Tab C] │
│ → Bấm tab → hiện dữ liệu │
└─────────────────────────────────────────────┘

```

**Kịch bản test:**

|                     | **TH1: BE sync**                            | **TH2: BE `BackgroundTasks`**   |
| ------------------- | ------------------------------------------- | ------------------------------- |
| Phần trên           | Loading… mãi mãi                            | Loading → có kết quả sau 3 giây |
| Phần dưới (tab)     | Bấm tab → **loading mãi, không có dữ liệu** | Bấm tab → **dữ liệu hiện ngay** |
| Nút "Mở modal"      | **Vẫn mở được** (browser thread rảnh)       | Vẫn mở được                     |
| Cảm nhận người dùng | "Trang này đơ rồi"                          | "Trang chạy bình thường"        |

**Điểm mạnh:** Cùng một FE code, chỉ khác BE, mà trải nghiệm khác hẳn. Không ai nói được "tại FE viết dở".

**Cách test BE (dùng Postman hoặc terminal):**

1. **Terminal 1** — vòng lặp gọi `/health` mỗi 0.5s:

   ```bash
   while true; do curl -s localhost:8000/health; echo; sleep 0.5; done
   ```

2. **Postman** — bắn `POST /api/reports`.
3. **Quan sát:**
   - **TH1 (sync):** `/health` **im lặng hoàn toàn** trong 3 giây. Event loop bị chặn.
   - **TH2 (background):** `/health` **vẫn in đều**. Event loop rảnh.

> 💡 Postman tiện để **đo thời gian chính xác** (hiện ms), nhưng **không chứng minh được "UI không đơ"** — vì Postman không phải UI của bạn. Muốn chứng minh UI, phải demo trên React.

**Lưu ý kỹ thuật quan trọng khi demo:**

- Chạy `uvicorn --workers 1`. Với nhiều worker, job status lưu trong dict bộ nhớ có thể "biến mất" khi request polling rơi vào process khác → 404 khó hiểu trước mặt giảng viên.
- `BackgroundTasks` phải là **hàm `def` (sync)** — FastAPI tự bọc `run_in_threadpool`. Nếu là `async def` mà bên trong toàn tính toán CPU (không `await`), nó **vẫn chặn event loop** → demo giống hệt bản sync.
- Mục tiêu **2–3 giây** là đủ thấy khác biệt, đỡ sốt ruột.

### 3.4. Demo 3 — Technical freeze (tùy chọn, tab riêng)

**Mục đích:** Minh họa **browser thread freeze thật** — khác với "đơ cảm nhận" ở Demo 2.

**Thiết kế:**

- Tách thành **tab riêng**, không ảnh hưởng demo chính.
- Hai nút: "Bắt đầu tác vụ nặng (5 giây)" và "Kiểm tra UI sống không".

**Cách tạo freeze — vòng lặp busy-wait có thời hạn:**

```javascript
function blockMainThreadFor(seconds) {
  const startTime = Date.now();
  const duration = seconds * 1000;
  while (Date.now() - startTime < duration) {
    // Thread bị khóa, không làm gì khác được
  }
}
```

**Kịch bản:**

1. Bấm "Bắt đầu tác vụ nặng (5 giây)".
2. Ngay lập tức thử bấm nút khác / cuộn trang → **không phản hồi**.
3. Sau 5 giây, main thread giải phóng → bấm nút khác → hoạt động ngay.

**Lưu ý an toàn:**

- **Đừng dùng `while(true)`** vô hạn — chỉ dùng vòng lặp có thời hạn (cách trên) để tránh phải tắt tab.
- Quay video dự phòng — vì đây là demo có thể gây "sự cố" cho trình duyệt.
- **Phân biệt rõ với giảng viên:** _"Đây là đơ kỹ thuật — browser thread bị khóa. Khác với đơ cảm nhận do BE chậm ở demo trước. Cả hai đều tệ, nhưng nguyên nhân gốc rễ khác nhau."_ — Câu này thể hiện hiểu sâu.

---

## 4. Lý thuyết đa luồng — bảng tổng hợp (optional đọc thêm sau)

| Nền tảng                      | Thread khác xử lý CPU-bound                      | Lý do                                               |
| ----------------------------- | ------------------------------------------------ | --------------------------------------------------- |
| **C# / .NET** (WinForms, WPF) | ✅ Nhanh hơn thật                                | Không có GIL, thread chạy song song trên nhiều core |
| **Python** (PyQt, Tkinter)    | ⚠️ UI **không đơ** nhưng CPU **không nhanh hơn** | GIL                                                 |
| **Python, cần nhanh thật**    | ✅ Dùng **process** (`multiprocessing`)          | Mỗi process có GIL riêng                            |

> **Nhắc lại:** đa luồng giải quyết **chặn UI**, nhưng chỉ **tăng tốc CPU-bound** khi không có GIL (hoặc dùng process).

---

## 5. Câu chốt cho slide

> **GUI treo = main thread bị chiếm.** Có hai nguyên nhân:
>
> 1. **CPU-bound chạy trên UI thread** → đẩy sang thread/process khác.
> 2. **I/O chạy đồng bộ** → dùng `async/await` để nhường event loop.
>
> Nhưng `async/await` **chỉ nhường được khi có điểm `await`**. CPU-bound **không có điểm `await`** bên trong vòng lặp tính toán, nên phải đẩy sang luồng khác — **không thể "async hóa" bản thân phép tính**.
>
> Trên web: **"UI không bị đơ" = "hệ thống vẫn phản hồi"**, không phải "browser thread không freeze".

---

## 6. Checklist trước khi thuyết trình

- [ ] Demo 1 chạy trơn: 3 widget delay khác nhau, có status loading/success/error.
- [ ] Demo 2 chạy trơn **cả hai bản** sync và `BackgroundTasks`, có tab dưới để so sánh.
- [ ] Test BE bằng terminal `/health` song song, quay video lại.
- [ ] Chạy `uvicorn --workers 1` cho buổi demo.
- [ ] Demo 3 (nếu làm) tách tab riêng, có video dự phòng.
- [ ] API thời tiết dùng Open-Meteo, có mock fallback.
- [ ] Câu chốt trên slide đã thuộc lòng.
- [ ] Chuẩn bị sẵn câu trả lời: _"Sao không demo browser freeze thật?"_ → _"Web fetch luôn async nên browser không freeze vì chờ API. Cái người dùng gọi là 'đơ' chính là khi BE không phản hồi — và đó là thứ demo này minh họa."_

---

<div align="center">

### ✨ Ghi chú này được tổng hợp từ quá trình suy luận của Tuấn Anh✨

</div>
