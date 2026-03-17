import path from "node:path";

import { defineConfig } from "@playwright/test";

export default defineConfig({
	testDir: path.join(__dirname, "e2e"),
	fullyParallel: false,
	forbidOnly: !!process.env.CI,
	retries: process.env.CI ? 2 : 0,
	workers: 1,
	reporter: "list",
	use: {
		baseURL: "http://127.0.0.1:4173",
		headless: true,
		trace: "on-first-retry",
	},
	webServer: {
		command: "npm run dev -- --host 127.0.0.1 --port 4173",
		cwd: path.join(__dirname, "../frontend"),
		url: "http://127.0.0.1:4173",
		reuseExistingServer: !process.env.CI,
		timeout: 120000,
	},
});
