#!/usr/bin/env bash
# File: setup_be.sh
# Chạy:  bash setup_be.sh
set -euo pipefail

echo "==> Tạo cây thư mục BE..."

# ---------- 1. Thư mục ----------
mkdir -p \
  app/core \
  app/models \
  app/repositories \
  app/schemas \
  app/services \
  app/jobs \
  app/routers \
  storage/reports

# ---------- 2. File rỗng ----------
# Gốc app
touch app/__init__.py

# core (bổ sung __init__.py cho package sạch)
touch app/core/__init__.py
touch app/core/config.py
touch app/core/database.py
touch app/core/security.py
touch app/core/deps.py

# schemas
touch app/schemas/__init__.py
touch app/schemas/auth.py
touch app/schemas/registration.py
touch app/schemas/report.py
touch app/schemas/weather.py
touch app/schemas/demo.py

# services
touch app/services/__init__.py
touch app/services/auth_service.py
touch app/services/registration_service.py
touch app/services/report_service.py
touch app/services/weather_service.py

# jobs
touch app/jobs/__init__.py
touch app/jobs/job_store.py

# routers
touch app/routers/__init__.py
touch app/routers/health.py
touch app/routers/auth.py
touch app/routers/registrations.py
touch app/routers/reports.py
touch app/routers/weather.py
touch app/routers/demo.py

# entry point + seed + config gốc
touch main.py
touch seed.py
touch .env.example
touch .gitignore
touch README.md
touch requirements.txt

# ---------- 3. Ghi chú ----------
echo "==> Xong. Cấu trúc hiện tại:"
find . -maxdepth 3 \( -path './.git' -o -path './.venv' -o -path './venv' \) -prune -o -print | sort

echo
echo "Lưu ý:"
echo "  - app/models/      : để TRỐNG, bạn bê file vào sau"
echo "  - app/repositories/: để TRỐNG, bạn bê file vào sau"
echo "  - storage/reports/ : để trống, dùng cho chặng sau"