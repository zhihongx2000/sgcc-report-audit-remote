export type AuditStatus = "pass" | "warn" | "fail" | "pending";

export type ApiEnvelope<T> = {
	success: boolean;
	message?: string;
	data: T;
};

export type AuditItem = {
	id: string;
	title: string;
	status: AuditStatus;
	reason: string;
	evidence: string[];
	updatedAt: string;
};

export type AuditResult = {
	reportId: string;
	reportName: string;
	collection: string;
	checkedAt: string;
	items: AuditItem[];
};

export type OverviewComponentCard = {
	title: string;
	value: string;
	detail: string;
};

export type CollectionStat = {
	name: string;
	documents: number;
	chunks: number;
	images: number;
};

export type HealthMetric = {
	title: string;
	value: string;
	sub: string;
};

export type OverviewStats = {
	componentCards: OverviewComponentCard[];
	collectionStats: CollectionStat[];
	healthMetrics: HealthMetric[];
};

export type TraceKind = "ingestion" | "query";
export type TraceStage = {
	key?: string;
	name: string;
	durationMs: number;
	status: "success" | "warning" | "failed" | "running";
	method?: string;
	provider?: string;
	inputCount?: number;
	outputCount?: number;
	detail?: string;
};

export type QueryTraceCandidate = {
	docId: string;
	title: string;
	source: string;
	rank: number;
	score: number;
	snippet?: string;
};

export type TraceRecord = {
	id: string;
	kind: TraceKind;
	queryText?: string;
	sourcePath?: string;
	collection?: string;
	startedAt: string;
	finishedAt?: string;
	totalDurationMs: number;
	status: "success" | "warning" | "failed" | "running";
	summary: string;
	rerankBackend?: string;
	fallbackTriggered?: boolean;
	chunkCount?: number;
	imageCount?: number;
	skippedCount?: number;
	failedCount?: number;
	denseCandidates?: QueryTraceCandidate[];
	sparseCandidates?: QueryTraceCandidate[];
	fusionCandidates?: QueryTraceCandidate[];
	rerankCandidates?: QueryTraceCandidate[];
	topKResults?: QueryTraceCandidate[];
	stages: TraceStage[];
};

export type IngestionTask = {
	taskId: string;
	sourcePath: string;
	status: "queued" | "running" | "failed" | "done";
	progressPercent: number;
	startedAt: string;
};

export type EvaluationMetrics = {
	hitRate: number;
	mrr: number;
	faithfulness: number;
};

export type EvaluationRunRecord = {
	runId: string;
	evaluator: "ragas" | "custom" | "all";
	dataset: string;
	status: "success" | "warning" | "failed" | "running";
	startedAt: string;
	durationMs: number;
	metrics: EvaluationMetrics;
	note: string;
};

export type FrontendMockDataMap = {
	auditResult: ApiEnvelope<AuditResult>;
	overviewStats: ApiEnvelope<OverviewStats>;
	ingestionTraces: ApiEnvelope<TraceRecord[]>;
	queryTraces: ApiEnvelope<TraceRecord[]>;
	ingestionTasks: ApiEnvelope<IngestionTask[]>;
	evaluationRun: ApiEnvelope<EvaluationRunRecord>;
};

export type AuditResultResponse = ApiEnvelope<AuditResult>;
export type OverviewStatsResponse = ApiEnvelope<OverviewStats>;
export type IngestionTraceResponse = ApiEnvelope<TraceRecord[]>;
export type QueryTraceResponse = ApiEnvelope<TraceRecord[]>;
export type IngestionTaskResponse = ApiEnvelope<IngestionTask[]>;
export type EvaluationRunResponse = ApiEnvelope<EvaluationRunRecord>;

export const SGCC_BACKEND_CONTRACT_VERSION = "2026-03-17.c10" as const;

