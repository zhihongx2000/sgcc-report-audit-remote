<script setup lang="ts">
import { computed } from "vue";

import type { QueryTraceCandidate, QueryTraceRecord } from "../../api/trace";

const props = defineProps<{
	trace: QueryTraceRecord;
}>();

type RerankDeltaRow = QueryTraceCandidate & {
	beforeRank: number | null;
	deltaText: string;
	deltaClass: "up" | "down" | "same" | "new";
};

const rerankDeltaRows = computed<RerankDeltaRow[]>(() => {
	const fusionRankMap = new Map<string, number>();
	for (const item of props.trace.fusionCandidates) {
		fusionRankMap.set(item.docId, item.rank);
	}

	return props.trace.rerankCandidates.map((item) => {
		const beforeRank = fusionRankMap.get(item.docId) ?? null;

		if (beforeRank === null) {
			return {
				...item,
				beforeRank,
				deltaText: "new",
				deltaClass: "new",
			};
		}

		const delta = beforeRank - item.rank;
		if (delta > 0) {
			return {
				...item,
				beforeRank,
				deltaText: `↑${delta}`,
				deltaClass: "up",
			};
		}

		if (delta < 0) {
			return {
				...item,
				beforeRank,
				deltaText: `↓${Math.abs(delta)}`,
				deltaClass: "down",
			};
		}

		return {
			...item,
			beforeRank,
			deltaText: "-",
			deltaClass: "same",
		};
	});
});

function scoreLabel(score: number): string {
	return score.toFixed(3);
}
</script>

<template>
	<section class="trace-detail-panel" data-testid="query-trace-detail-panel">
		<header class="panel-head">
			<h3>召回与重排对比</h3>
			<p>并列查看 dense/sparse 候选、fusion 与 rerank 排名变化。</p>
		</header>

		<div class="candidate-grid">
			<article class="candidate-card" data-testid="query-dense-panel">
				<header>
					<h4>Dense Top-N</h4>
					<span>{{ trace.denseCandidates.length }} 条</span>
				</header>
				<ul>
					<li v-for="item in trace.denseCandidates" :key="`dense-${item.docId}`">
						<span class="rank">#{{ item.rank }}</span>
						<div class="candidate-body">
							<p class="title" :title="item.title">{{ item.title }}</p>
							<p class="meta">{{ item.docId }} · {{ item.source }}</p>
						</div>
						<span class="score">{{ scoreLabel(item.score) }}</span>
					</li>
				</ul>
			</article>

			<article class="candidate-card" data-testid="query-sparse-panel">
				<header>
					<h4>Sparse Top-N</h4>
					<span>{{ trace.sparseCandidates.length }} 条</span>
				</header>
				<ul>
					<li v-for="item in trace.sparseCandidates" :key="`sparse-${item.docId}`">
						<span class="rank">#{{ item.rank }}</span>
						<div class="candidate-body">
							<p class="title" :title="item.title">{{ item.title }}</p>
							<p class="meta">{{ item.docId }} · {{ item.source }}</p>
						</div>
						<span class="score">{{ scoreLabel(item.score) }}</span>
					</li>
				</ul>
			</article>
		</div>

		<div class="candidate-grid">
			<article class="candidate-card" data-testid="query-fusion-panel">
				<header>
					<h4>Fusion 排名</h4>
					<span>{{ trace.fusionCandidates.length }} 条</span>
				</header>
				<ul>
					<li v-for="item in trace.fusionCandidates" :key="`fusion-${item.docId}`">
						<span class="rank">#{{ item.rank }}</span>
						<div class="candidate-body">
							<p class="title" :title="item.title">{{ item.title }}</p>
							<p class="meta">{{ item.docId }} · {{ item.source }}</p>
						</div>
						<span class="score">{{ scoreLabel(item.score) }}</span>
					</li>
				</ul>
			</article>

			<article class="candidate-card" data-testid="query-rerank-panel">
				<header>
					<h4>Rerank 排名</h4>
					<span>{{ trace.rerankCandidates.length }} 条</span>
				</header>
				<ul v-if="rerankDeltaRows.length > 0">
					<li v-for="item in rerankDeltaRows" :key="`rerank-${item.docId}`">
						<span class="rank">#{{ item.rank }}</span>
						<div class="candidate-body">
							<p class="title" :title="item.title">{{ item.title }}</p>
							<p class="meta">
								{{ item.docId }} · before {{ item.beforeRank ?? "-" }}
							</p>
						</div>
						<span class="delta" :class="item.deltaClass">{{ item.deltaText }}</span>
					</li>
				</ul>
				<p v-else class="empty-copy">Rerank 未返回结果，当前使用 fusion 排名。</p>
			</article>
		</div>

		<section class="topk-card" data-testid="query-topk-table">
			<header>
				<h4>最终 Top-K 结果</h4>
				<span>{{ trace.topKResults.length }} 条</span>
			</header>
			<table>
				<thead>
					<tr>
						<th>Rank</th>
						<th>文档</th>
						<th>来源</th>
						<th>分数</th>
					</tr>
				</thead>
				<tbody>
					<tr
						v-for="item in trace.topKResults"
						:key="`topk-${item.docId}`"
						:data-testid="`query-topk-row-${item.rank}`"
					>
						<td>#{{ item.rank }}</td>
						<td>
							<p class="title" :title="item.title">{{ item.title }}</p>
							<p class="meta">{{ item.docId }}</p>
						</td>
						<td>{{ item.source }}</td>
						<td>{{ scoreLabel(item.score) }}</td>
					</tr>
				</tbody>
			</table>
		</section>
	</section>
