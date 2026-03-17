<script setup lang="ts">
import { computed } from "vue";

import type { IngestionTraceStage } from "../../api/trace";

const props = withDefaults(
	defineProps<{
		stages: IngestionTraceStage[];
		selectedStageKey?: string | null;
	}>(),
	{
		selectedStageKey: null,
	},
);

const emit = defineEmits<{
	(event: "select", stage: IngestionTraceStage): void;
}>();

const totalDuration = computed(() =>
	Math.max(
		1,
		props.stages.reduce((sum, stage) => sum + stage.durationMs, 0),
	),
);

const waterfallBars = computed(() => {
	let offset = 0;
	return props.stages.map((stage) => {
		const widthPercent = (stage.durationMs / totalDuration.value) * 100;
		const offsetPercent = (offset / totalDuration.value) * 100;
		offset += stage.durationMs;
		return {
			stage,
			widthPercent,
			offsetPercent,
			percentOfTotal: (stage.durationMs / totalDuration.value) * 100,
		};
	});
});

function handleSelect(stage: IngestionTraceStage): void {
	emit("select", stage);
}
</script>

<template>
	<section class="waterfall-chart" data-testid="waterfall-chart" aria-label="Ingestion stage waterfall chart">
		<header class="chart-head">
			<h2>阶段耗时瀑布图</h2>
			<p>点击阶段查看 method/provider 与输入输出明细</p>
		</header>

		<ul class="waterfall-list">
			<li v-for="(item, index) in waterfallBars" :key="item.stage.key" class="stage-item">
				<button
					type="button"
					class="stage-button"
					:class="[
						`status-${item.stage.status}`,
						{ 'is-selected': selectedStageKey === item.stage.key },
					]"
					:data-testid="`waterfall-stage-${item.stage.key}`"
					@click="handleSelect(item.stage)"
				>
					<div class="stage-line">
						<span class="stage-index">{{ index + 1 }}</span>
						<span class="stage-name">{{ item.stage.name }}</span>
						<span class="stage-time">{{ item.stage.durationMs }}ms · {{ item.percentOfTotal.toFixed(1) }}%</span>
					</div>
					<span class="stage-track">
						<span
							class="stage-fill"
							:style="{
								'--bar-offset': `${item.offsetPercent}%`,
								'--bar-width': `${item.widthPercent}%`,
							}"
						/>
					</span>
				</button>
			</li>
		</ul>
	</section>
</template>

<style scoped>
.waterfall-chart {
	display: grid;
	gap: 0.72rem;
	padding: 0.8rem;
	border-radius: 14px;
	border: 1px solid color-mix(in srgb, var(--color-brand-300) 40%, white);
	background:
		linear-gradient(180deg, #ffffff 0%, #f4f8ff 100%),
		repeating-linear-gradient(
			90deg,
			rgba(31, 87, 147, 0.04) 0,
			rgba(31, 87, 147, 0.04) 1px,
			transparent 1px,
			transparent 16px
		);
	box-shadow: 0 12px 24px rgba(17, 49, 92, 0.09);
}

.chart-head h2 {
	margin: 0;
	font-size: 1.05rem;
	color: var(--color-brand-900);
}

.chart-head p {
	margin: 0.14rem 0 0;
	font-size: var(--text-sm);
	color: var(--color-text-secondary);
}

.waterfall-list {
	margin: 0;
	padding: 0;
	list-style: none;
	display: grid;
	gap: 0.48rem;
}

.stage-button {
	width: 100%;
	display: grid;
	gap: 0.3rem;
	padding: 0.48rem 0.52rem;
	border-radius: 10px;
	border: 1px solid color-mix(in srgb, var(--color-border-strong) 70%, white);
	background: color-mix(in srgb, var(--color-bg-panel) 96%, var(--color-brand-200));
	cursor: pointer;
	text-align: left;
	transition:
		transform var(--duration-fast) var(--ease-standard),
		border-color var(--duration-normal) var(--ease-standard),
		box-shadow var(--duration-normal) var(--ease-standard);
}

.stage-button:hover {
	transform: translateY(-1px);
	border-color: color-mix(in srgb, var(--color-brand-700) 50%, white);
	box-shadow: 0 7px 14px rgba(23, 63, 117, 0.14);
}

.stage-button.is-selected {
	border-color: var(--color-accent);
	box-shadow: 0 0 0 1px color-mix(in srgb, var(--color-accent) 38%, transparent);
}

.stage-line {
	display: grid;
	grid-template-columns: auto 1fr auto;
	gap: 0.4rem;
	align-items: center;
	min-width: 0;
}

.stage-index {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	width: 1.2rem;
	height: 1.2rem;
	border-radius: 50%;
	font-size: 0.72rem;
	font-weight: var(--weight-bold);
	background: color-mix(in srgb, var(--color-brand-300) 40%, white);
	color: var(--color-brand-900);
}

.stage-name {
	min-width: 0;
	font-size: var(--text-sm);
	font-weight: var(--weight-semibold);
	color: #24405e;
	white-space: nowrap;
	overflow: hidden;
	text-overflow: ellipsis;
}

.stage-time {
	font-size: 0.73rem;
	color: #4c6787;
	white-space: nowrap;
}

.stage-track {
	position: relative;
	height: 0.55rem;
	border-radius: var(--radius-pill);
	background: linear-gradient(
		90deg,
		rgba(45, 85, 132, 0.08) 0%,
		rgba(45, 85, 132, 0.12) 100%
	);
	overflow: hidden;
}

.stage-fill {
	position: absolute;
	inset-block: 0;
	left: var(--bar-offset);
	width: var(--bar-width);
	border-radius: var(--radius-pill);
	background: linear-gradient(
		90deg,
		var(--color-brand-700) 0%,
		var(--color-accent) 100%
	);
	box-shadow: 0 0 0 1px rgba(29, 85, 138, 0.16);
	animation: stage-grow 420ms var(--ease-standard);
	transform-origin: left;
}

.status-warning .stage-fill {
	background: linear-gradient(90deg, #b67a15 0%, #e4a33c 100%);
}

.status-failed .stage-fill {
	background: linear-gradient(90deg, #ba4452 0%, #ec7280 100%);
}

.status-running .stage-fill {
	background: linear-gradient(90deg, #2e9cb9 0%, #78d9ec 100%);
}

@keyframes stage-grow {
	from {
		transform: scaleX(0.25);
		opacity: 0.65;
	}

	to {
		transform: scaleX(1);
		opacity: 1;
	}
}

@media (max-width: 760px) {
	.stage-line {
		grid-template-columns: auto 1fr;
	}

	.stage-time {
		grid-column: 1 / -1;
		font-size: 0.7rem;
	}
}
</style>
