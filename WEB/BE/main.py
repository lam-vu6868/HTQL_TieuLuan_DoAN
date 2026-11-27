from app.core.asyncio_compat import apply_windows_selector_loop


apply_windows_selector_loop()
from fastapi import FastAPI  

app = FastAPI(title="HTQL TieuLuan DoAN API")


@app.get("/health", tags=["system"])
async def health_check() -> dict[str, str]:
    """Kiểm tra service còn sống."""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)