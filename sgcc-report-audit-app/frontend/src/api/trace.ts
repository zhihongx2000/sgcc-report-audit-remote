import { createHttpClient, type HttpClientOptions } from "./http";

import type {
	ApiEnvelope,
	EvaluationRunRecord,
	OverviewStats,
} from "../types";

type TraceApiEnvelope<T> = ApiEnvelope<T>;

export type TraceStageStatus = "success" | "warning" | "failed" | "running";

export type IngestionTraceStage = {
	key: string;
	name: string;
	durationMs: number;
	status: TraceStageStatus;
	method: string;
	provider: string;
	inputCount: number;
	outputCount: number;
	detail: string;
};

export type IngestionTraceRecord = {
	id: string;
	kind: "ingestion";
	sourcePath: string;
	collection: string;
	startedAt: string;
	finishedAt: string;
	totalDurationMs: number;
	status: TraceStageStatus;
	summary: string;
	chunkCount: number;
	imageCount: number;
	skippedCount: number;
	failedCount: number;
	stages: IngestionTraceStage[];
};

export type QueryTraceStage = IngestionTraceStage;

export type QueryTraceCandidate = {
	docId: string;
	title: string;
	source: string;
	rank: number;
	score: number;
	snippet: string;
};

export type QueryTraceRecord = {
	id: string;
	kind: "query";
	queryText: string;
	collection: string;
	startedAt: string;
	finishedAt: string;
	totalDurationMs: number;
	status: TraceStageStatus;
	summary: string;
	rerankBackend: string;
	fallbackTriggered: boolean;
	stages: QueryTraceStage[];
	denseCandidates: QueryTraceCandidate[];
	sparseCandidates: QueryTraceCandidate[];
	fusionCandidates: QueryTraceCandidate[];
	rerankCandidates: QueryTraceCandidate[];
	topKResults: QueryTraceCandidate[];
};

const DEFAULT_INGESTION_STAGE_ORDER = [
	"load",
	"split",
	"transform",
	"embed",
	"upsert",
] as const;

const DEFAULT_QUERY_STAGE_ORDER = [
	"query_processing",
	"dense",
	"sparse",
	"fusion",
	"rerank",
] as const;

const STAGE_NAME_FALLBACK_MAP: Record<string, string> = {
	load: "Load",
	split: "Split",
	transform: "Transform",
	embed: "Embed",
	upsert: "Upsert",
};

const STAGE_METHOD_FALLBACK_MAP: Record<string, string> = {
	load: "markitdown",
	split: "recursive-character",
	transform: "chunk-refine + metadata-enrich + image-caption",
	embed: "dense + sparse",
	upsert: "pgvector + bm25",
};

const STAGE_PROVIDER_FALLBACK_MAP: Record<string, string> = {
	load: "local",
	split: "langchain",
	transform: "qwen-vl",
	embed: "openai",
	upsert: "postgresql",
};

const QUERY_STAGE_NAME_FALLBACK_MAP: Record<string, string> = {
	query_processing: "Query Processing",
	dense: "Dense Retrieval",
	sparse: "Sparse Retrieval",
	fusion: "Fusion",
	rerank: "Rerank",
};

const QUERY_STAGE_METHOD_FALLBACK_MAP: Record<string, string> = {
	query_processing: "keyword-extractor + query-expander",
	dense: "cosine similarity",
	sparse: "bm25",
	fusion: "rrf",
	rerank: "cross-encoder",
};

const QUERY_STAGE_PROVIDER_FALLBACK_MAP: Record<string, string> = {
	query_processing: "rag-core",
	dense: "openai-embedding-3-small",
	sparse: "bm25-index",
	fusion: "rrf-engine",
	rerank: "bge-reranker-v2-m3",
};

type UnknownRecord = Record<string, unknown>;

function asRecord(value: unknown): UnknownRecord | null {
	if (!value || typeof value !== "object") {
		return null;
	}

	return value as UnknownRecord;
}

function asString(value: unknown, fallback: string): string {
	if (typeof value === "string" && value.trim().length > 0) {
		return value;
	}

	return fallback;
}

function asNumber(value: unknown, fallback: number): number {
	if (typeof value === "number" && Number.isFinite(value)) {
		return value;
	}

	return fallback;
}

function asBoolean(value: unknown, fallback: boolean): boolean {
	if (typeof value === "boolean") {
		return value;
	}

	return fallback;
}

function asStatus(value: unknown, fallback: TraceStageStatus): TraceStageStatus {
	if (
		value === "success" ||
		value === "warning" ||
		value === "failed" ||
		value === "running"
	) {
		return value;
	}

	return fallback;
}

