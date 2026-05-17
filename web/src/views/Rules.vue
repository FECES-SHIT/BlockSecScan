<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { getRules, type RuleItem } from "../api";
import { t } from "../i18n";
import SeverityBadge from "../components/SeverityBadge.vue";

const rules = ref<RuleItem[]>([]);
const loaded = ref(false);
const filterCategory = ref("all");

onMounted(async () => {
  try { rules.value = await getRules(); } catch { /* */ }
  loaded.value = true;
});

const cats = computed(() => ["all", ...new Set(rules.value.map(r => r.category))].sort());
const filtered = computed(() => {
  if (filterCategory.value === "all") return rules.value;
  return rules.value.filter(r => r.category === filterCategory.value);
});
</script>

<template>
  <div class="rules-head">
    <h1 class="page-title">{{ t("rules.title") }} <span class="count">{{ rules.length }}</span></h1>
    <div class="cat-bar">
      <button v-for="c in cats" :key="c" class="cat-btn" :class="{ active: filterCategory === c }" @click="filterCategory = c">{{ c === "all" ? t("rules.filterAll") : c }}</button>
    </div>
  </div>

  <div v-if="!loaded" class="empty"><div class="empty-icon">⏳</div><div class="empty-text">{{ t("common.loading") }}</div></div>
  <div v-else-if="filtered.length === 0" class="empty"><div class="empty-text">{{ t("rules.empty") }}</div></div>
  <div v-else class="rules-grid">
    <div v-for="r in filtered" :key="r.id" class="rule-card card">
      <div class="rule-top">
        <SeverityBadge :severity="r.severity" />
        <code class="rule-id">{{ r.id }}</code>
      </div>
      <div class="rule-name">{{ r.name }}</div>
      <p class="rule-desc">{{ r.description }}</p>
    </div>
  </div>
</template>

<style scoped>
.page-title { font-size: 1.5rem; font-weight: 700; margin-bottom: 0; }
.count { font-size: 0.9rem; color: var(--text3); font-weight: 400; }
.rules-head { display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.5rem; flex-wrap: wrap; gap: 0.75rem; }
.cat-bar { display: flex; gap: 0.35rem; flex-wrap: wrap; }
.cat-btn {
  padding: 0.3rem 0.7rem;
  border: 1px solid var(--border);
  border-radius: 100px;
  background: transparent;
  color: var(--text2);
  font-size: 0.78rem;
  font-weight: 500;
  font-family: var(--font);
  cursor: pointer;
  transition: all 0.15s;
}
.cat-btn:hover { border-color: var(--border-hover); color: var(--text); }
.cat-btn.active { background: var(--primary); border-color: var(--primary); color: #fff; }
.rules-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 0.75rem; }
.rule-card { transition: all 0.15s; }
.rule-card:hover { border-color: var(--border-hover); transform: translateY(-1px); }
.rule-top { display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.6rem; }
.rule-id { font-size: 0.7rem; color: var(--text3); background: var(--bg); padding: 0.1rem 0.45rem; border-radius: 4px; }
.rule-name { font-size: 0.92rem; font-weight: 600; margin-bottom: 0.4rem; }
.rule-desc { font-size: 0.8rem; color: var(--text3); line-height: 1.55; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
</style>
