<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";

import {
  loadQueryTrace,
  type QueryTraceRecord,
  type QueryTraceStage,
} from "../api/trace";
import TraceDetailPanel from "../components/traces/TraceDetailPanel.vue";
import WaterfallChart from "../components/traces/WaterfallChart.vue";

const traces = ref<QueryTraceRecord[]>([]);
const selectedTraceId = ref<string | null>(null);
const selectedStageKey = ref<string | null>(null);
const keyword = ref("");
const isLoading = ref(false);
const errorMessage = ref<string | null>(null);

const filteredTraces = computed(() => {
  const key = keyword.value.trim().toLowerCase();
  if (!key) {
    return traces.value;
  }

  return traces.value.filter((trace) => {
    const query = trace.queryText.toLowerCase();
    const summary = trace.summary.toLowerCase();
    return query.includes(key) || summary.includes(key);
  });
});

const selectedTrace = computed(() => {
  const pool = filteredTraces.value;
  if (pool.length === 0) {
    return null;
  }

  if (!selectedTraceId.value) {
    return pool[0];
  }

  return pool.find((trace) => trace.id === selectedTraceId.value) ?? pool[0];
});

const selectedStage = computed(() => {
  if (!selectedTrace.value || !selectedStageKey.value) {
    return null;
  }

  return (
    selectedTrace.value.stages.find((stage) => stage.key === selectedStageKey.value) ??
    null
  );
});

const successCount = computed(
  () => traces.value.filter((trace) => trace.status === "success").length,
);

const warningCount = computed(
  () => traces.value.filter((trace) => trace.status === "warning").length,
);

const averageDurationMs = computed(() => {
  if (traces.value.length === 0) {
    return 0;
  }

  const total = traces.value.reduce((sum, trace) => sum + trace.totalDurationMs, 0);
  return Math.round(total / traces.value.length);
});

const denseCount = computed(() => selectedTrace.value?.denseCandidates.length ?? 0);
const sparseCount = computed(() => selectedTrace.value?.sparseCandidates.length ?? 0);
const fusionCount = computed(() => selectedTrace.value?.fusionCandidates.length ?? 0);
const topKCount = computed(() => selectedTrace.value?.topKResults.length ?? 0);

watch(filteredTraces, (next) => {
  if (next.length === 0) {
    selectedTraceId.value = null;
    selectedStageKey.value = null;
    return;
  }

  const hasSelected = next.some((item) => item.id === selectedTraceId.value);
  if (!hasSelected) {
    selectedTraceId.value = next[0].id;
    selectedStageKey.value = next[0].stages[0]?.key ?? null;
  }
}, { immediate: true });

watch(selectedTrace, (next) => {
  if (!next) {
    selectedStageKey.value = null;
    return;
  }

  const hasSelectedStage = next.stages.some((stage) => stage.key === selectedStageKey.value);
  if (!hasSelectedStage) {
    selectedStageKey.value = next.stages[0]?.key ?? null;
  }
}, { immediate: true });

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
  const sec = String(asDate.getSeconds()).padStart(2, "0");
  return `${yyyy}-${mm}-${dd} ${hh}:${min}:${sec}`;
}

function formatDuration(value: number): string {
  if (value >= 1000) {
    return `${(value / 1000).toFixed(2)}s`;
  }

  return `${value}ms`;
}

function statusLabel(status: QueryTraceRecord["status"]): string {
  if (status === "success") {
    return "成功";
  }

  if (status === "warning") {
    return "告警";
  }

  if (status === "running") {
    return "进行中";
  }

  return "失败";
}

function selectTrace(traceId: string): void {
  const next = filteredTraces.value.find((trace) => trace.id === traceId);
  if (!next) {
    return;
  }

  selectedTraceId.value = next.id;
  selectedStageKey.value = next.stages[0]?.key ?? null;
}

function selectStage(stage: QueryTraceStage): void {
  selectedStageKey.value = stage.key;
}

async function refreshQueryTraces(): Promise<void> {
  isLoading.value = true;
  errorMessage.value = null;

  try {
    traces.value = await loadQueryTrace();
  } catch (error) {
    errorMessage.value =
      error instanceof Error ? error.message : "查询 Trace 加载失败";
  } finally {
    isLoading.value = false;
  }
}

onMounted(() => {
  void refreshQueryTraces();
});
</script>

