import axios from "axios";

const api = axios.create({
  baseURL: "/api", // Vite proxy chuyển /api sang http://localhost:8000
  timeout: 15000,
});

export default api;