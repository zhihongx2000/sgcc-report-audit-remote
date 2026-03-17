import { describe, expect, it, vi } from "vitest";

import { loadOverviewStats } from "../trace";

describe("trace api", () => {
	it("loads overview stats in mock mode", async () => {
		const data = await loadOverviewStats({ useMock: true });

		expect(data.componentCards.length).toBeGreaterThan(0);
		expect(
			data.componentCards.some((card) => card.title.toLowerCase() === "llm"),
		).toBe(true);
		expect(
			data.componentCards.some((card) => card.title.toLowerCase() === "vectorstore"),
		).toBe(true);
	});

	it("loads overview stats in live mode with custom fetcher", async () => {
		const fetcher = vi.fn(async () => ({
			ok: true,
			status: 200,
			statusText: "OK",
			json: async () => ({
				success: true,
				data: {
					componentCards: [
						{ title: "LLM", value: "openai / gpt-4o", detail: "provider + model" },
						{
							title: "VectorStore",
							value: "pgvector / rag_chunks / cosine",
							detail: "backend + table + metric",
						},
					],
					collectionStats: [
						{ name: "default", documents: 2, chunks: 120, images: 8 },
					],
					healthMetrics: [
						{
							title: "最近 Query Trace",
							value: "2026-03-17 19:40:00",
							sub: "总耗时 0.88s",
						},
					],
				},
			}),
		}));

		const data = await loadOverviewStats({
			useMock: false,
			fallbackToMockOnError: false,
			fetcher,
			baseUrl: "http://localhost:8080",
		});

		expect(fetcher).toHaveBeenCalledTimes(1);
		expect(data.collectionStats[0].documents).toBe(2);
		expect(data.healthMetrics[0].title).toContain("Query");
	});

	it("throws error when API reports unsuccessful payload", async () => {
		const fetcher = vi.fn(async () => ({
			ok: true,
			status: 200,
			statusText: "OK",
			json: async () => ({
				success: false,
				message: "overview not available",
				data: null,
			}),
		}));

		await expect(
			loadOverviewStats({
				useMock: false,
				fallbackToMockOnError: false,
				fetcher,
			}),
		).rejects.toThrow("overview not available");
	});
});
