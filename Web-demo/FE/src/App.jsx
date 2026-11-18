import { useState } from "react";
import DemoIO from "./pages/DemoIO";
import DemoReport from "./pages/DemoReport";
import Weather from "./pages/Weather";

const PAGES = [
  { id: "io", label: "Demo 1", sub: "I/O-bound", Component: DemoIO },
  { id: "report", label: "Demo 2", sub: "Blocking vs async", Component: DemoReport },
  { id: "weather", label: "API ngoài", sub: "Thời tiết", Component: Weather },
];

export default function App() {
  const [page, setPage] = useState("report");
  const Current = PAGES.find((p) => p.id === page).Component;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-indigo-50">
      <header className="sticky top-0 z-40 border-b border-slate-200/70 bg-white/80 backdrop-blur">
        <div className="mx-auto flex max-w-5xl items-center gap-3 px-6 py-3">
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-indigo-500 to-indigo-600 text-white shadow-sm">
              <svg className="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path strokeLinecap="round" strokeLinejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <div className="hidden md:block">
              <p className="text-sm font-semibold leading-tight text-slate-900">FastAPI + React</p>
              <p className="text-xs leading-tight text-slate-500">Concurrency demo</p>
            </div>
          </div>

          <nav className="ml-auto flex items-center gap-1 overflow-x-auto rounded-xl bg-slate-100/80 p-1">
            {PAGES.map((p) => {
              const active = page === p.id;
              return (
                <button
                  key={p.id}
                  onClick={() => setPage(p.id)}
                  className={`shrink-0 rounded-lg px-3.5 py-1.5 text-left transition ${
                    active
                      ? "bg-white text-slate-900 shadow-sm ring-1 ring-slate-200/80"
                      : "text-slate-600 hover:text-slate-900"
                  }`}
                >
                  <span className="block text-sm font-semibold leading-tight whitespace-nowrap">
                    {p.label}
                  </span>
                  <span
                    className={`hidden text-[11px] leading-tight whitespace-nowrap sm:block ${
                      active ? "text-slate-500" : "text-slate-400"
                    }`}
                  >
                    {p.sub}
                  </span>
                </button>
              );
            })}
          </nav>
        </div>
      </header>

      <Current />
    </div>
  );
}