import { describe, expect, it } from "vitest";

import { getMockData, mockAuditResult } from "../mock";

describe("mock adapters", () => {
  it("returns valid audit result payload", () => {
    const payload = mockAuditResult();

    expect(payload.success).toBe(true);
    expect(payload.data.reportId.length).toBeGreaterThan(0);
    expect(payload.data.items.length).toBeGreaterThan(0);
    expect(payload.data.items[0].evidence.length).toBeGreaterThan(0);
  });

  it("resolves data by mock key", () => {
    const overview = getMockData("overviewStats");
    const tasks = getMockData("ingestionTasks");

    expect(overview.data.collectionStats.length).toBeGreaterThan(0);
    expect(tasks.data[0].taskId).toContain("ing-task");
  });
});
