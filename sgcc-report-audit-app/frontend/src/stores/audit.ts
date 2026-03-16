import { reactive, readonly } from "vue";

export type AuditCheckStatus = "pass" | "warn" | "fail" | "pending";
export type AuditSortField = "title" | "updatedAt" | "status";
export type SortOrder = "asc" | "desc";

export type AuditCheckItem = {
	id: string;
	title: string;
	status: AuditCheckStatus;
	reason: string;
	evidenceCount: number;
	updatedAt: string;
};

export type AuditFilter = {
	status: AuditCheckStatus | "all";
	query: string;
};

export type AuditState = {
	selectedReportId: string | null;
	items: AuditCheckItem[];
	filter: AuditFilter;
	sortField: AuditSortField;
	sortOrder: SortOrder;
	isLoading: boolean;
	errorMessage: string | null;
	refreshedAtIso: string | null;
};

const DEFAULT_FILTER: AuditFilter = {
	status: "all",
	query: "",
};

export function createAuditStore() {
	const state = reactive<AuditState>({
		selectedReportId: null,
		items: [],
		filter: { ...DEFAULT_FILTER },
		sortField: "updatedAt",
		sortOrder: "desc",
		isLoading: false,
		errorMessage: null,
		refreshedAtIso: null,
	});

	function setSelectedReportId(reportId: string | null): void {
		state.selectedReportId = reportId;
	}

	function setItems(items: AuditCheckItem[]): void {
		state.items = items.map((item) => ({ ...item }));
		state.refreshedAtIso = new Date().toISOString();
	}

	function upsertItem(item: AuditCheckItem): void {
		const index = state.items.findIndex((existing) => existing.id === item.id);
		if (index >= 0) {
			state.items[index] = { ...item };
			return;
		}

		state.items.push({ ...item });
	}

	function setStatusFilter(status: AuditCheckStatus | "all"): void {
		state.filter.status = status;
	}

	function setQueryFilter(query: string): void {
		state.filter.query = query;
	}

	function setSort(field: AuditSortField, order: SortOrder): void {
		state.sortField = field;
		state.sortOrder = order;
	}

	function setLoading(loading: boolean): void {
		state.isLoading = loading;
	}

	function setErrorMessage(message: string | null): void {
		state.errorMessage = message;
	}

	// Refresh strategy: audit data is in-memory only and reset on page reload.
	function reset(): void {
		state.selectedReportId = null;
		state.items = [];
		state.filter = { ...DEFAULT_FILTER };
		state.sortField = "updatedAt";
		state.sortOrder = "desc";
		state.isLoading = false;
		state.errorMessage = null;
		state.refreshedAtIso = new Date().toISOString();
	}

	return {
		state: readonly(state),
		setSelectedReportId,
		setItems,
		upsertItem,
		setStatusFilter,
		setQueryFilter,
		setSort,
		setLoading,
		setErrorMessage,
		reset,
	};
}

export type AuditStore = ReturnType<typeof createAuditStore>;

const auditStore = createAuditStore();

export function useAuditStore(): AuditStore {
	return auditStore;
}