export const BACKEND_CONTRACT_FIELD_SNAPSHOT = {
	ApiEnvelope: ["success", "message", "data"],
	AuditItem: ["id", "title", "status", "reason", "evidence", "updatedAt"],
	AuditResult: ["reportId", "reportName", "collection", "checkedAt", "items"],
	OverviewComponentCard: ["title", "value", "detail"],
	CollectionStat: ["name", "documents", "chunks", "images"],
	HealthMetric: ["title", "value", "sub"],
	OverviewStats: ["componentCards", "collectionStats", "healthMetrics"],
	TraceStage: [
		"key",
		"name",
		"durationMs",
		"status",
		"method",
		"provider",
		"inputCount",
		"outputCount",
		"detail",
	],
	QueryTraceCandidate: ["docId", "title", "source", "rank", "score", "snippet"],
	TraceRecord: [
		"id",
		"kind",
		"queryText",
		"sourcePath",
		"collection",
		"startedAt",
		"finishedAt",
		"totalDurationMs",
		"status",
		"summary",
		"rerankBackend",
		"fallbackTriggered",
		"chunkCount",
		"imageCount",
		"skippedCount",
		"failedCount",
		"denseCandidates",
		"sparseCandidates",
		"fusionCandidates",
		"rerankCandidates",
		"topKResults",
		"stages",
	],
	IngestionTask: ["taskId", "sourcePath", "status", "progressPercent", "startedAt"],
	EvaluationMetrics: ["hitRate", "mrr", "faithfulness"],
	EvaluationRunRecord: [
		"runId",
		"evaluator",
		"dataset",
		"status",
		"startedAt",
		"durationMs",
		"metrics",
		"note",
	],
} as const;

type Assert<T extends true> = T;

type KeysMatch<Obj, ContractKeys extends readonly string[]> =
	Exclude<keyof Obj, ContractKeys[number]> extends never
		? Exclude<ContractKeys[number], keyof Obj> extends never
			? true
			: false
		: false;

type _ApiEnvelopeContract = Assert<
	KeysMatch<ApiEnvelope<unknown>, (typeof BACKEND_CONTRACT_FIELD_SNAPSHOT)["ApiEnvelope"]>
>;
type _AuditItemContract = Assert<
	KeysMatch<AuditItem, (typeof BACKEND_CONTRACT_FIELD_SNAPSHOT)["AuditItem"]>
>;
type _AuditResultContract = Assert<
	KeysMatch<AuditResult, (typeof BACKEND_CONTRACT_FIELD_SNAPSHOT)["AuditResult"]>
>;
type _OverviewCardContract = Assert<
	KeysMatch<OverviewComponentCard, (typeof BACKEND_CONTRACT_FIELD_SNAPSHOT)["OverviewComponentCard"]>
>;
type _CollectionStatContract = Assert<
	KeysMatch<CollectionStat, (typeof BACKEND_CONTRACT_FIELD_SNAPSHOT)["CollectionStat"]>
>;
type _HealthMetricContract = Assert<
	KeysMatch<HealthMetric, (typeof BACKEND_CONTRACT_FIELD_SNAPSHOT)["HealthMetric"]>
>;
type _OverviewStatsContract = Assert<
	KeysMatch<OverviewStats, (typeof BACKEND_CONTRACT_FIELD_SNAPSHOT)["OverviewStats"]>
>;
type _TraceStageContract = Assert<
	KeysMatch<TraceStage, (typeof BACKEND_CONTRACT_FIELD_SNAPSHOT)["TraceStage"]>
>;
type _QueryTraceCandidateContract = Assert<
	KeysMatch<QueryTraceCandidate, (typeof BACKEND_CONTRACT_FIELD_SNAPSHOT)["QueryTraceCandidate"]>
>;
type _TraceRecordContract = Assert<
	KeysMatch<TraceRecord, (typeof BACKEND_CONTRACT_FIELD_SNAPSHOT)["TraceRecord"]>
>;
type _IngestionTaskContract = Assert<
	KeysMatch<IngestionTask, (typeof BACKEND_CONTRACT_FIELD_SNAPSHOT)["IngestionTask"]>
>;
type _EvaluationMetricsContract = Assert<
	KeysMatch<EvaluationMetrics, (typeof BACKEND_CONTRACT_FIELD_SNAPSHOT)["EvaluationMetrics"]>
>;
type _EvaluationRunRecordContract = Assert<
	KeysMatch<
		EvaluationRunRecord,
		(typeof BACKEND_CONTRACT_FIELD_SNAPSHOT)["EvaluationRunRecord"]
	>
>;
