import { createApp } from 'vue';
import { createPinia } from 'pinia';
import axios from 'axios';

import App from './App.vue';
import router from './router';
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate';
import './style.css';

const app = createApp(App);
const pinia = createPinia();


axios.defaults.baseURL = "http://localhost:8080/ppdgui/api";
app.axios = axios;
app.$http = axios;
app.config.globalProperties.axios = axios;
app.config.globalProperties.$http = axios;


pinia.use(piniaPluginPersistedstate);

app.use(pinia);
app.use(router);

app.mount('#app')
