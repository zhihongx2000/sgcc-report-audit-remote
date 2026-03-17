<script setup lang="ts">
import { computed, onMounted } from "vue";

import CheckItemTable from "../components/audit/CheckItemTable.vue";
import {
  renderCheckItems,
  type AuditCheckItem,
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

const reportMeta = {
  reportId: "report-20260317-001",
  reportName: "华东区域风光储并网电能质量评估报告",
  collection: "sgcc-default",
  updatedAt: "2026-03-17T17:24:00.000Z",
};

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

function createMockItems(): AuditCheckItem[] {
  const titles = [
    "评估单位资质",
    "报告审批签章",
    "评估依据完整性",
    "用户接入信息",
    "用户设备参数",
    "用户干扰源特性",
    "原始提资资料",
    "电网设备信息",
    "电网容量信息",
    "评估指标覆盖",
    "指标限值选取",
    "背景测试数据",
    "背景与计算叠加",
    "仿真模型与截图",
    "评估考核点",
    "系统运行方式",
    "计算结果说明",
    "评估结论一致性",
    "治理建议有效性",
    "监测建议完整性",
  ];

  const statusPattern: AuditCheckStatus[] = [
    "pass",
    "pass",
    "review",
    "pass",
    "review",
    "pass",
    "fail",
    "pass",
    "review",
    "pass",
    "pass",
    "review",
    "fail",
    "review",
    "pass",
    "pass",
    "review",
    "pass",
    "fail",
    "review",
  ];

  const reasonByStatus: Record<AuditCheckStatus, string> = {
    pass: "已在报告正文中给出明确说明，结论与证据一致。",
    review: "当前证据可支持初步判定，建议补充原始附件后复核。",
    fail: "缺少关键约束或结果不一致，无法满足审查要求。",
  };

  const baseTime = Date.parse(reportMeta.updatedAt);

  return titles.map((title, index) => {
    const checkNumber = index + 1;
    const status = statusPattern[index];
    const checkId = `check-${String(checkNumber).padStart(2, "0")}`;
    return {
      id: checkId,
      title,
      status,
      reason: `${reasonByStatus[status]}（第 ${checkNumber} 项）`,
      evidence: [
        {
          id: `${checkId}-e1`,
          label: "正文段落",
          source: `chapter-${Math.ceil(checkNumber / 3)}.${(checkNumber % 3) + 1}`,
          page: checkNumber + 2,
        },
        {
          id: `${checkId}-e2`,
          label: "附录截图",
          source: `appendix-${String((checkNumber % 5) + 1).padStart(2, "0")}`,
          page: checkNumber + 8,
        },
      ],
      updatedAt: new Date(baseTime - index * 90_000).toISOString(),
    };
  });
}

function toggleSortOrder(): void {
  const nextOrder: SortOrder = store.state.sortOrder === "desc" ? "asc" : "desc";
  store.setSort(store.state.sortField, nextOrder);
}

onMounted(() => {
  if (store.state.items.length === 0) {
    store.setSelectedReportId(reportMeta.reportId);
    store.setItems(createMockItems());
  }
});
</script>

<template>
  <section data-page-id="audit-results" class="audit-result-view">
    <header class="hero">
      <div>
        <p class="hero-kicker">Report Intelligence</p>
        <h1 class="hero-title">20 项审查结果矩阵</h1>
        <p class="hero-subtitle">
          集中展示每一项判定结果、判定说明与证据定位，并支持状态筛选、关键词检索和排序。
        </p>
      </div>
      <div class="hero-meta">
        <p class="meta-name">{{ reportMeta.reportName }}</p>
        <p class="meta-id">{{ reportMeta.reportId }} · {{ reportMeta.collection }}</p>
      </div>
    </header>

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
        <strong>{{ statusStats.fail }}</strong>
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
  </section>
</template>

<style scoped>
.audit-result-view {
  display: grid;
  gap: 1rem;
  background:
    radial-gradient(circle at 95% 0%, rgba(47, 95, 159, 0.16), transparent 32%),
    linear-gradient(180deg, #f7fbff 0%, #ffffff 40%);
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
  .audit-result-view {
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
