<script setup lang="ts">
import { computed, ref } from "vue";

import { runEvaluation } from "../api/trace";
import { useAppStore } from "../stores/app";

const appStore = useAppStore();

const selectedEvaluator = ref<"ragas" | "custom" | "all">("all");
const selectedDataset = ref("golden_set.jsonl");

const panelEnabled = computed(() => appStore.state.evaluationEnabled);
const runs = computed(() => appStore.state.evaluationRuns);
const isRunning = computed(() => appStore.state.isEvaluationRunning);
const errorMessage = computed(() => appStore.state.evaluationErrorMessage);

const latestRun = computed(() => runs.value[0] ?? null);

const trendRows = computed(() => runs.value.slice(0, 6));

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

function scorePercent(value: number): string {
  return `${Math.round(Math.max(0, Math.min(1, value)) * 100)}%`;
}

function scoreLabel(value: number): string {
  return value.toFixed(3);
}

function enablePanel(): void {
  appStore.setEvaluationEnabled(true);
}

async function triggerEvaluation(): Promise<void> {
  appStore.setEvaluationRunning(true);
  appStore.setEvaluationErrorMessage(null);

  try {
    const result = await runEvaluation({
      evaluator: selectedEvaluator.value,
      dataset: selectedDataset.value,
    });
    appStore.appendEvaluationRun(result);
  } catch (error) {
    appStore.setEvaluationErrorMessage(
      error instanceof Error ? error.message : "评估执行失败",
    );
  } finally {
    appStore.setEvaluationRunning(false);
  }
}
</script>

<template>
  <section class="evaluation-panel-view" data-page-id="evaluation" data-testid="evaluation-view">
    <header class="hero-head">
      <div>
        <p class="hero-kicker">Evaluation Panel</p>
        <h1>评估面板</h1>
        <p>用于运行 RAG 质量评估并观察 hit_rate、MRR、faithfulness 的变化趋势。</p>
      </div>
      <div class="hero-pills">
        <span>运行次数 {{ runs.length }}</span>
        <span v-if="latestRun">最近耗时 {{ formatDuration(latestRun.durationMs) }}</span>
        <span v-else>最近耗时 -</span>
      </div>
    </header>

    <article
      v-if="!panelEnabled"
      class="disabled-state"
      data-testid="evaluation-disabled-state"
    >
      <h2>评估模块尚未启用</h2>
      <p>
        当前处于占位模式。启用后可手动触发评估，并展示指标表格与趋势占位容器。
      </p>
      <button
        type="button"
        class="enable-btn"
        data-testid="evaluation-enable-button"
        @click="enablePanel"
      >
        启用评估面板
      </button>
    </article>

    <template v-else>
      <section class="panel-card controls-panel" data-testid="evaluation-enabled-panel">
        <header>
          <h2>评估运行控制</h2>
          <p>选择评估器与数据集后触发运行。</p>
        </header>

        <div class="control-grid">
          <label>
            <span>Evaluator</span>
            <select v-model="selectedEvaluator" data-testid="evaluation-evaluator-select">
              <option value="all">all</option>
              <option value="ragas">ragas</option>
              <option value="custom">custom</option>
            </select>
          </label>

          <label>
            <span>Dataset</span>
            <select v-model="selectedDataset" data-testid="evaluation-dataset-select">
              <option value="golden_set.jsonl">golden_set.jsonl</option>
              <option value="golden_set-lite.jsonl">golden_set-lite.jsonl</option>
            </select>
          </label>

          <button
            type="button"
            class="run-btn"
            data-testid="evaluation-run-button"
            :disabled="isRunning"
            @click="void triggerEvaluation()"
          >
            {{ isRunning ? "评估中..." : "运行评估" }}
          </button>
        </div>

        <p v-if="errorMessage" class="error-banner" role="alert">{{ errorMessage }}</p>
      </section>

      <section class="panel-card metrics-panel">
        <header>
          <h2>指标表格</h2>
          <p>展示每次评估的核心指标。</p>
        </header>

        <div class="table-wrap" data-testid="evaluation-metrics-table">
          <table>
            <thead>
              <tr>
                <th>Run</th>
                <th>Evaluator</th>
                <th>Dataset</th>
                <th>Hit Rate</th>
                <th>MRR</th>
                <th>Faithfulness</th>
                <th>Duration</th>
                <th>Started At</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="run in runs"
                :key="run.runId"
                :data-testid="`evaluation-run-${run.runId}`"
              >
                <td>{{ run.runId }}</td>
                <td>{{ run.evaluator }}</td>
                <td>{{ run.dataset }}</td>
                <td>{{ scoreLabel(run.metrics.hitRate) }}</td>
                <td>{{ scoreLabel(run.metrics.mrr) }}</td>
                <td>{{ scoreLabel(run.metrics.faithfulness) }}</td>
                <td>{{ formatDuration(run.durationMs) }}</td>
                <td>{{ formatDateTime(run.startedAt) }}</td>
              </tr>
              <tr v-if="runs.length === 0">
                <td colspan="8" class="empty-row">暂无评估记录，点击“运行评估”生成首条结果。</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <section class="panel-card trend-panel" data-testid="evaluation-trend-placeholder">
        <header>
          <h2>趋势占位容器</h2>
          <p>为后续趋势图组件预留，当前展示最近评估的指标条。</p>
        </header>

        <ul class="trend-list">
          <li v-for="run in trendRows" :key="`trend-${run.runId}`">
            <p class="trend-title">{{ run.runId }}</p>
            <div class="trend-bars">
              <div>
                <span>hit_rate</span>
                <b :style="{ width: scorePercent(run.metrics.hitRate) }" />
              </div>
              <div>
                <span>mrr</span>
                <b :style="{ width: scorePercent(run.metrics.mrr) }" />
              </div>
              <div>
                <span>faithfulness</span>
                <b :style="{ width: scorePercent(run.metrics.faithfulness) }" />
              </div>
            </div>
          </li>
        </ul>

        <p v-if="trendRows.length === 0" class="empty-hint">暂无趋势数据。</p>
      </section>
    </template>
  </section>
