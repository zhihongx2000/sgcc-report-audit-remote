<script setup lang="ts">
import { computed, onMounted } from "vue";

import {
  getAuditReportDetail,
  listAuditReports,
  type AuditReportStatus,
} from "../api/documents";
import CheckItemTable from "../components/audit/CheckItemTable.vue";
import {
  renderCheckItems,
  type AuditCheckStatus,
  type AuditSortField,
  type SortOrder,
  useAuditStore,
} from "../stores/audit";

const store = useAuditStore();

type StatusOption = {
  label: string;
  value: AuditCheckStatus | "all";
};

type SortOption = {
  label: string;
  value: AuditSortField;
};

const statusOptions: StatusOption[] = [
  { label: "全部状态", value: "all" },
  { label: "满足", value: "pass" },
  { label: "需复核", value: "review" },
  { label: "不满足", value: "fail" },
];

const sortOptions: SortOption[] = [
  { label: "按状态", value: "status" },
  { label: "按更新时间", value: "updatedAt" },
  { label: "按审查项名称", value: "title" },
];

const reportStatusText: Record<AuditReportStatus, string> = {
  completed: "已完成",
  running: "进行中",
};

const activeReport = computed(() =>
  store.state.reports.find((report) => report.reportId === store.state.selectedReportId) ??
    store.state.reports[0] ??
    null,
);

const statusFilter = computed({
  get: () => store.state.filter.status,
  set: (value: AuditCheckStatus | "all") => store.setStatusFilter(value),
});

const keywordFilter = computed({
  get: () => store.state.filter.query,
  set: (value: string) => store.setQueryFilter(value),
});

const sortField = computed({
  get: () => store.state.sortField,
  set: (value: AuditSortField) => store.setSort(value, store.state.sortOrder),
});

const sortOrderLabel = computed(() =>
  store.state.sortOrder === "desc" ? "降序" : "升序",
);

const displayedItems = computed(() =>
  renderCheckItems({
    items: store.state.items,
    filter: store.state.filter,
    sortField: store.state.sortField,
    sortOrder: store.state.sortOrder,
  }),
);

const statusStats = computed(() => {
  const totals = {
    pass: 0,
    review: 0,
    fail: 0,
  };

  for (const item of store.state.items) {
    totals[item.status] += 1;
  }

  return totals;
});

function toggleSortOrder(): void {
  const nextOrder: SortOrder = store.state.sortOrder === "desc" ? "asc" : "desc";
  store.setSort(store.state.sortField, nextOrder);
}

async function selectReport(reportId: string): Promise<void> {
  if (store.state.selectedReportId === reportId) {
    return;
  }

  try {
    store.setLoading(true);
    if (!store.state.itemsByReportId[reportId]) {
      const detail = await getAuditReportDetail(reportId);
      store.setReportItems(reportId, detail.items);
    }
    store.selectReport(reportId);
    store.setErrorMessage(null);
  } catch (error) {
    const message = error instanceof Error ? error.message : "报告详情加载失败";
    store.setErrorMessage(message);
  } finally {
    store.setLoading(false);
  }
}

async function bootstrapReportDirectory(): Promise<void> {
  try {
    store.setLoading(true);
    const reports = await listAuditReports();
    store.setReports(reports);

    if (reports.length > 0) {
      const firstReport = reports[0];
      const detail = await getAuditReportDetail(firstReport.reportId);
      store.setReportItems(firstReport.reportId, detail.items);
      store.selectReport(firstReport.reportId);
    }

    store.setErrorMessage(null);
  } catch (error) {
    const message = error instanceof Error ? error.message : "报告目录加载失败";
    store.setErrorMessage(message);
  } finally {
    store.setLoading(false);
  }
}

onMounted(() => {
  if (store.state.reports.length === 0) {
    void bootstrapReportDirectory();
  }
});
</script>

