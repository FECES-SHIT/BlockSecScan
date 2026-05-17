<script setup lang="ts">
import { ref, onUnmounted } from "vue";
import { useRouter } from "vue-router";
import { startScan } from "../api";
import { t } from "../i18n";

const router = useRouter();
const targetType = ref("fabric_config");
const targetPath = ref("./labs");
const scanning = ref(false);
const error = ref("");
const progress = ref(0);
let _timer: ReturnType<typeof setInterval> | null = null;

onUnmounted(() => {
  if (_timer) { clearInterval(_timer); _timer = null; }
});

async function run() {
  if (!targetPath.value.trim()) return;
  scanning.value = true;
  error.value = "";
  progress.value = 0;
  _timer = setInterval(() => { if (progress.value < 90) progress.value += Math.random() * 20; }, 300);
  try {
    const { scan_id } = await startScan(targetType.value, targetPath.value.trim());
    clearInterval(_timer);
    _timer = null;
    progress.value = 100;
    setTimeout(() => router.push(`/scan/${scan_id}`), 200);
  } catch (e: any) {
    clearInterval(_timer);
    _timer = null;
    error.value = e.message || "scan failed";
    scanning.value = false;
  }
}
</script>

<template>
  <h1 class="page-title">{{ t("scan.title") }}</h1>

  <div class="form-card card" style="max-width:580px">
    <div class="type-picker">
      <button class="type-option" :class="{ active: targetType === 'fabric_config' }" @click="targetType = 'fabric_config'">
        <span class="type-icon">📄</span>
        <span class="type-label">{{ t("scan.typeConfig") }}</span>
      </button>
      <button class="type-option" :class="{ active: targetType === 'fabric_runtime' }" @click="targetType = 'fabric_runtime'">
        <span class="type-icon">🐳</span>
        <span class="type-label">{{ t("scan.typeRuntime") }}</span>
      </button>
    </div>

    <div class="form-group">
      <label class="form-label">{{ t("scan.path") }}</label>
      <input class="form-input" v-model="targetPath" :placeholder="t('scan.path')" @keyup.enter="run" />
      <div class="form-hint">{{ t("scan.pathHint") }}</div>
    </div>

    <div v-if="error" class="err">{{ error }}</div>

    <div v-if="scanning" class="progress-track">
      <div class="progress-fill" :style="{ width: Math.min(progress, 100) + '%' }"></div>
      <span class="progress-text">{{ t("scan.scanning") }}</span>
    </div>

    <button class="btn btn-primary btn-wide" @click="run" :disabled="scanning">
      {{ scanning ? t("scan.scanning") : t("scan.start") }}
    </button>
  </div>
</template>

<style scoped>
.page-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
}
.type-picker {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}
.type-option {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  padding: 1.25rem 1rem;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: var(--bg);
  color: var(--text2);
  cursor: pointer;
  font-family: var(--font);
  transition: all 0.15s;
}
.type-option:hover {
  border-color: var(--border-hover);
}
.type-option.active {
  border-color: var(--primary);
  background: var(--primary-bg);
  color: var(--primary-hover);
}
.type-icon {
  font-size: 1.5rem;
}
.type-label {
  font-size: 0.82rem;
  font-weight: 500;
  text-align: center;
}
.err {
  color: var(--danger);
  font-size: 0.82rem;
  margin-bottom: 1rem;
}
.progress-track {
  height: 6px;
  background: var(--border);
  border-radius: 3px;
  margin-bottom: 1rem;
  overflow: hidden;
  position: relative;
}
.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--primary), var(--primary-hover));
  border-radius: 3px;
  transition: width 0.3s;
  max-width: 100%;
}
.progress-text {
  position: absolute;
  right: 0;
  top: -1.5rem;
  font-size: 0.75rem;
  color: var(--text3);
}
.btn-wide {
  width: 100%;
  justify-content: center;
}
</style>
