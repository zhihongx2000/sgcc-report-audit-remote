import { describe, expect, it, vi } from "vitest";

import {
	loadIngestionTrace,
	loadOverviewStats,
	loadQueryTrace,
	runEvaluation,
} from "../trace";

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

	it("loads ingestion traces in mock mode and keeps waterfall snapshot stable", async () => {
		const traces = await loadIngestionTrace({ useMock: true });

		expect(traces.length).toBeGreaterThan(0);
		expect(traces[0].stages).toHaveLength(5);
		expect(
			traces[0].stages.map((stage) => ({
				key: stage.key,
				durationMs: stage.durationMs,
				status: stage.status,
				method: stage.method,
				provider: stage.provider,
				inputCount: stage.inputCount,
				outputCount: stage.outputCount,
			})),
		).toMatchInlineSnapshot(`
			[
			  {
			    "durationMs": 4300,
			    "inputCount": 1,
			    "key": "load",
			    "method": "markitdown",
			    "outputCount": 1,
			    "provider": "local",
			    "status": "success",
			  },
			  {
			    "durationMs": 5200,
			    "inputCount": 1,
			    "key": "split",
			    "method": "recursive-character",
			    "outputCount": 336,
			    "provider": "langchain",
			    "status": "success",
			  },
			  {
			    "durationMs": 6900,
			    "inputCount": 336,
			    "key": "transform",
			    "method": "chunk-refine + image-caption",
			    "outputCount": 324,
			    "provider": "qwen-vl",
			    "status": "success",
			  },
			  {
			    "durationMs": 4700,
			    "inputCount": 324,
			    "key": "embed",
			    "method": "dense + sparse",
			    "outputCount": 324,
			    "provider": "openai",
			    "status": "success",
			  },
			  {
			    "durationMs": 4580,
			    "inputCount": 324,
			    "key": "upsert",
			    "method": "pgvector + bm25",
			    "outputCount": 312,
			    "provider": "postgresql",
			    "status": "success",
			  },
			]
		`);
	});

	it("loads ingestion traces in live mode with custom fetcher", async () => {
		const fetcher = vi.fn(async () => ({
			ok: true,
			status: 200,
			statusText: "OK",
			json: async () => ({
				success: true,
				data: [
					{
						id: "trace-custom-001",
						kind: "ingestion",
						sourcePath: "/tmp/custom.pdf",
						collection: "default",
						startedAt: "2026-03-17T10:00:00.000Z",
						finishedAt: "2026-03-17T10:00:05.000Z",
						totalDurationMs: 5000,
						status: "success",
						summary: "ok",
						chunkCount: 20,
						imageCount: 3,
						skippedCount: 0,
						failedCount: 0,
						stages: [
							{
								key: "load",
								name: "Load",
								durationMs: 1200,
								status: "success",
							},
						],
					},
				],
			}),
		}));

		const traces = await loadIngestionTrace({
			useMock: false,
			fallbackToMockOnError: false,
			fetcher,
		});

		expect(fetcher).toHaveBeenCalledTimes(1);
		expect(traces[0].id).toBe("trace-custom-001");
		expect(traces[0].stages[0].method).toBe("markitdown");
	});

	it("loads query traces in mock mode with dense-sparse-rerank payload", async () => {
		const traces = await loadQueryTrace({ useMock: true });

		expect(traces.length).toBeGreaterThan(0);
		expect(traces[0].stages.map((stage) => stage.key)).toEqual([
			"query_processing",
			"dense",
			"sparse",
			"fusion",
			"rerank",
		]);
		expect(traces[0].denseCandidates.length).toBeGreaterThan(0);
		expect(traces[0].sparseCandidates.length).toBeGreaterThan(0);
		expect(traces[0].topKResults[0].docId).toBe("doc-grid-stability");
	});

	it("loads query traces in live mode and falls back top-k from rerank", async () => {
		const fetcher = vi.fn(async () => ({
			ok: true,
			status: 200,
			statusText: "OK",
			json: async () => ({
				success: true,
				data: [
					{
						id: "query-custom-001",
						kind: "query",
						queryText: "what is grid stability",
						collection: "default",
						startedAt: "2026-03-17T10:00:00.000Z",
						totalDurationMs: 3000,
						status: "success",
						summary: "ok",
						stages: [
							{ key: "dense", name: "Dense Retrieval", durationMs: 900, status: "success" },
						],
						rerankCandidates: [
							{
								docId: "doc-1",
								title: "Doc 1",
								source: "sample#1",
								rank: 1,
								score: 0.91,
							},
						],
					},
				],
			}),
		}));

		const traces = await loadQueryTrace({
			useMock: false,
			fallbackToMockOnError: false,
			fetcher,
		});

		expect(fetcher).toHaveBeenCalledTimes(1);
		expect(traces[0].id).toBe("query-custom-001");
		expect(traces[0].topKResults).toHaveLength(1);
		expect(traces[0].topKResults[0].docId).toBe("doc-1");
	});

	it("runs evaluation in mock mode", async () => {
		const result = await runEvaluation({
			useMock: true,
			evaluator: "all",
			dataset: "golden_set.jsonl",
		});

		expect(result.runId).toContain("eval-run");
		expect(result.metrics.hitRate).toBeGreaterThan(0);
		expect(result.dataset).toBe("golden_set.jsonl");
	});

	it("runs evaluation in live mode with custom fetcher", async () => {
		const fetcher = vi.fn(async () => ({
			ok: true,
			status: 200,
			statusText: "OK",
			json: async () => ({
				success: true,
				data: {
					runId: "eval-live-001",
					status: "success",
					startedAt: "2026-03-17T15:00:00.000Z",
					durationMs: 2200,
					metrics: {
						hitRate: 0.91,
						mrr: 0.79,
						faithfulness: 0.84,
					},
					note: "ok",
				},
			}),
		}));

		const result = await runEvaluation({
			useMock: false,
			fallbackToMockOnError: false,
			fetcher,
			evaluator: "ragas",
			dataset: "golden_set-lite.jsonl",
		});

		expect(fetcher).toHaveBeenCalledTimes(1);
		expect(result.runId).toBe("eval-live-001");
		expect(result.evaluator).toBe("ragas");
		expect(result.dataset).toBe("golden_set-lite.jsonl");
	});
});
