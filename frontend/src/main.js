import { createApp } from 'vue';
import './style.css';
import App from './App.vue';
import axios from 'axios';
import router from './router';

const app = createApp(App);

// axios configs
axios.defaults.baseURL = "http://localhost:8081/ppdgui/api";
app.axios = axios;
app.$http = axios;
app.config.globalProperties.axios = axios;
app.config.globalProperties.$http = axios;

app.use(router);
app.mount('#app')