</template>

<style scoped>
.evaluation-panel-view {
  display: grid;
  gap: 0.95rem;
  animation: page-enter 280ms var(--ease-standard);
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

.panel-card,
.disabled-state {
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
}

.panel-card > header {
  margin-bottom: 0.72rem;
}

.panel-card h2,
.disabled-state h2 {
  margin: 0;
  font-size: 1.05rem;
  color: var(--color-brand-900);
}

.panel-card p,
.disabled-state p {
  margin: 0.2rem 0 0;
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}

.enable-btn,
.run-btn {
  border: 1px solid var(--color-border-strong);
  border-radius: var(--radius-pill);
  padding: 0.42rem 0.84rem;
  font-size: 0.78rem;
  font-weight: var(--weight-semibold);
  color: var(--color-brand-900);
  background: color-mix(in srgb, var(--color-brand-200) 44%, white);
  cursor: pointer;
  transition:
    transform var(--duration-fast) var(--ease-standard),
    box-shadow var(--duration-fast) var(--ease-standard);
}

.enable-btn {
  margin-top: 0.65rem;
}

.enable-btn:hover,
.run-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 12px rgba(31, 75, 129, 0.15);
}

.run-btn:disabled {
  cursor: not-allowed;
  opacity: 0.7;
  transform: none;
}

.control-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.56rem;
  align-items: end;
}

.control-grid label {
  display: grid;
  gap: 0.28rem;
}

.control-grid span {
  font-size: 0.73rem;
  color: #587493;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.control-grid select {
  border-radius: 0.66rem;
  border: 1px solid var(--color-border-strong);
  padding: 0.38rem 0.5rem;
  background: rgba(255, 255, 255, 0.84);
  color: #254666;
}

.error-banner {
  margin: 0.6rem 0 0;
  padding: 0.46rem 0.6rem;
  border-radius: 0.55rem;
  border: 1px solid color-mix(in srgb, var(--color-danger) 42%, white);
  background: color-mix(in srgb, var(--color-danger) 10%, white);
  color: #9f3545;
}

.table-wrap {
  overflow: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  min-width: 760px;
}

th,
td {
  font-size: 0.75rem;
  text-align: left;
  padding: 0.38rem 0.34rem;
  border-bottom: 1px solid rgba(113, 158, 197, 0.28);
}

th {
  font-size: 0.68rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: #4e6d8f;
}

.empty-row {
  color: #547390;
}

.trend-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  gap: 0.5rem;
}

.trend-list li {
  border-radius: 10px;
  border: 1px solid color-mix(in srgb, var(--color-border-strong) 70%, white);
  background: color-mix(in srgb, var(--color-bg-panel) 95%, var(--color-brand-200));
  padding: 0.5rem;
}

.trend-title {
  margin: 0;
  font-size: 0.76rem;
  font-weight: var(--weight-semibold);
  color: #264463;
}

.trend-bars {
  margin-top: 0.3rem;
  display: grid;
  gap: 0.24rem;
}

.trend-bars > div {
  display: grid;
  grid-template-columns: 84px 1fr;
  align-items: center;
  gap: 0.4rem;
}

.trend-bars span {
  font-size: 0.7rem;
  color: #587493;
}

.trend-bars b {
  display: block;
  height: 0.42rem;
  border-radius: var(--radius-pill);
  background: linear-gradient(90deg, var(--color-brand-700) 0%, var(--color-accent) 100%);
}

.empty-hint {
  margin: 0;
  font-size: 0.8rem;
  color: #55718f;
}

@media (max-width: 900px) {
  .control-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 720px) {
  .hero-head {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
