# app/models/submission.py
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    BigInteger, Boolean, CheckConstraint, DateTime, Enum, ForeignKey,
    Index, Integer, Numeric, Text, UniqueConstraint, func, text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base
from app.models.enums import PublishStatus


class Milestone(Base):
    __tablename__ = "milestones"
    __table_args__ = (
        UniqueConstraint("assignment_id", "sequence_no", name="uq_milestone_sequence"),
        # Mỗi phân công chỉ có một mốc cuối
        Index(
            "uq_milestone_one_final",
            "assignment_id",
            unique=True,
            postgresql_where=text("is_final"),
        ),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    assignment_id: Mapped[int] = mapped_column(
        ForeignKey("supervisor_assignments.id", ondelete="CASCADE")
    )
    milestone_name: Mapped[str] = mapped_column(Text)
    sequence_no: Mapped[int] = mapped_column(Integer)
    deadline: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    is_final: Mapped[bool] = mapped_column(Boolean, default=False)


class Submission(Base):
    __tablename__ = "submissions"
    __table_args__ = (
        # Đồ án: mỗi (hồ sơ, mốc) một bài nộp hiện hành
        UniqueConstraint("registration_id", "milestone_id", name="uq_submission_milestone"),
        # Tiểu luận (không có mốc): mỗi hồ sơ một bài nộp hiện hành
        Index(
            "uq_submission_essay",
            "registration_id",
            unique=True,
            postgresql_where=text("milestone_id IS NULL"),
        ),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    registration_id: Mapped[int] = mapped_column(
        ForeignKey("topic_registrations.id", ondelete="CASCADE")
    )
    milestone_id: Mapped[int | None] = mapped_column(ForeignKey("milestones.id"))
    submitted_by_id: Mapped[int] = mapped_column(ForeignKey("students.id"))

    file_path: Mapped[str] = mapped_column(Text)
    original_filename: Mapped[str] = mapped_column(Text)
    submitted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    is_late: Mapped[bool] = mapped_column(Boolean, default=False)

    feedback: Mapped[str | None] = mapped_column(Text)
    feedback_by_id: Mapped[int | None] = mapped_column(ForeignKey("lecturers.id"))
    feedback_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class Result(Base):
    __tablename__ = "results"
    __table_args__ = (
        CheckConstraint("score >= 0 AND score <= 10", name="ck_result_score_range"),
    )

    registration_id: Mapped[int] = mapped_column(
        ForeignKey("topic_registrations.id", ondelete="CASCADE"), primary_key=True
    )
    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.id"), primary_key=True
    )
    score: Mapped[Decimal] = mapped_column(Numeric(4, 2))
    entered_by_id: Mapped[int] = mapped_column(ForeignKey("lecturers.id"))
    entered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    publish_status: Mapped[PublishStatus] = mapped_column(
        Enum(PublishStatus, native_enum=False), default=PublishStatus.UNPUBLISHED
    )
    published_by_id: Mapped[int | None] = mapped_column(ForeignKey("accounts.id"))
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))