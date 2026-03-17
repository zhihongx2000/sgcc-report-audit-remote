import { createHttpClient, type HttpClientOptions } from "./http";

import type { ApiEnvelope, OverviewStats } from "../types";

type TraceApiEnvelope<T> = ApiEnvelope<T>;

export type LoadOverviewStatsOptions = {
	client?: ReturnType<typeof createHttpClient>;
	baseUrl?: string;
	useMock?: boolean;
	fallbackToMockOnError?: boolean;
	fetcher?: HttpClientOptions["fetcher"];
};

function resolveClient(options: LoadOverviewStatsOptions): ReturnType<typeof createHttpClient> {
	if (options.client) {
		return options.client;
	}

	return createHttpClient({
		baseUrl: options.baseUrl,
		useMock: options.useMock,
		fallbackToMockOnError: options.fallbackToMockOnError,
		fetcher: options.fetcher,
	});
}

export async function loadOverviewStats(
	options: LoadOverviewStatsOptions = {},
): Promise<OverviewStats> {
	const client = resolveClient(options);
	const response = await client.get<TraceApiEnvelope<OverviewStats>>(
		"/overview/stats",
		undefined,
		"overviewStats",
	);

	if (!response.success) {
		throw new Error(response.message ?? "系统总览数据加载失败");
	}

	return response.data;
}
