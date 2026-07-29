<script setup>
import { ref, onMounted } from 'vue'
import userService from '@/modules/users/services/userService' // <-- Servisimizi içe aktarıyoruz
import {useRouter} from 'vue-router';

const router=useRouter();

const goToUserDetail=(userId) =>{
  router.push(`/user/${userId}`);
}


const users = ref([])
const loading = ref(true)
const errorMessage = ref('')

onMounted(async () => {
  try {
    // Uzun fetch yerine tek satırla baseService'ten gelen getAll metodunu kullanıyoruz
    const response = await userService.getAll()

    // Axios response.data içinde veriyi döndürür
    const data = response.data
    users.value = Array.isArray(data) ? data : (data.results || [])
  } catch (err) {
    errorMessage.value = 'Kullanıcılar yüklenemedi: ' + (err.message || 'Sunucu hatası')
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="users-container">
    <h2 class="section-title">All Users</h2>
    <div v-if="loading" class="status-msg">Yükleniyor...</div>
    <div v-else-if="errorMessage" class="status-msg error">{{ errorMessage }}</div>

    <div v-else class="users-grid">
      <!-- Kartın kendisine tıklama olayı eklendi -->
      <div
        v-for="user in users"
        :key="user.id"
        class="user-card"
        @click="goToUserDetail(user.id)"
      >
        <div class="card-header">
          <div class="avatar-container">
            <img v-if="user.avatar" :src="user.avatar" alt="Avatar" class="avatar-img" />
            <div v-else class="avatar">
              {{ user.name ? user.name.charAt(0).toUpperCase() : (user.username ? user.username.charAt(0).toUpperCase() : 'U') }}
            </div>
          </div>
          <div class="user-main-info">
            <h3 class="user-fullname">{{ user.name || user.username }}</h3>
            <span class="user-email">{{ user.email || 'E-posta belirtilmemiş' }}</span>
            <span class="user-phone">{{ user.phone || 'telefon belirtilmemiş' }}</span>
          </div>
        </div>

        <div class="card-divider"></div>

        <div class="card-details">
          <!-- Location Alanı -->
          <div class="detail-item">
            <svg class="detail-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
              <circle cx="12" cy="10" r="3"></circle>
            </svg>
            <div class="detail-text">
              <span class="detail-label">Location</span>
              <span class="detail-value">
                {{ user.address || user.location || 'Adres bilgisi girilmedi' }}
              </span>
            </div>
          </div>

          <!-- Company Alanı -->
          <div class="detail-item">
            <svg class="detail-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="4" y="2" width="16" height="20" rx="2" ry="2"></rect>
              <line x1="9" y1="22" x2="9" y2="12"></line>
              <line x1="15" y1="22" x2="15" y2="12"></line>
              <line x1="9" y1="6" x2="9.01" y2="6"></line>
              <line x1="15" y1="6" x2="15.01" y2="6"></line>
            </svg>
            <div class="detail-text">
              <span class="detail-label">Company</span>
              <span class="detail-value">{{ user.company || 'Şirket belirtilmedi' }}</span>
            </div>
          </div>

          <!-- Website Alanı -->
          <div class="detail-item">
            <svg class="detail-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="2" y1="12" x2="22" y2="12"></line>
              <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
            </svg>
            <div class="detail-text">
              <span class="detail-label">Website</span>
              <!-- @click.stop ile web sitesine tıklandığında karta tıklama olayının tetiklenmesi engellendi -->
              <a v-if="user.website" :href="user.website" target="_blank" class="detail-value link" @click.stop>{{ user.website }}</a>
              <span v-else class="detail-value">Website yok</span>
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.users-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.section-title {
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
}

.users-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 20px;
}

.user-card {
  background-color: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 30px 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s, box-shadow 0.2s;
  display: flex;
  flex-direction: column;
  cursor:pointer ;

}

.user-card:hover {
  transform:translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 16px;
}

.avatar-container {
  flex-shrink: 0;
}

.avatar {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  background-color: #e0e7ff;
  color: #4f46e5;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 26px;
}

.avatar-img {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  object-fit: cover;
}

.user-main-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 0;
}

.user-fullname {
  font-size: 19px;
  font-weight: 700;
  color: #1e293b;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-email, .user-phone {
  font-size: 13px;
  font-weight: 500;
  color: #475569;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.card-divider {
  height: 1px;
  background-color: #f1f5f9;
  margin: 20px 0;
}

.card-details {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.detail-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.detail-icon {
  width: 18px;
  height: 18px;
  color: #64748b;
  margin-top: 3px;
  flex-shrink: 0;
}

.detail-text {
  display: flex;
  flex-direction: column;
  gap: 3px;
  min-width: 0;
}

.detail-label {
  font-size: 12px;
  font-weight: 600;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.detail-value {
  font-size: 14px;
  font-weight: 400;
  color: #334155;
  line-height: 1.4;
  white-space: normal;
  word-break: break-word;
}

.detail-value.link {
  color: #4f46e5;
  font-weight: 500;
  text-decoration: none;
}

.detail-value.link:hover {
  text-decoration: underline;
}

.status-msg {
  font-size: 16px;
  font-weight: 300;
  color: #64748b;
  padding: 20px;
}

.status-msg.error {
  color: #ef4444;
  font-weight: 500;
}
</style>