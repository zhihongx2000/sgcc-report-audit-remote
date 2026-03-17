<script setup lang="ts">
import { computed, onMounted } from "vue";

import { loadOverviewStats } from "../api/trace";
import { useAppStore } from "../stores/app";

const appStore = useAppStore();

const componentConfigCards = computed(
  () => appStore.state.overviewStats?.componentCards ?? [],
);
const collectionStats = computed(
  () => appStore.state.overviewStats?.collectionStats ?? [],
);
const healthMetrics = computed(
  () => appStore.state.overviewStats?.healthMetrics ?? [],
);

const totalDocuments = computed(() =>
  collectionStats.value.reduce((acc, item) => acc + item.documents, 0),
);
const totalChunks = computed(() =>
  collectionStats.value.reduce((acc, item) => acc + item.chunks, 0),
);
const totalImages = computed(() =>
  collectionStats.value.reduce((acc, item) => acc + item.images, 0),
);

const cardLookup = computed(() => {
  const map = new Map<string, string>();
  for (const card of componentConfigCards.value) {
    map.set(card.title.toLowerCase(), card.value);
  }
  return map;
});

const providerModelLine = computed(
  () => cardLookup.value.get("llm") ?? "未获取 LLM provider/model",
);

const vectorStoreLine = computed(() => {
  const direct = cardLookup.value.get("vectorstore") ?? cardLookup.value.get("vector_store");
  if (direct) {
    return direct;
  }

  // Keep a stable fallback line so overview still communicates vector backend in mock-first mode.
  return "pgvector / rag_chunks / cosine";
});

async function fetchOverviewStats(): Promise<void> {
  try {
    appStore.setOverviewLoading(true);
    const stats = await loadOverviewStats();
    appStore.setOverviewStats(stats);
    appStore.setOverviewErrorMessage(null);
  } catch (error) {
    const message = error instanceof Error ? error.message : "系统总览数据加载失败";
    appStore.setOverviewErrorMessage(message);
  } finally {
    appStore.setOverviewLoading(false);
  }
}

onMounted(() => {
  if (!appStore.state.overviewStats) {
    void fetchOverviewStats();
  }
});
</script>

<template>
  <section class="overview-panel" data-page-id="overview">
    <header class="hero-head">
      <div>
        <h1>系统总览</h1>
        <p>
          页面内容按 DEV_SPEC 3.5.5
          定义：组件配置卡片、数据资产统计、系统健康指标。
        </p>
      </div>
      <div class="summary-pill">
        <span data-testid="overview-total-documents">文档 {{ totalDocuments }}</span>
        <span data-testid="overview-total-chunks">Chunk {{ totalChunks }}</span>
        <span data-testid="overview-total-images">图片 {{ totalImages }}</span>
      </div>
    </header>

    <p v-if="appStore.state.overviewErrorMessage" class="error-banner" role="alert">
      {{ appStore.state.overviewErrorMessage }}
    </p>

    <article class="signal-strip" data-testid="overview-signal-strip">
      <div>
        <p class="signal-kicker">Provider / Model</p>
        <p class="signal-value" data-testid="overview-provider-model">{{ providerModelLine }}</p>
      </div>
      <div>
        <p class="signal-kicker">VectorStore</p>
        <p class="signal-value" data-testid="overview-vectorstore">{{ vectorStoreLine }}</p>
      </div>
      <div>
        <p class="signal-kicker">Health Window</p>
        <p class="signal-value" data-testid="overview-health-line">
          {{ healthMetrics[0]?.value ?? "等待健康指标..." }}
        </p>
      </div>
    </article>

    <article class="panel-card">
      <header class="panel-head">
        <h2>组件配置卡片</h2>
        <p>读取 Settings 的可插拔组件状态</p>
      </header>
      <p v-if="appStore.state.isOverviewLoading" class="loading-hint">正在同步配置与统计数据...</p>
      <div class="config-grid">
        <div
          v-for="item in componentConfigCards"
          :key="item.title"
          class="config-card"
          :data-testid="`overview-config-${item.title.toLowerCase()}`"
        >
          <p class="config-title">{{ item.title }}</p>
          <p class="config-value">{{ item.value }}</p>
          <p class="config-detail">{{ item.detail }}</p>
        </div>
      </div>
    </article>

    <div class="lower-grid">
      <article class="panel-card">
        <header class="panel-head">
          <h2>数据资产统计</h2>
          <p>来自 DocumentManager.get_collection_stats()</p>
        </header>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>集合</th>
                <th>文档数</th>
                <th>Chunk 数</th>
                <th>图片数</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in collectionStats" :key="item.name">
                <td>{{ item.name }}</td>
                <td>{{ item.documents }}</td>
                <td>{{ item.chunks }}</td>
                <td>{{ item.images }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </article>

      <article class="panel-card">
        <header class="panel-head">
          <h2>系统健康指标</h2>
          <p>最近一次 Ingestion / Query Trace 时间与耗时</p>
        </header>
        <div class="health-list">
          <div
            v-for="item in healthMetrics"
            :key="item.title"
            class="health-item"
            :data-testid="`overview-health-${item.title}`"
          >
            <p class="health-title">{{ item.title }}</p>
            <p class="health-value">{{ item.value }}</p>
            <p class="health-sub">{{ item.sub }}</p>
          </div>
        </div>
      </article>
    </div>
  </section>
</template>

<style scoped>
.overview-panel {
  display: grid;
  gap: 0.95rem;
  animation: page-enter var(--duration-slow) var(--ease-standard);
}

.hero-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  padding: 0.2rem 0;
}

