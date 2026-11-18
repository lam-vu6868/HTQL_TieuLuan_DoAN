import { useEffect, useRef, useState } from "react";
import axios from "axios"; // dùng axios thường vì /health không nằm dưới /api

const SLOW_MS = 500;
const MAX_POINTS = 24;
const DISPLAY_MAX_MS = 1000; // mốc đỉnh của chart

export default function HealthPoller() {
  const [points, setPoints] = useState([]); // ms mỗi lần gọi, null = lỗi
  const [pendingMs, setPendingMs] = useState(0);
  const sentAt = useRef(null);

  useEffect(() => {
    let alive = true;
    const controller = new AbortController();

    async function loop() {
      while (alive) {
        const start = performance.now();
        sentAt.current = start;
        let ms = null;
        try {
          await axios.get("/health", { signal: controller.signal });
          ms = Math.round(performance.now() - start);
        } catch (err) {
          if (axios.isCancel(err)) return;
        }
        sentAt.current = null;
        if (!alive) return;
        setPoints((p) => [...p.slice(-(MAX_POINTS - 1)), ms]);
        await new Promise((r) => setTimeout(r, 500));
      }
    }
    loop();

    const timer = setInterval(() => {
      setPendingMs(sentAt.current ? Math.round(performance.now() - sentAt.current) : 0);
    }, 100);

    return () => {
      alive = false;
      controller.abort();
      clearInterval(timer);
    };
  }, []);

  const last = points[points.length - 1];
  const blocked = pendingMs > SLOW_MS;
  const okPoints = points.filter((p) => p != null && p <= SLOW_MS);
  const avg = okPoints.length
    ? Math.round(okPoints.reduce((a, b) => a + b, 0) / okPoints.length)
    : null;
  const maxOk = okPoints.length ? Math.max(...okPoints) : null;

  return (
    <div className="rounded-2xl bg-slate-50/70 p-5">
      <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
        <div>
          <p className="text-base font-medium text-slate-800">
            Gọi{" "}
            <span className="rounded bg-slate-200 px-1.5 py-0.5 font-mono text-sm">
              GET /health
            </span>{" "}
            mỗi 0,5 giây
          </p>
          <p className="mt-0.5 text-sm text-slate-500">
            Đo round-trip FE → server. Càng thấp càng tốt.
          </p>
        </div>
        {blocked ? (
          <span className="inline-flex items-center gap-2 rounded-full bg-red-50 px-3 py-1.5 text-sm font-medium text-red-700 ring-1 ring-red-200">
            <span className="h-2 w-2 animate-pulse rounded-full bg-red-500" />
            Đang chờ phản hồi… {(pendingMs / 1000).toFixed(1)}s
          </span>
        ) : (
          <span className="inline-flex items-center gap-2 rounded-full bg-emerald-50 px-3 py-1.5 text-sm font-medium text-emerald-700 ring-1 ring-emerald-200">
            <span className="h-2 w-2 rounded-full bg-emerald-500" />
            Bình thường{last != null ? ` · ${last} ms` : ""}
          </span>
        )}
      </div>

      {/* Chart */}
      <div className="flex h-32 gap-3 rounded-xl bg-white p-3 ring-1 ring-slate-200">
        {/* Trục Y */}
        <div className="flex flex-col justify-between py-px text-right font-mono text-[10px] text-slate-400">
          <span>1000</span>
          <span>500</span>
          <span>0</span>
        </div>

        <div className="relative flex-1">
          {/* Grid lines: đỉnh, ngưỡng 500ms, đáy */}
          <div className="pointer-events-none absolute inset-0 flex flex-col justify-between">
            <div className="border-t border-dashed border-slate-100" />
            <div className="border-t border-dashed border-amber-200" />
            <div className="border-t border-slate-200" />
          </div>

          {/* Bars */}
          <div className="flex h-full items-end gap-1">
            {points.length === 0 && (
              <span className="text-sm text-slate-400">Chưa có dữ liệu…</span>
            )}
            {points.map((ms, i) => {
              const ratio = ms == null ? 1 : Math.min(ms, DISPLAY_MAX_MS) / DISPLAY_MAX_MS;
              const h = ms == null ? 100 : Math.max(4, ratio * 100);
              const bad = ms == null || ms > SLOW_MS;
              return (
                <div
                  key={i}
                  title={ms == null ? "lỗi" : `${ms} ms`}
                  style={{ height: `${h}%` }}
                  className={`flex-1 rounded-sm transition-all hover:opacity-80 ${
                    bad ? "bg-red-500" : "bg-emerald-500"
                  }`}
                />
              );
            })}
          </div>
        </div>
      </div>

      {/* Legend + thống kê */}
      <div className="mt-3 flex flex-wrap items-center justify-between gap-3 text-sm">
        <div className="flex items-center gap-4">
          <span className="inline-flex items-center gap-1.5 text-slate-600">
            <span className="h-2 w-2 rounded-sm bg-emerald-500" /> &lt; 500ms
          </span>
          <span className="inline-flex items-center gap-1.5 text-slate-600">
            <span className="h-2 w-2 rounded-sm bg-red-500" /> ≥ 500ms / lỗi
          </span>
        </div>
        <div className="flex gap-4 font-mono text-slate-600">
          {avg != null && <span>TB {avg}ms</span>}
          {maxOk != null && <span>Max {maxOk}ms</span>}
        </div>
      </div>
    </div>
  );
}