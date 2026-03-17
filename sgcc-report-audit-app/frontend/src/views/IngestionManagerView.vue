<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from "vue";

import {
  listIngestionTasks,
  retryTask,
  startIngestion,
  type IngestionTaskRecord,
} from "../api/documents";
import { useAppStore } from "../stores/app";

type InputMode = "path" | "upload";

const appStore = useAppStore();

const inputMode = ref<InputMode>("path");
const sourcePathInput = ref("");
const uploadFileName = ref("");
const selectedCollection = ref("sgcc-default");
const submitErrorMessage = ref<string | null>(null);
const pendingTaskKey = ref<string | null>(null);
const lastSubmittedSource = ref("-");

const collectionOptions = ["sgcc-default", "sgcc-archive", "sgcc-samples"];

let refreshTimer: ReturnType<typeof setInterval> | null = null;

const tasks = computed(() => appStore.state.ingestionTasks);

const runningCount = computed(
  () =>
    tasks.value.filter((item) => item.status === "running" || item.status === "queued")
      .length,
);

const failedCount = computed(
  () => tasks.value.filter((item) => item.status === "failed").length,
);

const doneCount = computed(
  () => tasks.value.filter((item) => item.status === "done").length,
);

const canSubmit = computed(() => {
  if (pendingTaskKey.value !== null) {
    return false;
  }

  if (inputMode.value === "path") {
    return sourcePathInput.value.trim().length > 0;
  }

  return uploadFileName.value.trim().length > 0;
});

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

function statusLabel(status: IngestionTaskRecord["status"]): string {
  if (status === "queued") {
    return "排队中";
  }
  if (status === "running") {
    return "运行中";
  }
  if (status === "done") {
    return "完成";
  }
  return "失败";
}

function modeLabel(mode: IngestionTaskRecord["inputMode"]): string {
  return mode === "upload" ? "文件上传" : "路径输入";
}

function onFileChange(event: Event): void {
  const target = event.target as HTMLInputElement;
  uploadFileName.value = target.files?.[0]?.name ?? "";
}

function setInputMode(mode: InputMode): void {
  inputMode.value = mode;
  submitErrorMessage.value = null;
}

async function refreshTasks(showLoading: boolean): Promise<void> {
  if (showLoading) {
    appStore.setIngestionLoading(true);
  }

  try {
    const next = await listIngestionTasks();
    appStore.setIngestionTasks(next);
    appStore.setIngestionErrorMessage(null);
  } catch (error) {
    const message = error instanceof Error ? error.message : "摄取任务加载失败";
    appStore.setIngestionErrorMessage(message);
  } finally {
    if (showLoading) {
      appStore.setIngestionLoading(false);
    }
  }
}

async function submitIngestionTask(): Promise<void> {
  submitErrorMessage.value = null;

  const byPath = sourcePathInput.value.trim();
  const byUpload = uploadFileName.value.trim();

  if (inputMode.value === "path" && byPath.length === 0) {
    submitErrorMessage.value = "请输入文档路径后再启动摄取任务。";
    return;
  }

  if (inputMode.value === "upload" && byUpload.length === 0) {
    submitErrorMessage.value = "请先选择本地文件后再启动摄取任务。";
    return;
  }

  pendingTaskKey.value = "submit";
  try {
    const created = await startIngestion({
      sourcePath: inputMode.value === "path" ? byPath : undefined,
      fileName: inputMode.value === "upload" ? byUpload : undefined,
      collection: selectedCollection.value,
    });

    appStore.upsertIngestionTask(created);
    lastSubmittedSource.value = created.sourcePath;

    if (inputMode.value === "path") {
      sourcePathInput.value = "";
    } else {
      uploadFileName.value = "";
    }

    await refreshTasks(false);
  } catch (error) {
    submitErrorMessage.value =
      error instanceof Error ? error.message : "任务启动失败，请稍后重试";
  } finally {
    pendingTaskKey.value = null;
  }
}

