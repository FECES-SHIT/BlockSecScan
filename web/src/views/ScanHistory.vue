<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { listScans, deleteScan, type ScanListItem } from "../api";

const router = useRouter();
const scans = ref<ScanListItem[]>([]);
const loading = ref(true);

onMounted(async () => {
  await refresh();
  loading.value = false;
});

async function refresh() {
  try { scans.value = await listScans(50); } catch (e) { /* empty */ }
}

async function remove(id: string) {
  if (!confirm("Delete this scan?")) return;
  await deleteScan(id);
  await refresh();
}
</script>

<template>
  <h1>Scan History</h1>

  <div v-if="loading" class="empty-state"><p>Loading...</p></div>
  <div v-else-if="scans.length === 0" class="empty-state">
    <div class="icon">📋</div>
    <p>No scan history yet.</p>
  </div>
  <table v-else>
    <thead>
      <tr><th>Time</th><th>Type</th><th>Target</th><th>CRIT</th><th>HIGH</th><th>MED</th><th>Total</th><th>Duration</th><th></th></tr>
    </thead>
    <tbody>
      <tr v-for="s in scans" :key="s.id">
        <td>{{ s.created_at.replace("T"," ").slice(0,19) }}</td>
        <td>{{ s.target_type }}</td>
        <td style="font-family:monospace;font-size:0.8rem;max-width:250px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{{ s.target_path }}</td>
        <td><span :style="{color: s.summary.critical > 0 ? '#ff7b72' : '#484f58'}">{{ s.summary.critical }}</span></td>
        <td><span :style="{color: s.summary.high > 0 ? '#f85149' : '#484f58'}">{{ s.summary.high }}</span></td>
        <td><span :style="{color: s.summary.medium > 0 ? '#d29922' : '#484f58'}">{{ s.summary.medium }}</span></td>
        <td>{{ s.summary.total }}</td>
        <td>{{ s.duration.toFixed(1) }}s</td>
        <td>
          <button class="btn btn-sm" @click="router.push(`/scan/${s.id}`)">View</button>
          <button class="btn btn-sm btn-danger" @click="remove(s.id)" style="margin-left:0.25rem">×</button>
        </td>
      </tr>
    </tbody>
  </table>
</template>