function stageOrderIndex(key: string): number {
	const index = DEFAULT_INGESTION_STAGE_ORDER.findIndex((item) => item === key);
	return index < 0 ? DEFAULT_INGESTION_STAGE_ORDER.length + 1 : index;
}

function queryStageOrderIndex(key: string): number {
	const index = DEFAULT_QUERY_STAGE_ORDER.findIndex((item) => item === key);
	return index < 0 ? DEFAULT_QUERY_STAGE_ORDER.length + 1 : index;
}

function normalizeStage(
	rawStage: unknown,
	index: number,
	traceId: string,
): IngestionTraceStage {
	const record = asRecord(rawStage);
	const rawName = asString(record?.name, `stage-${index + 1}`);
	const key = asString(record?.key, rawName.toLowerCase());
	const durationMs = Math.max(1, asNumber(record?.durationMs, 1));

	return {
		key,
		name: asString(record?.name, STAGE_NAME_FALLBACK_MAP[key] ?? rawName),
		durationMs,
		status: asStatus(record?.status, "success"),
		method: asString(record?.method, STAGE_METHOD_FALLBACK_MAP[key] ?? "-"),
		provider: asString(record?.provider, STAGE_PROVIDER_FALLBACK_MAP[key] ?? "-"),
		inputCount: asNumber(record?.inputCount, 0),
		outputCount: asNumber(record?.outputCount, 0),
		detail: asString(
			record?.detail,
			`${traceId} ${key} stage detail not provided by backend; fallback mock detail is used.`,
		),
	};
}

function normalizeStages(rawStages: unknown, traceId: string): IngestionTraceStage[] {
	const source = Array.isArray(rawStages) ? rawStages : [];
	const normalized = source.map((stage, index) => normalizeStage(stage, index, traceId));

	if (normalized.length === 0) {
		return DEFAULT_INGESTION_STAGE_ORDER.map((key, index) =>
			normalizeStage(
				{
					key,
					name: STAGE_NAME_FALLBACK_MAP[key],
					durationMs: 1,
					status: "running",
					method: STAGE_METHOD_FALLBACK_MAP[key],
					provider: STAGE_PROVIDER_FALLBACK_MAP[key],
					inputCount: index === 0 ? 1 : 0,
					outputCount: 0,
					detail: "No stage details available.",
				},
				index,
				traceId,
			),
		);
	}

	return [...normalized].sort((a, b) => stageOrderIndex(a.key) - stageOrderIndex(b.key));
}

function normalizeTrace(rawTrace: unknown, index: number): IngestionTraceRecord {
	const record = asRecord(rawTrace);
	const id = asString(record?.id, `ing-trace-${String(index + 1).padStart(3, "0")}`);
	const startedAt = asString(record?.startedAt, new Date(0).toISOString());
	const stages = normalizeStages(record?.stages, id);
	const totalDurationMs = Math.max(
		1,
		asNumber(
			record?.totalDurationMs,
			stages.reduce((sum, stage) => sum + stage.durationMs, 0),
		),
	);

	return {
		id,
		kind: "ingestion",
		sourcePath: asString(record?.sourcePath, "unknown-source"),
		collection: asString(record?.collection, "default"),
		startedAt,
		finishedAt: asString(record?.finishedAt, startedAt),
		totalDurationMs,
		status: asStatus(record?.status, "success"),
		summary: asString(record?.summary, "ingestion trace"),
		chunkCount: Math.max(0, asNumber(record?.chunkCount, 0)),
		imageCount: Math.max(0, asNumber(record?.imageCount, 0)),
		skippedCount: Math.max(0, asNumber(record?.skippedCount, 0)),
		failedCount: Math.max(0, asNumber(record?.failedCount, 0)),
		stages,
	};
}

function normalizeQueryStage(
	rawStage: unknown,
	index: number,
	traceId: string,
): QueryTraceStage {
	const record = asRecord(rawStage);
	const rawName = asString(record?.name, `stage-${index + 1}`);
	const key = asString(record?.key, rawName.toLowerCase().replace(/\s+/g, "_"));
	const durationMs = Math.max(1, asNumber(record?.durationMs, 1));

	return {
		key,
		name: asString(record?.name, QUERY_STAGE_NAME_FALLBACK_MAP[key] ?? rawName),
		durationMs,
		status: asStatus(record?.status, "success"),
		method: asString(record?.method, QUERY_STAGE_METHOD_FALLBACK_MAP[key] ?? "-"),
		provider: asString(
			record?.provider,
			QUERY_STAGE_PROVIDER_FALLBACK_MAP[key] ?? "-",
		),
		inputCount: asNumber(record?.inputCount, 0),
		outputCount: asNumber(record?.outputCount, 0),
		detail: asString(
			record?.detail,
			`${traceId} ${key} stage detail not provided by backend; fallback mock detail is used.`,
		),
	};
}

