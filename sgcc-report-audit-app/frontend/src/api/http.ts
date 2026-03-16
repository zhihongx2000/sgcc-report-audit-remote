import { getMockData, type MockKey } from "../mock/mock";

type Primitive = string | number | boolean;
type QueryValue = Primitive | null | undefined;

type HttpMethod = "GET" | "POST" | "PUT" | "PATCH" | "DELETE";

export type HttpRequestConfig = {
	method?: HttpMethod;
	path: string;
	query?: Record<string, QueryValue>;
	body?: unknown;
	headers?: Record<string, string>;
	mockKey?: MockKey;
};

type FetchResponseLike = {
	ok: boolean;
	status: number;
	statusText: string;
	json: () => Promise<unknown>;
};

type Fetcher = (input: string, init?: RequestInit) => Promise<FetchResponseLike>;

export type HttpClientOptions = {
	baseUrl?: string;
	useMock?: boolean;
	fallbackToMockOnError?: boolean;
	timeoutMs?: number;
	fetcher?: Fetcher;
};

export class HttpRequestError extends Error {
	constructor(
		message: string,
		public readonly status: number,
		public readonly details?: unknown,
	) {
		super(message);
		this.name = "HttpRequestError";
	}
}

function parseBooleanEnv(value: string | undefined): boolean {
	if (!value) {
		return false;
	}

	return ["1", "true", "yes", "on"].includes(value.toLowerCase());
}

function resolveRuntimeConfig() {
	const env = import.meta.env as unknown as Record<string, string | undefined>;
	return {
		baseUrl: env.VITE_API_BASE_URL ?? "/api",
		useMock: parseBooleanEnv(env.VITE_USE_MOCK),
		timeoutMs: Number(env.VITE_API_TIMEOUT_MS ?? "10000"),
	};
}

function buildQueryString(query: Record<string, QueryValue> | undefined): string {
	if (!query) {
		return "";
	}

	const params = new URLSearchParams();
	for (const [key, value] of Object.entries(query)) {
		if (value === null || value === undefined) {
			continue;
		}
		params.append(key, String(value));
	}

	const encoded = params.toString();
	return encoded.length > 0 ? `?${encoded}` : "";
}

function inferMockKey(path: string): MockKey | null {
	if (path.includes("audit")) {
		return "auditResult";
	}
	if (path.includes("overview")) {
		return "overviewStats";
	}
	if (path.includes("ingestion") && path.includes("trace")) {
		return "ingestionTraces";
	}
	if (path.includes("query") && path.includes("trace")) {
		return "queryTraces";
	}
	if (path.includes("ingestion") && path.includes("task")) {
		return "ingestionTasks";
	}

	return null;
}

export function createHttpClient(userOptions: HttpClientOptions = {}) {
	const runtime = resolveRuntimeConfig();
	const options = {
		baseUrl: userOptions.baseUrl ?? runtime.baseUrl,
		useMock: userOptions.useMock ?? runtime.useMock,
		fallbackToMockOnError: userOptions.fallbackToMockOnError ?? true,
		timeoutMs: userOptions.timeoutMs ?? runtime.timeoutMs,
		fetcher: userOptions.fetcher ?? (fetch as unknown as Fetcher),
	};

	async function request<T>(config: HttpRequestConfig): Promise<T> {
		const method = config.method ?? "GET";
		const query = buildQueryString(config.query);
		const path = `${config.path}${query}`;
		const mockKey = config.mockKey ?? inferMockKey(config.path);

		if (options.useMock && mockKey) {
			return getMockData(mockKey) as unknown as T;
		}

		const controller = new AbortController();
		const timeoutHandle = globalThis.setTimeout(() => {
			controller.abort();
		}, options.timeoutMs);

		try {
			const response = await options.fetcher(`${options.baseUrl}${path}`, {
				method,
				headers: {
					"Content-Type": "application/json",
					...(config.headers ?? {}),
				},
				body: config.body !== undefined ? JSON.stringify(config.body) : undefined,
				signal: controller.signal,
			});

			const payload = await response.json();

			if (!response.ok) {
				throw new HttpRequestError(
					`HTTP ${response.status} ${response.statusText}`,
					response.status,
					payload,
				);
			}

			return payload as T;
		} catch (error) {
			if (options.fallbackToMockOnError && mockKey) {
				return getMockData(mockKey) as unknown as T;
			}
			throw error;
		} finally {
			clearTimeout(timeoutHandle);
		}
	}

	return {
		request,
		get: <T>(path: string, query?: Record<string, QueryValue>, mockKey?: MockKey) =>
			request<T>({ method: "GET", path, query, mockKey }),
		post: <T>(path: string, body?: unknown, mockKey?: MockKey) =>
			request<T>({ method: "POST", path, body, mockKey }),
		put: <T>(path: string, body?: unknown, mockKey?: MockKey) =>
			request<T>({ method: "PUT", path, body, mockKey }),
		patch: <T>(path: string, body?: unknown, mockKey?: MockKey) =>
			request<T>({ method: "PATCH", path, body, mockKey }),
		delete: <T>(path: string, mockKey?: MockKey) =>
			request<T>({ method: "DELETE", path, mockKey }),
	};
}
