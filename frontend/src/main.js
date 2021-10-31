import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import './assets/tailwind.css'
import axios from 'axios';

const base = axios.create({
    baseURL: 'http://localhost:8000'
})

const app = createApp(App)

app.use(store);
app.use(router);

app.config.globalProperties.$axios = base;

app.mount('#app');

