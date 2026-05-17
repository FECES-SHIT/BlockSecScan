<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { listScans, deleteScan, type ScanListItem } from "../api";
import { t } from "../i18n";

const router = useRouter();
const scans = ref<ScanListItem[]>([]);
const loaded = ref(false);

onMounted(async () => { await refresh(); loaded.value = true; });
async function refresh() { try { scans.value = await listScans(50); } catch { /* */ } }
async function remove(id: string) {
  if (!confirm(t("history.confirmDelete"))) return;
  await deleteScan(id);
  await refresh();
}
</script>

<template>
  <h1 class="page-title">{{ t("history.title") }}</h1>

  <div v-if="!loaded" class="empty"><div class="empty-icon">⏳</div><div class="empty-text">{{ t("common.loading") }}</div></div>
  <div v-else-if="scans.length === 0" class="empty">
    <div class="empty-icon">{{ t("history.emptyIcon") }}</div>
    <div class="empty-text">{{ t("history.empty") }}</div>
  </div>
  <div v-else class="history-list">
    <div v-for="s in scans" :key="s.id" class="history-card card" @click="router.push(`/scan/${s.id}`)">
      <div class="h-left">
        <span class="h-type">{{ s.target_type }}</span>
        <span class="h-path">{{ s.target_path }}</span>
      </div>
      <div class="h-sevs">
        <span v-if="s.summary.critical" class="h-sev crit">{{ s.summary.critical }}</span>
        <span v-if="s.summary.high" class="h-sev high">{{ s.summary.high }}</span>
        <span v-if="s.summary.medium" class="h-sev med">{{ s.summary.medium }}</span>
        <span v-if="s.summary.low" class="h-sev low">{{ s.summary.low }}</span>
        <span v-if="s.summary.total === 0" class="h-clean">✓ Clean</span>
      </div>
      <span class="h-time">{{ s.created_at.replace("T"," ").slice(5,16) }}</span>
      <span class="h-dur">{{ s.duration.toFixed(1) }}s</span>
      <button class="h-remove" @click.stop="remove(s.id)" title="Delete">&times;</button>
    </div>
  </div>
</template>

<style scoped>
.page-title { font-size: 1.5rem; font-weight: 700; margin-bottom: 1.5rem; }
.history-list { display: flex; flex-direction: column; gap: 0.5rem; }
.history-card {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  cursor: pointer;
  transition: all 0.15s;
}
.history-card:hover { border-color: var(--border-hover); transform: translateX(2px); }
.h-left { flex: 1; min-width: 0; display: flex; align-items: center; gap: 0.75rem; }
.h-type {
  font-size: 0.68rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--primary-hover);
  background: var(--primary-bg);
  padding: 0.15rem 0.5rem;
  border-radius: 4px;
  flex-shrink: 0;
}
.h-path { font-family: "SF Mono", "Fira Code", monospace; font-size: 0.8rem; color: var(--text2); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.h-sevs { display: flex; gap: 0.35rem; flex-shrink: 0; }
.h-sev {
  font-size: 0.65rem;
  font-weight: 700;
  font-variant-numeric: tabular-nums;
  padding: 0.1rem 0.4rem;
  border-radius: 100px;
}
.h-sev.crit { background: rgba(239,68,68,0.15); color: #f87171; }
.h-sev.high { background: rgba(239,68,68,0.08); color: #ef4444; }
.h-sev.med { background: rgba(245,158,11,0.1); color: #f59e0b; }
.h-sev.low { background: rgba(99,102,241,0.1); color: #6366f1; }
.h-clean { font-size: 0.75rem; color: var(--success); font-weight: 500; }
.h-time { font-size: 0.78rem; color: var(--text3); flex-shrink: 0; }
.h-dur { font-size: 0.78rem; color: var(--text3); font-variant-numeric: tabular-nums; flex-shrink: 0; min-width: 40px; text-align: right; }
.h-remove {
  width: 28px;
  height: 28px;
  border: 1px solid transparent;
  border-radius: var(--radius-sm);
  background: transparent;
  color: var(--text3);
  font-size: 1.1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: all 0.15s;
}
.h-remove:hover { border-color: var(--danger); color: var(--danger); }
</style>
