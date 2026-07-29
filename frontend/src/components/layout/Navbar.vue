<script setup>
import { ref } from 'vue'
import {onMounted} from 'vue'
import {useTheme} from '@/composables/useTheme'

const {isDark,toggleTheme,initTheme}=useTheme()
onMounted(()=>{
  initTheme()
})


// LocalStorage'dan veya varsayılan değerlerden kullanıcı bilgilerini alıyoruz
const userName = ref(localStorage.getItem('user_name') || 'deneme5')
const userEmail = ref(localStorage.getItem('user_email') || 'kullanci@ornek.com')

defineEmits(['logout'])
</script>

<template>
  <header class="top-navbar">
    <!-- Sol Taraf: Profil Görseli ve Bilgileri (Router-link ile tıklanabilir yapıldı) -->
    <div class="navbar-left">
      <router-link to="/profile" class="user-profile">
        <div class="avatar">
          {{ userName.charAt(0).toUpperCase() }}
        </div>
        <div class="user-info">
          <span class="user-name">{{ userName }}</span>
          <span class="user-email">{{ userEmail }}</span>
        </div>
      </router-link>

      <!-- ➕ EKLENEN TEMA GEÇİŞ BUTONU -->
      <button
        class="theme-toggle-btn"
        @click="toggleTheme"
        :title="isDark ? 'Açık Temaya Geç' : 'Koyu Temaya Geç'"
      >
        <span v-if="isDark" class="theme-content">☀️ Açık Tema</span>
        <span v-else class="theme-content">🌙 Koyu Tema</span>
      </button>
    </div>

    <!-- Sağ Taraf: Çıkış Butonu -->
    <div class="navbar-right">
      <button @click="$emit('logout')" class="logout-btn">Çıkış Yap</button>
    </div>
  </header>
</template>

<style scoped>
.top-navbar {
  height: 75px;
  background-color: #ffffff;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 30px;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  cursor: pointer;
  padding: 6px 10px;
  border-radius: 8px;
  transition: background-color 0.2s;
}

.user-profile:hover {
  background-color: #f1f5f9;
}

.avatar {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  background-color: #4f46e5;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 18px;
  box-shadow: 0 2px 4px rgba(79, 70, 229, 0.2);
}

.user-info {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-size: 15px;
  font-weight: 600;
  color: #1e293b;
}

.user-email {
  font-size: 13px;
  color: #64748b;
}

.logout-btn {
  background-color: #ef4444;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  font-size: 14px;
  transition: background 0.2s;
}

.logout-btn:hover {
  background-color: #dc2626;
}

.theme-toggle-btn {
  display : flex;
  align-items:center;
  gap:8px;
  padding:6px 14px;
  border-radius:8px;
  border:1px solid var(--border-color);
  background-color: var(--bg-main);
  color: var(--text-main);
  font-size:13px;
  font-weight:600;
  cursor:pointer;
  transition:all 0.2s ease;
  margin-left:20px;
}
.theme-toggle-btn:hover {
  border-color: var(--accent-color);
  transform: translateY(-1px);
}

</style>