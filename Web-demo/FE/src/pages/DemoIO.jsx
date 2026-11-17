import { useState } from "react";
import SlowWidget from "../components/SlowWidget";
import Modal from "../components/Modal";

export default function DemoIO() {
  const [showModal, setShowModal] = useState(false);
  const [fail2s, setFail2s] = useState(false);
  const [count, setCount] = useState(0);

  return (
    <div className="mx-auto max-w-4xl p-6">
      <h1 className="text-2xl font-bold">Demo 1: I/O-bound không chặn UI</h1>
      <p className="mt-1 text-slate-600">
        Ba widget gọi ba API chậm khác nhau. Widget nào xong trước hiện trước,
        và trong lúc chờ giao diện vẫn bấm được.
      </p>

      <div className="mt-4 flex flex-wrap items-center gap-4">
        <button
          onClick={() => setShowModal(true)}
          className="rounded bg-blue-600 px-4 py-2 text-white"
        >
          Mở modal
        </button>
        <button
          onClick={() => setCount((c) => c + 1)}
          className="rounded bg-slate-200 px-4 py-2"
        >
          Bấm thử: {count}
        </button>
        <label className="flex items-center gap-2 text-sm">
          <input
            type="checkbox"
            checked={fail2s}
            onChange={(e) => setFail2s(e.target.checked)}
          />
          Giả lập lỗi cho widget 2 giây
        </label>
      </div>

      <div className="mt-6 grid gap-4 md:grid-cols-3">
        <SlowWidget title="Widget 1 giây" url="/demo/slow-1s" />
        <SlowWidget
        title="Widget 2 giây"
        url={`/demo/slow-2s${fail2s ? "?fail=true" : ""}`}
        />
        <SlowWidget title="Widget 3 giây" url="/demo/slow-3s" />
      </div>

      <Modal open={showModal} onClose={() => setShowModal(false)}>
        <p>Modal mở được dù widget đang tải.</p>
      </Modal>
    </div>
  );
}