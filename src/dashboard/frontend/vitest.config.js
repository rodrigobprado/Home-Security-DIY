import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: "./src/test/setup.js",
    coverage: {
      provider: "v8",
      reporter: ["text", "lcov"],
      include: ["src/**/*.js", "src/**/*.jsx"],
      exclude: [
        "src/**/*.test.*",
        "src/main.jsx",
        "src/test/**",
        "src/pages/AssetsAdmin.jsx",
        "src/components/OperationalMap.jsx",
        "src/hooks/useWebSocket.js",
      ],
      thresholds: {
        lines: 90,
        functions: 85,
        branches: 60,
        statements: 85,
      },
    },
  },
});
