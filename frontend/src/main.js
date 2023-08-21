import { createApp } from 'vue';
import './style.css';
import App from './App.vue';
import axios from 'axios';
import router from './router';

const app = createApp(App);

// axios configs
// Required environment variable for backend API, should start with VITE_
const backend_api_base = import.meta.env.VITE_BACKEND_API_BASE_URL;
axios.defaults.baseURL = backend_api_base ? backend_api_base : "http://localhost:8081/ppdgui/api";
app.axios = axios;
app.$http = axios;
app.config.globalProperties.axios = axios;
app.config.globalProperties.$http = axios;

app.use(router);
app.mount('#app')
