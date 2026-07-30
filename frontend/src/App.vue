<script setup>
import { ref, onMounted } from 'vue'
import Account from './modules/users/pages/Account.vue'
import DashboardLayout from './components/layout/DashboardLayout.vue'

const isLoggedIn = ref(false)

onMounted(() => {
  const token = localStorage.getItem('access_token')
  if (token) {
    isLoggedIn.value = true
  }
})

const handleLoginSuccess = () => {
  isLoggedIn.value = true
}

const handleLogout = () => {
  localStorage.removeItem('access_token')
  isLoggedIn.value = false
}
</script>

<template>
  <Account v-if="!isLoggedIn" @loginSuccess="handleLoginSuccess" />
  <DashboardLayout v-else @logout="handleLogout" />
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', sans-serif;
}
:root {
  --bg-main: #f8fafc;
  --bg-header: #ffffff;
  --bg-card: #ffffff;
  --text-main: #1e293b;
  --text-muted: #64748b;
  --border-color: #e2e8f0;
}

.dark {
  --bg-main: #0f172a;
  --bg-header: #1e293b;
  --bg-card: #1e293b;
  --text-main: #f8fafc;
  --text-muted: #94a3b8;
  --border-color: #334155;
}

[data-theme="dark"] {
  --bg-main: #0f172a;        /* Derin koyu arka plan */
  --bg-card: #1e293b;        /* Kart arka planı */
  --bg-header: #1e293b;      /* Üst bar ve sidebar */
  --text-main: #ffffff;      /* Tam Beyaz (Ana yazılar için) */
  --text-muted: #cbd5e1;     /* Açık Gümüş (İkincil yazılar için) */
  --border-color: #334155;   /* Çerçeveler */
  --accent-color: #818cf8;   /* Parlak Vurgu Rengi */
}

[data-theme="dark"] h1,
[data-theme="dark"] h2,
[data-theme="dark"] h3,
[data-theme="dark"] .user-name,
[data-theme="dark"] .detail-value,
[data-theme="dark"] .page-title {
  color: #ffffff !important;
}

/* İkincil Metinler, E-postalar ve Detaylar (AÇIK GÜMÜŞ/GRİ) */
[data-theme="dark"] p,
[data-theme="dark"] span,
[data-theme="dark"] div,
[data-theme="dark"] .user-email,
[data-theme="dark"] .detail-item,
[data-theme="dark"] .location-text,
[data-theme="dark"] .company-text {
  color: #cbd5e1 !important;
}

/* Sol Menü (Sidebar) Linkleri ve Yazıları */
[data-theme="dark"] .sidebar a,
[data-theme="dark"] .nav-item,
[data-theme="dark"] .router-link-active {
  color: #e2e8f0 !important;
}

/* KÜÇÜK BAŞLIKLAR (LOCATION, COMPANY, WEBSITE vb.) */
[data-theme="dark"] label,
[data-theme="dark"] small,
[data-theme="dark"] .detail-label,
[data-theme="dark"] .info-header {
  color: #94a3b8 !important;
  font-weight: 600;
}

/* Kartların İçindeki Tüm İkonlar */
[data-theme="dark"] svg {
  stroke: #94a3b8;
}

body {
  background-color: var(--bg-main);
  color: var(--text-main);
  transition: background-color 0.3s ease, color 0.3s ease;
  margin: 0;
  font-family:'Inter', sans-serif ;
     }
.top-header, .top-navbar,.sidebar {
  background-color:var(--bg-header) !important ;
  border-color: var(--border-color)!important ;
  color:var(--text-main)!important ;
}

.user-card , card , .modal-box{
  background-color: var(--bg-card)!important ;
  border:1px solid var(--border-color)!important;
  color:var(--text-main)!important;
}

.user-email, .location-text, .company-text, .detail-label {
  color:var(--text-muted)!important;
}

.main-content, main, .content-container {
  background-color: var(--bg-main) !important;
  transition: background-color 0.3s ease;
}
</style>

