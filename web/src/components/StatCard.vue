<script setup lang="ts">
import { ref, onMounted, watch } from "vue";

const props = defineProps<{ value: number | string; label: string; color?: string }>();

const display = ref(0);

onMounted(() => {
  if (typeof props.value === "number") {
    animate(props.value);
  } else {
    display.value = null as any;
  }
});

watch(
  () => props.value,
  (v) => {
    if (typeof v === "number") animate(v);
  }
);

function animate(target: number) {
  const start = display.value || 0;
  const diff = target - start;
  const duration = 600;
  const startTime = performance.now();
  function step(now: number) {
    const elapsed = now - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    display.value = Math.round(start + diff * eased);
    if (progress < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}
</script>

<template>
  <div class="stat-card">
    <div v-if="typeof value === 'number'" class="stat-value" :style="{ color: color || 'var(--text)' }">{{ display }}</div>
    <div v-else class="stat-value" :style="{ color: color || 'var(--text)', fontSize: '1rem', fontVariantNumeric: 'normal' }">{{ value }}</div>
    <div class="stat-label">{{ label }}</div>
  </div>
</template>

<style scoped>
.stat-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.25rem 1.5rem;
  text-align: center;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.stat-card:hover {
  border-color: var(--border-hover);
  box-shadow: var(--shadow-md);
}
.stat-value {
  font-size: 2.25rem;
  font-weight: 800;
  font-variant-numeric: tabular-nums;
  line-height: 1.2;
  margin-bottom: 0.25rem;
}
.stat-label {
  font-size: 0.75rem;
  font-weight: 500;
  color: var(--text3);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
</style>
