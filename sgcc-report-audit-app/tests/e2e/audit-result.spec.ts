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

	test("menu jump renders overview skeleton", async ({ page }) => {
		await page.goto("/audit-results");
		await page.getByRole("link", { name: "系统总览" }).click();

		await expect(page).toHaveURL(/\/overview$/);
		await expect(page.getByRole("heading", { name: "系统总览" })).toBeVisible();
		await expect(page.locator("section[data-page-id='overview']")).toBeVisible();
		await expect(page.locator(".page-title")).toHaveText("系统总览");
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
