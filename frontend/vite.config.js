import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// In Docker the frontend container reaches the backend via the compose service name.
// Locally it falls back to localhost:8000.
const backendUrl = process.env.BACKEND_URL || "http://localhost:8000";

export default defineConfig({
  plugins: [react()],
  server: {
    host: true,   // bind 0.0.0.0 so Docker exposes the port
    port: 5173,
    proxy: {
      "/api": {
        target: backendUrl,
        changeOrigin: true,
      },
    },
  },
});
