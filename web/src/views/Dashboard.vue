<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { listScans, type ScanListItem } from "../api";
import SeverityBadge from "../components/SeverityBadge.vue";

const router = useRouter();
const scans = ref<ScanListItem[]>([]);
const loading = ref(true);

onMounted(async () => {
  try { scans.value = await listScans(20); } catch (e) { /* empty */ }
  loading.value = false;
});

const totalScans = () => scans.value.length;
const totalFindings = () => scans.value.reduce((s, sc) => s + (sc.summary?.total || 0), 0);
const totalHigh = () => scans.value.reduce((s, sc) => s + (sc.summary?.high || 0) + (sc.summary?.critical || 0), 0);
const lastScan = () => scans.value[0]?.created_at?.replace("T", " ").slice(0, 19) || "—";
</script>

<template>
  <h1>Dashboard</h1>

  <div class="stat-grid">
    <div class="stat-card"><div class="stat-value">{{ totalScans() }}</div><div class="stat-label">Total Scans</div></div>
    <div class="stat-card"><div class="stat-value" style="color:#f85149">{{ totalHigh() }}</div><div class="stat-label">High + Critical</div></div>
    <div class="stat-card"><div class="stat-value">{{ totalFindings() }}</div><div class="stat-label">Total Findings</div></div>
    <div class="stat-card"><div class="stat-value" style="font-size:1rem">{{ lastScan() }}</div><div class="stat-label">Last Scan</div></div>
  </div>

  <div style="margin-bottom:1.5rem">
    <button class="btn btn-primary" @click="router.push('/scan/new')">+ New Scan</button>
  </div>

  <h2>Recent Scans</h2>
  <div v-if="loading" class="empty-state"><p>Loading...</p></div>
  <div v-else-if="scans.length === 0" class="empty-state">
    <div class="icon">🔍</div>
    <p>No scans yet. Start your first scan!</p>
  </div>
  <table v-else>
    <thead>
      <tr><th>Time</th><th>Type</th><th>Target</th><th>Findings</th><th>Status</th><th></th></tr>
    </thead>
    <tbody>
      <tr v-for="s in scans.slice(0, 10)" :key="s.id">
        <td>{{ s.created_at.replace("T"," ").slice(0,19) }}</td>
        <td>{{ s.target_type }}</td>
        <td style="font-family:monospace;font-size:0.8rem;max-width:200px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{{ s.target_path }}</td>
        <td>
          <span style="color:#f85149" v-if="s.summary.critical + s.summary.high > 0">{{ s.summary.critical + s.summary.high }}</span>
          <span v-else style="color:#7ee787">0</span>
        </td>
        <td><span :style="{color: s.status === 'done' ? '#7ee787' : '#d29922'}">{{ s.status }}</span></td>
        <td><button class="btn btn-sm" @click="router.push(`/scan/${s.id}`)">View</button></td>
      </tr>
    </tbody>
  </table>
</template>