async function retryFailedTask(taskId: string): Promise<void> {
  pendingTaskKey.value = taskId;
  submitErrorMessage.value = null;

  try {
    const retried = await retryTask(taskId);
    appStore.upsertIngestionTask(retried);
    await refreshTasks(false);
  } catch (error) {
    submitErrorMessage.value =
      error instanceof Error ? error.message : "重试失败，请稍后重试";
  } finally {
    pendingTaskKey.value = null;
  }
}

onMounted(() => {
  void refreshTasks(true);
  refreshTimer = setInterval(() => {
    void refreshTasks(false);
  }, 4200);
});

onUnmounted(() => {
  if (refreshTimer !== null) {
    clearInterval(refreshTimer);
    refreshTimer = null;
  }
});
</script>

<template>
  <section class="ingestion-manager-view" data-page-id="ingestion-manager" data-testid="ingestion-manager-view">
    <header class="hero-head">
      <div>
        <p class="hero-kicker">Ingestion Manager</p>
        <h1>摄取管理</h1>
        <p>以任务队列方式统一管理文档摄取，支持路径输入、上传触发、进度跟踪与失败重试。</p>
      </div>
      <div class="hero-pills">
        <span data-testid="ingestion-running-count">运行中 {{ runningCount }}</span>
        <span data-testid="ingestion-failed-count">失败 {{ failedCount }}</span>
        <span data-testid="ingestion-done-count">完成 {{ doneCount }}</span>
      </div>
    </header>

    <p v-if="submitErrorMessage" class="error-banner" role="alert">{{ submitErrorMessage }}</p>
    <p v-if="appStore.state.ingestionErrorMessage" class="error-banner" role="alert">
      {{ appStore.state.ingestionErrorMessage }}
    </p>

    <div class="manager-grid">
      <article class="panel-card control-panel">
        <header>
          <h2>任务发起</h2>
          <p data-testid="ingestion-last-submission">最近提交：{{ lastSubmittedSource }}</p>
        </header>

        <div class="mode-switch" role="tablist" aria-label="摄取输入模式">
          <button
            type="button"
            class="mode-btn"
            :class="{ 'is-active': inputMode === 'path' }"
            data-testid="ingestion-mode-path"
            @click="setInputMode('path')"
          >
            路径输入
          </button>
          <button
            type="button"
            class="mode-btn"
            :class="{ 'is-active': inputMode === 'upload' }"
            data-testid="ingestion-mode-upload"
            @click="setInputMode('upload')"
          >
            本地上传
          </button>
        </div>

        <label v-if="inputMode === 'path'" class="field">
          <span>文档路径</span>
          <input
            v-model="sourcePathInput"
            data-testid="ingestion-path-input"
            type="text"
            placeholder="/data/documents/sgcc-default/your-report.pdf"
          />
        </label>

        <label v-else class="field">
          <span>本地文件</span>
          <input data-testid="ingestion-upload-input" type="file" @change="onFileChange" />
          <small>{{ uploadFileName || "尚未选择文件" }}</small>
        </label>

        <label class="field">
          <span>目标集合</span>
          <select v-model="selectedCollection" data-testid="ingestion-collection-select">
            <option v-for="collection in collectionOptions" :key="collection" :value="collection">
              {{ collection }}
            </option>
          </select>
        </label>

        <button
          type="button"
          class="primary-btn"
          data-testid="ingestion-start-button"
          :disabled="!canSubmit"
          @click="void submitIngestionTask()"
        >
          启动摄取任务
        </button>
      </article>

      <article class="panel-card queue-panel">
        <header>
          <h2>任务队列</h2>
          <p v-if="appStore.state.ingestionRefreshedAtIso">
            更新于 {{ formatDateTime(appStore.state.ingestionRefreshedAtIso) }}
          </p>
        </header>

        <p v-if="appStore.state.isIngestionLoading" class="loading-hint">正在同步摄取任务...</p>

        <ul class="task-list" data-testid="ingestion-task-list">
          <li v-for="task in tasks" :key="task.taskId" class="task-item" :data-testid="`ingestion-task-${task.taskId}`">
            <div class="task-head">
              <p>{{ task.taskId }}</p>
              <span class="status-pill" :class="`status-${task.status}`" :data-testid="`ingestion-status-${task.taskId}`">
                {{ statusLabel(task.status) }}
              </span>
            </div>

            <p class="task-source">{{ task.sourcePath }}</p>

            <div class="progress-track" role="progressbar" :aria-valuenow="task.progressPercent" aria-valuemin="0" aria-valuemax="100">
              <span :style="{ width: `${task.progressPercent}%` }" />
            </div>
            <p class="progress-meta" :data-testid="`ingestion-progress-${task.taskId}`">
              进度 {{ task.progressPercent }}%
            </p>

            <div class="task-meta">
              <span>{{ task.collection }}</span>
              <span>{{ modeLabel(task.inputMode) }}</span>
              <span>{{ formatDateTime(task.startedAt) }}</span>
            </div>

            <p v-if="task.errorMessage" class="task-error">{{ task.errorMessage }}</p>

            <div class="task-actions">
              <button
                v-if="task.status === 'failed'"
                type="button"
                class="retry-btn"
                :data-testid="`ingestion-retry-${task.taskId}`"
                :disabled="pendingTaskKey === task.taskId"
                @click="void retryFailedTask(task.taskId)"
              >
                失败重试
              </button>
            </div>
          </li>
        </ul>
      </article>
    </div>
  </section>
