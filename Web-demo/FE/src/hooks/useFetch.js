import { useCallback, useEffect, useState } from "react";
import axios from "axios";
import api from "../api/client";

const INITIAL = { status: "loading", data: null, error: null, elapsedMs: null };

export function useFetch(url) {
  const [state, setState] = useState(INITIAL);
  const [tick, setTick] = useState(0);

  useEffect(() => {
    const controller = new AbortController();

    async function load() {
      const start = performance.now();
      setState(INITIAL);
      try {
        const res = await api.get(url, { signal: controller.signal });
        setState({
          status: "success",
          data: res.data, // axios đã parse JSON sẵn
          error: null,
          elapsedMs: Math.round(performance.now() - start),
        });
      } catch (err) {
        if (axios.isCancel(err)) return; // request bị huỷ, bỏ qua
        setState({
          status: "error",
          data: null,
          // axios ném lỗi cho mọi status ngoài 2xx; detail là thông báo từ FastAPI
          error: err.response?.data?.detail ?? err.message,
          elapsedMs: Math.round(performance.now() - start),
        });
      }
    }

    load();
    return () => controller.abort();
  }, [url, tick]);

  const reload = useCallback(() => setTick((t) => t + 1), []);
  return { ...state, reload };
}