<script setup lang="ts">
defineProps<{ scanning: boolean }>();
</script>

<template>
  <div v-if="scanning" class="progress-overlay">
    <div class="progress-box">
      <div class="spinner"></div>
      <p>Scanning...</p>
    </div>
  </div>
</template>

<style scoped>
.progress-overlay { position: fixed; inset: 0; background: rgba(13,17,23,0.8); display: flex; align-items: center; justify-content: center; z-index: 100; }
.progress-box { text-align: center; }
.spinner { width: 40px; height: 40px; border: 3px solid #30363d; border-top-color: #58a6ff; border-radius: 50%; animation: spin 0.8s linear infinite; margin: 0 auto 1rem; }
@keyframes spin { to { transform: rotate(360deg); } }
.progress-box p { color: #8b949e; font-size: 0.9rem; }
</style>
