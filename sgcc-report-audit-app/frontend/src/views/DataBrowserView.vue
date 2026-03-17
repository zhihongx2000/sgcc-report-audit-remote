<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";

import {
  getBrowserDocumentDetail,
  listBrowserDocuments,
  type BrowserChunkRecord,
  type BrowserDocumentDetail,
  type BrowserDocumentSummary,
  type BrowserImageReference,
} from "../api/documents";
import ChunkViewer, { type MetadataRow } from "../components/data/ChunkViewer.vue";

type SpotlightSelection = {
  chunkId: string;
  image: BrowserImageReference;
};

const isLoading = ref(false);
const errorMessage = ref<string | null>(null);
const allDocuments = ref<BrowserDocumentSummary[]>([]);
const detailsByDocumentId = ref<Record<string, BrowserDocumentDetail>>({});
const selectedDocumentId = ref<string | null>(null);
const activeChunkId = ref<string | null>(null);
const spotlightSelection = ref<SpotlightSelection | null>(null);

const collectionFilter = ref("all");
const documentQuery = ref("");
const chunkQuery = ref("");

const collections = computed(() => {
  const set = new Set(allDocuments.value.map((item) => item.collection));
  return ["all", ...Array.from(set).sort((left, right) => left.localeCompare(right))];
});

const filteredDocuments = computed(() => {
  const collection = collectionFilter.value.trim().toLowerCase();
  const query = documentQuery.value.trim().toLowerCase();

  return allDocuments.value.filter((item) => {
    if (collection !== "all" && item.collection.toLowerCase() !== collection) {
      return false;
    }

    if (!query) {
      return true;
    }

    const searchable = `${item.reportName} ${item.sourcePath} ${item.documentId}`.toLowerCase();
    return searchable.includes(query);
  });
});

const selectedDocument = computed(() =>
  filteredDocuments.value.find((item) => item.documentId === selectedDocumentId.value) ?? null,
);

const selectedDetail = computed(() => {
  if (!selectedDocumentId.value) {
    return null;
  }

  return detailsByDocumentId.value[selectedDocumentId.value] ?? null;
});

const filteredChunks = computed(() => {
  const detail = selectedDetail.value;
  if (!detail) {
    return [];
  }

  const query = chunkQuery.value.trim().toLowerCase();
  if (!query) {
    return detail.chunks;
  }

  return detail.chunks.filter((chunk) => {
    const searchable = [
      chunk.chunkId,
      chunk.text,
      chunk.metadata.title,
      chunk.metadata.summary,
      chunk.metadata.tags.join(" "),
      chunk.metadata.source,
      chunk.metadata.headingPath,
    ]
      .join(" ")
      .toLowerCase();
    return searchable.includes(query);
  });
});

const selectedImageCaption = computed(
  () => spotlightSelection.value?.image.caption ?? "请从 Chunk 图片缩略图中选择一个预览目标。",
);

const selectedImageHighlight = computed(
  () => spotlightSelection.value?.image.highlight ?? "选中后将显示图片对应的关键定位描述。",
);

function formatDateTime(value: string): string {
  const asDate = new Date(value);
  if (Number.isNaN(asDate.getTime())) {
    return value;
  }

  const yyyy = asDate.getFullYear();
  const mm = String(asDate.getMonth() + 1).padStart(2, "0");
  const dd = String(asDate.getDate()).padStart(2, "0");
  const hh = String(asDate.getHours()).padStart(2, "0");
  const min = String(asDate.getMinutes()).padStart(2, "0");
  return `${yyyy}-${mm}-${dd} ${hh}:${min}`;
}

// C5 acceptance: metadata information is rendered in an explicit key/value format.
function renderMetadata(chunk: BrowserChunkRecord): MetadataRow[] {
  return [
    { label: "source", value: chunk.metadata.source },
    { label: "page", value: chunk.metadata.page ? `P${chunk.metadata.page}` : "未标注" },
    { label: "doc_type", value: chunk.metadata.docType },
    { label: "heading", value: chunk.metadata.headingPath },
    { label: "tags", value: chunk.metadata.tags.join(" / ") || "无" },
    { label: "ingested_at", value: formatDateTime(chunk.metadata.ingestedAt) },
  ];
}

async function loadDocuments(): Promise<void> {
  allDocuments.value = await listBrowserDocuments();
}

