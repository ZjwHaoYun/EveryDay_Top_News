import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
// 1. 引入Element Plus核心库和全部样式
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
// 2. 引入Element Plus全部图标（全局可用，无需单独导入）
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

const app = createApp(App)
// 3. 全局注册Element Plus
app.use(ElementPlus)
// 4. 全局注册所有Element Plus图标（遍历注册，图标名与组件名一致）
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}
app.use(router)

app.mount('#app')