<template>
  <section class="query-traces-view" data-page-id="query-traces" data-testid="query-traces-view">
    <header class="hero-head">
      <div>
        <p class="hero-kicker">Query Traces</p>
        <h1>查询追踪</h1>
        <p>回放 query_processing 到 rerank 全链路，查看候选变化与最终 Top-K 结果。</p>
      </div>
      <div class="hero-pills">
        <span>总数 {{ traces.length }}</span>
        <span>成功 {{ successCount }}</span>
        <span>告警 {{ warningCount }}</span>
        <span>平均 {{ formatDuration(averageDurationMs) }}</span>
      </div>
    </header>

    <p v-if="errorMessage" class="error-banner" role="alert">{{ errorMessage }}</p>
    <p v-else-if="isLoading" class="loading-hint">正在加载 Query Trace...</p>

    <div class="traces-grid">
      <article class="panel-card history-panel">
        <header>
          <div>
            <h2>查询历史</h2>
            <p>按开始时间倒序，可按关键词筛选</p>
          </div>
          <input
            v-model="keyword"
            class="query-filter"
            data-testid="query-trace-filter"
            type="search"
            placeholder="筛选 Query 关键词"
          />
        </header>

        <ul class="trace-list" data-testid="query-trace-history">
          <li v-for="trace in filteredTraces" :key="trace.id">
            <button
              type="button"
              class="trace-card"
              :class="[
                `trace-${trace.status}`,
                { 'is-active': selectedTrace?.id === trace.id },
              ]"
              :data-testid="`query-trace-item-${trace.id}`"
              @click="selectTrace(trace.id)"
            >
              <div class="trace-card-head">
                <p class="trace-query" :title="trace.queryText">{{ trace.queryText }}</p>
                <span class="status-pill">{{ statusLabel(trace.status) }}</span>
              </div>
              <p class="trace-summary">{{ trace.summary }}</p>
              <p class="trace-meta">{{ trace.collection }} · {{ formatDateTime(trace.startedAt) }}</p>
              <p class="trace-duration">总耗时 {{ formatDuration(trace.totalDurationMs) }}</p>
            </button>
          </li>
        </ul>
        <p v-if="filteredTraces.length === 0" class="empty-hint">未匹配到相关 Query Trace。</p>
      </article>

      <article class="panel-card detail-panel">
        <header>
          <div>
            <h2>阶段瀑布与候选对比</h2>
            <p v-if="selectedTrace">Trace ID: {{ selectedTrace.id }}</p>
          </div>
          <button type="button" class="refresh-btn" @click="void refreshQueryTraces()">刷新</button>
        </header>

        <template v-if="selectedTrace">
          <div class="metric-grid">
            <div>
              <p class="metric-label">Dense</p>
              <p class="metric-value">{{ denseCount }}</p>
            </div>
            <div>
              <p class="metric-label">Sparse</p>
              <p class="metric-value">{{ sparseCount }}</p>
            </div>
            <div>
              <p class="metric-label">Fusion</p>
              <p class="metric-value">{{ fusionCount }}</p>
            </div>
            <div>
              <p class="metric-label">Top-K</p>
              <p class="metric-value">{{ topKCount }}</p>
            </div>
          </div>

          <p v-if="selectedTrace.fallbackTriggered" class="warning-inline">
            Rerank fallback 触发：当前 Top-K 来自 fusion 排名。
          </p>

          <WaterfallChart
            :stages="selectedTrace.stages"
            :selected-stage-key="selectedStageKey"
            @select="selectStage"
          />

          <aside v-if="selectedStage" class="stage-drawer" data-testid="query-stage-drawer">
            <header>
              <h3>{{ selectedStage.name }} 阶段明细</h3>
              <p>{{ formatDuration(selectedStage.durationMs) }}</p>
            </header>

            <dl class="stage-detail-grid">
              <div>
                <dt>Method</dt>
                <dd data-testid="query-stage-method">{{ selectedStage.method }}</dd>
              </div>
              <div>
                <dt>Provider</dt>
                <dd>{{ selectedStage.provider }}</dd>
              </div>
              <div>
                <dt>Input</dt>
                <dd>{{ selectedStage.inputCount }}</dd>
              </div>
              <div>
                <dt>Output</dt>
                <dd>{{ selectedStage.outputCount }}</dd>
              </div>
            </dl>

            <p class="stage-detail-copy">{{ selectedStage.detail }}</p>
          </aside>

          <TraceDetailPanel :trace="selectedTrace" />
        </template>

        <p v-else class="empty-hint">当前没有可展示的 Query Trace。</p>
      </article>
    </div>
  </section>
