<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { getRules, type RuleItem } from "../api";
import SeverityBadge from "../components/SeverityBadge.vue";

const rules = ref<RuleItem[]>([]);
const loading = ref(true);

onMounted(async () => {
  try { rules.value = await getRules(); } catch (e) { /* empty */ }
  loading.value = false;
});

const categories = computed(() => [...new Set(rules.value.map(r => r.category))].sort());
</script>

<template>
  <h1>Rules ({{ rules.length }} total)</h1>

  <div v-if="loading" class="empty-state"><p>Loading...</p></div>
  <div v-else>
    <div v-for="cat in categories" :key="cat" style="margin-bottom:2rem">
      <h2>{{ cat }}</h2>
      <table>
        <thead><tr><th>ID</th><th>Name</th><th>Severity</th><th>Description</th></tr></thead>
        <tbody>
          <tr v-for="r in rules.filter(x => x.category === cat)" :key="r.id">
            <td style="font-family:monospace;font-size:0.8rem">{{ r.id }}</td>
            <td>{{ r.name }}</td>
            <td><SeverityBadge :severity="r.severity" /></td>
            <td style="font-size:0.85rem;color:#8b949e;max-width:400px">{{ r.description }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
