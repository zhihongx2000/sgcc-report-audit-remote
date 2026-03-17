<script setup lang="ts">
const props = defineProps<{
	caption: string;
	source: string;
	page: number | null;
	active?: boolean;
	testId?: string;
}>();

const emit = defineEmits<{
	open: [];
}>();

function openImageEvidence(): void {
	emit("open");
}
</script>

<template>
	<button
		type="button"
		class="image-preview"
		:class="{ 'is-active': props.active }"
		:data-testid="props.testId ?? 'evidence-image-preview'"
		@click="openImageEvidence"
	>
		<span class="thumb-plate" aria-hidden="true">
			<span class="thumb-grid" />
			<span class="thumb-mark">IMG</span>
		</span>
		<span class="thumb-meta">{{ props.source }}<template v-if="props.page"> · P{{ props.page }}</template></span>
		<span class="thumb-caption">{{ props.caption }}</span>
	</button>
</template>

<style scoped>
.image-preview {
	width: 100%;
	display: grid;
	gap: 0.3rem;
	padding: 0.52rem;
	border-radius: 0.66rem;
	border: 1px solid #c8dcf5;
	background: linear-gradient(180deg, #fcfeff 0%, #eff6ff 100%);
	text-align: left;
	cursor: pointer;
	transition:
		border-color var(--duration-fast) var(--ease-standard),
		box-shadow var(--duration-fast) var(--ease-standard),
		transform var(--duration-fast) var(--ease-standard);
}

.image-preview:hover {
	border-color: #7da9db;
	box-shadow: 0 10px 20px rgba(27, 68, 121, 0.16);
	transform: translateY(-1px);
}

.image-preview.is-active {
	border-color: #2d75c4;
	box-shadow:
		inset 3px 0 0 #2d75c4,
		0 12px 24px rgba(26, 66, 117, 0.2);
}

.thumb-plate {
	position: relative;
	display: block;
	aspect-ratio: 16 / 9;
	border-radius: 0.54rem;
	overflow: hidden;
	background:
		radial-gradient(circle at 20% 15%, rgba(66, 128, 204, 0.35), transparent 38%),
		radial-gradient(circle at 82% 84%, rgba(36, 160, 175, 0.28), transparent 32%),
		linear-gradient(140deg, #d9eaff 0%, #b8d2ef 46%, #97b8dc 100%);
}

.thumb-grid {
	position: absolute;
	inset: 0;
	background:
		repeating-linear-gradient(
			90deg,
			rgba(24, 74, 136, 0.16) 0,
			rgba(24, 74, 136, 0.16) 1px,
			transparent 1px,
			transparent 18px
		),
		repeating-linear-gradient(
			0deg,
			rgba(24, 74, 136, 0.12) 0,
			rgba(24, 74, 136, 0.12) 1px,
			transparent 1px,
			transparent 18px
		);
	opacity: 0.56;
}

.thumb-mark {
	position: absolute;
	right: 0.38rem;
	top: 0.32rem;
	padding: 0.08rem 0.38rem;
	border-radius: 999px;
	font-size: var(--text-xs);
	font-family: var(--font-display);
	color: #eaf4ff;
	background: rgba(16, 54, 99, 0.74);
}

.thumb-meta {
	font-size: var(--text-xs);
	color: #4c6f96;
	letter-spacing: 0.04em;
	text-transform: uppercase;
}

.thumb-caption {
	font-size: var(--text-sm);
	color: #21496f;
	line-height: 1.4;
}
</style>