<template>
  <section data-page-id="audit-results" class="audit-result-view">
    <div class="workspace-grid">
      <aside class="report-tree" aria-label="报告目录">
        <header class="report-tree-head">
          <p class="tree-kicker">Report Directory</p>
          <h2>报告目录</h2>
          <p>切换进行中/已完成报告，右侧详情实时联动。</p>
        </header>

        <ul class="report-list" data-testid="report-list">
          <li v-for="report in store.state.reports" :key="report.reportId">
            <button
              type="button"
              class="report-node"
              :class="{ 'is-active': report.reportId === store.state.selectedReportId }"
              :data-testid="`report-node-${report.reportId}`"
              @click="void selectReport(report.reportId)"
            >
              <span class="node-title">{{ report.reportName }}</span>
              <span class="node-meta">{{ report.reportId }} · {{ report.collection }}</span>
              <span
                class="node-status"
                :class="`node-status--${report.status}`"
              >
                {{ reportStatusText[report.status] }}
              </span>
            </button>
          </li>
        </ul>
      </aside>

      <div class="result-panel">
        <header class="hero">
          <div>
            <p class="hero-kicker">Report Intelligence</p>
            <h1 class="hero-title">20 项审查结果矩阵</h1>
            <p class="hero-subtitle">
              集中展示每一项判定结果、判定说明与证据定位，并支持状态筛选、关键词检索和排序。
            </p>
          </div>
          <div class="hero-meta" v-if="activeReport">
            <p class="meta-name">{{ activeReport.reportName }}</p>
            <p class="meta-id" data-testid="report-meta-id">
              {{ activeReport.reportId }} · {{ activeReport.collection }}
            </p>
          </div>
        </header>

        <p v-if="store.state.errorMessage" class="error-banner" role="alert">
          {{ store.state.errorMessage }}
        </p>

        <div class="stats-grid" data-testid="status-summary">
          <article class="stat-card stat-card--pass">
            <p>满足</p>
            <strong>{{ statusStats.pass }}</strong>
          </article>
          <article class="stat-card stat-card--review">
            <p>需复核</p>
            <strong>{{ statusStats.review }}</strong>
          </article>
          <article class="stat-card stat-card--fail">
            <p>不满足</p>
            <strong data-testid="status-fail-count">{{ statusStats.fail }}</strong>
          </article>
          <article class="stat-card stat-card--total">
            <p>当前命中</p>
            <strong>{{ displayedItems.length }}/20</strong>
          </article>
        </div>

        <div class="control-panel">
          <label>
            <span>状态筛选</span>
            <select v-model="statusFilter" data-testid="status-filter">
              <option v-for="option in statusOptions" :key="option.value" :value="option.value">
                {{ option.label }}
              </option>
            </select>
          </label>

          <label>
            <span>排序字段</span>
            <select v-model="sortField" data-testid="sort-field">
              <option v-for="option in sortOptions" :key="option.value" :value="option.value">
                {{ option.label }}
              </option>
            </select>
          </label>

          <button class="order-toggle" type="button" @click="toggleSortOrder" data-testid="sort-order-toggle">
            {{ sortOrderLabel }}
          </button>

          <label class="keyword-field">
            <span>关键词</span>
            <input
              v-model="keywordFilter"
              type="text"
              placeholder="输入审查项、判定说明、证据来源"
              data-testid="keyword-filter"
            />
          </label>
        </div>

        <CheckItemTable :items="displayedItems" />
      </div>
    </div>
  </section>
</template>

<style scoped>
.audit-result-view {
  display: block;
}

.workspace-grid {
  display: grid;
  grid-template-columns: minmax(250px, 320px) minmax(0, 1fr);
  gap: 0.86rem;
}

