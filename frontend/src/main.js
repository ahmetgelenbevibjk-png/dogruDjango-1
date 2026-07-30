import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router' // Router'ı içe aktar
import i18n from './i18n'
const app = createApp(App)

app.use(router) // Router'ı Vue uygulamasına dahil et
app.use(i18n) 
app.mount('#app')
// En alttaki o ikinci createApp satırı silindi!