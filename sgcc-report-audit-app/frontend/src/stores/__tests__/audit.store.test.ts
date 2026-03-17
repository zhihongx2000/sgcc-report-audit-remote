import { beforeEach, describe, expect, it } from "vitest";

import {
	createAuditStore,
	filterByStatus,
	renderCheckItems,
	type AuditCheckItem,
} from "../audit";

const baseItem: AuditCheckItem = {
  id: "check-01",
  title: "封面完整性",
  status: "pass",
  reason: "封面字段齐全",
  evidence: [
    {
      id: "check-01-e1",
      label: "正文段落",
      source: "chapter-1.1",
      page: 1,
    },
  ],
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

    store.upsertItem({ ...baseItem, status: "review", reason: "存在轻微格式偏差" });
    expect(store.state.items).toHaveLength(1);
    expect(store.state.items[0].status).toBe("review");

    store.upsertItem({
      ...baseItem,
      id: "check-02",
      title: "目录结构",
      status: "fail",
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

  it("filters by status helper", () => {
    const items: AuditCheckItem[] = [
      baseItem,
      { ...baseItem, id: "check-02", status: "review" },
      { ...baseItem, id: "check-03", status: "fail" },
    ];

    expect(filterByStatus(items, "all")).toHaveLength(3);
    expect(filterByStatus(items, "review")).toHaveLength(1);
    expect(filterByStatus(items, "fail")[0].id).toBe("check-03");
  });

  it("renders filtered and sorted check items", () => {
    const items: AuditCheckItem[] = [
      {
        ...baseItem,
        id: "check-03",
        title: "仿真模型",
        status: "fail",
        reason: "仿真数据与结论不一致",
      },
      { ...baseItem, id: "check-01", title: "封面完整性", status: "pass" },
      {
        ...baseItem,
        id: "check-02",
        title: "评估依据",
        status: "review",
        reason: "标准条文引用不充分",
      },
    ];

    const rendered = renderCheckItems({
      items,
      filter: { status: "all", query: "" },
      sortField: "status",
      sortOrder: "desc",
    });

    expect(rendered[0].status).toBe("fail");
    expect(rendered[1].status).toBe("review");

    const byQuery = renderCheckItems({
      items,
      filter: { status: "all", query: "封面" },
      sortField: "title",
      sortOrder: "asc",
    });

    expect(byQuery).toHaveLength(1);
    expect(byQuery[0].id).toBe("check-01");
  });
});
