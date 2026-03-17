<script setup lang="ts">
import type {
	BrowserChunkRecord,
	BrowserImageReference,
} from "../../api/documents";
import ImagePreview from "./ImagePreview.vue";

export type MetadataRow = {
	label: string;
	value: string;
};

const props = defineProps<{
	chunk: BrowserChunkRecord;
	metadataRows: MetadataRow[];
	activeImageId?: string | null;
	active?: boolean;
}>();

const emit = defineEmits<{
	"focus-chunk": [chunkId: string];
	"open-image": [payload: { chunkId: string; image: BrowserImageReference }];
}>();

function focusChunk(): void {
	emit("focus-chunk", props.chunk.chunkId);
}

function openImage(image: BrowserImageReference): void {
	emit("open-image", {
		chunkId: props.chunk.chunkId,
		image,
	});
}
</script>

<template>
	<article
		class="chunk-card"
		:class="{ 'chunk-card--active': props.active }"
		:data-testid="`chunk-card-${props.chunk.chunkId}`"
	>
		<header class="chunk-head">
			<div>
				<p class="chunk-kicker">Chunk {{ props.chunk.chunkIndex }}</p>
				<h3>{{ props.chunk.metadata.title }}</h3>
			</div>
			<button type="button" class="focus-button" @click="focusChunk">定位</button>
		</header>

		<p class="chunk-text">{{ props.chunk.text }}</p>

		<details class="metadata-block" :data-testid="`chunk-metadata-${props.chunk.chunkId}`">
			<summary>Metadata</summary>
			<ul>
				<li v-for="row in props.metadataRows" :key="row.label">
					<span>{{ row.label }}</span>
					<strong>{{ row.value }}</strong>
				</li>
			</ul>
		</details>

		<section class="image-rail">
			<header>
				<p>图片预览</p>
				<span>{{ props.chunk.metadata.imageRefs.length }} 张</span>
			</header>

			<div v-if="props.chunk.metadata.imageRefs.length > 0" class="image-grid">
				<ImagePreview
					v-for="image in props.chunk.metadata.imageRefs"
					:key="image.id"
					:caption="image.caption"
					:source="image.source"
					:page="image.page"
					:active="props.activeImageId === image.id"
					:test-id="`chunk-image-${props.chunk.chunkId}-${image.id}`"
					@open="openImage(image)"
				/>
			</div>

			<p v-else class="empty-hint">当前 Chunk 无关联图片。</p>
		</section>
	</article>
</template>

<style scoped>
.chunk-card {
	display: grid;
	gap: 0.62rem;
	padding: 0.78rem;
	border: 1px solid #cdddf1;
	border-radius: 0.72rem;
	background: linear-gradient(180deg, #fbfdff 0%, #f1f7ff 100%);
	box-shadow: 0 10px 20px rgba(24, 67, 118, 0.08);
	transition:
		border-color var(--duration-fast) var(--ease-standard),
		box-shadow var(--duration-fast) var(--ease-standard),
		transform var(--duration-fast) var(--ease-standard);
}

.chunk-card:hover {
	border-color: #8fb3dc;
	box-shadow: 0 14px 26px rgba(26, 66, 117, 0.16);
	transform: translateY(-1px);
}

.chunk-card--active {
	border-color: #2f6fb7;
	box-shadow:
		inset 3px 0 0 #2f6fb7,
		0 14px 26px rgba(20, 56, 103, 0.2);
}

.chunk-head {
	display: flex;
	justify-content: space-between;
	gap: 0.6rem;
	align-items: start;
}

.chunk-kicker {
	margin: 0;
	font-size: var(--text-xs);
	color: #54789f;
	letter-spacing: 0.08em;
	text-transform: uppercase;
}

.chunk-head h3 {
	margin: 0.15rem 0 0;
	font-size: var(--text-lg);
	line-height: 1.25;
	color: #22486f;
}

.focus-button {
	border: 1px solid #afc8e5;
	border-radius: 999px;
	padding: 0.3rem 0.6rem;
	background: #ffffff;
	color: #24537e;
	cursor: pointer;
}

.chunk-text {
	margin: 0;
	font-size: var(--text-sm);
	color: #2c4f73;
	line-height: 1.55;
	padding: 0.56rem 0.6rem;
	border-radius: 0.6rem;
	background: rgba(255, 255, 255, 0.78);
	border: 1px solid #d8e6f6;
}

.metadata-block {
	border: 1px solid #d3e2f4;
	border-radius: 0.6rem;
	background: #fafdff;
}

.metadata-block summary {
	cursor: pointer;
	list-style: none;
	padding: 0.45rem 0.56rem;
	font-size: var(--text-xs);
	text-transform: uppercase;
	letter-spacing: 0.08em;
	color: #4f739d;
}

.metadata-block ul {
	margin: 0;
	padding: 0 0.56rem 0.56rem;
	list-style: none;
	display: grid;
	gap: 0.34rem;
}

.metadata-block li {
	padding: 0.36rem 0.4rem;
	border: 1px solid #dbe8f7;
	border-radius: 0.44rem;
	display: flex;
	justify-content: space-between;
	gap: 0.5rem;
	background: white;
}

.metadata-block span {
	font-size: var(--text-xs);
	color: #6384a8;
	letter-spacing: 0.04em;
}

.metadata-block strong {
	font-size: var(--text-sm);
	color: #234a72;
	text-align: right;
}

.image-rail {
	display: grid;
	gap: 0.42rem;
}

.image-rail > header {
	display: flex;
	justify-content: space-between;
	align-items: center;
}

.image-rail p {
	margin: 0;
	font-size: var(--text-xs);
	letter-spacing: 0.08em;
	text-transform: uppercase;
	color: #4e749f;
}

.image-rail span {
	font-size: var(--text-xs);
	color: #6688ad;
}

.image-grid {
	display: grid;
	grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
	gap: 0.44rem;
}

.empty-hint {
	margin: 0;
	font-size: var(--text-sm);
	color: #6788ac;
	padding: 0.48rem 0.52rem;
	border-radius: 0.52rem;
	border: 1px dashed #bfd5ee;
	background: rgba(255, 255, 255, 0.65);
}
</style>
