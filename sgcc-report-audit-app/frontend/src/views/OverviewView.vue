<script setup lang="ts">
const componentConfigCards = [
  { title: "LLM", value: "azure / gpt-4o", detail: "provider + model" },
  {
    title: "Embedding",
    value: "openai / text-embedding-3-small / 1536",
    detail: "provider + model + dim",
  },
  {
    title: "Splitter",
    value: "recursive_character / chunk_size=1000 / overlap=150",
    detail: "type + chunk_size + overlap",
  },
  {
    title: "Reranker",
    value: "cross_encoder / bge-reranker-v2-m3",
    detail: "backend + model",
  },
  { title: "Evaluator", value: "ragas, custom", detail: "enabled backends" },
];

const collectionStats = [
  { name: "default", documents: 42, chunks: 1896, images: 117 },
  { name: "sgcc-samples", documents: 16, chunks: 724, images: 54 },
  { name: "eval", documents: 8, chunks: 301, images: 11 },
];

const healthMetrics = [
  {
    title: "最近 Ingestion Trace",
    value: "2026-03-16 14:58:42",
    sub: "总耗时 23.8s",
  },
  {
    title: "最近 Query Trace",
    value: "2026-03-16 15:08:11",
    sub: "总耗时 1.42s",
  },
  {
    title: "Trace 存储状态",
    value: "PostgreSQL + JSONL 镜像",
    sub: "obs_traces / obs_trace_stages",
  },
];

const totalDocuments = collectionStats.reduce(
  (acc, item) => acc + item.documents,
  0,
);
const totalChunks = collectionStats.reduce((acc, item) => acc + item.chunks, 0);
const totalImages = collectionStats.reduce((acc, item) => acc + item.images, 0);
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
        <span>文档 {{ totalDocuments }}</span>
        <span>Chunk {{ totalChunks }}</span>
        <span>图片 {{ totalImages }}</span>
      </div>
    </header>

    <article class="panel-card">
      <header class="panel-head">
        <h2>组件配置卡片</h2>
        <p>读取 Settings 的可插拔组件状态</p>
      </header>
      <div class="config-grid">
        <div
          v-for="item in componentConfigCards"
          :key="item.title"
          class="config-card"
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
  color: #203652;
}

.hero-head p {
  margin: 0.28rem 0 0;
  font-size: 0.9rem;
  color: #627892;
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
  border: 1px solid #c6d8f6;
  background: #ecf4ff;
  color: #284f86;
}

.panel-card {
  border: 1px solid #e2e9f4;
  border-radius: 12px;
  background: #ffffff;
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
  color: #233a56;
}

.panel-head p {
  margin: 0;
  font-size: 0.78rem;
  color: #70859f;
}

.config-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 0.6rem;
}

.config-card {
  padding: 0.72rem;
  border: 1px solid #e4ebf7;
  border-radius: 10px;
  background: linear-gradient(180deg, #fbfdff 0%, #f3f8ff 100%);
}

.config-title {
  margin: 0;
  font-size: 0.8rem;
  font-weight: 700;
  color: #30507a;
}

.config-value {
  margin: 0.26rem 0 0;
  font-size: 0.86rem;
  font-weight: 600;
  color: #253b58;
  line-height: 1.35;
  word-break: break-word;
}

.config-detail {
  margin: 0.28rem 0 0;
  font-size: 0.75rem;
  color: #6d829d;
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
  color: #2b405e;
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
  color: #244061;
}

.health-sub {
  margin: 0.2rem 0 0;
  font-size: 0.76rem;
  color: #7388a2;
}

@media (max-width: 1120px) {
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