async function loadChunks(documentId: string): Promise<void> {
  if (detailsByDocumentId.value[documentId]) {
    return;
  }

  const detail = await getBrowserDocumentDetail(documentId);
  detailsByDocumentId.value = {
    ...detailsByDocumentId.value,
    [documentId]: detail,
  };
}

function resetSelectionContext(): void {
  chunkQuery.value = "";
  activeChunkId.value = null;
  spotlightSelection.value = null;
}

async function selectDocument(documentId: string): Promise<void> {
  if (selectedDocumentId.value === documentId) {
    return;
  }

  selectedDocumentId.value = documentId;
  resetSelectionContext();
  await loadChunks(documentId);
  activeChunkId.value = detailsByDocumentId.value[documentId]?.chunks[0]?.chunkId ?? null;
}

function focusChunk(chunkId: string): void {
  activeChunkId.value = chunkId;
}

function openImage(payload: { chunkId: string; image: BrowserImageReference }): void {
  activeChunkId.value = payload.chunkId;
  spotlightSelection.value = payload;
}

async function bootstrapDataBrowser(): Promise<void> {
  try {
    isLoading.value = true;
    await loadDocuments();
    errorMessage.value = null;

    if (filteredDocuments.value.length === 0) {
      selectedDocumentId.value = null;
      return;
    }

    const first = filteredDocuments.value[0];
    selectedDocumentId.value = first.documentId;
    await loadChunks(first.documentId);
    activeChunkId.value = detailsByDocumentId.value[first.documentId]?.chunks[0]?.chunkId ?? null;
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "数据浏览器加载失败";
  } finally {
    isLoading.value = false;
  }
}

watch(filteredDocuments, (next) => {
  if (next.length === 0) {
    selectedDocumentId.value = null;
    resetSelectionContext();
    return;
  }

  const exists = next.some((item) => item.documentId === selectedDocumentId.value);
  if (!exists) {
    void selectDocument(next[0].documentId);
  }
});

onMounted(() => {
  void bootstrapDataBrowser();
});
</script>

<template>
  <section class="data-browser-view" data-page-id="data-browser" data-testid="data-browser-view">
    <header class="hero-head">
      <div>
        <p class="hero-kicker">Data Browser</p>
        <h1>数据浏览器</h1>
        <p>
          浏览文档列表、审阅 Chunk 明细并展开 Metadata，同时支持图片证据预览。
        </p>
      </div>
      <div class="hero-stats" v-if="selectedDocument">
        <span data-testid="browser-selected-doc-id">{{ selectedDocument.documentId }}</span>
        <span>{{ selectedDocument.chunkCount }} chunks</span>
        <span>{{ selectedDocument.imageCount }} images</span>
      </div>
    </header>

    <p v-if="errorMessage" class="error-banner" role="alert">{{ errorMessage }}</p>

    <section class="filter-strip">
      <label>
        <span>集合</span>
        <select v-model="collectionFilter" data-testid="browser-collection-filter">
          <option v-for="collection in collections" :key="collection" :value="collection">
            {{ collection }}
          </option>
        </select>
      </label>

      <label>
        <span>文档检索</span>
        <input
          v-model="documentQuery"
          data-testid="browser-document-search"
          type="text"
          placeholder="按文档名 / 路径 / 文档 ID 检索"
        />
      </label>

      <label>
        <span>Chunk 检索</span>
        <input
          v-model="chunkQuery"
          data-testid="browser-chunk-search"
          type="text"
          placeholder="按 chunk 内容或 metadata 筛选"
          :disabled="!selectedDocumentId"
        />
      </label>
    </section>

    <div class="browser-grid">
      <aside class="document-column" aria-label="文档列表">
        <header>
          <h2>文档列表</h2>
          <p>{{ filteredDocuments.length }} 项</p>
        </header>

        <p v-if="isLoading" class="loading-hint">正在加载文档索引...</p>

        <ul class="document-list" data-testid="browser-document-list">
          <li v-for="doc in filteredDocuments" :key="doc.documentId">
            <button
              type="button"
              class="document-item"
              :class="{ 'is-active': doc.documentId === selectedDocumentId }"
              :data-testid="`browser-doc-${doc.documentId}`"
              @click="void selectDocument(doc.documentId)"
            >
              <p class="doc-title">{{ doc.reportName }}</p>
              <p class="doc-meta">{{ doc.collection }} · {{ formatDateTime(doc.ingestedAt) }}</p>
              <p class="doc-path">{{ doc.sourcePath }}</p>
            </button>
          </li>
        </ul>
      </aside>

      <section class="chunk-column" aria-label="Chunk 明细">
        <header>
          <h2>Chunk 明细</h2>
          <p>{{ filteredChunks.length }} / {{ selectedDetail?.chunks.length ?? 0 }}</p>
        </header>

        <div class="chunk-list" data-testid="browser-chunk-list">
          <ChunkViewer
            v-for="chunk in filteredChunks"
            :key="chunk.chunkId"
            :chunk="chunk"
            :metadata-rows="renderMetadata(chunk)"
            :active-image-id="spotlightSelection?.image.id ?? null"
            :active="chunk.chunkId === activeChunkId"
            @focus-chunk="focusChunk"
            @open-image="openImage"
          />

          <p v-if="filteredChunks.length === 0" class="empty-hint">暂无可展示的 Chunk，请调整筛选条件。</p>
        </div>
      </section>

      <aside class="spotlight-column" aria-label="图片与元数据预览">
        <header>
          <h2>预览聚焦</h2>
          <p>点击 Chunk 图片后在此查看定位说明</p>
        </header>

        <article class="spotlight-card" data-testid="browser-image-spotlight">
          <p class="spotlight-caption" data-testid="browser-image-spotlight-caption">
            {{ selectedImageCaption }}
          </p>
          <p class="spotlight-highlight">{{ selectedImageHighlight }}</p>
        </article>

        <article class="meta-card" v-if="selectedDocument">
          <h3>当前文档</h3>
          <dl>
            <div>
              <dt>文档 ID</dt>
              <dd>{{ selectedDocument.documentId }}</dd>
            </div>
            <div>
              <dt>集合</dt>
              <dd>{{ selectedDocument.collection }}</dd>
            </div>
            <div>
              <dt>摄取时间</dt>
              <dd>{{ formatDateTime(selectedDocument.ingestedAt) }}</dd>
            </div>
            <div>
              <dt>路径</dt>
              <dd>{{ selectedDocument.sourcePath }}</dd>
            </div>
          </dl>
        </article>
      </aside>
    </div>
  </section>
