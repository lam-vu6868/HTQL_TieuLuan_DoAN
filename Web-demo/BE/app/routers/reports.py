import time

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db            # chỉnh theo tên thật của bạn
from app.repositories.report import ReportRepository
from app.schemas.report import ClassReportRow, ClassSummaryReport

router = APIRouter(prefix="/api/reports", tags=["reports"])


@router.get("/class-summary/blocking", response_model=ClassSummaryReport)
async def class_summary_blocking(
    delay: float = Query(3, ge=0, le=10),
    db: AsyncSession = Depends(get_db),
):
    start = time.perf_counter()
    time.sleep(delay)                      # BLOCKING: giữ cả event loop
    rows = await ReportRepository(db).class_summary()
    return ClassSummaryReport(
        mode="blocking",
        delay_seconds=delay,
        elapsed_ms=int((time.perf_counter() - start) * 1000),
        rows=[ClassReportRow(**r) for r in rows],
    )


@router.get("/class-summary/async", response_model=ClassSummaryReport)
async def class_summary_async(
    delay: float = Query(3, ge=0, le=10),
    db: AsyncSession = Depends(get_db),
):
    start = time.perf_counter()
    repo = ReportRepository(db)
    await repo.slow_db(delay)              # NON-BLOCKING: nhường event loop
    rows = await repo.class_summary()
    return ClassSummaryReport(
        mode="async",
        delay_seconds=delay,
        elapsed_ms=int((time.perf_counter() - start) * 1000),
        rows=[ClassReportRow(**r) for r in rows],
    )