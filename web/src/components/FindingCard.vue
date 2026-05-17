<script setup lang="ts">
import { ref } from "vue";
import type { Finding } from "../api";
import SeverityBadge from "./SeverityBadge.vue";

const props = defineProps<{ finding: Finding }>();
const expanded = ref(false);
</script>

<template>
  <div class="finding" :class="`sev-${finding.severity.toLowerCase()}`">
    <div class="finding-header" @click="expanded = !expanded">
      <SeverityBadge :severity="finding.severity" />
      <span class="finding-title">{{ finding.title }}</span>
      <span class="finding-rule">{{ finding.rule_id }}</span>
      <span class="expand-icon">{{ expanded ? '−' : '+' }}</span>
    </div>
    <div class="finding-file">{{ finding.file_path }}<span v-if="finding.line_start">:{{ finding.line_start }}</span></div>
    <div v-if="expanded" class="finding-body">
      <p class="finding-desc">{{ finding.description }}</p>
      <div class="finding-evidence"><code>{{ finding.evidence }}</code></div>
      <p class="finding-remediation"><strong>Fix:</strong> {{ finding.remediation }}</p>
      <div v-if="finding.references.length" class="finding-refs">
        <a v-for="ref in finding.references" :key="ref" :href="ref" target="_blank">{{ ref }}</a>
      </div>
    </div>
  </div>
</template>

<style scoped>
.finding { background: #161b22; border: 1px solid #30363d; border-radius: 6px; margin-bottom: 0.5rem; overflow: hidden; }
.finding.sev-critical { border-left: 3px solid #ff7b72; }
.finding.sev-high { border-left: 3px solid #f85149; }
.finding.sev-medium { border-left: 3px solid #d29922; }
.finding.sev-low { border-left: 3px solid #58a6ff; }
.finding.sev-info { border-left: 3px solid #8b949e; }
.finding-header { display: flex; align-items: center; gap: 0.6rem; padding: 0.75rem 1rem; cursor: pointer; user-select: none; }
.finding-header:hover { background: #1c2128; }
.finding-title { flex: 1; font-weight: 500; font-size: 0.9rem; }
.finding-rule { font-family: monospace; font-size: 0.75rem; color: #8b949e; }
.expand-icon { color: #8b949e; font-size: 1.1rem; width: 20px; text-align: center; }
.finding-file { padding: 0 1rem 0.5rem; font-family: monospace; font-size: 0.8rem; color: #8b949e; }
.finding-body { padding: 0 1rem 0.75rem; border-top: 1px solid #21262d; }
.finding-desc { margin: 0.75rem 0; font-size: 0.875rem; line-height: 1.5; }
.finding-evidence { background: #0d1117; border-radius: 4px; padding: 0.5rem; margin: 0.5rem 0; overflow-x: auto; }
.finding-evidence code { font-size: 0.8rem; }
.finding-remediation { color: #7ee787; font-size: 0.85rem; margin: 0.5rem 0; }
.finding-refs { margin-top: 0.5rem; display: flex; flex-wrap: wrap; gap: 0.5rem; }
.finding-refs a { font-size: 0.8rem; }
</style>
