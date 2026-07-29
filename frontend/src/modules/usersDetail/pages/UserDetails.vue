<script setup>
import {ref,onMounted} from 'vue';
import {useRoute} from 'vue-router';
import axios from '@/services/api';

const route =useRoute();
const userId=route.params.id ;

const user=ref(null);
const posts=ref([]);
const todos=ref([]);
const albums=ref([]);
const loading=ref(true);
const errorMessage=ref('');

const activeTab=ref('');

const fetchUserData=async ()=>{
  loading .value=true;
  errorMessage.value ='';

  try {
    const [userRes,postsRes,todosRes,albumsRes]=await Promise.all([
        axios.get(`/users/${userId}/`),
      axios.get(`/posts/?author=${userId}`),
      axios.get(`/todos/?user=${userId}`),
      axios.get(`/albums/?user=${userId}`)
    ]);
    user.value = userRes.data;
    posts.value = postsRes.data;
    todos.value = todosRes.data;
    albums.value = albumsRes.data;
  } catch (error) {
    console.error('Kullanıcı detayları çekilirken hata oluştu:', error);
    errorMessage.value = 'Kullanıcı bilgileri ve içerikleri yüklenirken bir hata oluştu.';
  } finally {
    loading.value = false;
  }
}
onMounted(() =>{
  fetchUserData();
});

</script>

<template>
  <div class="user-detail-container">

    <!-- Üst Başlık ve Geri Dönüş Linki -->
    <div class="page-navigation">
      <router-link to="/" class="back-button">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="19" y1="12" x2="5" y2="12"></line>
          <polyline points="12 19 5 12 12 5"></polyline>
        </svg>
        <span>Kullanıcılar Listesine Dön</span>
      </router-link>
    </div>

    <!-- Yükleniyor ve Hata Durumları -->
    <div v-if="loading" class="status-card">
      <div class="spinner"></div>
      <p>Kullanıcı bilgileri yükleniyor...</p>
    </div>

    <div v-else-if="errorMessage" class="status-card error">
      <p>{{ errorMessage }}</p>
    </div>

    <!-- Kullanıcı İçeriği -->
    <div v-else-if="user" class="profile-layout">

      <!-- Kullanıcı Profil Özeti Kartı -->
      <section class="profile-header-card">
        <div class="avatar-large">
          {{ user.name ? user.name.charAt(0).toUpperCase() : (user.username ? user.username.charAt(0).toUpperCase() : 'U') }}
        </div>
        <div class="profile-info">
          <h2>{{ user.name || user.username }}</h2>
          <span class="user-handle">@{{ user.username }}</span>
          <div class="meta-info">
            <span v-if="user.email">📧 {{ user.email }}</span>
            <span v-if="user.phone">📞 {{ user.phone }}</span>
          </div>
        </div>
      </section>

      <!-- Sekmeler (Tabs) -->
      <nav class="tabs-bar">
        <button
          :class="{ active: activeTab === 'posts' }"
          @click="activeTab = 'posts'"
        >
          Postlar ({{ posts.length }})
        </button>

        <button
          :class="{ active: activeTab === 'todos' }"
          @click="activeTab = 'todos'"
        >
          Yapılacaklar ({{ todos.length }})
        </button>

        <button
          :class="{ active: activeTab === 'albums' }"
          @click="activeTab = 'albums'"
        >
          Albümler ({{ albums.length }})
        </button>
      </nav>

      <!-- SEKMELERİN İÇERİĞİ -->
      <main class="tab-content">

        <!-- 1. POSTLAR SEKMESİ -->
        <div v-if="activeTab === 'posts'" class="cards-list">
          <div v-if="posts.length === 0" class="empty-state">
            Bu kullanıcı henüz hiç post paylaşmamış.
          </div>
          <div v-for="post in posts" :key="post.id" class="content-card">
            <h3 class="card-title">{{ post.title }}</h3>
            <p class="card-body">{{ post.body }}</p>
          </div>
        </div>

        <!-- 2. TODOLAR SEKMESİ -->
        <div v-if="activeTab === 'todos'" class="todos-list">
          <div v-if="todos.length === 0" class="empty-state">
            Bu kullanıcıya ait yapılacak iş bulunamadı.
          </div>
          <div
            v-for="todo in todos"
            :key="todo.id"
            class="todo-item"
            :class="{ completed: todo.completed }"
          >
            <input type="checkbox" :checked="todo.completed" disabled />
            <span class="todo-title">{{ todo.title }}</span>
          </div>
        </div>

        <!-- 3. ALBÜMLER SEKMESİ -->
        <div v-if="activeTab === 'albums'" class="cards-list">
          <div v-if="albums.length === 0" class="empty-state">
            Bu kullanıcıya ait albüm bulunamadı.
          </div>
          <div v-for="album in albums" :key="album.id" class="content-card">
            <h3 class="card-title">📁 {{ album.title }}</h3>
            <p v-if="album.description" class="card-body">{{ album.description }}</p>
          </div>
        </div>

      </main>

    </div>
  </div>
