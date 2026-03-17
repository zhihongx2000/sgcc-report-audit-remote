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
				id: "ing-trace-20260317-001",
				kind: "ingestion",
				sourcePath: "/data/documents/sgcc-default/华东区域风光储并网报告-v7.pdf",
				collection: "sgcc-default",
				startedAt: "2026-03-17T20:58:42.000Z",
				finishedAt: "2026-03-17T20:59:07.000Z",
				totalDurationMs: 25680,
				status: "success",
				summary: "摄取完成，主流程无失败阶段",
				chunkCount: 312,
				imageCount: 24,
				skippedCount: 3,
				failedCount: 0,
				stages: [
					{
						key: "load",
						name: "Load",
						durationMs: 4300,
						status: "success",
						method: "markitdown",
						provider: "local",
						inputCount: 1,
						outputCount: 1,
						detail: "解析 PDF 正文与目录结构，提取 24 张图像引用并建立初始 metadata。",
					},
					{
						key: "split",
						name: "Split",
						durationMs: 5200,
						status: "success",
						method: "recursive-character",
						provider: "langchain",
						inputCount: 1,
						outputCount: 336,
						detail: "按标题路径和段落边界切分，生成 336 个候选 chunk。",
					},
					{
						key: "transform",
						name: "Transform",
						durationMs: 6900,
						status: "success",
						method: "chunk-refine + image-caption",
						provider: "qwen-vl",
						inputCount: 336,
						outputCount: 324,
						detail: "清洗页眉页脚并注入图片描述，12 个低质量 chunk 被过滤。",
					},
					{
						key: "embed",
						name: "Embed",
						durationMs: 4700,
						status: "success",
						method: "dense + sparse",
						provider: "openai",
						inputCount: 324,
						outputCount: 324,
						detail: "批量执行 dense/sparse 编码，复用缓存后实际编码 318 条。",
					},
					{
						key: "upsert",
						name: "Upsert",
						durationMs: 4580,
						status: "success",
						method: "pgvector + bm25",
						provider: "postgresql",
						inputCount: 324,
						outputCount: 312,
						detail: "完成幂等 upsert，12 条重复记录被去重，最终落库 312 条。",
					},
				],
			},
			{
				id: "ing-trace-20260317-002",
				kind: "ingestion",
				sourcePath: "/data/documents/sgcc-samples/沿海风电接入系统复核报告.pdf",
				collection: "sgcc-samples",
				startedAt: "2026-03-17T19:21:15.000Z",
				finishedAt: "2026-03-17T19:21:36.000Z",
				totalDurationMs: 21120,
				status: "warning",
				summary: "摄取完成，但 transform 阶段有降级处理",
				chunkCount: 188,
				imageCount: 17,
				skippedCount: 0,
				failedCount: 1,
				stages: [
					{
						key: "load",
						name: "Load",
						durationMs: 3980,
						status: "success",
						method: "markitdown",
						provider: "local",
						inputCount: 1,
						outputCount: 1,
						detail: "成功解析 PDF，识别附录中的 17 张截图。",
					},
					{
						key: "split",
						name: "Split",
						durationMs: 4620,
						status: "success",
						method: "recursive-character",
						provider: "langchain",
						inputCount: 1,
						outputCount: 196,
						detail: "切分完成并保留 heading_path，平均 chunk 长度 438 字。",
					},
					{
						key: "transform",
						name: "Transform",
						durationMs: 5440,
						status: "warning",
						method: "chunk-refine + image-caption",
						provider: "qwen-vl",
						inputCount: 196,
						outputCount: 194,
						detail: "Vision 调用发生 1 次超时，降级为缓存描述并继续流程。",
					},
					{
						key: "embed",
						name: "Embed",
						durationMs: 3840,
						status: "success",
						method: "dense + sparse",
						provider: "openai",
						inputCount: 194,
						outputCount: 194,
						detail: "编码阶段全部成功，批量任务 4 组完成。",
					},
					{
						key: "upsert",
						name: "Upsert",
						durationMs: 3240,
						status: "success",
						method: "pgvector + bm25",
						provider: "postgresql",
						inputCount: 194,
						outputCount: 188,
						detail: "完成 upsert，6 条重复 chunk 被幂等合并。",
					},
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
