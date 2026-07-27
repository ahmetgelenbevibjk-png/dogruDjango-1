import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router' // Router'ı içe aktar

const app = createApp(App)

app.use(router) // Router'ı Vue uygulamasına dahil et
app.mount('#app')
// En alttaki o ikinci createApp satırı silindi!