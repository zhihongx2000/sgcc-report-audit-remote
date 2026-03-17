<script setup lang="ts">
import { computed } from "vue";

import type { AuditCheckStatus } from "../../stores/audit";

const props = defineProps<{
	status: AuditCheckStatus;
}>();

const textMap: Record<AuditCheckStatus, string> = {
	pass: "满足",
	fail: "不满足",
	review: "需复核",
};

const statusText = computed(() => textMap[props.status]);
</script>

<template>
	<span :class="['status-tag', `status-tag--${status}`]">{{ statusText }}</span>
</template>

<style scoped>
.status-tag {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	min-width: 4.6rem;
	border-radius: var(--radius-pill);
	padding: 0.2rem 0.66rem;
	font-size: var(--text-sm);
	font-weight: var(--weight-semibold);
	letter-spacing: 0.02em;
	border: 1px solid transparent;
}

.status-tag--pass {
	color: var(--color-success);
	background: color-mix(in srgb, var(--color-success) 15%, white);
	border-color: color-mix(in srgb, var(--color-success) 30%, white);
}

.status-tag--review {
	color: var(--color-warning);
	background: color-mix(in srgb, var(--color-warning) 13%, white);
	border-color: color-mix(in srgb, var(--color-warning) 28%, white);
}

.status-tag--fail {
	color: var(--color-danger);
	background: color-mix(in srgb, var(--color-danger) 13%, white);
	border-color: color-mix(in srgb, var(--color-danger) 28%, white);
}
</style>
