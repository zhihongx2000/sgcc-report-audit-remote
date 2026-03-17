import { beforeEach, describe, expect, it } from "vitest";

import {
  getBrowserDocumentDetail,
  listBrowserDocuments,
  listIngestionTasks,
  resetIngestionTaskState,
  retryTask,
  startIngestion,
} from "../documents";

describe("documents api - data browser contracts", () => {
  beforeEach(() => {
    resetIngestionTaskState();
  });

  it("lists browser documents in descending ingestedAt order", async () => {
    const docs = await listBrowserDocuments();

    expect(docs.length).toBeGreaterThan(0);
    expect(Date.parse(docs[0].ingestedAt)).toBeGreaterThanOrEqual(
      Date.parse(docs[docs.length - 1].ingestedAt),
    );
    expect(docs[0].chunkCount).toBeGreaterThan(0);
  });

  it("supports collection and query filters", async () => {
    const filteredByCollection = await listBrowserDocuments({
      collection: "sgcc-archive",
    });
    expect(filteredByCollection.length).toBeGreaterThan(0);
    expect(filteredByCollection.every((item) => item.collection === "sgcc-archive")).toBe(true);

    const filteredByQuery = await listBrowserDocuments({
      query: "沿海风电",
    });
    expect(filteredByQuery.length).toBeGreaterThan(0);
    expect(
      filteredByQuery.some(
        (item) =>
          item.reportName.includes("沿海风电") || item.sourcePath.includes("沿海风电"),
      ),
    ).toBe(true);
  });

  it("returns deep-cloned browser detail payload", async () => {
    const docs = await listBrowserDocuments();
    const detailA = await getBrowserDocumentDetail(docs[0].documentId);
    const detailB = await getBrowserDocumentDetail(docs[0].documentId);

    expect(detailA.summary.documentId).toBe(docs[0].documentId);
    expect(detailA.chunks.length).toBeGreaterThan(0);

    detailA.chunks[0].metadata.tags.push("mutated-tag");
    expect(detailB.chunks[0].metadata.tags.includes("mutated-tag")).toBe(false);
  });

  it("throws for unknown browser document id", async () => {
    await expect(getBrowserDocumentDetail("unknown-doc-id")).rejects.toThrow(
      "Unknown document",
    );
  });

  it("starts an ingestion task from source path and keeps it queryable", async () => {
    const created = await startIngestion({
      sourcePath: "/data/documents/sgcc-default/new-c6-source.pdf",
      collection: "sgcc-default",
    });

    expect(created.taskId).toContain("ing-task-");
    expect(created.status).toBe("queued");
    expect(created.sourcePath).toContain("new-c6-source.pdf");

    const tasks = await listIngestionTasks();
    expect(tasks.some((task) => task.taskId === created.taskId)).toBe(true);
  });

  it("retries failed ingestion task into running state", async () => {
    const tasks = await listIngestionTasks();
    const failed = tasks.find((task) => task.status === "failed");
    expect(failed).toBeDefined();

    const retried = await retryTask(failed!.taskId);
    expect(retried.status).toBe("running");
    expect(retried.retryCount).toBeGreaterThanOrEqual(1);
    expect(retried.errorMessage).toBeNull();
  });

  it("rejects startIngestion without source path or upload file name", async () => {
    await expect(startIngestion({ collection: "sgcc-default" })).rejects.toThrow(
      "sourcePath or fileName is required",
    );
  });
});
