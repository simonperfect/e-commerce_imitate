import { createApp } from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import elementIcon from './plugins/icons'
import ElementPlus from 'element-plus'  // 必须导入
import 'element-plus/dist/index.css'    // 必须导入样式




createApp(App).use(ElementPlus).use(router).use(elementIcon).mount('#app')
