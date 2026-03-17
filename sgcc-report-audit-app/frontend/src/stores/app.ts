import { reactive, readonly } from "vue";

import type { IngestionTaskRecord } from "../api/documents";
import type { OverviewStats } from "../types";

type StorageLike = Pick<Storage, "getItem" | "setItem" | "removeItem">;

const STORAGE_KEY = "sgcc-dashboard:app-store:v1";
const memoryStorage = new Map<string, string>();

type PersistedAppState = {
	sidebarCollapsed: boolean;
	activeCollection: string;
	autoRefresh: boolean;
	refreshIntervalSec: number;
	lastVisitedRoute: string;
};

export type AppState = PersistedAppState & {
	refreshedAtIso: string | null;
	overviewStats: OverviewStats | null;
	isOverviewLoading: boolean;
	overviewErrorMessage: string | null;
	overviewRefreshedAtIso: string | null;
	ingestionTasks: IngestionTaskRecord[];
	isIngestionLoading: boolean;
	ingestionErrorMessage: string | null;
	ingestionRefreshedAtIso: string | null;
};

function cloneIngestionTask(task: IngestionTaskRecord): IngestionTaskRecord {
	return { ...task };
}

function cloneIngestionTasks(
	tasks: readonly IngestionTaskRecord[],
): IngestionTaskRecord[] {
	return tasks.map((task) => cloneIngestionTask(task));
}

const DEFAULT_PERSISTED_STATE: PersistedAppState = {
	sidebarCollapsed: false,
	activeCollection: "default",
	autoRefresh: true,
	refreshIntervalSec: 5,
	lastVisitedRoute: "/overview",
};

function resolveStorage(): StorageLike {
	if (typeof window !== "undefined" && "sessionStorage" in window) {
		return window.sessionStorage;
	}

	return {
		getItem: (key) => memoryStorage.get(key) ?? null,
		setItem: (key, value) => {
			memoryStorage.set(key, value);
		},
		removeItem: (key) => {
			memoryStorage.delete(key);
		},
	};
}

function readPersistedState(storage: StorageLike): PersistedAppState {
	const raw = storage.getItem(STORAGE_KEY);
	if (!raw) {
		return { ...DEFAULT_PERSISTED_STATE };
	}

	try {
		const parsed = JSON.parse(raw) as Partial<PersistedAppState>;
		return {
			sidebarCollapsed:
				typeof parsed.sidebarCollapsed === "boolean"
					? parsed.sidebarCollapsed
					: DEFAULT_PERSISTED_STATE.sidebarCollapsed,
			activeCollection:
				typeof parsed.activeCollection === "string" &&
				parsed.activeCollection.trim().length > 0
					? parsed.activeCollection
					: DEFAULT_PERSISTED_STATE.activeCollection,
			autoRefresh:
				typeof parsed.autoRefresh === "boolean"
					? parsed.autoRefresh
					: DEFAULT_PERSISTED_STATE.autoRefresh,
			refreshIntervalSec:
				typeof parsed.refreshIntervalSec === "number" &&
				Number.isFinite(parsed.refreshIntervalSec)
					? Math.max(1, Math.round(parsed.refreshIntervalSec))
					: DEFAULT_PERSISTED_STATE.refreshIntervalSec,
			lastVisitedRoute:
				typeof parsed.lastVisitedRoute === "string" &&
				parsed.lastVisitedRoute.trim().length > 0
					? parsed.lastVisitedRoute
					: DEFAULT_PERSISTED_STATE.lastVisitedRoute,
		};
	} catch {
		return { ...DEFAULT_PERSISTED_STATE };
	}
}