function normalizeQueryStages(rawStages: unknown, traceId: string): QueryTraceStage[] {
	const source = Array.isArray(rawStages) ? rawStages : [];
	const normalized = source.map((stage, index) =>
		normalizeQueryStage(stage, index, traceId),
	);

	if (normalized.length === 0) {
		return DEFAULT_QUERY_STAGE_ORDER.map((key, index) =>
			normalizeQueryStage(
				{
					key,
					name: QUERY_STAGE_NAME_FALLBACK_MAP[key],
					durationMs: 1,
					status: "running",
					method: QUERY_STAGE_METHOD_FALLBACK_MAP[key],
					provider: QUERY_STAGE_PROVIDER_FALLBACK_MAP[key],
					inputCount: index === 0 ? 1 : 0,
					outputCount: 0,
					detail: "No stage details available.",
				},
				index,
				traceId,
			),
		);
	}

	return [...normalized].sort(
		(a, b) => queryStageOrderIndex(a.key) - queryStageOrderIndex(b.key),
	);
}

function normalizeCandidate(
	rawCandidate: unknown,
	index: number,
	prefix: string,
): QueryTraceCandidate {
	const record = asRecord(rawCandidate);
	const fallbackId = `${prefix}-${String(index + 1).padStart(2, "0")}`;

	return {
		docId: asString(record?.docId ?? record?.id, fallbackId),
		title: asString(record?.title, "Untitled chunk"),
		source: asString(record?.source, "unknown-source"),
		rank: Math.max(1, asNumber(record?.rank, index + 1)),
		score: asNumber(record?.score, 0),
		snippet: asString(record?.snippet, ""),
	};
}

function normalizeCandidates(
	rawCandidates: unknown,
	prefix: string,
): QueryTraceCandidate[] {
	const source = Array.isArray(rawCandidates) ? rawCandidates : [];
	const normalized = source.map((item, index) =>
		normalizeCandidate(item, index, prefix),
	);

	return [...normalized].sort((a, b) => a.rank - b.rank);
}

function normalizeQueryTrace(rawTrace: unknown, index: number): QueryTraceRecord {
	const record = asRecord(rawTrace);
	const id = asString(record?.id, `qry-trace-${String(index + 1).padStart(3, "0")}`);
	const startedAt = asString(record?.startedAt, new Date(0).toISOString());
	const stages = normalizeQueryStages(record?.stages, id);
	const denseCandidates = normalizeCandidates(record?.denseCandidates, "dense");
	const sparseCandidates = normalizeCandidates(record?.sparseCandidates, "sparse");
	const fusionCandidates = normalizeCandidates(record?.fusionCandidates, "fusion");
	const rerankCandidates = normalizeCandidates(record?.rerankCandidates, "rerank");
	const topKSource =
		record?.topKResults ?? record?.topK ?? record?.finalResults ?? [];
	const normalizedTopK = normalizeCandidates(topKSource, "topk");
	const topKResults =
		normalizedTopK.length > 0
			? normalizedTopK
			: (rerankCandidates.length > 0 ? rerankCandidates : fusionCandidates).slice(0, 5);

	const totalDurationMs = Math.max(
		1,
		asNumber(
			record?.totalDurationMs,
			stages.reduce((sum, stage) => sum + stage.durationMs, 0),
		),
	);

	return {
		id,
		kind: "query",
		queryText: asString(record?.queryText ?? record?.query, "unknown query"),
		collection: asString(record?.collection, "default"),
		startedAt,
		finishedAt: asString(record?.finishedAt, startedAt),
		totalDurationMs,
		status: asStatus(record?.status, "success"),
		summary: asString(record?.summary, "query trace"),
		rerankBackend: asString(record?.rerankBackend ?? record?.reranker, "none"),
		fallbackTriggered: asBoolean(
			record?.fallbackTriggered ?? record?.rerankFallback,
			false,
		),
		stages,
		denseCandidates,
		sparseCandidates,
		fusionCandidates,
		rerankCandidates,
		topKResults,
	};
}

function sortByStartedAtDesc(records: IngestionTraceRecord[]): IngestionTraceRecord[] {
	return [...records].sort(
		(a, b) =>
			new Date(b.startedAt).getTime() - new Date(a.startedAt).getTime(),
	);
}

export function normalizeIngestionTracePayload(payload: unknown): IngestionTraceRecord[] {
	const traces = Array.isArray(payload) ? payload : [];
	const normalized = traces.map((trace, index) => normalizeTrace(trace, index));
 
	return sortByStartedAtDesc(normalized);
}

