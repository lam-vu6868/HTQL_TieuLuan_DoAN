from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    BigInteger, Boolean, DateTime, Enum,
    ForeignKey, Integer, Numeric, Text, func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base
from app.models.enums import GradingMode, Role

class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    email: Mapped[str] = mapped_column(Text, unique=True)
    password_hash: Mapped[str] = mapped_column(Text)
    role: Mapped[Role] = mapped_column(Enum(Role, native_enum=False))


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id", ondelete="CASCADE"), unique=True
    )
    student_code: Mapped[str] = mapped_column(Text, unique=True)
    full_name: Mapped[str] = mapped_column(Text)


class Lecturer(Base):
    __tablename__ = "lecturers"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id", ondelete="CASCADE"), unique=True
    )
    lecturer_code: Mapped[str] = mapped_column(Text, unique=True)
    full_name: Mapped[str] = mapped_column(Text)


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id", ondelete="CASCADE"), index=True
    )
    token_hash: Mapped[str] = mapped_column(Text, unique=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    revoked: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    course_code: Mapped[str] = mapped_column(Text, unique=True)
    course_name: Mapped[str] = mapped_column(Text)


class CourseSection(Base):
    __tablename__ = "course_sections"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), index=True)
    lecturer_id: Mapped[int] = mapped_column(ForeignKey("lecturers.id"), index=True)
    section_code: Mapped[str] = mapped_column(Text)
    semester: Mapped[int] = mapped_column(Integer)
    academic_year: Mapped[str] = mapped_column(Text)

    registration_start_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True)
    )
    registration_deadline: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True)
    )
    submission_deadline: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True)
    )

    min_members: Mapped[int] = mapped_column(Integer)
    max_members: Mapped[int] = mapped_column(Integer)
    grading_mode: Mapped[GradingMode] = mapped_column(
        Enum(GradingMode, native_enum=False)
    )
    pass_threshold: Mapped[Decimal] = mapped_column(
        Numeric(4, 2), default=Decimal("4.00")
    )


class SectionStudent(Base):
    __tablename__ = "section_students"

    section_id: Mapped[int] = mapped_column(
        ForeignKey("course_sections.id", ondelete="CASCADE"), primary_key=True
    )
    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.id", ondelete="CASCADE"), primary_key=True
    )