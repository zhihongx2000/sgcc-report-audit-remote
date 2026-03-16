import { beforeEach, describe, expect, it } from "vitest";

import { createTraceStore, type TraceRecord } from "../trace";

const ingestionTrace: TraceRecord = {
  id: "trace-ing-01",
  kind: "ingestion",
  startedAt: "2026-03-16T17:40:00.000Z",
  totalDurationMs: 23840,
  status: "success",
  summary: "ingestion finished",
  stages: [
    { name: "load", durationMs: 5120, status: "success" },
    { name: "split", durationMs: 8220, status: "success" },
  ],
};

describe("trace store", () => {
  let store = createTraceStore();

  beforeEach(() => {
    store = createTraceStore();
  });

  it("stores traces by kind and keeps latest appended first", () => {
    store.setTraces("ingestion", [ingestionTrace]);
    expect(store.state.ingestionTraces).toHaveLength(1);

    const second = {
      ...ingestionTrace,
      id: "trace-ing-02",
      startedAt: "2026-03-16T17:41:00.000Z",
    };
    store.appendTrace(second);

    expect(store.state.ingestionTraces).toHaveLength(2);
    expect(store.state.ingestionTraces[0].id).toBe("trace-ing-02");
  });

  it("normalizes polling interval and clears runtime state on reset", () => {
    store.setPollingIntervalSec(0);
    expect(store.state.pollingIntervalSec).toBe(1);

    store.setSelectedTraceId("trace-ing-01");
    store.reset();

    expect(store.state.selectedTraceId).toBeNull();
    expect(store.state.ingestionTraces).toHaveLength(0);
    expect(store.state.queryTraces).toHaveLength(0);
    expect(store.state.pollingIntervalSec).toBe(5);
  });
});
