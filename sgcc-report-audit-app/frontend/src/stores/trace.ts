import { reactive, readonly } from "vue";

export type TraceKind = "ingestion" | "query";
export type TraceStatus = "success" | "warning" | "failed" | "running";

export type TraceStage = {
	name: string;
	durationMs: number;
	status: TraceStatus;
};

export type TraceRecord = {
	id: string;
	kind: TraceKind;
	startedAt: string;
	totalDurationMs: number;
	status: TraceStatus;
	summary: string;
	stages: TraceStage[];
};

export type TraceState = {
	selectedKind: TraceKind;
	ingestionTraces: TraceRecord[];
	queryTraces: TraceRecord[];
	selectedTraceId: string | null;
	autoRefresh: boolean;
	pollingIntervalSec: number;
	isLoading: boolean;
	errorMessage: string | null;
	refreshedAtIso: string | null;
};

export function createTraceStore() {
	const state = reactive<TraceState>({
		selectedKind: "ingestion",
		ingestionTraces: [],
		queryTraces: [],
		selectedTraceId: null,
		autoRefresh: true,
		pollingIntervalSec: 5,
		isLoading: false,
		errorMessage: null,
		refreshedAtIso: null,
	});

	function setSelectedKind(kind: TraceKind): void {
		state.selectedKind = kind;
	}

	function setTraces(kind: TraceKind, traces: TraceRecord[]): void {
		const normalized = traces.map((trace) => ({
			...trace,
			stages: trace.stages.map((stage) => ({ ...stage })),
		}));

		if (kind === "ingestion") {
			state.ingestionTraces = normalized;
		} else {
			state.queryTraces = normalized;
		}

		state.refreshedAtIso = new Date().toISOString();
	}

	function appendTrace(trace: TraceRecord): void {
		const normalized = {
			...trace,
			stages: trace.stages.map((stage) => ({ ...stage })),
		};

		if (trace.kind === "ingestion") {
			state.ingestionTraces = [normalized, ...state.ingestionTraces];
			return;
		}

		state.queryTraces = [normalized, ...state.queryTraces];
	}

	function setSelectedTraceId(traceId: string | null): void {
		state.selectedTraceId = traceId;
	}

	function setAutoRefresh(enabled: boolean): void {
		state.autoRefresh = enabled;
	}

	function setPollingIntervalSec(intervalSec: number): void {
		state.pollingIntervalSec = Number.isFinite(intervalSec)
			? Math.max(1, Math.round(intervalSec))
			: 5;
	}

	function setLoading(loading: boolean): void {
		state.isLoading = loading;
	}

	function setErrorMessage(message: string | null): void {
		state.errorMessage = message;
	}

	// Refresh strategy: trace records are runtime-only and are not persisted.
	function reset(): void {
		state.selectedKind = "ingestion";
		state.ingestionTraces = [];
		state.queryTraces = [];
		state.selectedTraceId = null;
		state.autoRefresh = true;
		state.pollingIntervalSec = 5;
		state.isLoading = false;
		state.errorMessage = null;
		state.refreshedAtIso = new Date().toISOString();
	}

	return {
		state: readonly(state),
		setSelectedKind,
		setTraces,
		appendTrace,
		setSelectedTraceId,
		setAutoRefresh,
		setPollingIntervalSec,
		setLoading,
		setErrorMessage,
		reset,
	};
}

export type TraceStore = ReturnType<typeof createTraceStore>;

const traceStore = createTraceStore();

export function useTraceStore(): TraceStore {
	return traceStore;
}