</template>

<style scoped>
.user-detail-container {
  width: 100%;
  padding: 30px 40px;
  color: #2d3748;
}

.profile-layout {
  max-width: 900px;
}
.page-navigation {
  margin-bottom: 20px;
}

.back-button {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: #4a5568;
  font-weight: 600;
  text-decoration: none;
  font-size: 14px;
  transition: color 0.2s ease;
}

.back-button:hover {
  color: #6b46c1;
}

/* Yükleme ve Hata Kartı */
.status-card {
  background: #ffffff;
  padding: 40px;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  color: #718096;
}

.status-card.error {
  color: #e53e3e;
}

/* Profil Üst Bilgisi */
.profile-header-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 24px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
}

.avatar-large {
  width: 68px;
  height: 68px;
  border-radius: 50%;
  background: linear-gradient(135deg, #6b46c1, #805ad5);
  color: #ffffff;
  font-size: 28px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.profile-info h2 {
  font-size: 22px;
  font-weight: 700;
  color: #1a202c;
  margin: 0 0 2px 0;
}

.user-handle {
  font-size: 14px;
  color: #718096;
}

.meta-info {
  display: flex;
  gap: 16px;
  margin-top: 8px;
  font-size: 13px;
  color: #4a5568;
}

/* Sekme Menüsü (Tabs) */
.tabs-bar {
  display: flex;
  gap: 12px;
  border-bottom: 2px solid #edf2f7;
  margin-bottom: 24px;
}

.tabs-bar button {
  background: none;
  border: none;
  padding: 12px 18px;
  font-size: 15px;
  font-weight: 600;
  color: #718096;
  cursor: pointer;
  border-bottom: 3px solid transparent;
  transition: all 0.2s ease;
}

.tabs-bar button:hover {
  color: #6b46c1;
}

.tabs-bar button.active {
  color: #6b46c1;
  border-bottom-color: #6b46c1;
}

/* Boş Durum */
.empty-state {
  text-align: center;
  padding: 30px;
  color: #a0aec0;
  font-style: italic;
  background: #ffffff;
  border-radius: 8px;
  border: 1px dashed #e2e8f0;
}

/* Post ve Albüm Kartları */
.cards-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.content-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.02);
}

.card-title {
  font-size: 16px;
  font-weight: 700;
  color: #2d3748;
  margin-bottom: 8px;
  word-break: break-word;
  overflow-wrap: break-word;
}

.card-body {
  font-size: 14px;
  color: #4a5568;
  line-height: 1.5;
  word-break: break-word;
  overflow-wrap: break-word;
}

/* Todo Elemanları */
.todos-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.todo-item {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  padding: 14px 18px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.todo-title {
  font-size: 14px;
  color: #2d3748;
  word-break: break-word;
  overflow-wrap: break-word;
}

.todo-item.completed .todo-title {
  text-decoration: line-through;
  color: #a0aec0;
}
</style>