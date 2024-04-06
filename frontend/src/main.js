import { createApp } from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import axios from "axios";

const app = createApp(App)
app.use(ElementPlus)
axios.defaults.baseURL = 'http://127.0.0.1:5001'
app.config.globalProperties.$axios = axios
app.mount('#app')