</template>

<style scoped>
.query-traces-view {
  display: grid;
  gap: 0.95rem;
}

.hero-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.hero-kicker {
  margin: 0;
  font-size: var(--text-xs);
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #5f7ea0;
}

.hero-head h1 {
  margin: 0.12rem 0 0;
  font-size: 1.66rem;
  color: var(--color-brand-900);
}

.hero-head p {
  margin: 0.2rem 0 0;
  color: var(--color-text-secondary);
}

.hero-pills {
  display: flex;
  gap: 0.48rem;
  flex-wrap: wrap;
}

.hero-pills span {
  padding: 0.34rem 0.72rem;
  border-radius: var(--radius-pill);
  border: 1px solid var(--color-border-strong);
  background: color-mix(in srgb, var(--color-brand-300) 22%, white);
  color: var(--color-brand-900);
  font-size: var(--text-xs);
  font-weight: var(--weight-semibold);
}

.loading-hint {
  margin: 0;
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
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

.traces-grid {
  display: grid;
  grid-template-columns: minmax(300px, 0.94fr) minmax(0, 1.06fr);
  gap: 0.95rem;
  min-width: 0;
}

.panel-card {
  border: 1px solid var(--color-border-soft);
  border-radius: 12px;
  background:
    linear-gradient(180deg, #ffffff 0%, #f6faff 100%),
    repeating-linear-gradient(
      90deg,
      rgba(31, 87, 147, 0.03) 0,
      rgba(31, 87, 147, 0.03) 1px,
      transparent 1px,
      transparent 14px
    );
  padding: 0.9rem;
  box-shadow: 0 10px 20px rgba(18, 42, 78, 0.08);
  min-width: 0;
}

.panel-card > header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 0.7rem;
  margin-bottom: 0.72rem;
}

.panel-card h2 {
  margin: 0;
  font-size: 1.05rem;
  color: var(--color-brand-900);
}

.panel-card > header p {
  margin: 0.2rem 0 0;
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}

.query-filter {
  width: min(260px, 48%);
  min-width: 140px;
  border-radius: var(--radius-pill);
  border: 1px solid var(--color-border-strong);
  background: rgba(255, 255, 255, 0.8);
  padding: 0.34rem 0.65rem;
  color: #234363;
}

.query-filter:focus {
  border-color: var(--color-accent);
}

.trace-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  gap: 0.6rem;
}

.trace-card {
  all: unset;
  display: grid;
  gap: 0.36rem;
  padding: 0.62rem;
  width: 100%;
  box-sizing: border-box;
  border-radius: 10px;
  border: 1px solid color-mix(in srgb, var(--color-border-strong) 70%, white);
  background: color-mix(in srgb, var(--color-bg-panel) 95%, var(--color-brand-200));
  cursor: pointer;
  overflow: hidden;
  transition:
    transform var(--duration-fast) var(--ease-standard),
    border-color var(--duration-normal) var(--ease-standard),
    box-shadow var(--duration-normal) var(--ease-standard);
}

.trace-card:hover {
  transform: translateY(-1px);
  border-color: color-mix(in srgb, var(--color-brand-700) 55%, white);
  box-shadow: 0 7px 14px rgba(24, 57, 106, 0.12);
}

.trace-card.is-active {
  border-color: var(--color-accent);
  box-shadow: 0 0 0 1px color-mix(in srgb, var(--color-accent) 32%, transparent);
}

.trace-card-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.45rem;
  min-width: 0;
}

.trace-query {
  margin: 0;
  min-width: 0;
  flex: 1 1 auto;
  font-size: var(--text-sm);
  font-weight: var(--weight-semibold);
  color: #263f5e;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.status-pill {
  flex-shrink: 0;
  padding: 0.17rem 0.5rem;
  border-radius: var(--radius-pill);
  font-size: 0.72rem;
  font-weight: var(--weight-semibold);
  border: 1px solid transparent;
}

.trace-success .status-pill {
  color: #0b7756;
  background: color-mix(in srgb, var(--color-success) 12%, white);
  border-color: color-mix(in srgb, var(--color-success) 40%, white);
}

.trace-warning .status-pill {
  color: #9a6510;
  background: color-mix(in srgb, var(--color-warning) 15%, white);
  border-color: color-mix(in srgb, var(--color-warning) 45%, white);
}