</template>

<style scoped>
.data-browser-view {
  display: grid;
  gap: 0.92rem;
  animation: page-enter var(--duration-slow) var(--ease-standard);
}

.hero-head {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  align-items: center;
}

.hero-kicker {
  margin: 0;
  font-size: var(--text-xs);
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #5d7fa4;
}

.hero-head h1 {
  margin: 0.16rem 0 0;
  color: var(--color-brand-900);
  font-size: 1.74rem;
}

.hero-head p {
  margin: 0.3rem 0 0;
  color: var(--color-text-secondary);
  font-size: var(--text-sm);
}

.hero-stats {
  display: flex;
  gap: 0.44rem;
  flex-wrap: wrap;
  justify-content: end;
}

.hero-stats span {
  padding: 0.34rem 0.58rem;
  border-radius: var(--radius-pill);
  border: 1px solid var(--color-border-strong);
  background: color-mix(in srgb, var(--color-brand-300) 18%, white);
  color: var(--color-brand-800);
  font-size: var(--text-xs);
  letter-spacing: 0.03em;
}

.error-banner {
  margin: 0;
  padding: 0.56rem 0.7rem;
  border: 1px solid color-mix(in srgb, var(--color-danger) 45%, white);
  border-radius: 0.6rem;
  background: color-mix(in srgb, var(--color-danger) 8%, white);
  color: #9b3242;
}

.filter-strip {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.62rem;
  padding: 0.72rem;
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border-soft);
  background:
    radial-gradient(circle at 4% 0%, rgba(38, 112, 182, 0.18), transparent 34%),
    linear-gradient(180deg, #fbfdff 0%, #eff6ff 100%);
}

.filter-strip label {
  display: grid;
  gap: 0.28rem;
}

