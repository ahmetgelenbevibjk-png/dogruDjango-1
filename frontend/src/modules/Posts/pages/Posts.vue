<script setup>
import { ref, onMounted } from 'vue';
import axios from '@/services/api';

const posts = ref([]);
const selectedPost = ref(null);
const isModalOpen = ref(false);
const newComment = ref('');
const loading = ref(false);
const newPostTitle = ref('');
const newPostBody = ref('');
const isCreateModalOpen = ref(false);

const createPost = async () => {
  if (!newPostTitle.value.trim() || !newPostBody.value.trim()) return;

  try {
    const response = await axios.post('/posts/', {
      title: newPostTitle.value,
      body: newPostBody.value
    });
    posts.value.unshift(response.data);

    newPostTitle.value = '';
    newPostBody.value = '';
    isCreateModalOpen.value = false;
  } catch (error) {
    console.error('Post eklenirken hata oluştu:', error);
  }
};

const fetchPosts = async () => {
  loading.value = true;
  try {
    const response = await axios.get('/posts/');
    posts.value = response.data;
  } catch (error) {
    console.error('Postlar yüklenirken hata oluştu:', error);
  } finally {
    loading.value = false;
  }
};

const openModal = (post) => {
  selectedPost.value = post;
  isModalOpen.value = true;
};

const closeModal = () => {
  selectedPost.value = null;
  isModalOpen.value = false;
  newComment.value = '';
};

const addComment = async () => {
  if (!newComment.value.trim() || !selectedPost.value) return;

  try {
    const response = await axios.post('/comments/', {
      post: selectedPost.value.id,
      content: newComment.value
    });

    if (!selectedPost.value.comments) {
      selectedPost.value.comments = [];
    }
    selectedPost.value.comments.push(response.data);
    newComment.value = '';
  } catch (error) {
    console.error('Yorum eklenirken bir hata oluştu:', error);
  }
};

onMounted(() => {
  fetchPosts();
});
</script>

<template>
  <div class="posts-page">
    <!-- Üst Kısım: Go Home -->
    <header class="page-header">
      <router-link to="/" class="go-home-link">
        <svg xmlns="http://www.w3.org/2000/svg" class="back-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
        <span>Go Home</span>
      </router-link>
    </header>

    <!-- Post Listesi Üstü: Yeni Post Ekle Butonu -->
    <div class="posts-action-bar">
      <button @click="isCreateModalOpen = true" class="create-post-btn">
        + New Post
      </button>
    </div>

    <!-- Post Listesi -->
    <main class="posts-list-container">
      <div v-for="post in posts" :key="post.id" class="post-card">
        <h2 class="post-title">{{ post.title }}</h2>
        <p class="post-body-snippet">{{ post.body }}</p>

        <div class="card-footer">
          <button @click="openModal(post)" class="see-more-btn">
            <span>See More</span>
            <svg xmlns="http://www.w3.org/2000/svg" class="arrow-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
            </svg>
          </button>
        </div>
      </div>
    </main>

    <!-- Detay Penceresi (Modal) -->
    <div v-if="isModalOpen" class="modal-overlay" @click.self="closeModal">
      <div class="modal-container">

        <!-- Sağ Üst Çarpı Kapatma Butonu -->
        <button @click="closeModal" class="modal-close-btn">
          <svg xmlns="http://www.w3.org/2000/svg" class="close-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>

        <!-- Sol Taraf: Post İçeriği ve Yazar İsmi -->
        <div class="modal-left-section">
          <div class="author-header">
            <span class="author-name">{{ selectedPost?.author_name }}</span>
          </div>
          <div class="modal-post-content">
            <p>{{ selectedPost?.body }}</p>
          </div>
        </div>

        <!-- Sağ Taraf: Yorumlar ve Yorum Ekleme Alanı -->
        <div class="modal-right-section">
          <h3 class="comments-title">Comments</h3>

          <div class="comments-scroll-area">
            <div v-for="comment in selectedPost?.comments" :key="comment.id" class="comment-item">
              <div class="comment-user-info">
                <span class="comment-author">{{ comment.username || 'Anonim' }}</span>
              </div>
              <p class="comment-body">{{ comment.content }}</p>
            </div>
          </div>

          <!-- Sağ Alt Yorum Ekleme Alanı -->
          <div class="comment-input-container">
            <input
              v-model="newComment"
              type="text"
              placeholder="Add a comment..."
              @keyup.enter="addComment"
              class="comment-input"
            />
            <button @click="addComment" class="comment-send-btn">Post</button>
          </div>

        </div>

      </div>
    </div>

    <!-- Yeni Post Ekleme Modalı -->
    <div v-if="isCreateModalOpen" class="modal-overlay" @click.self="isCreateModalOpen = false">
      <div class="create-modal-container">
        <h3 class="create-modal-title">Create a New Post</h3>

        <input
          v-model="newPostTitle"
          type="text"
          placeholder="Post Title..."
          class="create-input"
        />

        <textarea
          v-model="newPostBody"
          placeholder="What's on your mind?"
          class="create-textarea"
        ></textarea>

        <div class="create-modal-actions">
          <button @click="isCreateModalOpen = false" class="cancel-btn">Cancel</button>
          <button @click="createPost" class="submit-btn">Share</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.posts-page {
  padding: 40px;
  max-width: 1000px;
  margin: 0 auto;
  color: #2d3748;
}

