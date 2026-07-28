<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import axios from '@/services/api';

const route = useRoute();
const albums = ref([]);
const loading = ref(false);

// Modal ve Form State'leri
const showModal = ref(false);
const newTitle = ref('');
const newDescription = ref('');
const selectedFiles = ref([]);
const submitting = ref(false);

const fetchAlbums = async () => {
  loading.value = true;
  try {
    const userId = route.query.user;
    const params = userId ? { user: userId } : {};

    const response = await axios.get('/albums/', { params });
    albums.value = response.data;
  } catch (error) {
    console.error('Albümler yüklenirken hata oluştu:', error);
  } finally {
    loading.value = false;
  }
};

// Dosya seçimi
const handleFileChange = (event) => {
  selectedFiles.value = event.target.files;
};

// Yeni Albüm Oluşturma
const createAlbum = async () => {
  if (!newTitle.value.trim()) return;

  submitting.value = true;
  try {
    const albumResponse = await axios.post('/albums/', {
      title: newTitle.value,
      description: newDescription.value
    });

    const albumId = albumResponse.data.id;

    if (selectedFiles.value.length > 0) {
      for (let file of selectedFiles.value) {
        const formData = new FormData();
        formData.append('album', albumId);
        formData.append('image', file);

        await axios.post('/album-images/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
      }
    }

    newTitle.value = '';
    newDescription.value = '';
    selectedFiles.value = [];
    showModal.value = false;
    fetchAlbums();

  } catch (error) {
    console.error('Albüm eklenirken hata oluştu:', error);
  } finally {
    submitting.value = false;
  }
};

// Albüm Silme Fonksiyonu
const deleteAlbum = async (albumId) => {
  if (!confirm('Bu albümü silmek istediğinizden emin misiniz?')) return;

  try {
    await axios.delete(`/albums/${albumId}/`);
    // Listeden hızlıca kaldır
    albums.value = albums.value.filter(album => album.id !== albumId);
  } catch (error) {
    console.error('Albüm silinirken hata oluştu:', error);
    alert('Albüm silinemedi.');
  }
};

watch(() => route.query.user, () => {
  fetchAlbums();
});

onMounted(() => {
  fetchAlbums();
});
</script>

<template>
  <div class="albums-page">
    <!-- Üst Kısım -->
    <header class="page-header">
      <router-link to="/" class="go-home-link">
        <svg xmlns="http://www.w3.org/2000/svg" class="back-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
        <span>Go Home</span>
      </router-link>

      <button @click="showModal = true" class="add-album-btn">
        + Yeni Albüm Ekle
      </button>
    </header>

    <!-- Albüm Listesi Grid Alanı -->
    <main class="albums-grid-container">
      <div v-for="album in albums" :key="album.id" class="album-card">

        <!-- 2x2 Fotoğraf Kolaj Alanı -->
        <div class="album-images-grid">
          <div
            v-for="(imgObj, index) in album.images?.slice(0, 4)"
            :key="imgObj.id"
            class="grid-image-wrapper"
          >
            <img :src="imgObj.image" :alt="album.title" class="grid-img" />
          </div>

          <div v-if="!album.images || album.images.length === 0" class="no-image-placeholder">
            <span>Fotoğraf Yok</span>
          </div>
        </div>

        <!-- Albüm Bilgileri ve Silme Butonu Alt Alanı -->
        <div class="album-footer">
          <div class="album-info">
            <h3 class="album-title">{{ album.title }}</h3>
            <p class="album-text-snippet">{{ album.description }}</p>
          </div>

          <button @click="deleteAlbum(album.id)" class="delete-album-btn" title="Albümü Sil">
            <svg xmlns="http://www.w3.org/2000/svg" class="trash-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>

      </div>
    </main>

    <!-- Albüm Ekleme Modalı -->
    <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
      <div class="modal-content">
        <h2>Yeni Albüm Oluştur</h2>

        <form @submit.prevent="createAlbum" class="album-form">
          <div class="form-group">
            <label>Albüm Adı</label>
            <input type="text" v-model="newTitle" placeholder="Örn: Tatil Anıları" required />
          </div>

          <div class="form-group">
            <label>Açıklama</label>
            <textarea v-model="newDescription" placeholder="Albüm hakkında kısa bir açıklama yazın..."></textarea>
          </div>

          <div class="form-group">
            <label>Fotoğraflar (Birden fazla seçebilirsin)</label>
            <input type="file" multiple @change="handleFileChange" accept="image/*" />
          </div>

          <div class="modal-actions">
            <button type="button" class="cancel-btn" @click="showModal = false">İptal</button>
            <button type="submit" class="submit-btn" :disabled="submitting">
              {{ submitting ? 'Yükleniyor...' : 'Oluştur' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
.albums-page {
  padding: 12px 10px; /* Üst ve yan boşluklar daraltılarak sola ve yukarı alındı */
  max-width: 1200px;
  margin: 0 auto;
  color: #2d3748;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.go-home-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  color: #2d3748;
  font-weight: 600;
  font-size: 16px;
  transition: color 0.2s ease;
}

.go-home-link:hover {
  color: #805ad5;
}

.back-icon {
  width: 22px;
  height: 22px;
}

.add-album-btn {
  background-color: #805ad5;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

.add-album-btn:hover {
  background-color: #6b46c1;
}

.albums-grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 24px;
}

.album-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.album-images-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: repeat(2, 140px);
  gap: 6px;
  background: #f7fafc;
  border-radius: 8px;
  overflow: hidden;
}

.grid-image-wrapper {
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.grid-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.no-image-placeholder {
  grid-column: span 2;
  grid-row: span 2;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #a0aec0;
  font-size: 14px;
}

/* Albüm Alt Alanı ve Silme Butonu Tasarımı */
.album-footer {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
  padding: 0 4px;
}

.album-info {
  flex: 1;
  overflow: hidden;
}

.album-title {
  font-size: 16px;
  font-weight: 700;
  margin-bottom: 4px;
  color: #1a202c;
}

.album-text-snippet {
  font-size: 14px;
  color: #4a5568;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  word-break: break-all;
}

.delete-album-btn {
  background: #fff5f5;
  border: 1px solid #fed7d7;
  border-radius: 8px;
  width: 36px;
  height: 36px;
  min-width: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.2s, transform 0.2s;
}

.delete-album-btn:hover {
  background: #fee2e2;
  border-color: #f87171;
  transform: scale(1.05);
}

.trash-icon {
  width: 18px;
  height: 18px;
  color: #e53e3e;
}

/* Modal Stilleri */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 30px;
  border-radius: 12px;
  width: 100%;
  max-width: 500px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.modal-content h2 {
  margin-bottom: 20px;
  font-size: 20px;
}

.album-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group label {
  font-size: 14px;
  font-weight: 600;
  color: #4a5568;
}

.form-group input,
.form-group textarea {
  padding: 10px;
  border: 1px solid #cbd5e0;
  border-radius: 6px;
  font-size: 14px;
}

.form-group textarea {
  resize: vertical;
  min-height: 80px;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 10px;
}

.cancel-btn {
  background: #e2e8f0;
  border: none;
  padding: 10px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  color: #4a5568;
}

.submit-btn {
  background: #805ad5;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
}
</style>