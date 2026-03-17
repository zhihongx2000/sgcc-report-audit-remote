import { beforeEach, describe, expect, it } from "vitest";

import { createAppStore } from "../app";

describe("app store", () => {
  beforeEach(() => {
    const store = createAppStore();
    store.reset();
  });

  it("persists session-scoped preferences across store instances", () => {
    const first = createAppStore();
    first.setActiveCollection("sgcc-samples");
    first.toggleSidebar();
    first.setAutoRefresh(false);
    first.setRefreshIntervalSec(9);
    first.setLastVisitedRoute("/query-traces");

    const second = createAppStore();
    expect(second.state.activeCollection).toBe("sgcc-samples");
    expect(second.state.sidebarCollapsed).toBe(true);
    expect(second.state.autoRefresh).toBe(false);
    expect(second.state.refreshIntervalSec).toBe(9);
    expect(second.state.lastVisitedRoute).toBe("/query-traces");
  });

  it("normalizes invalid refresh intervals", () => {
    const store = createAppStore();
    store.setRefreshIntervalSec(0);

    expect(store.state.refreshIntervalSec).toBe(1);
  });

  it("tracks ingestion task list and supports upsert", () => {
    const store = createAppStore();
    const seedTask = {
      taskId: "ing-task-seed",
      sourcePath: "/data/documents/sgcc-default/seed.pdf",
      collection: "sgcc-default",
      status: "running" as const,
      progressPercent: 28,
      startedAt: "2026-03-17T12:00:00.000Z",
      updatedAt: "2026-03-17T12:00:10.000Z",
      errorMessage: null,
      retryCount: 0,
      inputMode: "path" as const,
    };

    store.setIngestionTasks([seedTask]);
    expect(store.state.ingestionTasks).toHaveLength(1);
    expect(store.state.ingestionTasks[0].taskId).toBe("ing-task-seed");

    const updated = {
      ...seedTask,
      status: "failed" as const,
      errorMessage: "split failed",
      progressPercent: 64,
    };
    store.upsertIngestionTask(updated);

    expect(store.state.ingestionTasks).toHaveLength(1);
    expect(store.state.ingestionTasks[0].status).toBe("failed");
    expect(store.state.ingestionTasks[0].errorMessage).toBe("split failed");

    store.upsertIngestionTask({
      ...seedTask,
      taskId: "ing-task-new",
      sourcePath: "/data/documents/sgcc-default/new.pdf",
      status: "queued",
      progressPercent: 0,
      updatedAt: "2026-03-17T12:00:20.000Z",
    });

    expect(store.state.ingestionTasks).toHaveLength(2);
    expect(store.state.ingestionTasks[0].taskId).toBe("ing-task-new");
  });

  it("clears ingestion task states on reset", () => {
    const store = createAppStore();
    store.setIngestionTasks([
      {
        taskId: "ing-task-reset",
        sourcePath: "/data/documents/sgcc-default/reset.pdf",
        collection: "sgcc-default",
        status: "running",
        progressPercent: 16,
        startedAt: "2026-03-17T12:00:00.000Z",
        updatedAt: "2026-03-17T12:00:16.000Z",
        errorMessage: null,
        retryCount: 0,
        inputMode: "path",
      },
    ]);
    store.setIngestionErrorMessage("temporary error");
    store.setIngestionLoading(true);

    store.reset();

    expect(store.state.ingestionTasks).toHaveLength(0);
    expect(store.state.ingestionErrorMessage).toBeNull();
    expect(store.state.isIngestionLoading).toBe(false);
  });
});
