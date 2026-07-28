import axios from 'axios'

const api = axios.create({
  // .env içindeki değişkeni otomatik olarak çeker
  baseURL: import.meta.env.VITE_API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// İleride token eklemek gerekirse interceptor hazır durur
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
}, (error) => {
  return Promise.reject(error)
})

export default api