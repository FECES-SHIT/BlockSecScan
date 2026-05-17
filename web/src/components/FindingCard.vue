<script setup lang="ts">
import { ref } from "vue";
import type { Finding } from "../api";
import { t } from "../i18n";
import SeverityBadge from "./SeverityBadge.vue";

const props = defineProps<{ finding: Finding }>();
const expanded = ref(false);
</script>

<template>
  <div class="finding" :class="`sev-${finding.severity.toLowerCase()}`">
    <div class="finding-bar" @click="expanded = !expanded">
      <div class="finding-left">
        <SeverityBadge :severity="finding.severity" />
        <span class="finding-title">{{ finding.title }}</span>
      </div>
      <div class="finding-right">
        <code class="finding-rule">{{ finding.rule_id }}</code>
        <span class="expand-icon">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
            <polyline v-if="!expanded" points="6 9 12 15 18 9" />
            <polyline v-else points="18 15 12 9 6 15" />
          </svg>
        </span>
      </div>
    </div>
    <div class="finding-meta">
      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
      {{ finding.file_path }}<span v-if="finding.line_start">:{{ finding.line_start }}</span>
    </div>

    <transition name="expand">
      <div v-if="expanded" class="finding-body">
        <p class="f-desc">{{ finding.description }}</p>

        <div class="f-section">
          <div class="f-section-label">{{ t("finding.evidence") }}</div>
          <pre class="f-evidence"><code>{{ finding.evidence }}</code></pre>
        </div>

        <div class="f-section">
          <div class="f-section-label">{{ t("finding.remediation") }}</div>
          <p class="f-remediation">{{ finding.remediation }}</p>
        </div>

        <div v-if="finding.references.length" class="f-section">
          <div class="f-section-label">{{ t("finding.references") }}</div>
          <div class="f-refs">
            <a v-for="ref in finding.references" :key="ref" :href="ref" target="_blank" class="f-ref">{{ ref }}</a>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<style scoped>
.finding {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  margin-bottom: 0.6rem;
  overflow: hidden;
  transition: border-color 0.2s;
}
.finding:hover {
  border-color: var(--border-hover);
}
.finding.sev-critical {
  border-left: 3px solid #f87171;
}
.finding.sev-high {
  border-left: 3px solid #ef4444;
}
.finding.sev-medium {
  border-left: 3px solid #f59e0b;
}
.finding.sev-low {
  border-left: 3px solid #6366f1;
}
.finding.sev-info {
  border-left: 3px solid #71717a;
}

.finding-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.85rem 1rem;
  cursor: pointer;
  user-select: none;
  transition: background 0.1s;
}
.finding-bar:hover {
  background: var(--surface2);
}
.finding-left {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  flex: 1;
  min-width: 0;
}
.finding-title {
  font-size: 0.9rem;
  font-weight: 500;
}
.finding-right {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-shrink: 0;
}
.finding-rule {
  font-size: 0.72rem;
  color: var(--text3);
  background: var(--bg);
  padding: 0.15rem 0.45rem;
  border-radius: 4px;
}
.expand-icon {
  color: var(--text3);
  display: flex;
  align-items: center;
}

.finding-meta {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0 1rem 0.6rem;
  font-size: 0.78rem;
  color: var(--text3);
  font-family: "SF Mono", "Fira Code", monospace;
}

.finding-body {
  border-top: 1px solid var(--border);
  padding: 1rem;
}
.f-desc {
  font-size: 0.875rem;
  line-height: 1.65;
  color: var(--text2);
  margin-bottom: 1rem;
}
.f-section {
  margin-bottom: 0.85rem;
}
.f-section-label {
  font-size: 0.7rem;
  font-weight: 600;
  color: var(--text3);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.35rem;
}
.f-evidence {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 0.65rem 0.85rem;
  font-size: 0.8rem;
  font-family: "SF Mono", "Fira Code", "JetBrains Mono", monospace;
  overflow-x: auto;
  white-space: pre-wrap;
  word-break: break-all;
}
.f-remediation {
  font-size: 0.85rem;
  line-height: 1.55;
  color: var(--success);
}
.f-refs {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}
.f-ref {
  font-size: 0.78rem;
  color: var(--primary-hover);
  padding: 0.2rem 0.5rem;
  background: var(--primary-bg);
  border-radius: 4px;
  transition: all 0.15s;
}
.f-ref:hover {
  background: rgba(99, 102, 241, 0.2);
}

/* expand animation */
.expand-enter-active {
  transition: all 0.25s ease;
}
.expand-leave-active {
  transition: all 0.15s ease;
}
.expand-enter-from,
.expand-leave-to {
  opacity: 0;
  max-height: 0;
  padding-top: 0;
  padding-bottom: 0;
}
.expand-enter-to,
.expand-leave-from {
  opacity: 1;
  max-height: 600px;
}
</style>
