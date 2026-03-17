import type {
	ApiEnvelope,
	AuditResult,
	FrontendMockDataMap,
	IngestionTask,
	OverviewStats,
	TraceRecord,
} from "../types";

const nowIso = () => new Date().toISOString();

export type MockKey = keyof FrontendMockDataMap;

export function mockAuditResult(): ApiEnvelope<AuditResult> {
	return {
		success: true,
		data: {
			reportId: "report-20260316-001",
			reportName: "华东区域电能质量分析报告",
			collection: "default",
			checkedAt: nowIso(),
			items: [
				{
					id: "check-01",
					title: "封面信息完整性",
					status: "pass",
					reason: "封面包含项目名称、日期和版本号。",
					evidence: ["page:1", "paragraph:cover-title"],
					updatedAt: nowIso(),
				},
				{
					id: "check-02",
					title: "目录结构一致性",
					status: "warn",
					reason: "目录页码与正文页码存在轻微偏移。",
					evidence: ["page:2", "paragraph:toc-3-2"],
					updatedAt: nowIso(),
				},
			],
		},
	};
}

export function mockOverviewStats(): ApiEnvelope<OverviewStats> {
	return {
		success: true,
		data: {
			componentCards: [
				{ title: "LLM", value: "azure / gpt-4o", detail: "provider + model" },
				{
					title: "Embedding",
					value: "openai / text-embedding-3-small / 1536",
					detail: "provider + model + dim",
				},
				{
					title: "VectorStore",
					value: "pgvector / rag_chunks / cosine",
					detail: "backend + table + metric",
				},
				{
					title: "Reranker",
					value: "cross_encoder / bge-reranker-v2-m3",
					detail: "backend + model",
				},
			],
			collectionStats: [
				{ name: "default", documents: 42, chunks: 1896, images: 117 },
				{ name: "sgcc-samples", documents: 16, chunks: 724, images: 54 },
			],
			healthMetrics: [
				{
					title: "最近 Ingestion Trace",
					value: "2026-03-16 14:58:42",
					sub: "总耗时 23.8s",
				},
				{
					title: "最近 Query Trace",
					value: "2026-03-16 15:08:11",
					sub: "总耗时 1.42s",
				},
				{
					title: "Trace 存储状态",
					value: "PostgreSQL + JSONL 镜像",
					sub: "obs_traces / obs_trace_stages",
				},
			],
		},
	};
}

export function mockIngestionTraces(): ApiEnvelope<TraceRecord[]> {
	return {
		success: true,
		data: [
			{
				id: "ing-trace-001",
				kind: "ingestion",
				startedAt: "2026-03-16T14:58:42.000Z",
				totalDurationMs: 23840,
				status: "success",
				summary: "Ingestion finished",
				stages: [
					{ name: "load", durationMs: 5120, status: "success" },
					{ name: "split", durationMs: 8060, status: "success" },
					{ name: "upsert", durationMs: 10660, status: "success" },
				],
			},
		],
	};
}

export function mockQueryTraces(): ApiEnvelope<TraceRecord[]> {
	return {
		success: true,
		data: [
			{
				id: "qry-trace-001",
				kind: "query",
				startedAt: "2026-03-16T15:08:11.000Z",
				totalDurationMs: 1420,
				status: "success",
				summary: "Hybrid retrieval completed",
				stages: [
					{ name: "dense", durationMs: 420, status: "success" },
					{ name: "sparse", durationMs: 380, status: "success" },
					{ name: "rerank", durationMs: 620, status: "success" },
				],
			},
		],
	};
}

export function mockIngestionTasks(): ApiEnvelope<IngestionTask[]> {
	return {
		success: true,
		data: [
			{
				taskId: "ing-task-001",
				sourcePath: "/data/documents/default/report.pdf",
				status: "running",
				progressPercent: 62,
				startedAt: "2026-03-16T15:11:10.000Z",
			},
		],
	};
}

const mockFactoryMap: { [K in MockKey]: () => FrontendMockDataMap[K] } = {
	auditResult: mockAuditResult,
	overviewStats: mockOverviewStats,
	ingestionTraces: mockIngestionTraces,
	queryTraces: mockQueryTraces,
	ingestionTasks: mockIngestionTasks,
};

export function getMockData<K extends MockKey>(key: K): FrontendMockDataMap[K] {
	return mockFactoryMap[key]();
}