.report-tree {
  border: 1px solid #d4e3f6;
  border-radius: var(--radius-md);
  background:
    radial-gradient(circle at 20% 0%, rgba(71, 117, 179, 0.2), transparent 44%),
    linear-gradient(180deg, #f4f9ff 0%, #ecf4ff 100%);
  padding: 0.78rem;
  box-shadow: var(--shadow-soft);
  animation: page-enter var(--duration-slow) var(--ease-standard);
}

.report-tree-head h2 {
  margin: 0.16rem 0 0;
  font-size: 1.04rem;
  color: #1f3f63;
}

.tree-kicker {
  margin: 0;
  font-size: var(--text-xs);
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #4c72a0;
}

.report-tree-head p {
  margin: 0.22rem 0 0;
  font-size: var(--text-sm);
  color: #54708f;
}

.report-list {
  list-style: none;
  margin: 0.72rem 0 0;
  padding: 0;
  display: grid;
  gap: 0.48rem;
}

.report-node {
  width: 100%;
  display: grid;
  gap: 0.2rem;
  text-align: left;
  padding: 0.58rem 0.6rem;
  border-radius: 0.64rem;
  border: 1px solid #c4d9f4;
  background: linear-gradient(180deg, #ffffff 0%, #f6faff 100%);
  cursor: pointer;
  transition:
    transform var(--duration-fast) var(--ease-standard),
    border-color var(--duration-fast) var(--ease-standard),
    box-shadow var(--duration-fast) var(--ease-standard);
}

.report-node:hover {
  border-color: #8eb5e3;
  transform: translateX(2px);
  box-shadow: 0 8px 18px rgba(40, 79, 132, 0.12);
}

.report-node.is-active {
  border-color: #548fce;
  box-shadow:
    inset 3px 0 0 #4a83bf,
    0 10px 20px rgba(38, 79, 132, 0.16);
}

.node-title {
  font-size: var(--text-sm);
  font-weight: var(--weight-semibold);
  color: #244361;
  line-height: 1.4;
}

.node-meta {
  font-size: var(--text-xs);
  color: #607e9f;
}

.node-status {
  justify-self: start;
  padding: 0.14rem 0.46rem;
  border-radius: var(--radius-pill);
  font-size: var(--text-xs);
  font-weight: var(--weight-semibold);
  border: 1px solid transparent;
}

.node-status--completed {
  color: var(--color-success);
  background: color-mix(in srgb, var(--color-success) 12%, white);
  border-color: color-mix(in srgb, var(--color-success) 32%, white);
}

.node-status--running {
  color: #7a6100;
  background: #fff5d8;
  border-color: #f1d17b;
}

.result-panel {
  display: grid;
  gap: 0.9rem;
  background:
    radial-gradient(circle at 95% 0%, rgba(47, 95, 159, 0.16), transparent 32%),
    linear-gradient(180deg, #f7fbff 0%, #ffffff 40%);
  padding: 0.04rem;
}

.hero {
  display: grid;
  grid-template-columns: 1fr minmax(260px, 320px);
  gap: 0.8rem;
  padding: 0.94rem;
  border: 1px solid #d5e3f6;
  border-radius: var(--radius-md);
  background: linear-gradient(120deg, #eff6ff 0%, #f6fbff 62%, #e9f4ff 100%);
  box-shadow: var(--shadow-soft);
  animation: page-enter var(--duration-slow) var(--ease-standard);
}

.hero-kicker {
  margin: 0;
  font-size: var(--text-xs);
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: #426d9f;
}

.hero-title {
  margin: 0.16rem 0 0;
  font-size: 1.42rem;
  color: #173a63;
}

.hero-subtitle {
  margin: 0.38rem 0 0;
  max-width: 58ch;
  font-size: var(--text-sm);
  color: #4f6d8f;
  line-height: 1.5;
}

.hero-meta {
  padding: 0.72rem 0.78rem;
  border-radius: var(--radius-md);
  background: rgba(22, 56, 97, 0.84);
  border: 1px solid rgba(162, 198, 244, 0.4);
  color: #f0f7ff;
  display: grid;
  align-content: center;
  gap: 0.26rem;
}

.error-banner {
  margin: 0;
  padding: 0.48rem 0.6rem;
  border-radius: 0.56rem;
  border: 1px solid color-mix(in srgb, var(--color-danger) 35%, white);
  background: color-mix(in srgb, var(--color-danger) 10%, white);
  color: #9f3545;
  font-size: var(--text-sm);
}

.meta-name {
  margin: 0;
  font-size: var(--text-md);
  font-weight: var(--weight-semibold);
  line-height: 1.45;
}

.meta-id {
  margin: 0;
  font-size: var(--text-xs);
  color: rgba(224, 238, 255, 0.86);
  letter-spacing: 0.04em;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 0.7rem;
}

.stat-card {
  padding: 0.75rem 0.82rem;
  border-radius: var(--radius-md);
  border: 1px solid #d7e5f8;
  box-shadow: 0 8px 18px rgba(29, 67, 127, 0.08);
  background: #f8fbff;
}

.stat-card p {
  margin: 0;
  font-size: var(--text-xs);
  letter-spacing: 0.09em;
  text-transform: uppercase;
}

.stat-card strong {
  display: block;
  margin-top: 0.16rem;
  font-size: var(--text-2xl);
  font-family: var(--font-display);
  line-height: 1;
}

.stat-card--pass p,
.stat-card--pass strong {
  color: #0e7f5c;
}

.stat-card--review p,
.stat-card--review strong {
  color: #9b6508;
}

.stat-card--fail p,
.stat-card--fail strong {
  color: #b33e4f;
}

.stat-card--total p,
.stat-card--total strong {
  color: #325682;
}

.control-panel {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 180px)) minmax(0, 1fr);
  gap: 0.7rem;
  align-items: end;
  padding: 0.74rem;
  border: 1px solid #d9e5f4;
  border-radius: var(--radius-md);
  background: linear-gradient(180deg, #fdfefe 0%, #f6faff 100%);
}

.control-panel label {
  display: grid;
  gap: 0.24rem;
  font-size: var(--text-xs);
  color: #506b88;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}

.control-panel select,
.keyword-field input,
.order-toggle {
  border-radius: 0.58rem;
  border: 1px solid #bfd4ed;
  padding: 0.45rem 0.56rem;
  font-size: var(--text-sm);
  background: #fff;
  color: #264666;
  transition:
    border-color var(--duration-fast) var(--ease-standard),
    box-shadow var(--duration-fast) var(--ease-standard),
    transform var(--duration-fast) var(--ease-standard);
}

.control-panel select:focus-visible,
.keyword-field input:focus-visible,
.order-toggle:focus-visible {
  border-color: #7fb0ea;
  box-shadow: 0 0 0 3px rgba(59, 123, 205, 0.16);
  outline: none;
}

.keyword-field {
  grid-column: span 1;
}

.keyword-field input {
  width: 100%;
  min-width: 0;
}

.order-toggle {
  cursor: pointer;
  font-weight: var(--weight-semibold);
  color: #1f4874;
  background: linear-gradient(180deg, #f4f9ff 0%, #e9f2ff 100%);
}

.order-toggle:hover {
  border-color: #8eb7e5;
  transform: translateY(-1px);
}

@media (max-width: 1100px) {
  .workspace-grid {
    grid-template-columns: 1fr;
  }

  .hero {
    grid-template-columns: 1fr;
  }

  .stats-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .control-panel {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .keyword-field {
    grid-column: span 2;
  }
}

@media (max-width: 720px) {
  .result-panel {
    gap: 0.72rem;
  }

  .stats-grid,
  .control-panel {
    grid-template-columns: 1fr;
  }

  .keyword-field {
    grid-column: span 1;
  }
}
</style>
