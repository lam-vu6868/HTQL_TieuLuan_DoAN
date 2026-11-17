import { useFetch } from "../hooks/useFetch";

export default function SlowWidget({ title, url }) {
  const { status, data, error, elapsedMs, reload } = useFetch(url);

  const border = {
    loading: "border-slate-300",
    success: "border-green-500",
    error: "border-red-500",
  }[status];

  return (
    <div className={`rounded-lg border-2 ${border} bg-white p-4 shadow-sm`}>
      <h3 className="font-semibold">{title}</h3>

      {status === "loading" && (
        <p className="mt-2 animate-pulse text-slate-500">Đang tải...</p>
      )}

      {status === "success" && (
        <div className="mt-2 text-green-700">
          <p>{data.message}</p>
          <p className="text-sm text-slate-500">FE đo được: {elapsedMs} ms</p>
        </div>
      )}

      {status === "error" && (
        <p className="mt-2 text-red-600">Lỗi: {error}</p>
      )}

      <button
        onClick={reload}
        disabled={status === "loading"}
        className="mt-3 rounded bg-slate-800 px-3 py-1 text-sm text-white disabled:opacity-40"
      >
        Tải lại
      </button>
    </div>
  );
}