/* Üst Kısım: Go Home */
.page-header {
  position: fixed;
  top: 95px;
  left: 280px;
  z-index: 100;
}

.go-home-link {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  color: #2d3748;
  font-weight: 600;
  font-size: 16px;
  white-space: nowrap;
  transition: color 0.2s ease;
}

.go-home-link:hover {
  color: #805ad5;
}

.go-home-link:hover .back-icon {
  stroke: #805ad5;
}

.back-icon {
  width: 22px;
  height: 22px;
}

/* Yeni Post Buton Alanı */
.posts-action-bar {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 20px;
}

.create-post-btn {
  background: #805ad5;
  color: #ffffff;
  border: none;
  padding: 10px 18px;
  border-radius: 6px;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.2s;
}

.create-post-btn:hover {
  background: #6b46c1;
}

/* Post Listesi */
.posts-list-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.post-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.post-title {
  font-weight: 700;
  font-size: 18px;
  margin-bottom: 10px;
  color: #1a202c;
  overflow-wrap: break-word;
  word-break: break-word;
}

.post-body-snippet {
  font-weight: 300;
  font-size: 14px;
  color: #4a5568;
  line-height: 1.6;
  margin-bottom: 16px;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  overflow-wrap: break-word;
  word-break: break-word;
}

.card-footer {
  display: flex;
  justify-content: flex-end;
}

.see-more-btn {
  background: none;
  border: none;
  color: #4a5568;
  font-weight: 600;
  font-size: 14px;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  padding: 4px 0;
}

.arrow-icon {
  width: 16px;
  height: 16px;
}

/* Detay Penceresi (Modal) */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

.modal-container {
  background: #ffffff;
  width: 900px;
  height: 500px;
  border-radius: 12px;
  display: flex;
  overflow: hidden;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
  position: relative;
  border: 1px solid #805ad5;
}

/* Sağ Üst Kapatma (Çarpı) Butonu */
.modal-close-btn {
  position: absolute;
  top: 12px;
  right: 12px;
  background: none;
  border: none;
  cursor: pointer;
  color: #a0aec0;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 4px;
  border-radius: 50%;
  transition: background 0.2s, color 0.2s;
  z-index: 10;
}

.modal-close-btn:hover {
  background: #f7fafc;
  color: #805ad5;
}

.close-icon {
  width: 20px;
  height: 20px;
}

/* Modal Sol Bölüm */
.modal-left-section {
  flex: 1;
  padding: 30px;
  border-right: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
}

.author-header {
  margin-bottom: 20px;
}

.author-name {
  font-weight: 600;
  font-size: 16px;
  color: #2d3748;
}

.modal-post-content {
  font-weight: 400;
  font-size: 14px;
  color: #4a5568;
  line-height: 1.7;
  overflow-y: auto;
  flex: 1;
}

/* Modal Sağ Bölüm */
.modal-right-section {
  flex: 1;
  padding: 30px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.comments-title {
  font-weight: 700;
  font-size: 18px;
  color: #1a202c;
  margin-bottom: 15px;
}

.comments-scroll-area {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 15px;
  padding-right: 5px;
}

.comment-item {
  background: #f7fafc;
  padding: 10px 14px;
  border-radius: 6px;
}

.comment-author {
  font-weight: 600;
  font-size: 13px;
  color: #2d3748;
  margin-bottom: 4px;
  display: block;
}

.comment-body {
  font-weight: 400;
  font-size: 13px;
  color: #4a5568;
  overflow-wrap: break-word;
  word-break: break-word;
}

/* Sağ Alt Yorum Ekleme Alanı */
.comment-input-container {
  display: flex;
  gap: 8px;
  align-items: center;
}

.comment-input {
  flex: 1;
  padding: 10px 12px;
  border: 1px solid #cbd5e0;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 400;
  outline: none;
}

.comment-input:focus {
  border-color: #a0aec0;
}

.comment-send-btn {
  background: #805ad5;
  color: white;
  border: none;
  padding: 10px 16px;
  border-radius: 6px;
  font-weight: 600;
  font-size: 13px;
  cursor: pointer;
}

.comment-send-btn:hover {
  background: #6b46c1;
}

/* Yeni Post Ekleme Modalı Özel Stilleri */
.create-modal-container {
  background: #ffffff;
  width: 500px;
  padding: 30px;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  gap: 15px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
}

.create-modal-title {
  font-weight: 700;
  font-size: 18px;
  color: #1a202c;
}

.create-input {
  padding: 10px 12px;
  border: 1px solid #cbd5e0;
  border-radius: 6px;
  font-size: 14px;
  outline: none;
}

.create-textarea {
  padding: 10px 12px;
  border: 1px solid #cbd5e0;
  border-radius: 6px;
  font-size: 14px;
  height: 120px;
  resize: none;
  outline: none;
  font-family: inherit;
}

.create-modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 5px;
}

.cancel-btn {
  background: #e2e8f0;
  color: #4a5568;
  border: none;
  padding: 10px 16px;
  border-radius: 6px;
  font-weight: 600;
  font-size: 13px;
  cursor: pointer;
}

.cancel-btn:hover {
  background: #cbd5e0;
}

.submit-btn {
  background: #805ad5;
  color: #ffffff;
  border: none;
  padding: 10px 16px;
  border-radius: 6px;
  font-weight: 600;
  font-size: 13px;
  cursor: pointer;
}

.submit-btn:hover {
  background: #6b46c1;
}
</style>