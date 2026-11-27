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
  app/routers \
  storage/reports

# ---------- 2. File rỗng ----------

# repository
touch app/repositories/__init__.py

#  models
touch app/models/__init__.py

# Gốc app
touch app/__init__.py

# core (bổ sung __init__.py cho package sạch)
touch app/core/__init__.py
touch app/core/config.py
touch app/core/database.py
touch app/core/security.py

# schemas
touch app/schemas/__init__.py

# services
touch app/services/__init__.py


# routers
touch app/routers/__init__.py

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