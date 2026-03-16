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
	name: string;
	durationMs: number;
	status: "success" | "warning" | "failed" | "running";
};

export type TraceRecord = {
	id: string;
	kind: TraceKind;
	startedAt: string;
	totalDurationMs: number;
	status: "success" | "warning" | "failed" | "running";
	summary: string;
	stages: TraceStage[];
};

export type IngestionTask = {
	taskId: string;
	sourcePath: string;
	status: "queued" | "running" | "failed" | "done";
	progressPercent: number;
	startedAt: string;
};

export type FrontendMockDataMap = {
	auditResult: ApiEnvelope<AuditResult>;
	overviewStats: ApiEnvelope<OverviewStats>;
	ingestionTraces: ApiEnvelope<TraceRecord[]>;
	queryTraces: ApiEnvelope<TraceRecord[]>;
	ingestionTasks: ApiEnvelope<IngestionTask[]>;
};
