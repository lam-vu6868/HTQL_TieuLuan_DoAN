import { useState } from "react";
import SlowWidget from "../components/SlowWidget";
import Modal from "../components/Modal";

export default function DemoIO() {
  const [showModal, setShowModal] = useState(false);
  const [fail2s, setFail2s] = useState(false);
  const [count, setCount] = useState(0);

  return (
    <div className="mx-auto max-w-5xl px-6 py-10">
      <header className="mb-8">
        <div className="inline-flex items-center gap-2 rounded-full bg-indigo-100 px-3 py-1 text-sm font-medium text-indigo-700">
          <span className="h-2 w-2 rounded-full bg-indigo-500" />
          Demo 01
        </div>
        <h1 className="mt-3 text-4xl font-bold tracking-tight text-slate-900">
          I/O-bound không chặn UI
        </h1>
        <p className="mt-2 max-w-2xl text-lg text-slate-600">
          Ba widget gọi ba API chậm khác nhau. Widget nào xong trước hiện trước, và trong lúc chờ giao
          diện vẫn bấm được.
        </p>
      </header>

      <section className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
        <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 bg-slate-50/60 px-5 py-4">
          <div>
            <h2 className="text-lg font-semibold text-slate-900">Điều khiển</h2>
            <p className="text-sm text-slate-500">Thử tương tác khi widget đang tải dữ liệu</p>
          </div>

          <div className="flex flex-wrap items-center gap-2">
            <button
              onClick={() => setShowModal(true)}
              className="inline-flex items-center gap-2 rounded-xl bg-indigo-600 px-4 py-2 text-sm font-medium text-white shadow-sm transition hover:bg-indigo-700 active:scale-[0.98]"
            >
              <svg className="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 4v16m8-8H4" />
              </svg>
              Mở modal
            </button>

            <button
              onClick={() => setCount((c) => c + 1)}
              className="inline-flex items-center gap-1.5 rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm font-medium text-slate-700 shadow-sm transition hover:bg-slate-50"
            >
              <svg className="h-3.5 w-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path strokeLinecap="round" strokeLinejoin="round" d="M15 15l-2 5L9 9l11 4-5 2z" />
              </svg>
              Bấm thử
              <span className="rounded bg-slate-100 px-1.5 py-0.5 font-mono text-xs text-slate-800">
                {count}
              </span>
            </button>

            <label className="inline-flex cursor-pointer items-center gap-2 rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm text-slate-700 shadow-sm transition hover:bg-slate-50">
              <input
                type="checkbox"
                checked={fail2s}
                onChange={(e) => setFail2s(e.target.checked)}
                className="h-4 w-4 rounded border-slate-300 text-indigo-600 focus:ring-indigo-500"
              />
              Lỗi widget 2s
            </label>
          </div>
        </div>

        <div className="grid gap-4 p-5 md:grid-cols-3">
          <SlowWidget title="Widget 1 giây" url="/demo/slow-1s" accent="emerald" />
          <SlowWidget
            title="Widget 2 giây"
            url={`/demo/slow-2s${fail2s ? "?fail=true" : ""}`}
            accent="amber"
          />
          <SlowWidget title="Widget 3 giây" url="/demo/slow-3s" accent="rose" />
        </div>
      </section>

      <Modal open={showModal} onClose={() => setShowModal(false)}>
        <div className="text-center">
          <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-indigo-100">
            <svg className="h-6 w-6 text-indigo-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <h3 className="text-xl font-semibold text-slate-900">Modal vẫn mở được</h3>
          <p className="mt-1 text-base text-slate-600">
            Giao diện vẫn tương tác bình thường trong khi các widget đang tải dữ liệu.
          </p>
        </div>
      </Modal>
    </div>
  );
}