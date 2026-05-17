<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { getScan, deleteScan, reportUrl, type ScanDetail } from "../api";
import { t } from "../i18n";
import FindingCard from "../components/FindingCard.vue";
import StatCard from "../components/StatCard.vue";

const route = useRoute();
const router = useRouter();
const scan = ref<ScanDetail | null>(null);
const loaded = ref(false);
const err = ref("");
const filter = ref("all");

onMounted(async () => {
  try { scan.value = await getScan(route.params.id as string); } catch (e: any) { err.value = e.message; }
  loaded.value = true;
});

const filtered = computed(() => {
  if (!scan.value) return [];
  if (filter.value === "all") return scan.value.findings;
  return scan.value.findings.filter(f => f.severity.toLowerCase() === filter.value);
});

async function remove() {
  if (!scan.value || !confirm(t("history.confirmDelete"))) return;
  await deleteScan(scan.value.id);
  router.push("/history");
}

const filters = ["all", "critical", "high", "medium", "low"];
</script>

<template>
  <div v-if="!loaded" class="empty"><div class="empty-icon">⏳</div><div class="empty-text">{{ t("common.loading") }}</div></div>
  <div v-else-if="err" class="empty"><div class="empty-text">{{ err }}</div></div>

  <template v-else-if="scan">
    <div class="result-head">
      <div>
        <h1 class="page-title" style="margin-bottom:0.25rem">{{ t("result.title") }}</h1>
        <p class="result-path">{{ scan.target_type }} &rarr; {{ scan.target_path }} &middot; {{ scan.created_at.replace("T"," ").slice(0,19) }} &middot; {{ scan.duration.toFixed(1) }}s</p>
      </div>
      <div class="result-actions">
        <a :href="reportUrl(scan.id, 'html')" target="_blank" class="btn btn-sm">{{ t("result.exportHtml") }}</a>
        <a :href="reportUrl(scan.id, 'markdown')" target="_blank" class="btn btn-sm">{{ t("result.exportMd") }}</a>
        <a :href="reportUrl(scan.id, 'json')" target="_blank" class="btn btn-sm">{{ t("result.exportJson") }}</a>
        <a :href="reportUrl(scan.id, 'sarif')" target="_blank" class="btn btn-sm">{{ t("result.exportSarif") }}</a>
        <button class="btn btn-sm btn-danger" @click="remove">{{ t("result.delete") }}</button>
      </div>
    </div>

    <div class="stats-row">
      <StatCard :value="scan.summary.critical" :label="t('severity.critical')" color="#f87171" />
      <StatCard :value="scan.summary.high" :label="t('severity.high')" color="#ef4444" />
      <StatCard :value="scan.summary.medium" :label="t('severity.medium')" color="#f59e0b" />
      <StatCard :value="scan.summary.low" :label="t('severity.low')" color="#6366f1" />
      <StatCard :value="scan.summary.info" :label="t('severity.info')" color="#a1a1aa" />
    </div>

    <div class="filter-bar">
      <button v-for="f in filters" :key="f" class="filter-btn" :class="{ active: filter === f }" @click="filter = f">
        {{ t(f === 'all' ? 'result.filterAll' : `result.filter${f.charAt(0).toUpperCase() + f.slice(1)}`) }}
      </button>
    </div>

    <div v-if="filtered.length === 0" class="empty">
      <div class="empty-icon">✅</div>
      <div class="empty-text">{{ filter === "all" ? t("result.empty") : t("result.emptyFilter") }}</div>
    </div>
    <FindingCard v-for="f in filtered" :key="f.id" :finding="f" />
  </template>
</template>

<style scoped>
.page-title { font-size: 1.5rem; font-weight: 700; }
.result-head { display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: 1.5rem; flex-wrap: wrap; gap: 1rem; }
.result-path { font-size: 0.82rem; color: var(--text3); margin-top: 0.25rem; }
.result-actions { display: flex; gap: 0.4rem; flex-wrap: wrap; }
.stats-row { display: grid; grid-template-columns: repeat(5, 1fr); gap: 0.75rem; margin-bottom: 1.5rem; }
@media (max-width: 768px) { .stats-row { grid-template-columns: repeat(3, 1fr); } }
.filter-bar { display: flex; gap: 0.4rem; margin-bottom: 1rem; }
.filter-btn {
  padding: 0.35rem 0.85rem;
  border: 1px solid var(--border);
  border-radius: 100px;
  background: transparent;
  color: var(--text2);
  font-size: 0.8rem;
  font-weight: 500;
  font-family: var(--font);
  cursor: pointer;
  transition: all 0.15s;
  text-transform: capitalize;
}
.filter-btn:hover { border-color: var(--border-hover); color: var(--text); }
.filter-btn.active { background: var(--primary); border-color: var(--primary); color: #fff; }
</style>
