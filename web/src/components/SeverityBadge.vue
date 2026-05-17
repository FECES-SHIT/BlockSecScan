<script setup lang="ts">
import { t } from "../i18n";

defineProps<{ severity: string }>();

function key(s: string) {
  const m: Record<string, string> = {
    CRITICAL: "severity.critical",
    HIGH: "severity.high",
    MEDIUM: "severity.medium",
    LOW: "severity.low",
    INFO: "severity.info",
  };
  return m[s] || s;
}
</script>

<template>
  <span :class="`badge badge-${severity.toLowerCase()}`">{{ t(key(severity)) }}</span>
</template>
