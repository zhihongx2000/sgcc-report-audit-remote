import { expect, test } from "@playwright/test";

test.describe("dashboard skeleton smoke - trace pages", () => {
	test("menu jump renders ingestion manager skeleton", async ({ page }) => {
		await page.goto("/audit-results");
		await page.getByRole("link", { name: "Ingestion管理" }).click();

		await expect(page).toHaveURL(/\/ingestion-manager$/);
		await expect(page.getByRole("heading", { name: "摄取管理" })).toBeVisible();
		await expect(page.locator("section[data-page-id='ingestion-manager']")).toBeVisible();
		await expect(page.locator(".page-title")).toHaveText("Ingestion管理");
	});

	test("menu jump renders ingestion trace skeleton", async ({ page }) => {
		await page.goto("/audit-results");
		await page.getByRole("link", { name: "Ingestion追踪" }).click();

		await expect(page).toHaveURL(/\/ingestion-traces$/);
		await expect(page.getByRole("heading", { name: "摄取追踪" })).toBeVisible();
		await expect(page.locator("section[data-page-id='ingestion-traces']")).toBeVisible();
		await expect(page.locator(".page-title")).toHaveText("Ingestion追踪");

		await expect(page.locator("[data-testid='ingestion-trace-history']")).toBeVisible();
		await expect(page.locator("[data-testid^='trace-item-']").first()).toBeVisible();
		await expect(page.locator("[data-testid='waterfall-chart']")).toBeVisible();
		await expect(page.locator("[data-testid^='waterfall-stage-']")).toHaveCount(5);

		await page.locator("[data-testid='waterfall-stage-transform']").click();
		await expect(page.locator("[data-testid='ingestion-stage-drawer']")).toBeVisible();
		await expect(page.locator("[data-testid='ingestion-stage-method']")).toContainText(
			"chunk-refine",
		);
	});

	test("menu jump renders query trace skeleton", async ({ page }) => {
		await page.goto("/audit-results");
		await page.getByRole("link", { name: "Query追踪" }).click();

		await expect(page).toHaveURL(/\/query-traces$/);
		await expect(page.getByRole("heading", { name: "查询 Trace" })).toBeVisible();
		await expect(page.locator("section[data-page-id='query-traces']")).toBeVisible();
		await expect(page.locator(".page-title")).toHaveText("Query追踪");
	});
});
