# Hướng dẫn làm việc với nhánh Git — nhóm 2 người

Repo này đã có `main`, `dev` và remote `origin` trên GitHub. `main` giữ bản ổn định; `dev` là nơi ghép và kiểm thử công việc của cả nhóm. `origin/dev` là bản `dev` trên GitHub, không phải một nhánh cần tạo riêng.

```text
feat/be-db-init ─┐
                 ├─ Pull Request → dev ── Pull Request → main
feat/fe-login ───┘
```

## 1. Trước khi tạo nhánh

Mở PowerShell tại thư mục dự án:

```powershell
git status
git branch --show-current
```

Nếu `git status` báo có file đang sửa/chưa commit, hãy hoàn tất và commit trên nhánh dành cho việc đó trước. Khi tạo hoặc chuyển nhánh với thay đổi chưa commit, Git có thể mang các thay đổi ấy sang nhánh mới. **Trong repo này đang có thay đổi tên file UML chưa commit**; xử lý việc đó trước khi bắt đầu một tính năng khác.

## 2. Tạo nhánh làm việc riêng từ `dev`

Mỗi việc tạo một nhánh ngắn hạn. Ví dụ người làm BE/DB bắt đầu phần kết nối database:

```powershell
git switch dev
git pull --ff-only origin dev
git switch -c feat/be-db-init
```

Người làm FE có thể tạo `feat/fe-login` theo cùng ba lệnh, chỉ đổi tên ở lệnh cuối. Bạn cũng có thể đứng ở nhánh khác và chạy `git switch -c feat/be-db-init dev`; nhánh mới vẫn tách từ `dev`.

Tên gợi ý cho các việc tiếp theo: `feat/be-auth`, `feat/be-essay`, `feat/be-thesis`, `feat/fe-essay`, `feat/fe-thesis`. Không dùng một nhánh cá nhân cố định cho toàn bộ bài.

## 3. Lưu và đẩy công việc lên GitHub

Sau khi sửa file và kiểm tra phần mình làm:

```powershell
git status
git add .
git commit -m "feat: ket noi BE voi PostgreSQL"
git push -u origin feat/be-db-init
```

Ở những lần đẩy sau trên cùng nhánh, chỉ cần `git push`. Trước `git add .`, xem `git status` để chắc rằng không đưa nhầm `.env`, file báo cáo hoặc thay đổi của việc khác vào commit.

## 4. Ghép vào `dev`

Trên GitHub, mở **Pull Request** với:

```text
base:    dev
compare: feat/be-db-init
```

Người còn lại xem thay đổi, hai người kiểm tra chức năng liên quan rồi merge. Sau đó cập nhật `dev` trên máy:

```powershell
git switch dev
git pull --ff-only origin dev
```

Tạo nhánh mới từ `dev` đã cập nhật cho việc tiếp theo. GitHub cho phép chọn nhánh đích (*base*) và nhánh nguồn (*compare*) khi mở Pull Request: [hướng dẫn của GitHub](https://docs.github.com/en/pull-requests/how-tos/create-pull-requests/creating-a-pull-request).

## 5. Đưa bản đã kiểm thử về `main`

Khi hai luồng Tiểu luận và Đồ án trên `dev` đã chạy ổn, mở Pull Request:

```text
base:    main
compare: dev
```

Hai người xem lại và merge. Sau đó cập nhật `main` trên máy bằng `git switch main` và `git pull --ff-only origin main`. Không làm tính năng trực tiếp trên `main`.

## Nếu chưa có `dev` ở một repo khác

Trong **repo hiện tại** bỏ qua mục này vì `dev` và `origin/dev` đã tồn tại. Với repo mới, từ `main` sạch có thể tạo một lần:

```powershell
git switch main
git pull --ff-only origin main
git switch -c dev
git push -u origin dev
```