export function normalizeQueryTracePayload(payload: unknown): QueryTraceRecord[] {
	const traces = Array.isArray(payload) ? payload : [];
	const normalized = traces.map((trace, index) => normalizeQueryTrace(trace, index));

	return sortByStartedAtDesc(normalized);
}

export type LoadOverviewStatsOptions = {
	client?: ReturnType<typeof createHttpClient>;
	baseUrl?: string;
	useMock?: boolean;
	fallbackToMockOnError?: boolean;
	fetcher?: HttpClientOptions["fetcher"];
};

export type LoadIngestionTraceOptions = LoadOverviewStatsOptions;
export type LoadQueryTraceOptions = LoadOverviewStatsOptions;
export type RunEvaluationOptions = LoadOverviewStatsOptions & {
	evaluator?: "ragas" | "custom" | "all";
	dataset?: string;
};

function resolveClient(options: LoadOverviewStatsOptions): ReturnType<typeof createHttpClient> {
	if (options.client) {
		return options.client;
	}

	return createHttpClient({
		baseUrl: options.baseUrl,
		useMock: options.useMock,
		fallbackToMockOnError: options.fallbackToMockOnError,
		fetcher: options.fetcher,
	});
}

export async function loadOverviewStats(
	options: LoadOverviewStatsOptions = {},
): Promise<OverviewStats> {
	const client = resolveClient(options);
	const response = await client.get<TraceApiEnvelope<OverviewStats>>(
		"/overview/stats",
		undefined,
		"overviewStats",
	);

	if (!response.success) {
		throw new Error(response.message ?? "系统总览数据加载失败");
	}

	return response.data;
}

export async function loadIngestionTrace(
	options: LoadIngestionTraceOptions = {},
): Promise<IngestionTraceRecord[]> {
	const client = resolveClient(options);
	const response = await client.get<TraceApiEnvelope<unknown>>(
		"/traces/ingestion",
		undefined,
		"ingestionTraces",
	);

	if (!response.success) {
		throw new Error(response.message ?? "摄取 Trace 数据加载失败");
	}

	return normalizeIngestionTracePayload(response.data);
}

export async function loadQueryTrace(
	options: LoadQueryTraceOptions = {},
): Promise<QueryTraceRecord[]> {
	const client = resolveClient(options);
	const response = await client.get<TraceApiEnvelope<unknown>>(
		"/traces/query",
		undefined,
		"queryTraces",
	);

	if (!response.success) {
		throw new Error(response.message ?? "查询 Trace 数据加载失败");
	}

	return normalizeQueryTracePayload(response.data);
}

function normalizeEvaluationRunPayload(
	payload: unknown,
	fallback: {
		evaluator: "ragas" | "custom" | "all";
		dataset: string;
	},
): EvaluationRunRecord {
	const record = asRecord(payload);
	const status = asStatus(record?.status, "success");
	const durationMs = Math.max(1, asNumber(record?.durationMs, 1));

	const evaluatorRaw = asString(record?.evaluator, fallback.evaluator);
	const evaluator: "ragas" | "custom" | "all" =
		evaluatorRaw === "ragas" || evaluatorRaw === "custom" || evaluatorRaw === "all"
			? evaluatorRaw
			: fallback.evaluator;

	return {
		runId: asString(record?.runId, `eval-run-${Date.now()}`),
		evaluator,
		dataset: asString(record?.dataset, fallback.dataset),
		status,
		startedAt: asString(record?.startedAt, new Date().toISOString()),
		durationMs,
		metrics: {
			hitRate: asNumber(asRecord(record?.metrics)?.hitRate, 0),
			mrr: asNumber(asRecord(record?.metrics)?.mrr, 0),
			faithfulness: asNumber(asRecord(record?.metrics)?.faithfulness, 0),
		},
		note: asString(
			record?.note,
			status === "failed" ? "Evaluation failed." : "Evaluation completed.",
		),
	};
}

export async function runEvaluation(
	options: RunEvaluationOptions = {},
): Promise<EvaluationRunRecord> {
	const client = resolveClient(options);
	const evaluator = options.evaluator ?? "all";
	const dataset = options.dataset ?? "golden_set.jsonl";

	const response = await client.post<TraceApiEnvelope<unknown>>(
		"/evaluation/run",
		{
			evaluator,
			dataset,
		},
		"evaluationRun",
	);

	if (!response.success) {
		throw new Error(response.message ?? "评估运行失败");
	}

	return normalizeEvaluationRunPayload(response.data, {
		evaluator,
		dataset,
	});
}
