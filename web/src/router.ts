import { createRouter, createWebHistory } from "vue-router";
import Dashboard from "./views/Dashboard.vue";
import NewScan from "./views/NewScan.vue";
import ScanResult from "./views/ScanResult.vue";
import ScanHistory from "./views/ScanHistory.vue";
import Rules from "./views/Rules.vue";

const routes = [
  { path: "/", name: "dashboard", component: Dashboard },
  { path: "/scan/new", name: "new-scan", component: NewScan },
  { path: "/scan/:id", name: "scan-result", component: ScanResult },
  { path: "/history", name: "history", component: ScanHistory },
  { path: "/rules", name: "rules", component: Rules },
];

export default createRouter({
  history: createWebHistory(),
  routes,
});