</template>

<style scoped>
.ingestion-manager-view {
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
  color: #557798;
}

.hero-head h1 {
  margin: 0.1rem 0 0;
  font-size: 1.68rem;
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
  padding: 0.34rem 0.7rem;
  border-radius: var(--radius-pill);
  border: 1px solid var(--color-border-strong);
  background: color-mix(in srgb, var(--color-brand-300) 23%, white);
  color: var(--color-brand-900);
  font-size: var(--text-xs);
  font-weight: var(--weight-semibold);
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

.manager-grid {
  display: grid;
  grid-template-columns: minmax(280px, 0.88fr) minmax(0, 1.12fr);
  gap: 0.95rem;
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
}

.panel-card header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 0.8rem;
  margin-bottom: 0.72rem;
}

.panel-card h2 {
  margin: 0;
  font-size: 1.04rem;
  color: var(--color-brand-900);
}

.panel-card p {
  margin: 0;
  color: var(--color-text-secondary);
  font-size: var(--text-sm);
}

.control-panel {
  display: grid;
  gap: 0.68rem;
  align-content: start;
}

.mode-switch {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0.45rem;
}

.mode-btn {
  border: 1px solid var(--color-border-strong);
  background: #f4f8ff;
  border-radius: 0.66rem;
  padding: 0.48rem;
  color: #2d4f74;
  font-weight: var(--weight-semibold);
  transition:
    border-color var(--duration-normal) var(--ease-standard),
    transform var(--duration-fast) var(--ease-standard),
    background-color var(--duration-fast) var(--ease-standard);
}

.mode-btn:hover {
  transform: translateY(-1px);
  border-color: #93bbe8;
}

