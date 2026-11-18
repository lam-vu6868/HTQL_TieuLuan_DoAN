import { useState } from "react";
import DemoIO from "./pages/DemoIO";
import DemoReport from "./pages/DemoReport";

const PAGES = [
  { id: "io", label: "Demo 1", sub: "I/O-bound", Component: DemoIO },
  { id: "report", label: "Demo 2", sub: "Blocking vs async", Component: DemoReport },
];

export default function App() {
  const [page, setPage] = useState("report");
  const Current = PAGES.find((p) => p.id === page).Component;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-indigo-50">
      <header className="sticky top-0 z-40 border-b border-slate-200/70 bg-white/80 backdrop-blur">
        <div className="mx-auto flex max-w-5xl items-center gap-4 px-6 py-3">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-indigo-600 text-white shadow-sm">
            <svg className="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path strokeLinecap="round" strokeLinejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <div className="mr-2 hidden sm:block">
            <p className="text-sm font-semibold text-slate-900">FastAPI + React</p>
            <p className="text-xs text-slate-500">Demo concurrency</p>
          </div>

          <nav className="flex gap-1">
            {PAGES.map((p) => {
              const active = page === p.id;
              return (
                <button
                  key={p.id}
                  onClick={() => setPage(p.id)}
                  className={`rounded-xl px-3 py-1.5 text-left transition ${
                    active
                      ? "bg-slate-900 text-white shadow-sm"
                      : "text-slate-600 hover:bg-slate-100"
                  }`}
                >
                  <span className="block text-sm font-semibold">{p.label}</span>
                  <span className={`block text-xs ${active ? "text-slate-300" : "text-slate-400"}`}>
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