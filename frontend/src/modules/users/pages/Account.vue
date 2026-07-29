<script setup>
import { ref } from 'vue'
import userService from '@/modules/users/services/userService'
import api from '@/services/api' // Token / Giriş işlemleri için merkezi api servisi

const emit = defineEmits(["loginSuccess"])
const activeModal = ref(null)
const username = ref('')
const name = ref('')
const phone = ref('')
const website = ref('')
const company = ref('')
const address = ref('')
const email = ref('')
const password = ref('')
const message = ref('')
const isError = ref(false)

const openModal = (type) => {
  activeModal.value = type
  username.value = ''
  name.value = ''
  phone.value = ''
  website.value = ''
  company.value = ''
  address.value = ''
  email.value = ''
  password.value = ''
  message.value = ''
}

const closeModal = () => {
  activeModal.value = null
}

const handleSubmit = async () => {
  message.value = ''
  isError.value = false

  const requestBody = activeModal.value === 'register'
    ? {
        username: username.value,
        name: name.value,
        phone: phone.value,
        website: website.value,
        company: company.value,
        address: address.value,
        email: email.value,
        password: password.value
      }
    : {
        username: username.value,
        password: password.value
      }

  try {
    let response

    if (activeModal.value === 'register') {
      // userService üzerinden kayıt isteği (baseService'in create metodunu kullanır)
      response = await userService.create(requestBody)
    } else {
      // Giriş (Token) isteği için merkezi api servisini kullanıyoruz
      response = await api.post('token/', requestBody)
    }

    const data = response.data

    isError.value = false
    message.value = activeModal.value === 'register'
      ? 'Kayıt başarıyla oluşturuldu!'
      : 'Giriş başarılı!'

    if (activeModal.value === 'login' && data.access) {
      localStorage.setItem('access_token', data.access)
      localStorage.setItem('user_name', username.value)
    }

    setTimeout(() => {
      const isLogin = activeModal.value === 'login'
      closeModal()
      if (isLogin) {
        emit('loginSuccess')
      }
    }, 1500)

  } catch (err) {
    isError.value = true
    const responseData = err.response?.data
    message.value = responseData?.error || responseData?.detail || (typeof responseData === 'object' ? JSON.stringify(responseData) : null) || 'Sunucuya bağlanılamadı: ' + err.message
  }
}
</script>

