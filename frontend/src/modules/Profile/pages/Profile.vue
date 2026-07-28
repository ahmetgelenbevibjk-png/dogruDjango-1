<script setup>
import { ref, onMounted } from 'vue'
import userService from '@/modules/users/services/userService'

const username = ref('')
const name = ref('')
const phone = ref('')
const website = ref('')
const company = ref('')
const email = ref('')
const address = ref('')

const message = ref('')
const isError = ref(false)

const avatarFile = ref(null)
const imagePreview = ref(null)

// Sayfa yüklendiğinde kullanıcı bilgilerini çek
onMounted(async () => {
  const storedUsername = localStorage.getItem('user_name')

  if (!storedUsername) {
    isError.value = true
    message.value = 'Kullanıcı bulunamadı.'
    return
  }

  // Kullanıcı adını anında inputa yazdır
  username.value = storedUsername

  try {
    // userService.getById metodu ile kullanıcı verisini çekiyoruz
    const response = await userService.getById(storedUsername)
    const data = response.data

    name.value = data.name || ''
    phone.value = data.phone || ''
    website.value = data.website || ''
    company.value = data.company || ''
    email.value = data.email || ''
    address.value = data.address || ''

    if (data.avatar) {
      imagePreview.value = data.avatar
    }
  } catch (err) {
    isError.value = true
    message.value = 'Sunucuya bağlanılamadı.'
  }
})

// Fotoğraf seçildiğinde önizleme
const handleImageChange = (e) => {
  const file = e.target.files[0]
  if (file) {
    avatarFile.value = file
    imagePreview.value = URL.createObjectURL(file)
  }
}

// Güncelleme isteği
const handleUpdate = async () => {
  message.value = ''
  isError.value = false

  const formData = new FormData()
  formData.append('name', name.value)
  formData.append('phone', phone.value)
  formData.append('website', website.value)
  formData.append('company', company.value)
  formData.append('email', email.value)
  formData.append('address', address.value)

  if (avatarFile.value instanceof File) {
    formData.append('avatar', avatarFile.value)
  }

  try {
    // userService.patch metodu ile güncellemeyi gönderiyoruz
    const response = await userService.patch(username.value, formData)
    const data = response.data

    isError.value = false
    message.value = 'Profil bilgileriniz başarıyla güncellendi!'
    if (data.avatar) {
      imagePreview.value = data.avatar
    }
  } catch (err) {
    isError.value = true
    message.value = 'Güncelleme başarısız oldu.'
  }
}
</script>

<template>
  <div class="profile-container">
    <div class="profile-card">
      <div class="profile-header">
        <h2>Profil Bilgileri</h2>
      </div>

      <!-- Avatar Bölümü -->
      <div class="avatar-section">
        <div class="avatar-wrapper">
          <img v-if="imagePreview" :src="imagePreview" alt="Profil" class="avatar-img" />
          <div v-else class="avatar-placeholder">
            {{ username ? username.charAt(0).toUpperCase() : 'U' }}
          </div>
        </div>
        <div class="upload-box">
          <label for="file-input" class="upload-btn">Fotoğrafı Değiştir</label>
          <input
            id="file-input"
            type="file"
            accept="image/*"
            @change="handleImageChange"
            style="display: none;"
          />
          <span class="upload-hint">JPG, PNG veya GIF</span>
        </div>
      </div>

      <!-- Profil Formu -->
      <form class="profile-form" @submit.prevent="handleUpdate">
        <div class="form-group">
          <label>Kullanıcı Adı (Değiştirilemez)</label>
          <input type="text" v-model="username" disabled class="input-disabled" />
        </div>

        <div class="form-group">
          <label>Ad Soyad (Name)</label>
          <input type="text" v-model="name" placeholder="Adınız Soyadınız" required />
        </div>

        <div class="form-group">
          <label>E-posta Adresi</label>
          <input type="email" v-model="email" placeholder="ornek@email.com" required />
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
          <label>Konum (Location / Address)</label>
          <input type="text" v-model="address" placeholder="Şehir veya Adres" /> <!-- v-model address olarak düzeltildi -->
        </div>

        <div class="form-group">
          <label>Website</label>
          <input type="url" v-model="website" placeholder="https://ornek.com" />
        </div>

        <p v-if="message" :style="{ color: isError ? 'red' : 'green', fontSize: '14px' }">
          {{ message }}
        </p>

        <button type="submit" class="submit-btn">Değişiklikleri Kaydet</button>
      </form>
    </div>
  </div>
</template>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.profile-container {
  min-height: 100vh;
  width: 100vw;
  background-color: var(--bg-color, #c4c4c4);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.profile-card {
  background-color: #ffffff;
  padding: 30px;
  border-radius: 12px;
  width: 100%;
  max-width: 500px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}

.profile-header {
  margin-bottom: 20px;
}

.profile-header h2 {
  font-size: 22px;
  color: #222;
}

.avatar-section {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.avatar-wrapper {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  overflow: hidden;
  background-color: #4f46e5;
  display: flex;
  justify-content: center;
  align-items: center;
}

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  color: #ffffff;
  font-size: 28px;
  font-weight: bold;
}

.upload-box {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.upload-btn {
  background-color: #f1f5f9;
  color: #334155;
  padding: 8px 14px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  border: 1px solid #cbd5e1;
  text-align: center;
}

.upload-hint {
  font-size: 11px;
  color: #888;
}

.profile-form {
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

.input-disabled {
  background-color: #f8fafc;
  color: #888;
  cursor: not-allowed;
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