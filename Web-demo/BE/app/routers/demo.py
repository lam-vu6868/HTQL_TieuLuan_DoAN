import asyncio
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException

from app.schemas.demo import SlowResponse

router = APIRouter(prefix="/demo", tags=["demo"])


async def _slow(seconds: int, fail: bool) -> SlowResponse:
    # await asyncio.sleep: mô phỏng việc CHỜ I/O (gọi mạng, query DB...).
    # Trong lúc chờ, event loop rảnh để phục vụ request khác.
    await asyncio.sleep(seconds)
    if fail:
        raise HTTPException(status_code=500, detail=f"Lỗi giả lập sau {seconds}s")
    return SlowResponse(
        message=f"Xong sau {seconds} giây",
        delay_seconds=seconds,
        finished_at=datetime.now(timezone.utc),
    )


@router.get("/slow-1s", response_model=SlowResponse)
async def slow_1s(fail: bool = False):
    return await _slow(1, fail)


@router.get("/slow-2s", response_model=SlowResponse)
async def slow_2s(fail: bool = False):
    return await _slow(2, fail)


@router.get("/slow-3s", response_model=SlowResponse)
async def slow_3s(fail: bool = False):
    return await _slow(3, fail)