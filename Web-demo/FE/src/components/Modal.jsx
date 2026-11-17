export default function Modal({ open, onClose, children }) {
  if (!open) return null;
  return (
    <div
      className="fixed inset-0 flex items-center justify-center bg-black/40"
      onClick={onClose}
    >
      <div
        className="w-80 rounded-lg bg-white p-6 shadow-lg"
        onClick={(e) => e.stopPropagation()}
      >
        {children}
        <button
          onClick={onClose}
          className="mt-4 rounded bg-slate-800 px-3 py-1 text-sm text-white"
        >
          Đóng
        </button>
      </div>
    </div>
  );
}