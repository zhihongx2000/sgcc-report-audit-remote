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
});
