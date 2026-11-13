import { defineConfig, devices } from "@playwright/test";

// O E2E roda contra a stack completa (frontend + API + PostgreSQL) já no ar.
// `make e2e` sobe uma stack isolada; `make frontend-test-e2e` usa a que estiver
// rodando (padrão: stack de desenvolvimento em http://localhost:5173).
const baseURL = process.env.E2E_BASE_URL ?? "http://localhost:5173";

export default defineConfig({
  testDir: "./tests/e2e",
  forbidOnly: Boolean(process.env.CI),
  retries: process.env.CI ? 1 : 0,
  reporter: process.env.CI ? [["github"], ["html", { open: "never" }]] : "list",
  use: { baseURL, trace: "on-first-retry" },
  projects: [{ name: "chromium", use: { ...devices["Desktop Chrome"] } }],
});
