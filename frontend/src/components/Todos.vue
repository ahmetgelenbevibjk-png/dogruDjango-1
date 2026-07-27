<script setup>
import { ref, onMounted } from 'vue'

const todos = ref([])
const newTodoTitle = ref('')
const loading = ref(true)
const errorMessage = ref('')

const fetchTodos = async () => {
  try {
    const token = localStorage.getItem('access_token')
    const response = await fetch('http://127.0.0.1:8000/api/todos/', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { 'Authorization': `Bearer ${token}` } : {})
      }
    })

    if (response.ok) {
      const data = await response.json()
      todos.value = Array.isArray(data) ? data : (data.results || [])
    } else {
      errorMessage.value = 'Görevler yüklenemedi.'
    }
  } catch (err) {
    errorMessage.value = 'Sunucuya bağlanılamadı: ' + err.message
  } finally {
    loading.value = false
  }
}

const addTodo = async () => {
  if (!newTodoTitle.value.trim()) return

  try {
    const token = localStorage.getItem('access_token')
    const response = await fetch('http://127.0.0.1:8000/api/todos/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { 'Authorization': `Bearer ${token}` } : {})
      },
      body: JSON.stringify({ title: newTodoTitle.value, completed: false })
    })

    if (response.ok) {
      const newTodo = await response.json()
      todos.value.unshift(newTodo)
      newTodoTitle.value = ''
    }
  } catch (err) {
    console.error('Görev eklenirken hata oluştu:', err)
  }
}

const toggleTodo = async (todo) => {
  try {
    const token = localStorage.getItem('access_token')
    const response = await fetch(`http://127.0.0.1:8000/api/todos/${todo.id}/`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { 'Authorization': `Bearer ${token}` } : {})
      },
      body: JSON.stringify({ completed: !todo.completed })
    })

    if (response.ok) {
      todo.completed = !todo.completed
    }
  } catch (err) {
    console.error('Görev güncellenirken hata oluştu:', err)
  }
}

const deleteTodo = async (id) => {
  try {
    const token = localStorage.getItem('access_token')
    const response = await fetch(`http://127.0.0.1:8000/api/todos/${id}/`, {
      method: 'DELETE',
      headers: {
        ...(token ? { 'Authorization': `Bearer ${token}` } : {})
      }
    })

    if (response.ok) {
      todos.value = todos.value.filter(t => t.id !== id)
    }
  } catch (err) {
    console.error('Görev silinirken hata oluştu:', err)
  }
}

onMounted(() => {
  fetchTodos()
})
</script>

<template>
  <div class="todos-page">
    <!-- Go Home yazısı -->
    <div class="top-nav">
      <router-link to="/home" class="home-link">← Go Home</router-link>
    </div>

    <!-- Başlık, form ve liste ortalandı -->
    <div class="todos-container">
      <h2 class="section-title">My Todos</h2>

      <!-- Yeni Görev Ekleme Formu -->
      <form @submit.prevent="addTodo" class="todo-form">
        <input
          type="text"
          v-model="newTodoTitle"
          placeholder="Yeni bir görev ekle..."
          class="todo-input"
        />
        <button type="submit" class="todo-btn">Ekle</button>
      </form>

      <div v-if="loading" class="status-msg">Yükleniyor...</div>
      <div v-else-if="errorMessage" class="status-msg error">{{ errorMessage }}</div>

      <!-- Görev Listesi -->
      <div v-else class="todo-list">
        <div v-if="todos.length === 0" class="status-msg">Henüz eklenmiş bir görev yok.</div>

        <div v-for="todo in todos" :key="todo.id" class="todo-item" :class="{ completed: todo.completed }">
          <div class="todo-left" @click="toggleTodo(todo)">
            <input type="checkbox" :checked="todo.completed" @click.stop="toggleTodo(todo)" />
            <span class="todo-text">{{ todo.title }}</span>
          </div>
          <button @click="deleteTodo(todo.id)" class="delete-btn">Sil</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.todos-page {
  display: flex;
  flex-direction: column;
  gap: 15px;
  width: 100%;
}

.top-nav {
  width: 100%;
  padding-left: 10px;
}

.home-link {
  color: #1e293b; /* Normalde siyah/koyu renk */
  text-decoration: none;
  font-weight: 600;
  font-size: 20px;
  letter-spacing: 0.3px;
  transition: color 0.2s, font-weight 0.2s;
}

.home-link:hover {
  color: #6366f1; /* Üzerine gelince mor renk */
  font-weight: 700; /* Biraz daha kalınlaşır */
}

.todos-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  max-width: 700px;
  width: 100%;
  margin: 0 auto;
}

.section-title {
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
}

.todo-form {
  display: flex;
  gap: 10px;
}

.todo-input {
  flex: 1;
  padding: 12px 16px;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  font-size: 15px;
  outline: none;
  transition: border-color 0.2s;
}

.todo-input:focus {
  border-color: #4f46e5;
}

.todo-btn {
  padding: 0 20px;
  background-color: #4f46e5;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

.todo-btn:hover {
  background-color: #4338ca;
}

.todo-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.todo-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: white;
  padding: 14px 18px;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
  transition: all 0.2s;
}

.todo-item.completed .todo-text {
  text-decoration: line-through;
  color: #94a3b8;
}

.todo-left {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  flex: 1;
}

.todo-text {
  font-size: 15px;
  color: #334155;
}

.delete-btn {
  background: transparent;
  color: #ef4444;
  border: none;
  font-weight: 500;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  transition: background 0.2s;
}

.delete-btn:hover {
  background: #fee2e2;
}

.status-msg {
  font-size: 15px;
  color: #64748b;
  padding: 10px 0;
}

.status-msg.error {
  color: #ef4444;
}
</style>