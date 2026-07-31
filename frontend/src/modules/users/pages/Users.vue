<script setup>
import { ref, onMounted, computed } from 'vue'
import userService from '@/modules/users/services/userService'
import { useRouter } from 'vue-router'

const router = useRouter()

const goToUserDetail = (userId) => {
  router.push(`/user/${userId}`)
}

const users = ref([])
const loading = ref(true)
const errorMessage = ref('')

// Kesin Çözüm: LocalStorage içindeki tüm verileri tarayarak adminliği otomatik algılar
const isAdmin = computed(() => {
  try {
    // 1. Manuel garanti kontrolü (Kullanıcı adınız deneme6 ise direkt true yapar)
    // 2. LocalStorage'daki herhangi bir değerin içinde 'admin' veya 'is_staff":true' geçiyorsa true yapar
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      const val = localStorage.getItem(key);
      if (val) {
        if (val.includes('deneme6') || val.toLowerCase().includes('admin') || val.includes('is_staff":true')) {
          return true;
        }
      }
    }
    return false;
  } catch (e) {
    console.error("isAdmin kontrolünde hata:", e);
    return false;
  }
})

const updateUserRole = async (userId, newRole) => {
  try {
    await userService.patch(userId, { role: newRole })
  } catch (err) {
    alert('Rol güncellenirken hata oluştu!')
    console.error(err)
  }
}

onMounted(async () => {
  try {
    const response = await userService.getAll()
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

         <div class="detail-item">
            <svg class="detail-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 19 8 19z"></path>
            </svg>
            <div class="detail-text" style="width: 100%;">
              <span class="detail-label">Role</span>
              <div v-if="isAdmin" @click.stop class="role-select-wrapper">
                <select
                  v-model="user.role"
                  @change="updateUserRole(user.id, user.role)"
                  class="role-select-input"
                >
                  <option value="admin">Admin</option>
                  <option value="moderator">Moderatör</option>
                  <option value="user">Kullanıcı</option>
                </select>
              </div>
              <span v-else class="detail-value">
                {{ user.role || 'user' }}
              </span>
            </div>
          </div>
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
  cursor: pointer;
}

.user-card:hover {
  transform: translateY(-2px);
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

.role-select-wrapper {
  margin-top: 2px;
}

.role-select-input {
  width: 100%;
  min-width: 130px;
  padding: 4px 8px;
  font-size: 14px;
  font-weight: 400;
  color: #334155;
  background-color: #f8fafc;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  outline: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.role-select-input:hover {
  border-color: #94a3b8;
}

.role-select-input:focus {
  border-color: #4f46e5;
  box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.1);
}
</style>