import { useState } from "react";
import api from "../api/client";
import HealthPoller from "../components/HealthPoller";
import SlowWidget from "../components/SlowWidget";

const TABS = [
  {
    id: "health",
    label: "Health (theo dõi server)",
    icon: (
      <svg className="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <path strokeLinecap="round" strokeLinejoin="round" d="M3 12h4l2-8 4 16 2-8h6" />
      </svg>
    ),
  },
  {
    id: "slow",
    label: "API nhẹ 1 giây",
    icon: (
      <svg className="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <circle cx="12" cy="12" r="9" />
        <path strokeLinecap="round" strokeLinejoin="round" d="M12 8v4l3 3" />
      </svg>
    ),
  },
];

function Spinner({ className = "h-4 w-4" }) {
  return (
    <svg className={`animate-spin ${className}`} viewBox="0 0 24 24" fill="none">
      <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="3" opacity="0.25" />
      <path d="M22 12a10 10 0 0 1-10 10" stroke="currentColor" strokeWidth="3" strokeLinecap="round" />
    </svg>
  );
}

function ModeButton({ variant, loading, active, onClick, title, subtitle, icon, spinner }) {
  const styles = {
    blocking: {
      border: "border-rose-200 hover:border-rose-300",
      bg: "bg-rose-50 hover:bg-rose-100",
      chip: "bg-rose-500",
      title: "text-rose-900",
      subtitle: "text-rose-600",
      ring: "ring-rose-300",
    },
    async: {
      border: "border-emerald-200 hover:border-emerald-300",
      bg: "bg-emerald-50 hover:bg-emerald-100",
      chip: "bg-emerald-500",
      title: "text-emerald-900",
      subtitle: "text-emerald-600",
      ring: "ring-emerald-300",
    },
  }[variant];

  return (
    <button
      onClick={onClick}
      disabled={loading}
      className={`group relative overflow-hidden rounded-xl border-2 p-4 text-left transition active:scale-[0.99] disabled:cursor-not-allowed disabled:opacity-60 ${styles.border} ${styles.bg} ${
        active ? `ring-2 ring-offset-2 ${styles.ring}` : ""
      }`}
    >
      <div className="flex items-center gap-3">
        <div
          className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-lg text-white shadow-sm ${styles.chip}`}
        >
          {loading && active ? <Spinner className="h-5 w-5" /> : spinner}
        </div>
        <div className="min-w-0">
          <p className={`font-semibold leading-tight ${styles.title}`}>{title}</p>
          <p className={`text-xs leading-tight ${styles.subtitle}`}>{subtitle}</p>
        </div>
      </div>
      {icon && <div className="pointer-events-none absolute -right-4 -top-4 opacity-10">{icon}</div>}
    </button>
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
  const isBlocking = report.mode === "blocking";

  return (
    <div className="mx-auto max-w-5xl px-6 py-10">
      <header className="mb-8">
        <div className="inline-flex items-center gap-2 rounded-full bg-rose-100 px-3 py-1 text-sm font-medium text-rose-700">
          <span className="h-2 w-2 rounded-full bg-rose-500" />
          Demo 02
        </div>
        <h1 className="mt-3 text-4xl font-bold tracking-tight text-slate-900">
          Báo cáo nặng: blocking vs async
        </h1>
        <p className="mt-2 max-w-2xl text-lg text-slate-600">
          Bấm xuất báo cáo, rồi nhìn xuống panel{" "}
          <span className="font-medium text-slate-800">Giám sát phụ trợ</span> bên dưới — server có còn
          phục vụ các API nhẹ không?
        </p>
      </header>

      {/* SECTION 1: Xuất báo cáo */}
      <section className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
        {/* Header panel */}
        <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 bg-slate-50/60 px-5 py-4">
          <div>
            <h2 className="text-lg font-semibold text-slate-900">Xuất báo cáo</h2>
            <p className="text-sm text-slate-500">Chọn chế độ và quan sát tác động lên server</p>
          </div>
          <div className="flex items-center gap-2">
            <label className="inline-flex items-center gap-2 text-sm text-slate-700">
              <span className="text-slate-500">Chờ</span>
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
              title="Bấm thử để chứng minh UI không bị đơ"
              className="inline-flex items-center gap-1.5 rounded-lg border border-slate-200 bg-white px-2.5 py-1.5 text-sm text-slate-700 shadow-sm transition hover:bg-slate-50"
            >
              <svg className="h-3.5 w-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path strokeLinecap="round" strokeLinejoin="round" d="M15 15l-2 5L9 9l11 4-5 2z" />
              </svg>
              <span className="hidden sm:inline">Test UI</span>
              <span className="rounded bg-slate-100 px-1.5 py-0.5 font-mono text-xs text-slate-800">
                {count}
              </span>
            </button>
          </div>
        </div>

        {/* Mode buttons */}
        <div className="grid gap-3 p-5 sm:grid-cols-2">
          <ModeButton
            variant="blocking"
            loading={loading}
            active={loading && isBlocking}
            onClick={() => exportReport("blocking")}
            title="Xuất báo cáo (blocking)"
            subtitle="Chặn event loop — mọi request khác bị xếp hàng"
            spinner={
              <svg className="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="12" cy="12" r="9" />
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 8v4l3 3" />
              </svg>
            }
          />
          <ModeButton
            variant="async"
            loading={loading}
            active={loading && !isBlocking}
            onClick={() => exportReport("async")}
            title="Xuất báo cáo (async)"
            subtitle="Nhường event loop — request khác vẫn được phục vụ"
            spinner={
              <svg className="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path strokeLinecap="round" strokeLinejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            }
          />
        </div>

        {/* Kết quả */}
        <div className="border-t border-slate-100 bg-slate-50/40 p-5">
          {report.status === "idle" && (
            <div className="flex flex-col items-center justify-center rounded-xl border border-dashed border-slate-200 bg-white py-10 text-center">
              <svg className="h-9 w-9 text-slate-300" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                <circle cx="12" cy="12" r="9" />
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 8v4m0 4h.01" />
              </svg>
              <p className="mt-2 text-base font-medium text-slate-600">Chưa xuất báo cáo</p>
              <p className="mt-0.5 text-sm text-slate-400">
                Bấm một trong hai nút phía trên để bắt đầu
              </p>
            </div>
          )}

          {loading && (
            <div className="rounded-xl border border-amber-200 bg-amber-50 p-4">
              <div className="flex items-start gap-3">
                <Spinner className="mt-0.5 h-5 w-5 shrink-0 text-amber-600" />
                <div>
                  <p className="font-medium text-amber-900">
                    Đang xuất báo cáo — chế độ{" "}
                    <span className="font-mono">{report.mode}</span>
                  </p>
                  <p className="text-sm text-amber-700">
                    Giao diện vẫn tương tác được. Thử bấm "Test UI" hoặc chuyển tab bên dưới để kiểm chứng.
                  </p>
                </div>
              </div>
              <div className="relative mt-3 h-1.5 overflow-hidden rounded-full bg-amber-200">
                <div
                  className="absolute h-full w-2/5 rounded-full bg-amber-500"
                  style={{ animation: "progress-indeterminate 1.2s ease-in-out infinite" }}
                />
              </div>
            </div>
          )}

          {report.status === "error" && (
            <div className="flex items-start gap-3 rounded-xl bg-red-50 p-4 text-base text-red-700 ring-1 ring-red-200">
              <svg className="mt-0.5 h-5 w-5 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v4m0 4h.01M10.29 3.86l-8.18 14.14A2 2 0 0 0 3.83 21h16.34a2 2 0 0 0 1.72-3L13.71 3.86a2 2 0 0 0-3.42 0z" />
              </svg>
              <div>
                <p className="font-medium">Xuất báo cáo thất bại</p>
                <p className="text-sm text-red-600">{report.error}</p>
              </div>
            </div>
          )}

          {report.status === "success" && (
            <div className="space-y-4">
              {/* Metric cards */}
              <div className="grid gap-3 sm:grid-cols-3">
                <div className="rounded-xl border border-slate-200 bg-white p-3.5">
                  <p className="text-[11px] font-medium uppercase tracking-wider text-slate-500">
                    Chế độ
                  </p>
                  <div className="mt-1.5">
                    <span
                      className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-sm font-semibold ${
                        report.data.mode === "blocking"
                          ? "bg-rose-100 text-rose-700"
                          : "bg-emerald-100 text-emerald-700"
                      }`}
                    >
                      <span
                        className={`h-1.5 w-1.5 rounded-full ${
                          report.data.mode === "blocking" ? "bg-rose-500" : "bg-emerald-500"
                        }`}
                      />
                      {report.data.mode === "blocking" ? "Blocking" : "Async"}
                    </span>
                  </div>
                </div>

                <div className="rounded-xl border border-slate-200 bg-white p-3.5">
                  <p className="text-[11px] font-medium uppercase tracking-wider text-slate-500">
                    FE đo được
                  </p>
                  <p className="mt-1 font-mono text-2xl font-semibold text-slate-900">
                    {report.elapsedMs}
                    <span className="ml-1 text-sm font-normal text-slate-500">ms</span>
                  </p>
                </div>

                <div className="rounded-xl border border-slate-200 bg-white p-3.5">
                  <p className="text-[11px] font-medium uppercase tracking-wider text-slate-500">
                    Server đo được
                  </p>
                  <p className="mt-1 font-mono text-2xl font-semibold text-slate-900">
                    {report.data.elapsed_ms}
                    <span className="ml-1 text-sm font-normal text-slate-500">ms</span>
                  </p>
                </div>
              </div>

              {/* Table */}
              <div className="overflow-hidden rounded-xl border border-slate-200 bg-white">
                <div className="overflow-x-auto">
                  <table className="w-full text-left text-sm">
                    <thead className="bg-slate-50 text-[11px] uppercase tracking-wider text-slate-500">
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
                          <td className="px-4 py-3 font-mono text-xs text-slate-700">{r.ma_lop}</td>
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

      {/* SECTION 2: Giám sát phụ trợ */}
      <section className="mt-6 overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
        <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 bg-slate-50/60 px-5 py-4">
          <div>
            <h2 className="text-lg font-semibold text-slate-900">Giám sát phụ trợ</h2>
            <p className="text-sm text-slate-500">
              Nếu các API nhẹ này chậm, chứng tỏ server đang bị chặn
            </p>
          </div>

          <div className="flex items-center gap-1 rounded-xl bg-slate-100 p-1">
            {TABS.map((t) => {
              const active = tab === t.id;
              return (
                <button
                  key={t.id}
                  onClick={() => setTab(t.id)}
                  className={`inline-flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-sm font-medium transition ${
                    active
                      ? "bg-white text-slate-900 shadow-sm ring-1 ring-slate-200/80"
                      : "text-slate-600 hover:text-slate-900"
                  }`}
                >
                  {t.icon}
                  {t.label}
                </button>
              );
            })}
          </div>
        </div>

        <div className="p-5">
          {tab === "health" && <HealthPoller />}
          {tab === "slow" && (
            <div className="space-y-4">
              <div className="rounded-xl border border-indigo-100 bg-indigo-50/60 p-3 text-sm text-indigo-800">
                <span className="font-medium">Mẹo:</span> trong lúc xuất báo cáo blocking, nếu widget này
                load &gt; 1 giây thì đó là dấu hiệu server đang bị chặn — các request đang xếp hàng.
              </div>
              <div className="max-w-sm">
                <SlowWidget title="Widget 1 giây" url="/demo/slow-1s" accent="emerald" />
              </div>
            </div>
          )}
        </div>
      </section>
    </div>
  );
}