</template>

<style scoped>
.trace-detail-panel {
	display: grid;
	gap: 0.68rem;
	min-width: 0;
}

.panel-head h3 {
	margin: 0;
	font-size: 1rem;
	color: #1f3d5d;
}

.panel-head p {
	margin: 0.12rem 0 0;
	font-size: 0.78rem;
	color: #4f6d8c;
}

.candidate-grid {
	display: grid;
	grid-template-columns: repeat(2, minmax(0, 1fr));
	gap: 0.6rem;
	min-width: 0;
}

.candidate-card {
	border-radius: 11px;
	border: 1px solid color-mix(in srgb, var(--color-border-strong) 75%, white);
	background:
		linear-gradient(180deg, #ffffff 0%, #eef5ff 100%),
		radial-gradient(circle at 88% 0%, rgba(36, 184, 203, 0.15) 0, transparent 42%);
	padding: 0.62rem;
	min-width: 0;
}

.candidate-card > header {
	display: flex;
	justify-content: space-between;
	align-items: baseline;
	margin-bottom: 0.48rem;
	gap: 0.4rem;
}

.candidate-card h4,
.topk-card h4 {
	margin: 0;
	font-size: 0.84rem;
	color: #1d3c5f;
}

.candidate-card > header span,
.topk-card > header span {
	font-size: 0.72rem;
	color: #557595;
}

.candidate-card ul {
	list-style: none;
	margin: 0;
	padding: 0;
	display: grid;
	gap: 0.4rem;
}

.candidate-card li {
	display: grid;
	grid-template-columns: auto 1fr auto;
	gap: 0.45rem;
	align-items: center;
	min-width: 0;
	padding: 0.36rem 0.4rem;
	border-radius: 8px;
	background: rgba(255, 255, 255, 0.72);
	border: 1px solid rgba(95, 145, 189, 0.26);
}

.rank {
	font-size: 0.72rem;
	font-weight: var(--weight-bold);
	color: #1f5d8f;
}

.candidate-body {
	min-width: 0;
}

.title {
	margin: 0;
	font-size: 0.78rem;
	font-weight: var(--weight-semibold);
	color: #24405f;
	white-space: nowrap;
	overflow: hidden;
	text-overflow: ellipsis;
}

.meta {
	margin: 0.1rem 0 0;
	font-size: 0.7rem;
	color: #5a7695;
	white-space: nowrap;
	overflow: hidden;
	text-overflow: ellipsis;
}

.score,
.delta {
	font-size: 0.72rem;
	font-weight: var(--weight-semibold);
	white-space: nowrap;
}

.delta.up {
	color: #0f7a55;
}

.delta.down {
	color: #9e3d4a;
}

.delta.same {
	color: #45698d;
}

.delta.new {
	color: #1f7d95;
}

.empty-copy {
	margin: 0;
	font-size: 0.76rem;
	color: #5a7694;
}

.topk-card {
	border-radius: 11px;
	border: 1px solid color-mix(in srgb, var(--color-accent) 38%, white);
	background:
		linear-gradient(180deg, #ffffff 0%, #ebf9ff 100%),
		repeating-linear-gradient(
			90deg,
			rgba(35, 125, 144, 0.06) 0,
			rgba(35, 125, 144, 0.06) 1px,
			transparent 1px,
			transparent 15px
		);
	padding: 0.62rem;
	overflow: auto;
}

.topk-card > header {
	display: flex;
	justify-content: space-between;
	align-items: baseline;
	gap: 0.4rem;
	margin-bottom: 0.45rem;
}

table {
	width: 100%;
	border-collapse: collapse;
	min-width: 600px;
}

th,
td {
	font-size: 0.76rem;
	text-align: left;
	padding: 0.36rem 0.3rem;
	border-bottom: 1px solid rgba(113, 158, 197, 0.28);
	vertical-align: top;
}

th {
	color: #4e6d8f;
	font-weight: var(--weight-semibold);
	text-transform: uppercase;
	letter-spacing: 0.04em;
	font-size: 0.68rem;
}

@media (max-width: 900px) {
	.candidate-grid {
		grid-template-columns: 1fr;
	}
}
</style>
