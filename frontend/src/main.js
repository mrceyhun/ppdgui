import { createApp } from 'vue';
import './style.css';
import App from './App.vue';
import axios from 'axios';
import router from './router';

const app = createApp(App);
const isEnvDev = import.meta.env.DEV;

// axios configs
// Required environment variable for backend API, should start with VITE_
// frontend/run.sh will replace it. Read it for more details.

if (isEnvDev) {
    axios.defaults.baseURL = "http://localhost:8081/ppdgui/api";
} else {
    axios.defaults.baseURL = "VITE_BACKEND_API_BASE_URL";
}
app.axios = axios;
app.$http = axios;
app.config.globalProperties.axios = axios;
app.config.globalProperties.$http = axios;

app.use(router);
app.mount('#app')
