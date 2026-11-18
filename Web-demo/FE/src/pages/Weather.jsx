import WeatherWidget from "../components/WeatherWidget";

export default function Weather() {
  return (
    <div className="mx-auto max-w-5xl px-6 py-10">
      <header className="mb-8">
        <div className="inline-flex items-center gap-2 rounded-full bg-sky-100 px-3 py-1 text-sm font-medium text-sky-700">
          <span className="h-2 w-2 rounded-full bg-sky-500" />
          Demo 03
        </div>
        <h1 className="mt-3 text-4xl font-bold tracking-tight text-slate-900">
          Gọi API ngoài (thời tiết)
        </h1>
        <p className="mt-2 max-w-2xl text-lg text-slate-600">
          Server đóng vai proxy gọi API bên thứ ba. Quan sát độ trễ và cách xử lý khi nhà cung cấp
          chậm hoặc lỗi — quan trọng vì event loop của bạn không được chặn bởi mạng bên ngoài.
        </p>
      </header>

      <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <WeatherWidget />
      </section>
    </div>
  );
}