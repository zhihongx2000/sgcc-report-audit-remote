import { reactive, readonly } from "vue";

export type AuditCheckStatus = "pass" | "fail" | "review";
export type AuditSortField = "title" | "updatedAt" | "status";
export type SortOrder = "asc" | "desc";

export type AuditEvidence = {
	id: string;
	label: string;
	source: string;
	page: number | null;
};

export type AuditCheckItem = {
	id: string;
	title: string;
	status: AuditCheckStatus;
	reason: string;
	evidence: readonly AuditEvidence[];
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

const STATUS_WEIGHT: { [K in AuditCheckStatus]: number } = {
	pass: 0,
	review: 1,
	fail: 2,
};

const DEFAULT_FILTER: AuditFilter = {
	status: "all",
	query: "",
};

export function filterByStatus(
	items: readonly AuditCheckItem[],
	status: AuditCheckStatus | "all",
): AuditCheckItem[] {
	if (status === "all") {
		return [...items];
	}

	return items.filter((item) => item.status === status);
}

function sortCheckItems(
	items: readonly AuditCheckItem[],
	field: AuditSortField,
	order: SortOrder,
): AuditCheckItem[] {
	const direction = order === "asc" ? 1 : -1;

	return [...items].sort((left, right) => {
		if (field === "title") {
			return direction * left.title.localeCompare(right.title, "zh-Hans-CN");
		}

		if (field === "status") {
			return direction * (STATUS_WEIGHT[left.status] - STATUS_WEIGHT[right.status]);
		}

		const leftTime = Date.parse(left.updatedAt);
		const rightTime = Date.parse(right.updatedAt);
		if (Number.isNaN(leftTime) || Number.isNaN(rightTime)) {
			return 0;
		}

		return direction * (leftTime - rightTime);
	});
}

function filterByQuery(items: readonly AuditCheckItem[], query: string): AuditCheckItem[] {
	const trimmed = query.trim().toLowerCase();
	if (!trimmed) {
		return [...items];
	}

	return items.filter((item) => {
		const reason = item.reason.toLowerCase();
		const evidenceText = item.evidence
			.map((entry) => `${entry.label} ${entry.source}`.toLowerCase())
			.join(" ");
		return (
			item.id.toLowerCase().includes(trimmed) ||
			item.title.toLowerCase().includes(trimmed) ||
			reason.includes(trimmed) ||
			evidenceText.includes(trimmed)
		);
	});
}

export type RenderCheckItemsInput = {
	items: readonly AuditCheckItem[];
	filter: AuditFilter;
	sortField: AuditSortField;
	sortOrder: SortOrder;
};

export function renderCheckItems(state: RenderCheckItemsInput): AuditCheckItem[] {
	const statusFiltered = filterByStatus(state.items, state.filter.status);
	const queryFiltered = filterByQuery(statusFiltered, state.filter.query);
	return sortCheckItems(queryFiltered, state.sortField, state.sortOrder);
}

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
		state.items = items.map((item) => ({
			...item,
			evidence: item.evidence.map((entry) => ({ ...entry })),
		}));
		state.refreshedAtIso = new Date().toISOString();
	}

	function upsertItem(item: AuditCheckItem): void {
		const index = state.items.findIndex((existing) => existing.id === item.id);
		if (index >= 0) {
			state.items[index] = {
				...item,
				evidence: item.evidence.map((entry) => ({ ...entry })),
			};
			return;
		}

		state.items.push({
			...item,
			evidence: item.evidence.map((entry) => ({ ...entry })),
		});
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
