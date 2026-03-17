<script setup lang="ts">
import type { AuditCheckItem } from "../../stores/audit";
import StatusTag from "../common/StatusTag.vue";

defineProps<{
	items: AuditCheckItem[];
}>();

function formatCheckId(id: string): string {
	const numberPart = id.replace(/[^0-9]/g, "");
	return numberPart ? numberPart.padStart(2, "0") : id;
}

function formatTime(iso: string): string {
	const parsed = new Date(iso);
	if (Number.isNaN(parsed.getTime())) {
		return iso;
	}
	return parsed.toLocaleString("zh-CN", {
		year: "2-digit",
		month: "2-digit",
		day: "2-digit",
		hour: "2-digit",
		minute: "2-digit",
	});
}
</script>

<template>
	<div class="check-table-shell">
		<table v-if="items.length > 0" class="check-table" data-testid="check-items-table">
			<thead>
				<tr>
					<th scope="col">审查项</th>
					<th scope="col">状态</th>
					<th scope="col">判定说明</th>
					<th scope="col">证据定位</th>
					<th scope="col">更新时间</th>
				</tr>
			</thead>
			<tbody>
				<tr v-for="item in items" :key="item.id" class="check-row" :data-testid="`check-row-${item.id}`">
					<td>
						<p class="check-id">#{{ formatCheckId(item.id) }}</p>
						<p class="check-title">{{ item.title }}</p>
					</td>
					<td>
						<StatusTag :status="item.status" />
					</td>
					<td>
						<p class="reason-text">{{ item.reason }}</p>
					</td>
					<td>
						<ul class="evidence-list">
							<li v-for="entry in item.evidence" :key="entry.id" class="evidence-item">
								<span class="evidence-label">{{ entry.label }}</span>
								<span class="evidence-meta">{{ entry.source }}<template v-if="entry.page"> · P{{ entry.page }}</template></span>
							</li>
						</ul>
					</td>
					<td>
						<p class="updated-text">{{ formatTime(item.updatedAt) }}</p>
					</td>
				</tr>
			</tbody>
		</table>
		<div v-else class="empty-hint" role="status">当前筛选条件下没有命中的审查项。</div>
	</div>
</template>

<style scoped>
.check-table-shell {
	overflow-x: auto;
}

.check-table {
	width: 100%;
	min-width: 920px;
	border-collapse: separate;
	border-spacing: 0;
	border: 1px solid var(--color-border-soft);
	border-radius: var(--radius-md);
	background: #fff;
}

.check-table th,
.check-table td {
	text-align: left;
	padding: 0.72rem 0.78rem;
	border-bottom: 1px solid #e6edf7;
	vertical-align: top;
}

.check-table th {
	position: sticky;
	top: 0;
	background: linear-gradient(180deg, #f8fbff 0%, #edf4ff 100%);
	font-size: var(--text-sm);
	color: #335170;
	font-weight: var(--weight-semibold);
}

.check-row {
	transition: background-color var(--duration-fast) var(--ease-standard);
}

.check-row:hover {
	background: #f5f9ff;
}

.check-id {
	margin: 0;
	font-size: var(--text-xs);
	letter-spacing: 0.08em;
	color: #6282a8;
}

.check-title {
	margin: 0.16rem 0 0;
	font-size: var(--text-md);
	color: #1d3551;
	font-weight: var(--weight-semibold);
}

.reason-text {
	margin: 0;
	font-size: var(--text-sm);
	color: #294360;
	line-height: 1.45;
}

.evidence-list {
	list-style: none;
	margin: 0;
	padding: 0;
	display: grid;
	gap: 0.34rem;
}

.evidence-item {
	display: grid;
	gap: 0.06rem;
	padding: 0.34rem 0.44rem;
	border-radius: 0.5rem;
	border: 1px solid #dce8f8;
	background: #f8fbff;
}

.evidence-label {
	font-size: var(--text-sm);
	color: #274768;
	font-weight: var(--weight-medium);
}

.evidence-meta {
	font-size: var(--text-xs);
	color: #5e7a98;
}

.updated-text {
	margin: 0;
	font-size: var(--text-xs);
	color: #607a95;
	white-space: nowrap;
}

.empty-hint {
	padding: 1.1rem 1rem;
	border-radius: var(--radius-md);
	border: 1px dashed #bfd2ea;
	color: #4c698a;
	background: #f8fbff;
}

@media (max-width: 700px) {
	.check-table th,
	.check-table td {
		padding: 0.58rem;
	}
}
</style>
