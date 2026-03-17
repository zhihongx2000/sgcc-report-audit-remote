import { expect, test } from "@playwright/test";

test.describe("dashboard skeleton smoke - audit and core pages", () => {
	test("homepage redirects to audit result route", async ({ page }) => {
		await page.goto("/");

		await expect(page).toHaveURL(/\/audit-results$/);
		await expect(page.getByRole("heading", { name: "审查结果" })).toBeVisible();
		await expect(page.locator(".page-title")).toHaveText("报告审查");
	});

	test("audit result page renders 20 items and supports status filter", async ({ page }) => {
		await page.goto("/audit-results");

		const tableRows = page.locator("[data-testid^='check-row-']");
		await expect(tableRows).toHaveCount(20);

		await page.locator("[data-testid='status-filter']").selectOption("fail");
		await expect(tableRows).toHaveCount(3);
	});

	test("evidence drawer supports page anchor and image jump", async ({ page }) => {
		await page.goto("/audit-results");

		const trigger = page.locator(
			"[data-testid='evidence-trigger-check-01-check-01-e2-report-20260317-001']",
		);
		await trigger.click();

		const drawer = page.locator("[data-testid='evidence-drawer']");
		await expect(drawer).toBeVisible();
		await expect(drawer).toContainText("check-01");

		await page.locator("[data-testid='evidence-jump-page']").click();
		await expect(page.locator("[data-testid='evidence-jump-notice']")).toContainText(
			"页码",
		);

		await page.locator("[data-testid='evidence-jump-anchor']").click();
		await expect(page.locator("[data-testid='evidence-jump-notice']")).toContainText(
			"段落锚点",
		);

		await page.locator("[data-testid='evidence-jump-image']").click();
		await expect(page.locator("[data-testid='evidence-jump-notice']")).toContainText(
			"图片缩略图",
		);

		await expect(page.locator("[data-testid='check-row-check-01']")).toHaveClass(
			/check-row--active/,
		);
		await expect(trigger).toHaveClass(/is-active/);
	});

	test("report tree selection updates right-side details", async ({ page }) => {
		await page.goto("/audit-results");

		await expect(page.locator("[data-testid='report-meta-id']")).toContainText(
			"report-20260317-001",
		);
		await expect(page.locator("[data-testid='status-fail-count']")).toHaveText("3");

		await page.locator("[data-testid='report-node-report-20260317-002']").click();

		await expect(page.locator("[data-testid='report-meta-id']")).toContainText(
			"report-20260317-002",
		);
		await expect(page.locator("[data-testid='status-fail-count']")).toHaveText("1");
	});

	test("menu jump renders overview skeleton", async ({ page }) => {
		await page.goto("/audit-results");
		await page.getByRole("link", { name: "系统总览" }).click();

		await expect(page).toHaveURL(/\/overview$/);
		await expect(page.getByRole("heading", { name: "系统总览" })).toBeVisible();
		await expect(page.locator("section[data-page-id='overview']")).toBeVisible();
		await expect(page.locator(".page-title")).toHaveText("系统总览");
		await expect(page.locator("[data-testid='overview-provider-model']")).toContainText(
			"/",
		);
		await expect(page.locator("[data-testid='overview-vectorstore']")).toContainText(
			"pgvector",
		);
		await expect(page.locator("[data-testid='overview-health-line']")).not.toHaveText(
			"",
		);
		await expect(page.locator("[data-testid='overview-config-llm']")).toBeVisible();
	});

	test("menu jump renders data browser skeleton", async ({ page }) => {
		await page.goto("/audit-results");
		await page.getByRole("link", { name: "数据浏览器" }).click();

		await expect(page).toHaveURL(/\/data-browser$/);
		await expect(page.getByRole("heading", { name: "数据浏览" })).toBeVisible();
		await expect(page.locator("section[data-page-id='data-browser']")).toBeVisible();
		await expect(page.locator(".page-title")).toHaveText("数据浏览器");
	});

	test("menu jump renders evaluation skeleton", async ({ page }) => {
		await page.goto("/audit-results");
		await page.getByRole("link", { name: "评估面板" }).click();

		await expect(page).toHaveURL(/\/evaluation$/);
		await expect(page.getByRole("heading", { name: "评估面板" })).toBeVisible();
		await expect(page.locator("section[data-page-id='evaluation']")).toBeVisible();
		await expect(page.locator(".page-title")).toHaveText("评估面板");
	});
});
