import { describe, expect, it, vi } from "vitest";

import { createHttpClient, HttpRequestError } from "../http";

describe("http client", () => {
  it("returns mock payload when useMock is enabled", async () => {
    const client = createHttpClient({ useMock: true });
    const response = await client.get("/audit/results", undefined, "auditResult");

    expect((response as { success: boolean }).success).toBe(true);
  });

  it("falls back to mock on network error when enabled", async () => {
    const fetcher = vi.fn(async () => {
      throw new Error("network down");
    });

    const client = createHttpClient({
      useMock: false,
      fallbackToMockOnError: true,
      fetcher,
    });

    const response = await client.get("/overview/stats", undefined, "overviewStats");
    expect((response as { success: boolean }).success).toBe(true);
  });

  it("throws HttpRequestError for non-2xx responses when fallback is disabled", async () => {
    const fetcher = vi.fn(async () => ({
      ok: false,
      status: 500,
      statusText: "Internal Server Error",
      json: async () => ({ success: false }),
    }));

    const client = createHttpClient({
      useMock: false,
      fallbackToMockOnError: false,
      fetcher,
    });

    await expect(
      client.get("/overview/stats", undefined, "overviewStats"),
    ).rejects.toBeInstanceOf(HttpRequestError);
  });

  it("serializes query params for live HTTP requests", async () => {
    const fetcher = vi.fn(async () => ({
      ok: true,
      status: 200,
      statusText: "OK",
      json: async () => ({ success: true, data: [] }),
    }));

    const client = createHttpClient({
      baseUrl: "http://localhost:9000",
      useMock: false,
      fallbackToMockOnError: false,
      fetcher,
    });

    await client.get("/documents", { collection: "default", limit: 20 });
    expect(fetcher).toHaveBeenCalledTimes(1);
    expect(fetcher).toHaveBeenCalledWith(
      "http://localhost:9000/documents?collection=default&limit=20",
      expect.any(Object),
    );
  });
});
