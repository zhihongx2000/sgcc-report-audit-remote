<script setup lang="ts">
withDefaults(
  defineProps<{
    title: string;
    description: string;
  }>(),
  {},
);
</script>

<template>
  <div class="empty-state" role="status">
    <p class="empty-kicker">Pending</p>
    <h2 class="empty-title">{{ title }}</h2>
    <p class="empty-description">{{ description }}</p>
  </div>
</template>

<style scoped>
.empty-state {
  display: grid;
  gap: 0.4rem;
  padding: 1.05rem 1.1rem;
  border: 1px dashed #c9d8ec;
  border-radius: 12px;
  background: linear-gradient(180deg, #fbfdff 0%, #f4f8ff 100%);
}

.empty-kicker {
  margin: 0;
  font-size: 0.72rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #35629a;
}

.empty-title {
  margin: 0;
  font-size: 1.02rem;
  font-weight: 700;
  color: #1f3755;
}

.empty-description {
  margin: 0;
  font-size: 0.88rem;
  color: #5f738d;
  line-height: 1.5;
}
</style>