.trace-failed .status-pill {
  color: #9f3545;
  background: color-mix(in srgb, var(--color-danger) 12%, white);
  border-color: color-mix(in srgb, var(--color-danger) 42%, white);
}

.trace-running .status-pill {
  color: #1f6f86;
  background: color-mix(in srgb, var(--color-accent) 13%, white);
  border-color: color-mix(in srgb, var(--color-accent) 38%, white);
}

.trace-summary,
.trace-meta,
.trace-duration {
  margin: 0;
  font-size: 0.78rem;
  color: #4f6784;
}

.detail-panel {
  display: grid;
  gap: 0.82rem;
  align-content: start;
}

.refresh-btn {
  padding: 0.35rem 0.68rem;
  border-radius: var(--radius-pill);
  border: 1px solid var(--color-border-strong);
  background: color-mix(in srgb, var(--color-brand-200) 46%, white);
  color: var(--color-brand-900);
  font-size: 0.76rem;
  font-weight: var(--weight-semibold);
  cursor: pointer;
  transition:
    transform var(--duration-fast) var(--ease-standard),
    background-color var(--duration-fast) var(--ease-standard);
}

.refresh-btn:hover {
  transform: translateY(-1px);
  background: color-mix(in srgb, var(--color-brand-300) 40%, white);
}

.metric-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 0.5rem;
}

.metric-grid > div {
  padding: 0.52rem 0.58rem;
  border-radius: 10px;
  border: 1px solid color-mix(in srgb, var(--color-brand-300) 35%, white);
  background: linear-gradient(180deg, #fefefe 0%, #edf5ff 100%);
}

.metric-label {
  margin: 0;
  font-size: 0.72rem;
  color: #53708f;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.metric-value {
  margin: 0.15rem 0 0;
  font-size: 1.1rem;
  font-weight: var(--weight-bold);
  color: var(--color-brand-900);
}

.warning-inline {
  margin: 0;
  padding: 0.5rem 0.6rem;
  border-radius: 9px;
  border: 1px solid color-mix(in srgb, var(--color-warning) 40%, white);
  background: color-mix(in srgb, var(--color-warning) 10%, white);
  color: #8f5e12;
  font-size: 0.76rem;
}

.stage-drawer {
  position: relative;
  padding: 0.72rem;
  border-radius: 12px;
  border: 1px solid color-mix(in srgb, var(--color-accent) 45%, white);
  background:
    linear-gradient(180deg, #f9fcff 0%, #e7f4ff 100%),
    radial-gradient(circle at 105% -10%, rgba(34, 184, 203, 0.28) 0%, transparent 52%);
  overflow: hidden;
}

.stage-drawer > header {
  display: flex;
  justify-content: space-between;
  gap: 0.6rem;
  align-items: baseline;
}

.stage-drawer h3 {
  margin: 0;
  font-size: 1rem;
  color: #1f3b5a;
}

.stage-drawer > header p {
  margin: 0;
  font-size: 0.78rem;
  color: #446685;
}

.stage-detail-grid {
  margin: 0.65rem 0 0;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0.45rem;
}

.stage-detail-grid div {
  padding: 0.46rem 0.5rem;
  border-radius: 9px;
  background: rgba(255, 255, 255, 0.66);
  border: 1px solid rgba(96, 151, 187, 0.3);
}

.stage-detail-grid dt {
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: #4d6e8b;
}

.stage-detail-grid dd {
  margin: 0.16rem 0 0;
  font-size: 0.82rem;
  font-weight: var(--weight-semibold);
  color: #1f3e5e;
  word-break: break-word;
}

.stage-detail-copy {
  margin: 0.68rem 0 0;
  font-size: 0.82rem;
  line-height: 1.5;
  color: #2f5274;
}

.empty-hint {
  margin: 0;
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}

@media (max-width: 1060px) {
  .traces-grid {
    grid-template-columns: 1fr;
  }

  .history-panel {
    order: 2;
  }

  .detail-panel {
    order: 1;
  }
}

@media (max-width: 720px) {
  .hero-head {
    flex-direction: column;
    align-items: flex-start;
  }

  .panel-card > header {
    flex-direction: column;
    align-items: flex-start;
  }

  .query-filter {
    width: 100%;
    min-width: 0;
  }

  .metric-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .stage-detail-grid {
    grid-template-columns: 1fr;
  }
}
</style>
