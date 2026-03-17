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
