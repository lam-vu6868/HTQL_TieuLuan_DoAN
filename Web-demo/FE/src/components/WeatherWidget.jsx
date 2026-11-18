import { useState } from "react";
import { useFetch } from "../hooks/useFetch";

const CITIES = [
  { key: "ho-chi-minh", label: "TP. Hồ Chí Minh" },
  { key: "binh-duong", label: "Bình Dương" },
  { key: "ha-noi", label: "Hà Nội" },
  { key: "da-nang", label: "Đà Nẵng" },
];

export default function WeatherWidget() {
  const [city, setCity] = useState("ho-chi-minh");
  const [mock, setMock] = useState(false);
  const { status, data, error, elapsedMs, reload } = useFetch(
    `/weather/current?city=${city}${mock ? "&force_mock=true" : ""}`
  );

  return (
    <div className="max-w-md rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
      <div className="mb-4 flex items-center gap-3">
        <select
          value={city}
          onChange={(e) => setCity(e.target.value)}
          className="rounded-lg border border-slate-200 bg-white px-2 py-1.5 text-base"
        >
          {CITIES.map((c) => (
            <option key={c.key} value={c.key}>{c.label}</option>
          ))}
        </select>
        <label className="ml-auto inline-flex items-center gap-2 text-base text-slate-700">
          <input type="checkbox" checked={mock} onChange={(e) => setMock(e.target.checked)} />
          Giả lập mất mạng
        </label>
      </div>

      <div className="min-h-[110px]">
        {status === "loading" && <p className="text-base text-slate-500">Đang tải thời tiết...</p>}
        {status === "error" && (
          <p className="rounded-lg bg-red-50 p-3 text-base text-red-700">{error}</p>
        )}
        {status === "success" && (
          <div>
            <div className="flex items-baseline gap-3">
              <span className="text-5xl font-bold text-slate-900">{Math.round(data.temperature_c)}°C</span>
              <span className="text-lg text-slate-600">{data.description}</span>
            </div>
            <p className="mt-2 text-base text-slate-600">
              Độ ẩm {data.humidity_percent}% · Gió {data.wind_kmh} km/h
            </p>
            <div className="mt-3 flex flex-wrap items-center gap-2 text-sm">
              <span
                className={`rounded-full px-2.5 py-1 font-medium ${
                  data.source === "open-meteo"
                    ? "bg-emerald-50 text-emerald-700"
                    : "bg-amber-50 text-amber-700"
                }`}
              >
                Nguồn: {data.source}
              </span>
              <span className="rounded-lg bg-slate-100 px-2.5 py-1 text-slate-600">
                BE {data.elapsed_ms} ms · FE {elapsedMs} ms
              </span>
            </div>
            {data.fallback_reason && (
              <p className="mt-2 text-sm text-amber-700">Dùng dữ liệu giả: {data.fallback_reason}</p>
            )}
          </div>
        )}
      </div>

      <button
        onClick={reload}
        disabled={status === "loading"}
        className="mt-4 w-full rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-base font-medium text-slate-700 hover:bg-slate-50 disabled:opacity-50"
      >
        Tải lại
      </button>
    </div>
  );
}