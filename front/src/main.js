import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'
import './styles/main.css'

// 创建应用
const app = createApp(App)

// 使用路由
app.use(router)

// 使用Pinia状态管理
app.use(createPinia())

// 挂载应用
app.mount('#app')