export function createAppStore() {
	const storage = resolveStorage();
	const state = reactive<AppState>({
		...DEFAULT_PERSISTED_STATE,
		refreshedAtIso: null,
		overviewStats: null,
		isOverviewLoading: false,
		overviewErrorMessage: null,
		overviewRefreshedAtIso: null,
		ingestionTasks: [],
		isIngestionLoading: false,
		ingestionErrorMessage: null,
		ingestionRefreshedAtIso: null,
	});

	function applyPersistedState(nextState: PersistedAppState): void {
		state.sidebarCollapsed = nextState.sidebarCollapsed;
		state.activeCollection = nextState.activeCollection;
		state.autoRefresh = nextState.autoRefresh;
		state.refreshIntervalSec = nextState.refreshIntervalSec;
		state.lastVisitedRoute = nextState.lastVisitedRoute;
	}

	function persistState(): void {
		const payload: PersistedAppState = {
			sidebarCollapsed: state.sidebarCollapsed,
			activeCollection: state.activeCollection,
			autoRefresh: state.autoRefresh,
			refreshIntervalSec: state.refreshIntervalSec,
			lastVisitedRoute: state.lastVisitedRoute,
		};

		storage.setItem(STORAGE_KEY, JSON.stringify(payload));
	}

	// Refresh strategy: app-level preferences are persisted in session scope.
	function hydrateFromStorage(): void {
		const persisted = readPersistedState(storage);
		applyPersistedState(persisted);
		state.refreshedAtIso = new Date().toISOString();
	}

	function setSidebarCollapsed(collapsed: boolean): void {
		state.sidebarCollapsed = collapsed;
		persistState();
	}

	function toggleSidebar(): void {
		state.sidebarCollapsed = !state.sidebarCollapsed;
		persistState();
	}

	function setActiveCollection(collection: string): void {
		state.activeCollection = collection.trim() || DEFAULT_PERSISTED_STATE.activeCollection;
		persistState();
	}

	function setAutoRefresh(enabled: boolean): void {
		state.autoRefresh = enabled;
		persistState();
	}

	function setRefreshIntervalSec(intervalSec: number): void {
		const normalized = Number.isFinite(intervalSec)
			? Math.max(1, Math.round(intervalSec))
			: DEFAULT_PERSISTED_STATE.refreshIntervalSec;
		state.refreshIntervalSec = normalized;
		persistState();
	}

	function setLastVisitedRoute(routePath: string): void {
		state.lastVisitedRoute = routePath.trim() || DEFAULT_PERSISTED_STATE.lastVisitedRoute;
		persistState();
	}

	function setOverviewStats(stats: OverviewStats): void {
		state.overviewStats = {
			componentCards: stats.componentCards.map((card) => ({ ...card })),
			collectionStats: stats.collectionStats.map((collection) => ({ ...collection })),
			healthMetrics: stats.healthMetrics.map((metric) => ({ ...metric })),
		};
		state.overviewErrorMessage = null;
		state.overviewRefreshedAtIso = new Date().toISOString();
	}

	function setOverviewLoading(loading: boolean): void {
		state.isOverviewLoading = loading;
	}

	function setOverviewErrorMessage(message: string | null): void {
		state.overviewErrorMessage = message;
	}

	function setIngestionTasks(tasks: IngestionTaskRecord[]): void {
		state.ingestionTasks = cloneIngestionTasks(tasks);
		state.ingestionErrorMessage = null;
		state.ingestionRefreshedAtIso = new Date().toISOString();
	}

	function upsertIngestionTask(task: IngestionTaskRecord): void {
		const normalized = cloneIngestionTask(task);
		const index = state.ingestionTasks.findIndex((item) => item.taskId === task.taskId);
		if (index < 0) {
			state.ingestionTasks = [normalized, ...state.ingestionTasks];
		} else {
			state.ingestionTasks = [
				...state.ingestionTasks.slice(0, index),
				normalized,
				...state.ingestionTasks.slice(index + 1),
			];
		}
		state.ingestionRefreshedAtIso = new Date().toISOString();
	}

	function setIngestionLoading(loading: boolean): void {
		state.isIngestionLoading = loading;
	}

	function setIngestionErrorMessage(message: string | null): void {
		state.ingestionErrorMessage = message;
	}

	function reset(): void {
		applyPersistedState(DEFAULT_PERSISTED_STATE);
		state.refreshedAtIso = new Date().toISOString();
		state.overviewStats = null;
		state.isOverviewLoading = false;
		state.overviewErrorMessage = null;
		state.overviewRefreshedAtIso = null;
		state.ingestionTasks = [];
		state.isIngestionLoading = false;
		state.ingestionErrorMessage = null;
		state.ingestionRefreshedAtIso = null;
		storage.removeItem(STORAGE_KEY);
	}

	hydrateFromStorage();

	return {
		state: readonly(state),
		hydrateFromStorage,
		setSidebarCollapsed,
		toggleSidebar,
		setActiveCollection,
		setAutoRefresh,
		setRefreshIntervalSec,
		setLastVisitedRoute,
		setOverviewStats,
		setOverviewLoading,
		setOverviewErrorMessage,
		setIngestionTasks,
		upsertIngestionTask,
		setIngestionLoading,
		setIngestionErrorMessage,
		reset,
	};
}

export type AppStore = ReturnType<typeof createAppStore>;

const appStore = createAppStore();

export function useAppStore(): AppStore {
	return appStore;
}
