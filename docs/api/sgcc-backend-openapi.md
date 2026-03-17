# SGCC Backend OpenAPI Contract (Frozen in C10)

Contract version: `2026-03-17.c10`

This document freezes the backend response contract used by `sgcc-report-audit-app/frontend`.

## 1. Global Envelope

All business endpoints return this envelope:

```json
{
	"success": true,
	"message": "optional",
	"data": {}
}
```

Field semantics:

- `success`: whether request is handled successfully.
- `message`: optional diagnostic hint.
- `data`: typed payload by endpoint.

## 2. Endpoint Contract

### 2.1 GET `/overview/stats`

Response: `ApiEnvelope<OverviewStats>`

### 2.2 GET `/traces/ingestion`

Response: `ApiEnvelope<TraceRecord[]>` where each record uses `kind = ingestion`.

### 2.3 GET `/traces/query`

Response: `ApiEnvelope<TraceRecord[]>` where each record uses `kind = query` and may include
`denseCandidates` / `sparseCandidates` / `fusionCandidates` / `rerankCandidates` / `topKResults`.

### 2.4 GET `/ingestion/tasks`

Response: `ApiEnvelope<IngestionTask[]>`

### 2.5 POST `/evaluation/run`

Request body:

```json
{
	"evaluator": "ragas | custom | all",
	"dataset": "golden_set.jsonl"
}
```

Response: `ApiEnvelope<EvaluationRunRecord>`

### 2.6 GET `/audit/results/{report_id}`

Response: `ApiEnvelope<AuditResult>`

## 3. Component Schemas (Canonical Field Names)

### 3.1 AuditResult

- `reportId`, `reportName`, `collection`, `checkedAt`, `items`

### 3.2 AuditItem

- `id`, `title`, `status`, `reason`, `evidence`, `updatedAt`

### 3.3 OverviewStats

- `componentCards`, `collectionStats`, `healthMetrics`

### 3.4 OverviewComponentCard

- `title`, `value`, `detail`

### 3.5 CollectionStat

- `name`, `documents`, `chunks`, `images`

### 3.6 HealthMetric

- `title`, `value`, `sub`

### 3.7 TraceRecord

- `id`, `kind`, `queryText`, `sourcePath`, `collection`, `startedAt`, `finishedAt`, `totalDurationMs`, `status`, `summary`, `rerankBackend`, `fallbackTriggered`, `chunkCount`, `imageCount`, `skippedCount`, `failedCount`, `denseCandidates`, `sparseCandidates`, `fusionCandidates`, `rerankCandidates`, `topKResults`, `stages`

### 3.8 TraceStage

- `key`, `name`, `durationMs`, `status`, `method`, `provider`, `inputCount`, `outputCount`, `detail`

### 3.9 QueryTraceCandidate

- `docId`, `title`, `source`, `rank`, `score`, `snippet`

### 3.10 IngestionTask

- `taskId`, `sourcePath`, `status`, `progressPercent`, `startedAt`

### 3.11 EvaluationRunRecord

- `runId`, `evaluator`, `dataset`, `status`, `startedAt`, `durationMs`, `metrics`, `note`

### 3.12 EvaluationMetrics

- `hitRate`, `mrr`, `faithfulness`

## 4. Schema Diff Snapshot

The JSON below is machine-readable and used by backend/frontend contract tests.

<!-- CONTRACT_FIELD_SNAPSHOT_BEGIN -->
```json
{
	"ApiEnvelope": ["success", "message", "data"],
	"AuditItem": ["id", "title", "status", "reason", "evidence", "updatedAt"],
	"AuditResult": ["reportId", "reportName", "collection", "checkedAt", "items"],
	"OverviewComponentCard": ["title", "value", "detail"],
	"CollectionStat": ["name", "documents", "chunks", "images"],
	"HealthMetric": ["title", "value", "sub"],
	"OverviewStats": ["componentCards", "collectionStats", "healthMetrics"],
	"TraceStage": ["key", "name", "durationMs", "status", "method", "provider", "inputCount", "outputCount", "detail"],
	"QueryTraceCandidate": ["docId", "title", "source", "rank", "score", "snippet"],
	"TraceRecord": ["id", "kind", "queryText", "sourcePath", "collection", "startedAt", "finishedAt", "totalDurationMs", "status", "summary", "rerankBackend", "fallbackTriggered", "chunkCount", "imageCount", "skippedCount", "failedCount", "denseCandidates", "sparseCandidates", "fusionCandidates", "rerankCandidates", "topKResults", "stages"],
	"IngestionTask": ["taskId", "sourcePath", "status", "progressPercent", "startedAt"],
	"EvaluationMetrics": ["hitRate", "mrr", "faithfulness"],
	"EvaluationRunRecord": ["runId", "evaluator", "dataset", "status", "startedAt", "durationMs", "metrics", "note"]
}
```
<!-- CONTRACT_FIELD_SNAPSHOT_END -->

