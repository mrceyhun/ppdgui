import { createApp } from "vue";
import { createPinia } from "pinia";

import App from "./App.vue";
import router from "./router";
import axios from "axios";
import { useMainRunStore } from "@/stores/mainRun.js";
import { useStyleStore } from "@/stores/style.js";
import { darkModeKey, styleKey } from "@/config.js";

import "./css/main.css";

/* Set axios base url */
const isEnvDev = import.meta.env.DEV;
console.log("Env:" + isEnvDev);
if (isEnvDev) {
  // axios.defaults.baseURL = "http://ceyhun-k8s-lbva4duqns2g-node-0:32001/ppdgui/api";
  axios.defaults.baseURL = "http://ceyhun-vm.cern.ch:8081/ppdgui/api";
  console.log("Env:" + isEnvDev);
} else {
  axios.defaults.baseURL = "VITE_BACKEND_API_BASE_URL";
}

/* Init Pinia */
const pinia = createPinia();

/* Create Vue app */
createApp(App).use(router).use(pinia).mount("#app");

/* Init Pinia stores */
useMainRunStore(pinia);
const styleStore = useStyleStore(pinia);

/* App style */
styleStore.setStyle(localStorage[styleKey] ?? "basic");

/* Get histograms */
// mainRunStore.getRunHistorgrams(2023, mainRunStore.runNumber);

/* Dark mode */
if (
  (!localStorage[darkModeKey] &&
    window.matchMedia("(prefers-color-scheme: dark)").matches) ||
  localStorage[darkModeKey] === "1"
) {
  styleStore.setDarkMode(true);
}

/* Default title tag */
const defaultDocumentTitle = "Home";

/* Set document title from route meta */
router.afterEach((to) => {
  document.title = to.meta?.title
    ? `${to.meta.title} — ${defaultDocumentTitle}`
    : defaultDocumentTitle;
});
