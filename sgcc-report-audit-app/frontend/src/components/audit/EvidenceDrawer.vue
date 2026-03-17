<script setup lang="ts">
import { computed } from "vue";

import type { AuditEvidence } from "../../stores/audit";
import ImagePreview from "../data/ImagePreview.vue";

export type EvidenceJumpTarget = "page" | "anchor" | "image";

export type EvidenceSelection = {
	checkId: string;
	checkTitle: string;
	evidence: AuditEvidence;
};

const props = defineProps<{
	open: boolean;
	selection: EvidenceSelection | null;
}>();

const emit = defineEmits<{
	"update:open": [value: boolean];
	jump: [payload: { target: EvidenceJumpTarget; selection: EvidenceSelection }];
}>();

const hasSelection = computed(() => Boolean(props.selection));
const hasImage = computed(() => Boolean(props.selection?.evidence.imageHint));

function closeDrawer(): void {
	emit("update:open", false);
}

function emitJump(target: EvidenceJumpTarget): void {
	if (!props.selection) {
		return;
	}

	emit("jump", {
		target,
		selection: props.selection,
	});
}
</script>

<template>
	<aside
		v-show="props.open && hasSelection"
		class="evidence-drawer"
		data-testid="evidence-drawer"
		aria-label="证据定位侧栏"
	>
		<header class="drawer-head">
			<div>
				<p class="drawer-kicker">Evidence Navigator</p>
				<h3>{{ props.selection?.checkTitle }}</h3>
				<p class="drawer-code">{{ props.selection?.checkId }} · {{ props.selection?.evidence.label }}</p>
			</div>
			<button type="button" class="drawer-close" data-testid="evidence-drawer-close" @click="closeDrawer">
				收起
			</button>
		</header>

		<section class="drawer-body">
			<p class="excerpt">{{ props.selection?.evidence.excerpt }}</p>

			<div class="meta-grid">
				<p>
					<span>来源</span>
					<strong>{{ props.selection?.evidence.source }}</strong>
				</p>
				<p>
					<span>页码</span>
					<strong>{{ props.selection?.evidence.page ? `P${props.selection.evidence.page}` : "未标注" }}</strong>
				</p>
				<p>
					<span>段落锚点</span>
					<strong>{{ props.selection?.evidence.paragraphAnchor ?? "未标注" }}</strong>
				</p>
			</div>

			<div class="jump-actions">
				<button type="button" data-testid="evidence-jump-page" @click="emitJump('page')">跳转到页码定位</button>
				<button type="button" data-testid="evidence-jump-anchor" @click="emitJump('anchor')">跳转到段落锚点</button>
			</div>

			<div v-if="hasImage" class="image-area">
				<p class="image-title">图片证据</p>
				<ImagePreview
					:caption="props.selection?.evidence.imageHint ?? ''"
					:source="props.selection?.evidence.source ?? ''"
					:page="props.selection?.evidence.page ?? null"
					:active="true"
					@open="emitJump('image')"
				/>
				<button type="button" class="image-jump" data-testid="evidence-jump-image" @click="emitJump('image')">
					跳转到图片缩略图
				</button>
			</div>
		</section>
	</aside>
</template>

<style scoped>
.evidence-drawer {
	position: sticky;
	top: 0.9rem;
	height: fit-content;
	border-radius: var(--radius-md);
	border: 1px solid #bfd5ee;
	background:
		radial-gradient(circle at 90% 0%, rgba(54, 116, 186, 0.24), transparent 30%),
		linear-gradient(180deg, #f7fbff 0%, #edf5ff 100%);
	box-shadow: var(--shadow-soft);
	animation: drawer-enter var(--duration-normal) var(--ease-standard);
}

.drawer-head {
	padding: 0.72rem 0.78rem;
	border-bottom: 1px solid #d5e4f7;
	display: flex;
	justify-content: space-between;
	align-items: start;
	gap: 0.6rem;
}

.drawer-kicker {
	margin: 0;
	font-size: var(--text-xs);
	letter-spacing: 0.1em;
	text-transform: uppercase;
	color: #4d729c;
}

.drawer-head h3 {
	margin: 0.12rem 0 0;
	font-size: var(--text-lg);
	color: #21466e;
	line-height: 1.2;
}

.drawer-code {
	margin: 0.22rem 0 0;
	font-size: var(--text-xs);
	color: #6686a9;
	letter-spacing: 0.04em;
	text-transform: uppercase;
}

.drawer-close,
.jump-actions button,
.image-jump {
	border-radius: 0.56rem;
	border: 1px solid #b8d0ea;
	background: #ffffff;
	color: #21486f;
	font-size: var(--text-sm);
	padding: 0.38rem 0.52rem;
	cursor: pointer;
	transition:
		border-color var(--duration-fast) var(--ease-standard),
		box-shadow var(--duration-fast) var(--ease-standard),
		transform var(--duration-fast) var(--ease-standard);
}

.drawer-close:hover,
.jump-actions button:hover,
.image-jump:hover {
	border-color: #78a6d9;
	box-shadow: 0 8px 16px rgba(26, 66, 117, 0.16);
	transform: translateY(-1px);
}

.drawer-body {
	display: grid;
	gap: 0.68rem;
	padding: 0.74rem 0.78rem 0.82rem;
}

.excerpt {
	margin: 0;
	padding: 0.52rem 0.58rem;
	border-radius: 0.6rem;
	background: rgba(255, 255, 255, 0.8);
	border: 1px solid #d2e2f4;
	font-size: var(--text-sm);
	line-height: 1.45;
	color: #2f5377;
}

.meta-grid {
	display: grid;
	grid-template-columns: 1fr;
	gap: 0.34rem;
}

.meta-grid p {
	margin: 0;
	padding: 0.4rem 0.5rem;
	border-radius: 0.52rem;
	border: 1px solid #d8e6f7;
	background: #fafdff;
	display: flex;
	justify-content: space-between;
	align-items: center;
	gap: 0.5rem;
}

.meta-grid span {
	font-size: var(--text-xs);
	color: #5d7c9d;
	letter-spacing: 0.06em;
	text-transform: uppercase;
}

.meta-grid strong {
	font-size: var(--text-sm);
	color: #21476d;
}

.jump-actions {
	display: grid;
	gap: 0.42rem;
}

.image-area {
	display: grid;
	gap: 0.4rem;
}

.image-title {
	margin: 0;
	font-size: var(--text-xs);
	letter-spacing: 0.1em;
	text-transform: uppercase;
	color: #4f739d;
}

@keyframes drawer-enter {
	from {
		opacity: 0;
		transform: translateX(8px);
	}

	to {
		opacity: 1;
		transform: translateX(0);
	}
}

@media (max-width: 1100px) {
	.evidence-drawer {
		position: static;
	}
}
</style>
