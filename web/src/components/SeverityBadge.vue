<script setup lang="ts">
defineProps<{ severity: string }>();
</script>

<template>
  <span :class="`badge badge-${severity.toLowerCase()}`">{{ severity }}</span>
</template>
