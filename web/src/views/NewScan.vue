<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { startScan } from "../api";
import ScanProgress from "../components/ScanProgress.vue";

const router = useRouter();
const targetType = ref("fabric_config");
const targetPath = ref("./labs");
const scanning = ref(false);
const error = ref("");

async function run() {
  if (!targetPath.value.trim()) return;
  scanning.value = true;
  error.value = "";
  try {
    const { scan_id } = await startScan(targetType.value, targetPath.value.trim());
    router.push(`/scan/${scan_id}`);
  } catch (e: any) {
    error.value = e.message || "scan failed";
    scanning.value = false;
  }
}
</script>

<template>
  <h1>New Scan</h1>

  <ScanProgress :scanning="scanning" />

  <div class="card" style="max-width:560px">
    <div class="form-group">
      <label>Scan Type</label>
      <select v-model="targetType">
        <option value="fabric_config">Fabric Config (static files)</option>
        <option value="fabric_runtime">Fabric Runtime (Docker containers)</option>
      </select>
    </div>

    <div class="form-group">
      <label>Target Path</label>
      <input v-model="targetPath" placeholder="./labs or /path/to/fabric-project" />
      <div style="font-size:0.75rem;color:#484f58;margin-top:0.3rem">
        Config: path to project directory &nbsp;|&nbsp; Runtime: "local" for Docker
      </div>
    </div>

    <div v-if="error" style="color:#f85149;font-size:0.85rem;margin-bottom:1rem">{{ error }}</div>

    <button class="btn btn-primary" @click="run" :disabled="scanning">
      {{ scanning ? 'Scanning...' : 'Start Scan' }}
    </button>
  </div>
</template>
