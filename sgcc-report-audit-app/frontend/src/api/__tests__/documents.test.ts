import { describe, expect, it } from "vitest";

import {
  getBrowserDocumentDetail,
  listBrowserDocuments,
} from "../documents";

describe("documents api - data browser contracts", () => {
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
});