.hero-head h1 {
  margin: 0;
  font-size: 1.7rem;
  color: var(--color-brand-900);
}

.hero-head p {
  margin: 0.28rem 0 0;
  font-size: 0.9rem;
  color: var(--color-text-secondary);
}

.summary-pill {
  display: flex;
  gap: 0.45rem;
  flex-wrap: wrap;
}

.summary-pill span {
  padding: 0.36rem 0.62rem;
  font-size: 0.78rem;
  border-radius: 999px;
  border: 1px solid var(--color-border-strong);
  background: color-mix(in srgb, var(--color-brand-300) 22%, white);
  color: var(--color-brand-800);
}

.error-banner {
  margin: 0;
  padding: 0.52rem 0.66rem;
  border-radius: 0.62rem;
  border: 1px solid color-mix(in srgb, var(--color-danger) 40%, white);
  background: color-mix(in srgb, var(--color-danger) 10%, white);
  color: #9f3545;
  font-size: var(--text-sm);
}

.signal-strip {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.68rem;
  padding: 0.72rem;
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border-soft);
  background:
    radial-gradient(circle at 0% 0%, color-mix(in srgb, var(--color-accent) 18%, white), transparent 34%),
    linear-gradient(180deg, #fafdff 0%, #f1f7ff 100%);
}

.signal-kicker {
  margin: 0;
  font-size: var(--text-xs);
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #5f7f9f;
}

.signal-value {
  margin: 0.24rem 0 0;
  font-size: var(--text-md);
  font-weight: var(--weight-semibold);
  color: var(--color-brand-800);
  line-height: 1.35;
}

.panel-card {
  border: 1px solid var(--color-border-soft);
  border-radius: 12px;
  background: var(--color-bg-panel);
  padding: 0.9rem;
  box-shadow: 0 10px 20px rgba(18, 42, 78, 0.08);
}

.panel-head {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 0.8rem;
  margin-bottom: 0.72rem;
}

.panel-head h2 {
  margin: 0;
  font-size: 1.02rem;
  color: var(--color-brand-900);
}

.panel-head p {
  margin: 0;
  font-size: 0.78rem;
  color: var(--color-text-secondary);
}

.loading-hint {
  margin: 0 0 0.62rem;
  font-size: var(--text-sm);
  color: #4f7399;
}

.config-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 0.6rem;
}

.config-card {
  padding: 0.72rem;
  border: 1px solid var(--color-border-soft);
  border-radius: 10px;
  background: linear-gradient(180deg, #fbfdff 0%, #f3f8ff 100%);
  transition:
    border-color var(--duration-fast) var(--ease-standard),
    transform var(--duration-fast) var(--ease-standard),
    box-shadow var(--duration-fast) var(--ease-standard);
}

.config-card:hover {
  border-color: #9ec2ea;
  transform: translateY(-1px);
  box-shadow: 0 10px 20px rgba(20, 55, 100, 0.14);
}

.config-title {
  margin: 0;
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--color-brand-800);
}

.config-value {
  margin: 0.26rem 0 0;
  font-size: 0.86rem;
  font-weight: 600;
  color: var(--color-text-primary);
  line-height: 1.35;
  word-break: break-word;
}

.config-detail {
  margin: 0.28rem 0 0;
  font-size: 0.75rem;
  color: var(--color-text-secondary);
}

.lower-grid {
  display: grid;
  grid-template-columns: 1.2fr 1fr;
  gap: 0.95rem;
}

.table-wrap {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.86rem;
}

th,
td {
  padding: 0.52rem 0.45rem;
  text-align: left;
  border-bottom: 1px solid #e8eef8;
  white-space: nowrap;
}

th {
  font-size: 0.77rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: #6b819d;
}

td {
  color: var(--color-text-primary);
}

.health-list {
  display: grid;
  gap: 0.56rem;
}

.health-item {
  padding: 0.62rem;
  border-radius: 10px;
  border: 1px solid #e4ebf7;
  background: #f8fbff;
}

.health-title {
  margin: 0;
  font-size: 0.8rem;
  color: #56708e;
}

.health-value {
  margin: 0.26rem 0 0;
  font-size: 0.92rem;
  font-weight: 700;
  color: var(--color-brand-900);
}

.health-sub {
  margin: 0.2rem 0 0;
  font-size: 0.76rem;
  color: #7388a2;
}

@media (max-width: 1120px) {
  .signal-strip {
    grid-template-columns: 1fr;
  }

  .config-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .lower-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 700px) {
  .hero-head {
    flex-direction: column;
    align-items: flex-start;
  }

  .hero-head h1 {
    font-size: 1.35rem;
  }

  .config-grid {
    grid-template-columns: 1fr;
  }
}
</style>