.mode-btn.is-active {
  background: linear-gradient(90deg, #dbe9fd 0%, #ebf3ff 100%);
  border-color: #7ca9dc;
  box-shadow: inset 0 0 0 1px rgba(76, 126, 184, 0.15);
}

.field {
  display: grid;
  gap: 0.32rem;
  font-size: var(--text-sm);
  color: #355779;
}

.field input,
.field select {
  border: 1px solid var(--color-border-strong);
  border-radius: 0.62rem;
  padding: 0.5rem 0.58rem;
  background: #ffffff;
  color: var(--color-text-primary);
}

.field small {
  color: #5f7895;
}

.primary-btn {
  border: none;
  border-radius: 0.68rem;
  padding: 0.58rem 0.8rem;
  background: linear-gradient(92deg, #2462a8 0%, #1b467f 100%);
  color: #f3f8ff;
  font-weight: var(--weight-semibold);
  cursor: pointer;
  transition:
    transform var(--duration-fast) var(--ease-standard),
    box-shadow var(--duration-fast) var(--ease-standard),
    opacity var(--duration-fast) var(--ease-standard);
}

.primary-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 10px 20px rgba(21, 57, 102, 0.24);
}

.primary-btn:disabled {
  opacity: 0.48;
  cursor: not-allowed;
}

.queue-panel {
  display: grid;
  gap: 0.58rem;
}

.loading-hint {
  margin: 0;
  font-size: var(--text-sm);
  color: #4f7399;
}

.task-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  gap: 0.54rem;
  max-height: 520px;
  overflow-y: auto;
}

.task-item {
  border: 1px solid #d9e6f6;
  border-radius: 10px;
  padding: 0.66rem;
  background: linear-gradient(180deg, #fbfdff 0%, #f2f7ff 100%);
}

.task-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.6rem;
}

.task-head p {
  margin: 0;
  font-size: var(--text-sm);
  color: #2a4666;
  font-weight: var(--weight-semibold);
}

.status-pill {
  padding: 0.18rem 0.52rem;
  border-radius: var(--radius-pill);
  font-size: var(--text-xs);
  font-weight: var(--weight-bold);
}

.status-queued,
.status-running {
  background: color-mix(in srgb, var(--color-accent) 24%, white);
  color: #0f6172;
}

.status-done {
  background: color-mix(in srgb, var(--color-success) 24%, white);
  color: #13664d;
}

.status-failed {
  background: color-mix(in srgb, var(--color-danger) 22%, white);
  color: #9d3042;
}

.task-source {
  margin: 0.34rem 0 0;
  font-size: var(--text-sm);
  color: #2d4a6d;
  word-break: break-word;
}

.progress-track {
  margin-top: 0.46rem;
  height: 8px;
  border-radius: 999px;
  background: #d9e7f8;
  overflow: hidden;
}

.progress-track span {
  display: block;
  height: 100%;
  background: linear-gradient(90deg, #1f4e8c 0%, #1ea5ba 100%);
  transition: width var(--duration-normal) var(--ease-standard);
}

.progress-meta {
  margin: 0.3rem 0 0;
  font-size: var(--text-xs);
  color: #42658a;
}

.task-meta {
  margin-top: 0.3rem;
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  font-size: var(--text-xs);
  color: #60748f;
}

.task-error {
  margin-top: 0.36rem;
  padding: 0.34rem 0.44rem;
  border-radius: 0.5rem;
  background: color-mix(in srgb, var(--color-danger) 10%, white);
  color: #9f3545;
  font-size: var(--text-xs);
}

.task-actions {
  margin-top: 0.44rem;
  display: flex;
  justify-content: flex-end;
}

.retry-btn {
  border: 1px solid #d58d99;
  border-radius: 0.58rem;
  background: #fff5f6;
  color: #97394a;
  font-size: var(--text-xs);
  font-weight: var(--weight-semibold);
  padding: 0.34rem 0.56rem;
  cursor: pointer;
}

.retry-btn:hover:not(:disabled) {
  border-color: #c96e7f;
  background: #ffe9ec;
}

.retry-btn:disabled {
  opacity: 0.52;
  cursor: not-allowed;
}

@media (max-width: 980px) {
  .manager-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 700px) {
  .hero-head {
    flex-direction: column;
    align-items: flex-start;
  }

  .hero-pills {
    width: 100%;
  }

  .hero-pills span {
    flex: 1;
    text-align: center;
  }
}
</style>