.filter-strip span {
  font-size: var(--text-xs);
  color: #587ca3;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.filter-strip input,
.filter-strip select {
  border: 1px solid #bfd3eb;
  border-radius: 0.56rem;
  background: white;
  color: #234a72;
  min-height: 2rem;
  padding: 0 0.56rem;
}

.filter-strip input:disabled {
  background: #eef3fa;
  color: #7b95b2;
}

.browser-grid {
  display: grid;
  grid-template-columns: 270px minmax(0, 1fr) 310px;
  gap: 0.72rem;
  min-width: 0;
}

.document-column,
.chunk-column,
.spotlight-column {
  border: 1px solid var(--color-border-soft);
  border-radius: var(--radius-md);
  background: var(--color-bg-panel);
  box-shadow: var(--shadow-soft);
  min-width: 0;
}

.document-column,
.chunk-column,
.spotlight-column {
  padding: 0.68rem;
  display: grid;
  gap: 0.58rem;
  align-content: start;
}

.document-column header,
.chunk-column header,
.spotlight-column header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
}

.document-column h2,
.chunk-column h2,
.spotlight-column h2 {
  margin: 0;
  color: #21466d;
  font-size: var(--text-xl);
}

.document-column header p,
.chunk-column header p,
.spotlight-column header p {
  margin: 0;
  color: #6284a8;
  font-size: var(--text-xs);
}

.loading-hint,
.empty-hint {
  margin: 0;
  padding: 0.48rem 0.54rem;
  border-radius: 0.56rem;
  border: 1px dashed #bfd5ee;
  color: #6385ab;
  background: rgba(245, 250, 255, 0.82);
}

.document-list {
  margin: 0;
  padding: 0;
  list-style: none;
  display: grid;
  gap: 0.44rem;
  max-height: 66vh;
  overflow: auto;
}

.document-item {
  width: 100%;
  border: 1px solid #cfdef1;
  border-radius: 0.64rem;
  background: linear-gradient(180deg, #fbfdff 0%, #f2f7ff 100%);
  padding: 0.56rem;
  text-align: left;
  display: grid;
  gap: 0.2rem;
  cursor: pointer;
  transition:
    border-color var(--duration-fast) var(--ease-standard),
    transform var(--duration-fast) var(--ease-standard),
    box-shadow var(--duration-fast) var(--ease-standard);
}

.document-item:hover {
  border-color: #90b4dc;
  box-shadow: 0 12px 22px rgba(24, 66, 117, 0.14);
  transform: translateY(-1px);
}

.document-item.is-active {
  border-color: #2f70b8;
  box-shadow:
    inset 3px 0 0 #2f70b8,
    0 12px 22px rgba(22, 63, 111, 0.18);
}

.doc-title {
  margin: 0;
  color: #234a72;
  font-size: var(--text-md);
  font-weight: var(--weight-semibold);
}

.doc-meta,
.doc-path {
  margin: 0;
  font-size: var(--text-xs);
  color: #6284a9;
}

.doc-path {
  word-break: break-all;
}

.chunk-list {
  display: grid;
  gap: 0.52rem;
  max-height: 72vh;
  overflow: auto;
}

.spotlight-card,
.meta-card {
  border: 1px solid #cbdcf1;
  border-radius: 0.68rem;
  background: linear-gradient(180deg, #fbfdff 0%, #f2f7ff 100%);
  padding: 0.62rem;
}

.spotlight-caption {
  margin: 0;
  color: #21486f;
  font-size: var(--text-md);
  font-weight: var(--weight-semibold);
}

.spotlight-highlight {
  margin: 0.4rem 0 0;
  color: #496d96;
  font-size: var(--text-sm);
}

.meta-card h3 {
  margin: 0;
  color: #21486f;
  font-size: var(--text-md);
}

.meta-card dl {
  margin: 0.52rem 0 0;
  display: grid;
  gap: 0.42rem;
}

.meta-card div {
  display: grid;
  gap: 0.2rem;
  border: 1px solid #d8e6f6;
  border-radius: 0.52rem;
  background: white;
  padding: 0.42rem;
}

.meta-card dt {
  margin: 0;
  font-size: var(--text-xs);
  color: #6284a9;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}

.meta-card dd {
  margin: 0;
  font-size: var(--text-sm);
  color: #21486f;
  word-break: break-all;
}

@media (max-width: 1320px) {
  .browser-grid {
    grid-template-columns: 250px minmax(0, 1fr);
  }

  .spotlight-column {
    grid-column: 1 / -1;
  }
}

@media (max-width: 980px) {
  .hero-head {
    flex-direction: column;
    align-items: start;
  }

  .hero-stats {
    justify-content: start;
  }

  .filter-strip {
    grid-template-columns: 1fr;
  }

  .browser-grid {
    grid-template-columns: 1fr;
  }

  .document-list,
  .chunk-list {
    max-height: none;
  }
}
</style>
