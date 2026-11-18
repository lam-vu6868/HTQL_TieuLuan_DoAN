import { useState } from "react";
import api from "../api/client";
import HealthPoller from "../components/HealthPoller";
import SlowWidget from "../components/SlowWidget";

const TABS = [
  { id: "health", label: "Health (theo dõi server)" },
  { id: "slow", label: "API nhẹ 1 giây" },
];

function Spinner({ className = "h-4 w-4" }) {
  return (
    <svg className={`animate-spin ${className}`} viewBox="0 0 24 24" fill="none">
      <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="3" opacity="0.25" />
      <path d="M22 12a10 10 0 0 1-10 10" stroke="currentColor" strokeWidth="3" strokeLinecap="round" />
    </svg>
  );
}

export default function DemoReport() {
  const [delay, setDelay] = useState(5);
  const [tab, setTab] = useState("health");
  const [count, setCount] = useState(0);
  const [report, setReport] = useState({
    status: "idle",
    mode: null,
    data: null,
    error: null,
    elapsedMs: null,
  });

  async function exportReport(mode) {
    const start = performance.now();
    setReport({ status: "loading", mode, data: null, error: null, elapsedMs: null });
    try {
      const res = await api.get(`/reports/class-summary/${mode}`, { params: { delay } });
      setReport({
        status: "success",
        mode,
        data: res.data,
        error: null,
        elapsedMs: Math.round(performance.now() - start),
      });
    } catch (err) {
      setReport({
        status: "error",
        mode,
        data: null,
        error: err.response?.data?.detail ?? err.message,
        elapsedMs: Math.round(performance.now() - start),
      });
    }
  }

  const loading = report.status === "loading";

  return (
    <div className="mx-auto max-w-5xl px-6 py-10">
      <header className="mb-8">
        <div className="inline-flex items-center gap-2 rounded-full bg-rose-100 px-3 py-1 text-sm font-medium text-rose-700">
          <span className="h-2 w-2 rounded-full bg-rose-500" />
          Demo 02
        </div>
        <h1 className="mt-3 text-4xl font-bold tracking-tight text-slate-900">
          Báo cáo nặng: blocking và async
        </h1>
        <p className="mt-2 max-w-2xl text-lg text-slate-600">
          Bấm xuất báo cáo, rồi quan sát phần bên dưới: server có còn phục vụ các API nhẹ không.
        </p>
      </header>

      {/* Xuất báo cáo */}
      <section className="mb-8 rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
        <div className="flex flex-wrap items-center gap-3">
          <button
            onClick={() => exportReport("blocking")}
            disabled={loading}
            className="inline-flex items-center gap-2 rounded-xl bg-rose-600 px-4 py-2.5 text-base font-medium text-white shadow-sm transition hover:bg-rose-700 active:scale-[0.98] disabled:cursor-not-allowed disabled:opacity-50"
          >
            {loading && report.mode === "blocking" ? (
              <Spinner />
            ) : (
              <svg className="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="12" cy="12" r="9" />
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 8v4l3 3" />
              </svg>
            )}
            Xuất báo cáo (blocking)
          </button>

          <button
            onClick={() => exportReport("async")}
            disabled={loading}
            className="inline-flex items-center gap-2 rounded-xl bg-emerald-600 px-4 py-2.5 text-base font-medium text-white shadow-sm transition hover:bg-emerald-700 active:scale-[0.98] disabled:cursor-not-allowed disabled:opacity-50"
          >
            {loading && report.mode === "async" ? (
              <Spinner />
            ) : (
              <svg className="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path strokeLinecap="round" strokeLinejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            )}
            Xuất báo cáo (async)
          </button>

          <label className="ml-auto inline-flex items-center gap-2 text-base text-slate-700">
            Thời gian chờ
            <select
              value={delay}
              onChange={(e) => setDelay(Number(e.target.value))}
              disabled={loading}
              className="rounded-lg border border-slate-200 bg-white px-2.5 py-1.5 text-sm shadow-sm disabled:opacity-50"
            >
              {[3, 5, 8].map((s) => (
                <option key={s} value={s}>
                  {s} giây
                </option>
              ))}
            </select>
          </label>

          <button
            onClick={() => setCount((c) => c + 1)}
            className="inline-flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-base font-medium text-slate-700 shadow-sm transition hover:bg-slate-50 active:scale-[0.98]"
          >
            Bấm thử:
            <span className="rounded-md bg-slate-100 px-2 py-0.5 font-mono text-sm text-slate-800">
              {count}
            </span>
          </button>
        </div>

        <div className="mt-5">
          {report.status === "idle" && (
            <div className="flex items-center gap-3 rounded-xl border border-dashed border-slate-200 bg-slate-50/60 p-4 text-base text-slate-500">
              <svg className="h-5 w-5 text-slate-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="12" cy="12" r="9" />
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 8v4m0 4h.01" />
              </svg>
              Chưa xuất báo cáo — bấm nút phía trên để bắt đầu.
            </div>
          )}

          {loading && (
            <div className="flex items-center gap-3 rounded-xl border border-amber-200 bg-amber-50 p-4 text-base text-amber-800">
              <Spinner className="h-5 w-5 text-amber-600" />
              Đang xuất báo cáo ({report.mode})… giao diện vẫn tương tác được.
            </div>
          )}

          {report.status === "error" && (
            <div className="flex items-start gap-3 rounded-xl bg-red-50 p-4 text-base text-red-700 ring-1 ring-red-200">
              <svg className="mt-0.5 h-5 w-5 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M12 9v4m0 4h.01M10.29 3.86l-8.18 14.14A2 2 0 0 0 3.83 21h16.34a2 2 0 0 0 1.72-3L13.71 3.86a2 2 0 0 0-3.42 0z"
                />
              </svg>
              <span>{report.error}</span>
            </div>
          )}

          {report.status === "success" && (
            <div>
              <div className="mb-4 flex flex-wrap items-center gap-3 rounded-xl bg-emerald-50 p-4 ring-1 ring-emerald-200">
                <span
                  className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-sm font-semibold ${
                    report.data.mode === "blocking"
                      ? "bg-rose-100 text-rose-700"
                      : "bg-emerald-100 text-emerald-700"
                  }`}
                >
                  {report.data.mode === "blocking" ? "Blocking" : "Async"}
                </span>
                <div className="flex flex-wrap items-center gap-x-4 gap-y-1 text-base text-slate-700">
                  <span>
                    FE đo: <b className="font-mono">{report.elapsedMs} ms</b>
                  </span>
                  <span className="text-slate-300">·</span>
                  <span>
                    Server đo: <b className="font-mono">{report.data.elapsed_ms} ms</b>
                  </span>
                </div>
              </div>

              <div className="overflow-hidden rounded-xl ring-1 ring-slate-200">
                <div className="overflow-x-auto">
                  <table className="w-full text-left text-base">
                    <thead className="bg-slate-50 text-sm uppercase tracking-wide text-slate-500">
                      <tr>
                        <th className="px-4 py-3">Lớp</th>
                        <th className="px-4 py-3">Môn</th>
                        <th className="px-4 py-3">Giảng viên</th>
                        <th className="px-4 py-3 text-right">SV</th>
                        <th className="px-4 py-3 text-right">Hồ sơ</th>
                        <th className="px-4 py-3 text-right">Chờ</th>
                        <th className="px-4 py-3 text-right">Duyệt</th>
                        <th className="px-4 py-3 text-right">Từ chối</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100">
                      {report.data.rows.map((r) => (
                        <tr key={r.lop_id} className="transition hover:bg-slate-50/70">
                          <td className="px-4 py-3 font-mono text-sm text-slate-700">{r.ma_lop}</td>
                          <td className="px-4 py-3 text-slate-800">{r.ten_mon}</td>
                          <td className="px-4 py-3 text-slate-600">{r.giang_vien}</td>
                          <td className="px-4 py-3 text-right font-mono">{r.so_sinh_vien}</td>
                          <td className="px-4 py-3 text-right font-mono">{r.tong_ho_so}</td>
                          <td className="px-4 py-3 text-right font-mono text-amber-600">{r.cho_duyet}</td>
                          <td className="px-4 py-3 text-right font-mono text-emerald-600">{r.da_duyet}</td>
                          <td className="px-4 py-3 text-right font-mono text-rose-600">{r.tu_choi}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}
        </div>
      </section>

      {/* Tabs API nhẹ */}
      <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
        <div className="mb-4 flex flex-wrap gap-1 border-b border-slate-200">
          {TABS.map((t) => {
            const active = tab === t.id;
            return (
              <button
                key={t.id}
                onClick={() => setTab(t.id)}
                className={`-mb-px inline-flex items-center gap-2 border-b-2 px-4 py-2.5 text-base font-medium transition ${
                  active
                    ? "border-indigo-600 text-indigo-700"
                    : "border-transparent text-slate-500 hover:text-slate-800"
                }`}
              >
                {t.id === "health" ? (
                  <svg className="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M3 12h4l2-8 4 16 2-8h6" />
                  </svg>
                ) : (
                  <svg className="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <circle cx="12" cy="12" r="9" />
                    <path strokeLinecap="round" strokeLinejoin="round" d="M12 8v4l3 3" />
                  </svg>
                )}
                {t.label}
              </button>
            );
          })}
        </div>

        {tab === "health" && <HealthPoller />}
        {tab === "slow" && (
          <div className="max-w-sm">
            <SlowWidget title="Widget 1 giây" url="/demo/slow-1s" accent="emerald" />
          </div>
        )}
      </section>
    </div>
  );
}