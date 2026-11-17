"""Nạp toàn bộ 14 bảng vào metadata cho Alembic."""

from app.database import Base
from app.models import account, academic, assessment, registration, term  # noqa: F401

__all__ = ["Base"]