<template>
  <div class="page-container">

    <!-- EKRANIN ORTASINDAKİ KARŞILAMA KARTI -->
    <main class="welcome-card">
      <h1 class="welcome-title">Hoş Geldiniz</h1>
      <p class="welcome-subtitle">
        Sisteme erişmek ve içerikleri keşfetmek için lütfen giriş yapın veya yeni bir hesap oluşturun.
      </p>

      <div class="nav-links">
        <a href="#" class="nav-item btn-signup" @click.prevent="openModal('register')">
          <svg class="nav-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path>
            <circle cx="9" cy="7" r="4"></circle>
            <line x1="19" y1="8" x2="19" y2="14"></line>
            <line x1="22" y1="11" x2="16" y2="11"></line>
          </svg>
          Kayıt Ol
        </a>

        <a href="#" class="nav-item btn-signin" @click.prevent="openModal('login')">Giriş Yap</a>
      </div>
    </main>

    <!-- MODAL PENCERESİ -->
    <div class="modal-overlay" v-if="activeModal" @click="closeModal">
      <div class="modal-box" @click.stop>
        <div class="modal-header">
          <h2>{{ activeModal === 'register' ? 'Hesap Oluştur' : 'Giriş Yap' }}</h2>
          <button class="close-btn" @click="closeModal">&times;</button>
        </div>

        <form class="modal-form" @submit.prevent="handleSubmit">
          <!-- KAYIT OL ALANLARI -->
          <template v-if="activeModal === 'register'">
            <div class="form-group">
              <label>Kullanıcı Adı</label>
              <input type="text" v-model="username" placeholder="kullaniciadi" required />
            </div>

            <div class="form-group">
              <label>Ad Soyad (Name)</label>
              <input type="text" v-model="name" placeholder="Adınız Soyadınız" required />
            </div>

            <div class="form-group">
              <label>Telefon Numarası</label>
              <input type="tel" v-model="phone" placeholder="05XXXXXXXXX" required />
            </div>

            <div class="form-group">
              <label>Şirket (Company)</label>
              <input type="text" v-model="company" placeholder="Şirket Adı" />
            </div>

            <div class="form-group">
              <label>Konum / Adres (Address)</label>
              <input type="text" v-model="address" placeholder="Şehir veya Adres" />
            </div>

            <div class="form-group">
              <label>Website (İsteğe Bağlı)</label>
              <input type="url" v-model="website" placeholder="https://ornek.com" />
            </div>

            <div class="form-group">
              <label>E-posta Adresi</label>
              <input type="email" v-model="email" placeholder="ornek@email.com" required />
            </div>
          </template>

          <!-- GİRİŞ YAP ALANLARI -->
          <template v-if="activeModal === 'login'">
            <div class="form-group">
              <label>Kullanıcı Adı</label>
              <input type="text" v-model="username" placeholder="kullaniciadi" required />
            </div>
          </template>

          <div class="form-group">
            <label>Şifre</label>
            <input type="password" v-model="password" placeholder="••••••••" required />
          </div>

          <p v-if="message" :style="{ color: isError ? 'red' : 'green', fontSize: '14px' }">
            {{ message }}
          </p>

          <button type="submit" class="submit-btn">
            {{ activeModal === 'register' ? 'Kayıt Ol' : 'Giriş Yap' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* Ekranı dikey ve yatayda tam ortalayan ana alan */
.page-container {
  min-height: 100vh;
  width: 100vw;
  background-color: var(--bg-color);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

/* Ortadaki Karşılama Kartı */
.welcome-card {
  background: #ffffff;
  padding: 40px 32px;
  border-radius: 16px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  text-align: center;
  max-width: 440px;
  width: 100%;
}

.welcome-title {
  font-size: 26px;
  font-weight: 700;
  color: #1a202c;
  margin-bottom: 8px;
}

.welcome-subtitle {
  font-size: 14px;
  color: #666666;
  line-height: 1.5;
  margin-bottom: 28px;
}

.nav-links {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
}

.nav-item {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  text-decoration: none;
  font-size: 15px;
  font-weight: 600;
  padding: 12px 20px;
  border-radius: 8px;
  transition: all 0.2s ease;
  flex: 1; /* Butonları eşit genişlikte hizalar */
}

.btn-signup {
  background-color: #4f46e5;
  color: #ffffff;
  border: none;
}

.btn-signup:hover {
  background-color: #4338ca;
  transform: translateY(-1px);
}

.btn-signin {
  background-color: #ffffff;
  color: #333333;
  border: 1px solid #a0a0a0;
}

.btn-signin:hover {
  background-color: #f8f8f8;
  border-color: #666;
  transform: translateY(-1px);
}

.nav-icon {
  width: 18px;
  height: 18px;
}

/* MODAL STİLLERİ */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-box {
  background-color: #ffffff;
  padding: 30px;
  border-radius: 12px;
  width: 100%;
  max-width: 450px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  position: relative;
  text-align: left;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.modal-header h2 {
  font-size: 20px;
  color: #222;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
}

.close-btn:hover {
  color: #000;
}

.modal-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.form-group label {
  font-size: 14px;
  font-weight: 500;
  color: #444;
}

.form-group input {
  padding: 10px 12px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 14px;
  outline: none;
}

.form-group input:focus {
  border-color: #4f46e5;
}

.submit-btn {
  background-color: #4f46e5;
  color: #ffffff;
  border: none;
  padding: 12px;
  border-radius: 6px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  margin-top: 5px;
}

.submit-btn:hover {
  background-color: #4338ca;
}
</style>

<style>
:root {
  --bg-color: #c4c4c4;
}

body {
  font-family: 'Inter', sans-serif;
}
</style>