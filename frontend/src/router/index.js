import { createRouter, createWebHashHistory } from "vue-router";
import Home from "@/views/HomeView.vue";
import OverlayRuns from "@/views/OverlayRunsView.vue";

const routes = [
  {
    meta: {
      title: "PPD Dashboard",
    },
    path: "/",
    name: "dashboard",
    component: Home,
  },
  {
    meta: {
      title: "PPD Dashboard",
    },
    path: "/overlay",
    name: "overlay",
    component: OverlayRuns,
  },
  {
    meta: {
      title: "Forms",
    },
    path: "/forms",
    name: "forms",
    component: Home,
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    return savedPosition || { top: 0 };
  },
});

export default router;
