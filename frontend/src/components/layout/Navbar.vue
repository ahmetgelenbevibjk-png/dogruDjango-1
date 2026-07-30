<script setup>
import { ref, onMounted } from 'vue'
import { useTheme } from '@/composables/useTheme'
import { useI18n } from 'vue-i18n'

const { locale } = useI18n()

// Dil menüsünün açılır kapanır durumu
const showLangDropdown = ref(false)

const toggleLangDropdown = () => {
  showLangDropdown.value = !showLangDropdown.value
}

const selectLanguage = (lang) => {
  locale.value = lang
  showLangDropdown.value = false
}

const { isDark, toggleTheme, initTheme } = useTheme()
onMounted(() => {
  initTheme()
})

// LocalStorage'dan veya varsayılan değerlerden kullanıcı bilgilerini alıyoruz
const userName = ref(localStorage.getItem('user_name') || 'deneme5')
const userEmail = ref(localStorage.getItem('user_email') || 'kullanci@ornek.com')

defineEmits(['logout'])
</script>

<template>
  <header class="top-navbar">
    <!-- Sol Taraf: Profil Görseli ve Bilgileri -->
    <div class="navbar-left">
      <router-link to="/profile" class="user-profile">
        <div class="avatar">
          {{ userName ? userName.charAt(0).toUpperCase() : '' }}
        </div>
        <div class="user-info">
          <span class="user-name">{{ userName }}</span>
          <span class="user-email">{{ userEmail }}</span>
        </div>
      </router-link>
    </div>

    <!-- Sağ Taraf: Dil Butonu, Tema Butonu ve Çıkış Yap -->
    <div class="navbar-right">
      <!-- Dil Değiştirme Menüsü -->
      <div class="lang-dropdown-container">
        <button
          class="theme-toggle-icon-btn"
          @click="toggleLangDropdown"
          title="Dil Seç / Select Language"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="m5 8 6 6"></path>
            <path d="m4 14 6-6 2-3"></path>
            <path d="M2 5h12"></path>
            <path d="M7 2h1"></path>
            <path d="m22 22-5-10-5 10"></path>
            <path d="M14 18h6"></path>
          </svg>
        </button>

        <!-- Açılır Liste (Dropdown) -->
        <div v-if="showLangDropdown" class="lang-menu">
          <button @click="selectLanguage('tr')" :class="{ active: locale === 'tr' }">Türkçe</button>
          <button @click="selectLanguage('en')" :class="{ active: locale === 'en' }">English</button>
        </div>
      </div>

      <!-- Tema Değiştirme Butonu -->
      <button
        class="theme-toggle-icon-btn"
        @click="toggleTheme"
        :title="isDark ? 'Açık Temaya Geç' : 'Koyu Temaya Geç'"
      >
        <span v-if="isDark">☀️</span>
        <span v-else>🌙</span>
      </button>

      <button @click="$emit('logout')" class="logout-btn">{{ $t('nav.logout') }}</button>
    </div>
  </header>
</template>

<style scoped>
.top-navbar {
  height: 75px;
  background-color: var(--bg-header, #ffffff);
  border-bottom: 1px solid var(--border-color, #e2e8f0);
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
  background-color: var(--bg-main, #f1f5f9);
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
  color: var(--text-main, #1e293b);
}

.user-email {
  font-size: 13px;
  color: var(--text-muted, #64748b);
}

.navbar-right {
  display: flex;
  align-items: center;
  gap: 12px;
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

.theme-toggle-icon-btn {
  background: var(--bg-main);
  border: 1px solid var(--border-color);
  color: var(--text-main);
  width: 38px;
  height: 38px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.theme-toggle-icon-btn:hover {
  border-color: var(--accent-color);
  transform: scale(1.05);
}

/* Dil Dropdown Stilleri */
.lang-dropdown-container {
  position: relative;
}

.lang-menu {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  background-color: var(--bg-card, #ffffff);
  border: 1px solid var(--border-color, #e2e8f0);
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  min-width: 110px;
  z-index: 100;
  overflow: hidden;
}

.lang-menu button {
  background: none;
  border: none;
  padding: 10px 14px;
  text-align: left;
  font-size: 14px;
  color: var(--text-main, #1e293b);
  cursor: pointer;
  transition: background 0.2s;
}

.lang-menu button:hover {
  background-color: var(--bg-main, #f1f5f9);
}

.lang-menu button.active {
  font-weight: 600;
  color: #4f46e5;
}

.icon-btn {
  background-color : #f1f5f9;
  border: none ;
  cursor:pointer;
  padding: 8px 10px;
  border-radius:8px;
  display:flex;
  align-items:center;
  justify-content: center;
  color:#64748b;
  transition:all 0.2s ease;
}

.icon-btn:hover{
  background-color:#e2e8f0;
  color: #1e293b;
}
</style>