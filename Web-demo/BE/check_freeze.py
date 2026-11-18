"""Demo 2: so sánh blocking và async bằng cách thăm dò /health khi báo cáo đang chạy.

Chạy:  python check_freeze.py            (cả 2 chế độ, delay 5s)
       python check_freeze.py async 3    (một chế độ, delay 3s)
"""

import asyncio
import sys
import time

import httpx

BASE = "http://localhost:8000"
PROBE_INTERVAL = 0.5     # giây giữa 2 lần thăm dò
SLOW_THRESHOLD = 0.5     # /health chậm hơn mức này thì đánh dấu "TREO"


async def probe_health(client: httpx.AsyncClient, stop: asyncio.Event, t0: float, log: list):
    """Gọi /health liên tục cho đến khi báo cáo xong."""
    while not stop.is_set():
        sent = time.perf_counter()
        try:
            await client.get(f"{BASE}/health", timeout=30)
            latency = time.perf_counter() - sent
        except httpx.HTTPError:
            latency = float("inf")
        log.append(latency)
        flag = "  <-- TREO" if latency > SLOW_THRESHOLD else ""
        print(f"  [{sent - t0:5.1f}s] /health {latency * 1000:8.0f} ms{flag}")
        await asyncio.sleep(PROBE_INTERVAL)


async def run_mode(mode: str, delay: float):
    print(f"\n=== {mode.upper()} (delay={delay}s) ===")
    stop = asyncio.Event()
    log: list[float] = []
    t0 = time.perf_counter()

    async with httpx.AsyncClient() as client:
        probe = asyncio.create_task(probe_health(client, stop, t0, log))
        await asyncio.sleep(1.0)  # để thấy /health bình thường trước khi gọi báo cáo
        print(f"  [{time.perf_counter() - t0:5.1f}s] >>> gọi báo cáo {mode}")
        resp = await client.get(
            f"{BASE}/reports/class-summary/{mode}",
            params={"delay": delay},
            timeout=60,
        )
        if resp.status_code != 200:
            stop.set()
            await probe
            print(f"  !!! {resp.status_code} {resp.request.url}")
            print(f"  !!! {resp.text[:500]}")
            return
        data = resp.json()
        print(f"  [{time.perf_counter() - t0:5.1f}s] <<< báo cáo xong: "
              f"{len(data['rows'])} lớp, server đo {data['elapsed_ms']} ms")
        await asyncio.sleep(1.0)  # xem /health sau khi xong
        stop.set()
        await probe

    worst = max(log) * 1000
    print(f"  => /health chậm nhất: {worst:.0f} ms "
          f"({'BỊ CHẶN' if worst > SLOW_THRESHOLD * 1000 else 'không bị chặn'})")


async def main():
    modes = [sys.argv[1]] if len(sys.argv) > 1 else ["blocking", "async"]
    delay = float(sys.argv[2]) if len(sys.argv) > 2 else 5.0
    for mode in modes:
        await run_mode(mode, delay)


if __name__ == "__main__":
    asyncio.run(main())