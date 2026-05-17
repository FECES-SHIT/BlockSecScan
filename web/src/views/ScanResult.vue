<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { getScan, deleteScan, reportUrl, type ScanDetail, type Finding } from "../api";
import SeverityBadge from "../components/SeverityBadge.vue";
import FindingCard from "../components/FindingCard.vue";

const route = useRoute();
const router = useRouter();
const scan = ref<ScanDetail | null>(null);
const loading = ref(true);
const error = ref("");
const filter = ref("all");

onMounted(async () => {
  try {
    scan.value = await getScan(route.params.id as string);
  } catch (e: any) {
    error.value = e.message || "not found";
  }
  loading.value = false;
});

const filteredFindings = computed(() => {
  if (!scan.value) return [];
  if (filter.value === "all") return scan.value.findings;
  return scan.value.findings.filter(f => f.severity.toLowerCase() === filter.value);
});

async function remove() {
  if (!scan.value || !confirm("Delete this scan?")) return;
  await deleteScan(scan.value.id);
  router.push("/history");
}
</script>

<template>
  <div v-if="loading" class="empty-state"><p>Loading...</p></div>
  <div v-else-if="error" class="empty-state"><p>{{ error }}</p></div>

  <template v-else-if="scan">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:1.5rem">
      <div>
        <h1 style="margin-bottom:0.25rem">Scan Result</h1>
        <div style="font-size:0.8rem;color:#8b949e">
          {{ scan.target_type }} → {{ scan.target_path }} · {{ scan.created_at.replace("T"," ").slice(0,19) }} · {{ scan.duration.toFixed(1) }}s
        </div>
      </div>
      <div style="display:flex;gap:0.5rem">
        <a :href="reportUrl(scan.id, 'html')" target="_blank" class="btn btn-sm">HTML</a>
        <a :href="reportUrl(scan.id, 'markdown')" target="_blank" class="btn btn-sm">MD</a>
        <a :href="reportUrl(scan.id, 'json')" target="_blank" class="btn btn-sm">JSON</a>
        <button class="btn btn-sm btn-danger" @click="remove">Delete</button>
      </div>
    </div>

    <div class="stat-grid">
      <div class="stat-card"><div class="stat-value" style="color:#ff7b72">{{ scan.summary.critical }}</div><div class="stat-label">Critical</div></div>
      <div class="stat-card"><div class="stat-value" style="color:#f85149">{{ scan.summary.high }}</div><div class="stat-label">High</div></div>
      <div class="stat-card"><div class="stat-value" style="color:#d29922">{{ scan.summary.medium }}</div><div class="stat-label">Medium</div></div>
      <div class="stat-card"><div class="stat-value" style="color:#58a6ff">{{ scan.summary.low }}</div><div class="stat-label">Low</div></div>
      <div class="stat-card"><div class="stat-value" style="color:#8b949e">{{ scan.summary.info }}</div><div class="stat-label">Info</div></div>
    </div>

    <div style="display:flex;gap:0.5rem;margin-bottom:1rem">
      <button v-for="f in ['all','critical','high','medium','low']" :key="f"
        class="btn btn-sm" :class="{ 'btn-primary': filter === f }" @click="filter = f"
        style="text-transform:capitalize">{{ f }}</button>
    </div>

    <div v-if="filteredFindings.length === 0" class="empty-state">
      <div class="icon">✅</div>
      <p v-if="filter === 'all'">No security issues found.</p>
      <p v-else>No {{ filter }} findings.</p>
    </div>

    <FindingCard v-for="f in filteredFindings" :key="f.id" :finding="f" />
  </template>
</template>
