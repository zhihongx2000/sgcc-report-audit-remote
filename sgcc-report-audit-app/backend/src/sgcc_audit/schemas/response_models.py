from __future__ import annotations

from typing import Generic, Literal, TypeVar

from pydantic import BaseModel, ConfigDict

AuditStatus = Literal["pass", "warn", "fail", "pending"]
TraceStatus = Literal["success", "warning", "failed", "running"]
TraceKind = Literal["ingestion", "query"]
IngestionTaskStatus = Literal["queued", "running", "failed", "done"]
EvaluatorType = Literal["ragas", "custom", "all"]

PayloadT = TypeVar("PayloadT")


class ContractBaseModel(BaseModel):
	"""Shared model base for strict response-contract DTOs."""

	model_config = ConfigDict(extra="forbid", populate_by_name=True)


class ApiEnvelope(ContractBaseModel, Generic[PayloadT]):
	success: bool
	message: str | None = None
	data: PayloadT


class AuditItemResponse(ContractBaseModel):
	id: str
	title: str
	status: AuditStatus
	reason: str
	evidence: list[str]
	updatedAt: str


class AuditResultResponse(ContractBaseModel):
	reportId: str
	reportName: str
	collection: str
	checkedAt: str
	items: list[AuditItemResponse]


class OverviewComponentCardResponse(ContractBaseModel):
	title: str
	value: str
	detail: str


class CollectionStatResponse(ContractBaseModel):
	name: str
	documents: int
	chunks: int
	images: int


class HealthMetricResponse(ContractBaseModel):
	title: str
	value: str
	sub: str


class OverviewStatsResponse(ContractBaseModel):
	componentCards: list[OverviewComponentCardResponse]
	collectionStats: list[CollectionStatResponse]
	healthMetrics: list[HealthMetricResponse]


class TraceStageResponse(ContractBaseModel):
	key: str | None = None
	name: str
	durationMs: int
	status: TraceStatus
	method: str | None = None
	provider: str | None = None
	inputCount: int | None = None
	outputCount: int | None = None
	detail: str | None = None


class QueryTraceCandidateResponse(ContractBaseModel):
	docId: str
	title: str
	source: str
	rank: int
	score: float
	snippet: str | None = None


class TraceRecordResponse(ContractBaseModel):
	id: str
	kind: TraceKind
	queryText: str | None = None
	sourcePath: str | None = None
	collection: str | None = None
	startedAt: str
	finishedAt: str | None = None
	totalDurationMs: int
	status: TraceStatus
	summary: str
	rerankBackend: str | None = None
	fallbackTriggered: bool | None = None
	chunkCount: int | None = None
	imageCount: int | None = None
	skippedCount: int | None = None
	failedCount: int | None = None
	denseCandidates: list[QueryTraceCandidateResponse] | None = None
	sparseCandidates: list[QueryTraceCandidateResponse] | None = None
	fusionCandidates: list[QueryTraceCandidateResponse] | None = None
	rerankCandidates: list[QueryTraceCandidateResponse] | None = None
	topKResults: list[QueryTraceCandidateResponse] | None = None
	stages: list[TraceStageResponse]


class IngestionTaskResponse(ContractBaseModel):
	taskId: str
	sourcePath: str
	status: IngestionTaskStatus
	progressPercent: int
	startedAt: str


class EvaluationMetricsResponse(ContractBaseModel):
	hitRate: float
	mrr: float
	faithfulness: float


class EvaluationRunRecordResponse(ContractBaseModel):
	runId: str
	evaluator: EvaluatorType
	dataset: str
	status: TraceStatus
	startedAt: str
	durationMs: int
	metrics: EvaluationMetricsResponse
	note: str


def _fields_of(model_type: type[BaseModel]) -> list[str]:
	return list(model_type.model_fields.keys())


def build_backend_contract_snapshot() -> dict[str, list[str]]:
	"""Machine-readable response-schema snapshot used by C10 contract tests."""

	return {
		"ApiEnvelope": _fields_of(ApiEnvelope[dict]),
		"AuditItem": _fields_of(AuditItemResponse),
		"AuditResult": _fields_of(AuditResultResponse),
		"OverviewComponentCard": _fields_of(OverviewComponentCardResponse),
		"CollectionStat": _fields_of(CollectionStatResponse),
		"HealthMetric": _fields_of(HealthMetricResponse),
		"OverviewStats": _fields_of(OverviewStatsResponse),
		"TraceStage": _fields_of(TraceStageResponse),
		"QueryTraceCandidate": _fields_of(QueryTraceCandidateResponse),
		"TraceRecord": _fields_of(TraceRecordResponse),
		"IngestionTask": _fields_of(IngestionTaskResponse),
		"EvaluationMetrics": _fields_of(EvaluationMetricsResponse),
		"EvaluationRunRecord": _fields_of(EvaluationRunRecordResponse),
	}


__all__ = [
	"ApiEnvelope",
	"AuditItemResponse",
	"AuditResultResponse",
	"OverviewComponentCardResponse",
	"CollectionStatResponse",
	"HealthMetricResponse",
	"OverviewStatsResponse",
	"TraceStageResponse",
	"QueryTraceCandidateResponse",
	"TraceRecordResponse",
	"IngestionTaskResponse",
	"EvaluationMetricsResponse",
	"EvaluationRunRecordResponse",
	"build_backend_contract_snapshot",
]
