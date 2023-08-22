import { createApp } from 'vue';
import './style.css';
import App from './App.vue';
import axios from 'axios';
import router from './router';

const app = createApp(App);

// axios configs
// Required environment variable for backend API, should start with VITE_
// frontend/substitute_environment_variables.sh will replace it. Read it for more details.

axios.defaults.baseURL = "VITE_BACKEND_API_BASE_URL";
app.axios = axios;
app.$http = axios;
app.config.globalProperties.axios = axios;
app.config.globalProperties.$http = axios;

app.use(router);
app.mount('#app')
