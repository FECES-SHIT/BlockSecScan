<script setup lang="ts">
import { useRouter } from "vue-router";
const router = useRouter();
</script>

<template>
  <div class="app">
    <nav class="sidebar">
      <div class="logo">BlockSecScan</div>
      <div class="nav-links">
        <router-link to="/" class="nav-item">Dashboard</router-link>
        <router-link to="/scan/new" class="nav-item">New Scan</router-link>
        <router-link to="/history" class="nav-item">History</router-link>
        <router-link to="/rules" class="nav-item">Rules</router-link>
      </div>
      <div class="version">v0.3.0</div>
    </nav>
    <main class="content">
      <router-view />
    </main>
  </div>
</template>

<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0d1117; color: #c9d1d9; }
a { color: #58a6ff; text-decoration: none; }
a:hover { text-decoration: underline; }
.app { display: flex; min-height: 100vh; }
.sidebar { width: 220px; background: #161b22; border-right: 1px solid #30363d; padding: 1.5rem 0; display: flex; flex-direction: column; }
.logo { font-size: 1.1rem; font-weight: bold; color: #58a6ff; padding: 0 1.25rem; margin-bottom: 2rem; }
.nav-links { flex: 1; display: flex; flex-direction: column; gap: 0.25rem; }
.nav-item { padding: 0.6rem 1.25rem; color: #8b949e; font-size: 0.9rem; border-left: 2px solid transparent; transition: all 0.15s; }
.nav-item:hover { color: #c9d1d9; text-decoration: none; background: #1c2128; }
.nav-item.router-link-active { color: #f0f6fc; border-left-color: #58a6ff; background: #1c2128; }
.version { color: #484f58; font-size: 0.75rem; padding: 0 1.25rem; margin-top: auto; }
.content { flex: 1; padding: 2rem; overflow-y: auto; max-width: 1200px; }
h1 { font-size: 1.5rem; font-weight: 600; margin-bottom: 1.5rem; color: #f0f6fc; }
h2 { font-size: 1.2rem; font-weight: 600; margin: 1.5rem 0 0.75rem; color: #f0f6fc; }
.btn { display: inline-flex; align-items: center; gap: 0.4rem; padding: 0.5rem 1rem; border: 1px solid #30363d; border-radius: 6px; background: #21262d; color: #c9d1d9; font-size: 0.875rem; cursor: pointer; transition: all 0.15s; }
.btn:hover { background: #30363d; border-color: #58a6ff; }
.btn-primary { background: #238636; border-color: rgba(240,246,252,0.1); color: #fff; }
.btn-primary:hover { background: #2ea043; }
.btn-danger { border-color: #f85149; color: #f85149; }
.btn-danger:hover { background: #da3633; color: #fff; }
.btn-sm { padding: 0.3rem 0.6rem; font-size: 0.8rem; }
input, select { padding: 0.5rem 0.75rem; border: 1px solid #30363d; border-radius: 6px; background: #0d1117; color: #c9d1d9; font-size: 0.875rem; width: 100%; }
input:focus, select:focus { outline: none; border-color: #58a6ff; }
label { display: block; margin-bottom: 0.35rem; font-size: 0.85rem; color: #8b949e; font-weight: 500; }
.card { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 1.25rem; }
table { width: 100%; border-collapse: collapse; }
th { text-align: left; padding: 0.6rem 0.75rem; font-size: 0.8rem; color: #8b949e; font-weight: 500; border-bottom: 1px solid #30363d; }
td { padding: 0.6rem 0.75rem; font-size: 0.875rem; border-bottom: 1px solid #21262d; }
tr:hover td { background: #1c2128; }
.badge { display: inline-block; padding: 0.15rem 0.5rem; border-radius: 12px; font-size: 0.7rem; font-weight: 600; text-transform: uppercase; }
.badge-critical { background: #ff7b72; color: #0d1117; }
.badge-high { background: #f85149; color: #fff; }
.badge-medium { background: #d29922; color: #0d1117; }
.badge-low { background: #58a6ff; color: #0d1117; }
.badge-info { background: #8b949e; color: #0d1117; }
.stat-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 1rem; margin-bottom: 2rem; }
.stat-card { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 1rem 1.25rem; text-align: center; }
.stat-value { font-size: 1.75rem; font-weight: 700; }
.stat-label { font-size: 0.75rem; color: #8b949e; text-transform: uppercase; margin-top: 0.25rem; }
.form-group { margin-bottom: 1rem; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.empty-state { text-align: center; padding: 3rem; color: #484f58; }
.empty-state .icon { font-size: 2.5rem; margin-bottom: 0.5rem; }
</style>
