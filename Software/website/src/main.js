import { createApp } from 'vue'
import './assets/css/bootstrap.min.css'
import './assets/css/style.css'
import App from './App.vue'
import router from './router/routes';

createApp(App).use(router).mount('#app');
