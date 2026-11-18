import { useFetch } from "../hooks/useFetch";

const ACCENTS = {
  emerald: {
    ring: "ring-emerald-500",
    bar: "bg-emerald-500",
    badge: "bg-emerald-50 text-emerald-700",
    dot: "bg-emerald-500",
  },
  amber: {
    ring: "ring-amber-500",
    bar: "bg-amber-500",
    badge: "bg-amber-50 text-amber-700",
    dot: "bg-amber-500",
  },
  rose: {
    ring: "ring-rose-500",
    bar: "bg-rose-500",
    badge: "bg-rose-50 text-rose-700",
    dot: "bg-rose-500",
  },
};

export default function SlowWidget({ title, url, accent = "emerald" }) {
  const { status, data, error, elapsedMs, reload } = useFetch(url);
  const a = ACCENTS[accent];

  return (
    <div
      className={`group relative overflow-hidden rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition hover:shadow-md ${
        status === "loading" ? "ring-2 ring-offset-2 " + a.ring : ""
      }`}
    >
      {/* Accent bar */}
      <div className={`absolute left-0 top-0 h-1 w-full ${a.bar}`} />

      {/* Header */}
      <div className="mb-4 flex items-center justify-between">
        <h3 className="text-xl font-semibold text-slate-900">{title}</h3>

        {status === "loading" && (
          <span className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-sm font-medium ${a.badge}`}>
            <span className={`h-2 w-2 animate-pulse rounded-full ${a.dot}`} />
            Đang tải
          </span>
        )}
        {status === "success" && (
          <span className="inline-flex items-center gap-1.5 rounded-full bg-emerald-50 px-2.5 py-1 text-sm font-medium text-emerald-700">
            <span className="h-2 w-2 rounded-full bg-emerald-500" />
            Thành công
          </span>
        )}
        {status === "error" && (
          <span className="inline-flex items-center gap-1.5 rounded-full bg-red-50 px-2.5 py-1 text-sm font-medium text-red-700">
            <span className="h-2 w-2 rounded-full bg-red-500" />
            Lỗi
          </span>
        )}
      </div>

      {/* Body */}
      <div className="min-h-[84px]">
        {status === "loading" && (
          <div className="flex items-center gap-3 text-slate-500">
            <svg className="h-5 w-5 animate-spin text-slate-400" viewBox="0 0 24 24" fill="none">
              <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="3" opacity="0.25" />
              <path d="M22 12a10 10 0 0 1-10 10" stroke="currentColor" strokeWidth="3" strokeLinecap="round" />
            </svg>
            <span className="text-base">Đang tải dữ liệu...</span>
          </div>
        )}

        {status === "success" && (
          <div>
            <p className="text-base font-medium text-slate-800">{data.message}</p>
            <div className="mt-3 inline-flex items-center gap-1.5 rounded-lg bg-slate-100 px-2.5 py-1 text-sm text-slate-600">
              <svg className="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="12" cy="12" r="9" />
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 7v5l3 3" />
              </svg>
              FE đo được <span className="font-mono font-semibold text-slate-900">{elapsedMs} ms</span>
            </div>
          </div>
        )}

        {status === "error" && (
          <div className="flex items-start gap-2 rounded-lg bg-red-50 p-3 text-base text-red-700">
            <svg className="mt-0.5 h-4 w-4 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v4m0 4h.01M10.29 3.86l-8.18 14.14A2 2 0 0 0 3.83 21h16.34a2 2 0 0 0 1.72-3L13.71 3.86a2 2 0 0 0-3.42 0z" />
            </svg>
            <span>{error}</span>
          </div>
        )}
      </div>

      {/* Footer */}
      <button
        onClick={reload}
        disabled={status === "loading"}
        className="mt-4 inline-flex w-full items-center justify-center gap-2 rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-base font-medium text-slate-700 transition hover:bg-slate-50 active:scale-[0.99] disabled:cursor-not-allowed disabled:opacity-50"
      >
        <svg
          className={`h-4 w-4 ${status === "loading" ? "animate-spin" : ""}`}
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
        >
          <path strokeLinecap="round" strokeLinejoin="round" d="M4 4v6h6M20 20v-6h-6M20 8a8 8 0 0 0-14.93-2M4 16a8 8 0 0 0 14.93 2" />
        </svg>
        Tải lại
      </button>
    </div>
  );
}