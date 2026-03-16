import { beforeEach, describe, expect, it } from "vitest";

import { createAuditStore, type AuditCheckItem } from "../audit";

const baseItem: AuditCheckItem = {
  id: "check-01",
  title: "封面完整性",
  status: "pass",
  reason: "封面字段齐全",
  evidenceCount: 2,
  updatedAt: "2026-03-16T17:30:00.000Z",
};

describe("audit store", () => {
  let store = createAuditStore();

  beforeEach(() => {
    store = createAuditStore();
  });

  it("supports replacing and upserting check items", () => {
    store.setItems([baseItem]);
    expect(store.state.items).toHaveLength(1);

    store.upsertItem({ ...baseItem, status: "warn", reason: "存在轻微格式偏差" });
    expect(store.state.items).toHaveLength(1);
    expect(store.state.items[0].status).toBe("warn");

    store.upsertItem({
      ...baseItem,
      id: "check-02",
      title: "目录结构",
      status: "pending",
    });
    expect(store.state.items).toHaveLength(2);
  });

  it("resets transient state on refresh strategy", () => {
    store.setSelectedReportId("report-001");
    store.setStatusFilter("fail");
    store.setQueryFilter("封面");
    store.setLoading(true);

    store.reset();

    expect(store.state.selectedReportId).toBeNull();
    expect(store.state.items).toHaveLength(0);
    expect(store.state.filter.status).toBe("all");
    expect(store.state.filter.query).toBe("");
    expect(store.state.isLoading).toBe(false);
  });
});
